---
name: terraform
description: Generic Terraform / OpenTofu guidance — module structure, variable + output design, block ordering, version pinning, native `terraform test`, CI/CD, security scanning, and state hygiene. Use when authoring or reviewing any Terraform/OpenTofu module, making IaC architecture decisions, picking a testing approach, setting up pipelines, or debugging state. For Schuberg Philis MCAF modules, the MCAF-specific overlays live in the `mcaf-module` and `review-mcaf` skills — use this one for baseline rules that apply regardless of organisation.
---

# Terraform / OpenTofu — baseline way of working

Inspired by Anton Babenko's [`terraform-skill`](https://github.com/antonbabenko/terraform-skill) and the patterns at terraform-best-practices.com. This is the generic base; organisation-specific overlays live in separate skills.

## When to use this skill

Use when:

- Creating or reviewing a Terraform/OpenTofu module.
- Choosing between testing approaches (`validate`, plan tests, native `terraform test`, Terratest).
- Structuring multi-environment deployments.
- Setting up CI/CD for IaC.
- Reviewing or refactoring existing configs.
- Deciding between module patterns or state-management approaches.

Don't use for:

- Basic HCL syntax questions.
- Provider-specific API reference (link to upstream docs).

## Reference files

Detailed guidance lives in `references/`:

- [`module-patterns.md`](references/module-patterns.md) — module hierarchy, layout, variable/output design, tag patterns, anti-patterns.
- [`code-patterns.md`](references/code-patterns.md) — block ordering, `count` vs `for_each`, `optional(…)`, `moved {}`, version management.
- [`testing.md`](references/testing.md) — the decision matrix across `terraform validate`, plan tests, native `terraform test`, and Terratest.
- [`ci-cd.md`](references/ci-cd.md) — GitHub Actions shape, conventional commits, release-drafter, pre-commit.
- [`security-compliance.md`](references/security-compliance.md) — checkov/tfsec/trivy, secrets hygiene, state security.
- [`quick-reference.md`](references/quick-reference.md) — cheat sheets, decision flowchart, troubleshooting.

## Core principles

### 1. Module hierarchy

| Level | Scope | Example |
|---|---|---|
| **Resource module** | One logical group of connected resources | VPC + subnets; Security group + rules |
| **Infrastructure module** | A set of resource modules for one purpose in one region/account | Landing zone in one account |
| **Composition** | A complete deployment, potentially multi-region/account | Whole org |

Build bottom-up: resource → resource module → infrastructure module → composition. Never skip a level by inlining across levels.

### 2. Repository layout for a resource module

```
<root>/
├── main.tf
├── variables.tf           # every variable with type + description
├── outputs.tf             # every output with description
├── terraform.tf           # required_version + required_providers
├── locals.tf              # only if non-empty
├── data.tf                # only if non-empty
├── README.md              # prose + auto-injected terraform-docs
├── CHANGELOG.md
├── LICENSE
├── .github/workflows/     # CI
├── .pre-commit-config.yaml
├── examples/              # one subdir per scenario, each runnable
│   ├── default/
│   └── <feature>/
└── tests/                 # native terraform test
    ├── main.tftest.hcl
    └── setup/             # optional fixture module
```

### 3. Version pinning

```hcl
terraform {
  required_version = ">= 1.9"   # a reasonable modern floor, no upper bound

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.0"            # floor only for AWS; some providers need an upper bound
    }
  }
}
```

- `required_version` floor-only with `>=`. No upper bound on Terraform. The exact floor is not important — focus on the constraint shape.
- Provider `version` — floor-only for most providers (no upper bound). Some providers need an upper bound at the next major. Never `= X.Y.Z` (exact) in a reusable module.
- Patch-tight (`~> X.Y.Z`) is almost always wrong — it blocks security patches.

### 4. Variables

```hcl
variable "name" {
  type        = string
  description = "The name of the resource. Conflicts with `name_prefix`."
  default     = null
}

variable "mode" {
  type        = string
  default     = null
  description = "The operating mode."

  validation {
    condition     = var.mode == null || contains(["A", "B"], var.mode)
    error_message = "mode must be one of A or B."
  }
}
```

Rules:

- Every variable has `type` + `description`.
- Internal arg order: `type` → `default` → `description` → `nullable` → `sensitive` → `validation`.
- Prefer complex typed objects with `optional(field, default)` over flat variable sprawl.
- Use `validation` for enumerated values, regex constraints, cross-field invariants.
- `sensitive = true` on secrets.
- `nullable = false` when `null` is not a valid caller value.
- Use `default = null` for "unset", not `""`.
- Snake_case names. Booleans read as statements of state (`versioning`, not `enable_versioning`).
- No redundant prefixes (`arn`, not `bucket_arn`).

