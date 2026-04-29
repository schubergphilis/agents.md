# Testing

> Part of: [`terraform`](../SKILL.md) skill.
> Purpose: testing approach decision matrix and patterns.

## The pyramid

Do these in order. Each catches different classes of issues and costs more than the last.

| Layer | Tool | Cost | Catches |
|---|---|---|---|
| 1. Format | `terraform fmt -check -recursive` | free | formatting drift |
| 2. Lint | `tflint` | free | provider-specific mistakes, naming |
| 3. Static validation | `terraform validate` | free | syntax, type mismatches |
| 4. Security scan | `checkov` / `tfsec` / `trivy` | free | insecure defaults |
| 5. Plan test | `terraform plan` on every example | free | missing inputs, graph errors |
| 6. Native test | `terraform test` with `mock_provider` | free | derived logic, validation branches |
| 7. Apply test | Terratest, `terraform apply` in sandbox | cost | real infrastructure integration |

Ship layers 1–6 on every PR. Layer 7 only when you actually need to verify real cloud behaviour.

## Layer 1-4: pre-commit + CI

Ship a `.pre-commit-config.yaml` with hooks for formatting, linting, validation, docs generation, and security scanning (e.g. checkov). The canonical config is maintained in [`mcaf-github-workflows/sync-root/.pre-commit-config.yaml`](https://github.com/schubergphilis/mcaf-github-workflows/blob/main/sync-root/.pre-commit-config.yaml) — read the repository's copy for exact hooks and versions.

Run the same tools in CI. No exceptions that are only in local. No exceptions that are only in CI.

## Layer 5: plan test per example

CI step that validates every example can plan:

```yaml
- name: Terraform validate examples
  run: |
    for d in examples/*/; do
      echo "Validating ${d}"
      terraform -chdir="$d" init -backend=false
      terraform -chdir="$d" validate -no-color
    done
```

If an example has provider credentials available, run `terraform plan` too — catches reference errors.

## Layer 6: native `terraform test`

Live under `tests/`:

```
tests/
├── main.tftest.hcl
└── setup/
    └── main.tf          # optional fixture module
```

Basic shape:

```hcl
# tests/main.tftest.hcl

mock_provider "aws" {
  mock_data "aws_region" {
    defaults = { region = "eu-central-1" }
  }
}

run "setup" {
  module { source = "./tests/setup" }
}

run "default" {
  command = plan
  module  { source = "./" }

  assert {
    condition     = aws_s3_bucket.default.bucket != null
    error_message = "Expected a bucket to be planned."
  }
}

run "invalid_input_is_rejected" {
  command = plan

  variables {
    mode = "not_a_valid_mode"
  }

  expect_failures = [var.mode]
}
```

Patterns:

- **Always start with `mock_provider`** so tests run without cloud credentials.
- **One `run` per behaviour**: `default`, `with_logging`, `invalid_foo`.
- **Assert on derived values**, not fields equal to the input variable. Testing `bucket.name == var.name` is a tautology.
- **Use `expect_failures`** for negative paths — checks the validation fires, doesn't just swallow the apply error.
- **Use `override_data`** to mock expensive policy documents:
  ```hcl
  run "default" {
    override_data {
      target = data.aws_iam_policy_document.combined
      values = { json = "{\"fake\":true}" }
    }
    # …
  }
  ```
- **Fixtures in `tests/setup/`** for things multiple `run` blocks need (mock VPCs, buckets, etc.).

## Layer 7: Terratest (only when necessary)

Reach for Terratest (Go) only when:

- You need to assert on real cloud behaviour that a mock cannot simulate (e.g. TLS handshake, HTTP behaviour).
- The module has tricky post-apply behaviour (data sources that only resolve after create).
- You're testing a composition, not a resource module.

Cost: requires Go toolchain, real credentials, often ~10 minutes per run vs seconds for native tests. Every Terratest is a maintenance burden.

Native `terraform test` with `mock_provider` replaces ~90% of what Terratest used to be used for.

## What to actually test

**Do test:**

- Conditional resource creation (`count = var.x ? 1 : 0`).
- Derived values in locals (`local.name = coalesce(var.override, var.name)`).
- Every `validation` block fires on invalid inputs.
- Cross-field invariants expressed in `precondition`.
- `for_each` expansion for edge cases (empty map, single entry, many entries).
- Sensitive output wiring (smoke test, not the value).

**Don't test:**

- Terraform itself (`aws_s3_bucket.default.bucket == var.name`).
- Provider behaviour (`terraform test` won't catch AWS API bugs).
- Upstream module internals.
- Things already covered by `validation` — the validation IS the test.

## Examples as tests

Keep every example runnable against a real cloud. They serve triple duty:

1. Documentation.
2. Smoke tests in CI (`terraform validate`).
3. Optional `terraform plan` in PR (if cloud credentials available).

Put realistic inputs in examples. `examples/default/main.tf` that passes zero variables does not demonstrate anything useful.

## Test naming

- File: `tests/main.tftest.hcl` plus one file per major scenario.
- `run` block names: short, describe the branch (`default`, `with_encryption`, `public_access_blocked`, `invalid_region`).
- No `run "test_1"`, `run "basic_test_2"` — the name describes behaviour, not index.

## Debugging a failing test

```bash
# Full output
terraform test -verbose

# Just one run block
terraform test -filter=tests/main.tftest.hcl -filter='run.with_encryption'
```

If the failure is about a mocked resource field returning `null`:

- `mock_data` for data sources.
- `mock_resource` for resources (provider-level default).
- `override_data` / `override_resource` inside a `run` block (test-level overrides).

## Parallel test hazards

Native tests run sequentially by default. If you use `parallel` settings, watch out for:

- Shared `mock_provider` state mutations.
- Fixture modules creating resources that another `run` depends on.

Safer: keep `run` blocks independent, each with its own `module { source = "./" }` call.
