---
name: mcaf-module
description: Author or structurally review a Schuberg Philis MCAF Terraform module (`terraform-<provider>-mcaf-<name>`). Use when creating a new MCAF module, modifying an existing one, or reviewing a PR against one. This skill layers MCAF-specific rules on top of the generic `terraform` skill — start there for baseline guidance (module layout, variable/output design, testing, CI, security) and come here for the Schuberg Philis specifics (`terraform.tf` not `versions.tf`, reuse of `mcaf-github-workflows`, `var.tags` on every taggable resource, native `terraform test` with `mock_provider`, conventional-commit PR labels, release-drafter flow, and the recurring anti-patterns observed across the 91-module corpus). For a full qualitative review producing good/bad/verdict reports, use the `review-mcaf` skill instead.
---

# MCAF module

MCAF-specific overlay on top of the generic [`terraform`](../terraform/SKILL.md) skill. Read that first for baseline Terraform/OpenTofu rules. This skill only documents the **deltas** — the things MCAF does that a generic module wouldn't.

The authoritative source for every MCAF rule is [`GUIDE.md`](GUIDE.md) bundled with this skill.

## When this skill applies

- Creating a new repo named `terraform-<provider>-mcaf-<name>`.
- Editing files in an existing MCAF module.
- Reviewing a PR to an MCAF module for structural compliance.
- User mentions "MCAF module", "mcaf-github-workflows", or a `schubergphilis/terraform-*-mcaf-*` repo.

For a full **qualitative** review (good/bad, design critique, verdict), use `review-mcaf`.

## Reference implementations

- **AWS full-surface**: `terraform-aws-mcaf-s3`
- **AWS thin wrapper**: `terraform-aws-mcaf-kms`
- **Azure full-surface**: `terraform-azure-mcaf-storage-account`
- **GitHub / GitLab / TFE reference**: `terraform-github-mcaf-repository`
- **Shared CI**: `schubergphilis/mcaf-github-workflows`

Diff against the reference for that provider when unsure.

## MCAF deltas from the generic `terraform` skill

These override or tighten the base skill. Everything not listed here defers to the generic skill.

### Filenames

- Use **`terraform.tf`** (not `versions.tf`) for `required_version` + `required_providers`.
- Prefer `Taskfile.yaml` (lowercase `.yaml`).
- No camelCase file names (`functionApp.tf` etc.).

### Version pinning floors

The exact floor number is not important — what matters is the **bounds**: a floor-only constraint for Terraform and most providers (no upper bound), and a major-version range for AzureAD, Azurerm, and Datadog (floor + upper bound at the next major). Don't bikeshed the minor; just ensure the constraint shape is correct.

- Terraform: `required_version` must allow the newest Terraform (no upper bound). Any floor is acceptable (e.g. `">= 1.9"`).
- AWS: `>= 6` (no upper bound).
- AzureAD: `>= 3, < 4`. Azurerm: `>= 4, < 5`. Datadog: `>= 3, < 4`. Upper bound at the next major.

### Resource labels

- AWS / GitHub / Datadog / TFE / GitLab → `"default"`.
- Azure → `"this"`.
- Never mix in one repo.

### Tags

Every taggable resource references `var.tags`. No `try(var.tags)` cargo-cult. No `local.tags` indirection unless the module genuinely needs to inject extra tags.

### CI via `mcaf-github-workflows`

Five workflow files copied verbatim from `schubergphilis/mcaf-github-workflows`, with the `DO NOT CHANGE THIS FILE DIRECTLY` header intact:

- `pr-validation.yaml`
- `terraform-validation.yaml`
- `label-synchronization.yaml`
- `release-drafter.yaml`
- `update-changelog.yaml`

Plus `terraform-test.yaml` if using Taskfile-driven tests.

Do not hand-edit these files. If you need different behaviour, change it upstream in `mcaf-github-workflows`.

### PR requirements

- Conventional-commit title with one of: `breaking`, `bug`, `chore`, `documentation`, `enhancement`, `feature`, `fix`, `security`.
- At least one matching label.
- Breaking change → entry in `UPGRADING.md`.

### Pre-commit