### 5. Outputs

- Every output has a `description`.
- First outputs: `id`, `arn`, `name` — whatever maps to downstream caller references.
- Mark sensitive outputs `sensitive = true`.
- **Never return whole resources.** `output "resource" { value = aws_x.this }` leaks every attribute, including sensitive ones. Curate.
- Minimum useful surface — not every attribute re-exported.

### 6. Tags (cloud providers that support them)

```hcl
resource "aws_s3_bucket" "default" {
  # ...
  tags = var.tags
}
```

- Expose `variable "tags"` as `map(string)` with `default = {}`.
- Reference `var.tags` on every taggable resource. No `local.tags` indirection unless the module genuinely needs to inject extra tags.
- Drop `try(var.tags, {})` noise — `var.tags` has a default, `try()` around it hides type errors.

### 7. Testing

Use the layered strategy in [`references/testing.md`](references/testing.md):

1. **Pre-commit**: `terraform fmt`, `tflint`, `terraform validate`, `terraform_docs`, `checkov`/`tfsec`/`trivy`.
2. **CI static**: same tools, plus per-example `terraform init && terraform validate`.
3. **Native `terraform test`**: `mock_provider`, `run` blocks, `assert`/`expect_failures`. Free of cloud credentials, fast.
4. **Terratest** (Go): only when you need real apply against a real cloud.

Prefer native tests unless you actually need to hit a cloud. Keep tests under `tests/`.

### 8. CI/CD

At minimum:

- PR validation (title format, labels).
- Terraform validation (fmt + lint + validate on every example + `terraform test`).
- Docs injection (`terraform-docs` into README).
- Security scan (checkov).
- Release automation (release-drafter + CHANGELOG).

See [`references/ci-cd.md`](references/ci-cd.md) for GitHub Actions shape.

### 9. Security and state

- Run checkov in pre-commit + CI. Skip rules only with explicit rationale in comments.
- Never commit provider credentials, `.terraform/`, lock files for root modules where they could leak.
- State: remote backend with locking. Encrypt at rest. Never share state across environments.
- Secrets: caller passes ARNs/IDs of secret managers; modules don't take plaintext secrets. If they must, mark `sensitive = true`.

### 10. Release flow

- Conventional-commit PR titles: `feat`, `fix`, `breaking`, `docs`, `chore`.
- Labels drive version bump: `breaking` → major; `feat`/`enhancement` → minor; `fix`/`chore`/`docs` → patch.
- `release-drafter` maintains a draft release note on every merge; publish when ready.
- Add `UPGRADING.md` entries for breaking changes.

## Module anti-patterns

Things that bite teams repeatedly:

- Whole-resource outputs that leak sensitive state.
- Hard-pinned child-module refs (`source = "…?ref=vX.Y.Z"`) — propagate version debt.
- Two sources of truth for the same input (a flat `var.name` AND a nested `var.obj.name`).
- `try(var.tags)` cargo-cult around variables that already have a default.
- `default = null` on required inputs — contradicts the description.
- Empty `outputs.tf` — module is a black box.
- Missing `sensitive = true` on passwords/keys/tokens.
- Floating `:latest` / `:main` image/version defaults — non-idempotent.
- Dead variables / locals / files.
- File-naming drift (camelCase, `backend.tf`/`module.tf`/`versions.tf` in place of canonical names).
- Nested ternaries where `optional(field, default)` would do it.
- `null_resource` / deprecated resources (`aws_s3_bucket_object`, `azurerm_function_app`).

## Decision quick-reference

- **Alphabetical or grouped variable order?** Either, but pick one per repo. CI's `terraform-docs --sort-by required` normalises the rendered README regardless.
- **`count` vs `for_each`?** `for_each` on maps/sets for stable keys. `count` only when the multiplicity is truly positional.
- **`locals.tf` or inline `locals {}`?** Separate file when you have >~3 locals or when locals cross domains.
- **Providers in the module or in the caller?** In the caller. Modules use `configuration_aliases` only when they genuinely need multi-provider orchestration (e.g. cross-account S3 replication).

## Further reading

- `references/module-patterns.md`
- `references/code-patterns.md`
- `references/testing.md`
- `references/ci-cd.md`
- `references/security-compliance.md`
- `references/quick-reference.md`