The canonical config is maintained in [`mcaf-github-workflows/sync-root/.pre-commit-config.yaml`](https://github.com/schubergphilis/mcaf-github-workflows/blob/main/sync-root/.pre-commit-config.yaml). Read the repository's copy for exact hooks and versions.

Key policy notes on skipped checkov rules:

- `CKV_GIT_5` / `CKV_GLB_1` — MCAF requires ≥1 approval, not ≥2.
- `CKV_TF_1` — modules use semver tags, not commit SHAs.

### Taskfile

```yaml
version: "3"
env: { TF_IN_AUTOMATION: 1 }
tasks:
  default:
    cmds: [{ cmd: "task --list", ignore_error: true }]
    silent: true
  clean:
    cmds:
      - rm -rf .terraform.lock.hcl .terraform
      - rm -rf **/.terraform.lock.hcl **/.terraform
    silent: true
  test:
    cmds: ["terraform init", "terraform test"]
    silent: true
  verbose-test:
    cmds: ["terraform init", "terraform test -verbose"]
    silent: true
```

### README structure

```markdown
# terraform-<provider>-mcaf-<name>

<one-line purpose>

IMPORTANT: We do not pin modules to versions in our examples. We highly recommend that in your code you pin the version to the exact version you are using so that your infrastructure remains stable.

<prose sections for non-obvious behaviour>

<!-- BEGIN_TF_DOCS -->
<!-- END_TF_DOCS -->

## Licensing

100% Open Source and licensed under the Apache License Version 2.0. See [LICENSE](LICENSE) for full details.
```

### Release flow

- `release-drafter` maintains a draft release on every merge.
- Version bump rules:
  - `breaking` → major
  - `feature` / `enhancement` → minor
  - `fix` / `bug` / `security` / `documentation` / `chore` → patch
- `no-changelog` label excludes a PR from release notes.
- Only MCAF Contributors publish releases.

## Lifecycle / currency (MCAF floors)

Block new code adding instances of these:

- Terraform `required_version` set and allows the newest Terraform (no upper bound). Any floor is acceptable.
- AWS `>= 6` (no upper bound). AzureAD `>= 3, < 4`, Azurerm `>= 4, < 5`, Datadog `>= 3, < 4` (upper bound at next major).
- No exact or patch-tight provider pins inside a module.
- No deprecated AWS resources (`aws_s3_bucket_object`, inline `aws_s3_bucket` sub-blocks).
- No deprecated HCL constructors (`list(...)`, `map(...)`).
- Action pins up to date: `hashicorp/setup-terraform@v3`, `actions/checkout@v4`, `actions/github-script@v7`, `terraform-docs/gh-actions@v1.3.0`.

If a module has older action pins, it has drifted from `mcaf-github-workflows` — re-sync the workflow files rather than hand-bumping.

## Supply chain (MCAF-specific)

Blocking findings for a PR review:

- Any action using `@master` / `@main` — mutable ref.
- Any action from `Dirrk`, `triat`, `danielchabr`, `anothrNick`, `jessfraz` — replace with the MCAF-standard equivalent.
- Node `package.json` without a committed lockfile.
- Python dependency in a Lambda `requirements.txt` without `==X.Y.Z`.
- Docker image action pinned by mutable tag — prefer `@sha256:...`.

**MCAF trusted publishers** (major-tag OK):
`actions`, `github`, `hashicorp`, `terraform-docs`, `terraform-linters`, `bridgecrewio`, `arduino`, `release-drafter`, `amannn`, `marocchino`, `agilepathway`, `crazy-max`, `stefanzweifel`.

Everything else → SHA pin or replace.

## Recurring MCAF anti-patterns

The generic `terraform` skill's anti-pattern list covers most cases. These are the MCAF-corpus-specific additions:

1. **Two sources of truth for resource group on Azure** — `var.resource_group_name` AND `var.<obj>.resource_group_name` with a `count`-toggled internal `azurerm_resource_group.this`. The caller owns the RG, always.
2. **Hard-pinned child-module refs** — `source = "github.com/schubergphilis/...?ref=vX.Y.Z"`. Use registry + `version = "~> X.Y"`.
3. **Floating `:latest` / `:main` image defaults** — e.g. `ghcr.io/schubergphilis/<image>:main`. Pin to a known-good version and document `"latest"` as opt-in.
4. **`try(var.tags)` around a var with a default** — cargo-cult that masks real errors.

Bug classes spotted in the corpus worth explicit spot-checks:

- Swapped output wiring (VPC endpoint IDs pointing at the wrong endpoint).
- `each.value.*` vs `var.*` copy-paste inside `for_each` (user node pool inheriting system pool).
- Policy conditions using `.name` where `.arn` is required.
- `archive_file.output_path` as a relative path (writes to caller's CWD).
- References to `azurerm_resource_group.this` that is never declared.
- Cron expressions with the wrong number of fields.

## Authoring workflow

1. Create repo `terraform-<provider>-mcaf-<name>` in `schubergphilis`, default branch `main`.
2. Copy skeleton from the reference for that provider (see list above). Don't copy lock files or state.
3. Replace `.github/workflows/*` and `.pre-commit-config.yaml` with current versions from `mcaf-github-workflows` (preserve `DO NOT CHANGE` header).
4. Write `terraform.tf` with a `required_version` that allows the newest Terraform (e.g. `">= 1.9"` — floor only, no upper bound) and provider ranges.
5. Write `variables.tf` with types, descriptions, validations, `sensitive`/`nullable` as needed. Follow arg order rule.
6. Write `main.tf`. Reference `var.tags` on every taggable resource. Use canonical label (`"default"` or `"this"`).
7. Write `outputs.tf`: `id` / `arn` / `name` first, each with `description`. No whole-resource dumps.
8. Write `examples/default/main.tf` using `source = "../../"`, no `version =`.
9. Add one example per major feature branch.
10. Write `tests/main.tftest.hcl` with `mock_provider`, `run "setup"` if fixtures, `run "default"`, and a `run` per conditional path. `expect_failures` for negatives.
11. Write `Taskfile.yaml` with `default`, `clean`, `test`, `verbose-test`.
12. Write `README.md`; inject terraform-docs locally; CI regenerates on every PR.
13. Standard `CONTRIBUTING.md`.
14. `pre-commit run -a` until clean.
15. Push. CI must go green on `terraform-validation` and `pr-validation`. Apply a label.
16. On merge, `release-drafter` updates the draft release. Publish from the Releases page.

## PR review workflow

In order, fail fast:

1. **PR hygiene** — conventional-commit title? label applied? `CHANGELOG.md` / `UPGRADING.md` updated?
2. **File layout** — right locations? no `versions.tf` / `backend.tf` / `module.tf` / camelCase / `Makefile`?
3. **`terraform.tf`** — provider bumps widen the upper bound? `required_version` not lowered?
4. **Variables** — new var has `description` + `type`? enumerated values have `validation`? secrets `sensitive = true`? rename/retype triggers `breaking` label + `UPGRADING.md`? arg order inside block correct?
5. **Outputs** — `description` present? no whole-resource leak? sensitive values marked?
6. **Tags** — new taggable resource references `var.tags`? `try(var.tags)` removed if present?
7. **Examples** — at least one exercises the change? still valid?
8. **Tests** — new `run` block covers the new branch? `expect_failures` for negatives?
9. **Workflows / pre-commit** — untouched? If edited: reject and point at `mcaf-github-workflows`.
10. **LCM / supply-chain** — no new `@master` ref, no flagged publisher, no hard-pinned child module, provider floors still met.
11. **Anti-patterns** — walk the corpus-specific list.
12. **README** — prose sections accurate? (TF-docs block will be re-injected by CI.)

## Common traps

- Using `versions.tf` because some older module did — use `terraform.tf`.
- Pinning providers with `version = "6.1.2"`. Use ranges.
- Hand-written `## Usage` HCL snippets in the README — point to `examples/` instead.
- Editing a `mcaf-github-workflows`-sourced file locally.
- Mock provider omitted from tests — test tries to hit a real cloud.
- Dumping every attribute into `outputs.tf`.
- Mixed default representations: `""` vs `null`. Prefer `null`.
- Creating a resource group inside a module when caller should own it.

## Useful one-liners

```bash
# Diff workflows against current mcaf-github-workflows
gh api repos/schubergphilis/mcaf-github-workflows/contents/.github/workflow-templates | jq -r '.[].name'

# Validate loop locally
for d in examples/*/; do (cd "$d" && terraform init -backend=false && terraform validate); done

# Mocked tests
task test

# Render the terraform-docs section
terraform-docs . --sort-by required
```

## Related

- [`terraform`](../terraform/SKILL.md) skill — generic baseline.
- [`review-mcaf`](../review-mcaf/SKILL.md) skill — qualitative module review.
- `GUIDE.md` — the MCAF way-of-working reference.
