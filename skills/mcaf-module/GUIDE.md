# MCAF Terraform Module — Way of Working

Synthesised from **91 active `schubergphilis/terraform-*-mcaf-*` public modules** (47 AWS, 39 Azure, 2 TFE, 1 GitHub, 1 GitLab, 1 Datadog). Each rule lists the adoption rate seen in the corpus so the "defaults" are grounded in what the codebase actually does, not aspiration.

This document is the reference humans read when starting, maintaining, or reviewing an MCAF module. It is also the authority that three skills cite:

- `.claude/skills/terraform/` — generic Terraform / OpenTofu baseline (module patterns, testing, CI/CD, security). MCAF is layered on top.
- `.claude/skills/mcaf-module/` — MCAF deltas over the generic skill; structural authoring and PR review.
- `.claude/skills/review-mcaf/` — full qualitative review (best practices, usability, LCM, supply chain, security).

Rules below carry the adoption rate seen in the corpus so "default" reflects what MCAF actually does, not aspiration.

---

## 1. Repository layout

```
<root>/
├── main.tf                    # (86%) primary resources
├── variables.tf               # (94%) every variable, with description + type
├── variables.<topic>.tf       # split by domain when the module is large (seen in azure storage-account, core)
├── outputs.tf                 # (82%) every output, with description
├── terraform.tf               # (82%) REQUIRED file name — holds required_version + required_providers
├── locals.tf                  # (24%) only when locals actually exist
├── data.tf                    # (8%)  only when data sources exist
├── examples/                  # (90%) one subdir per scenario — at minimum a "default" example
│   └── default/
├── tests/                     # (17% but growing) native terraform test harness
│   ├── main.tftest.hcl
│   └── setup/                 # optional fixture module invoked via `run "setup"`
├── modules/                   # (17%) only for multi-module repos (landing-zone, account-baseline …)
├── .github/workflows/         # (97%) copied verbatim from mcaf-github-workflows
├── .pre-commit-config.yaml    # (92%)
├── Taskfile.yaml              # (26% combined .yaml/.yml, now the default for new modules)
├── README.md                  # (96%) prose + auto-injected terraform-docs block
├── CHANGELOG.md               # (75%) maintained by release-drafter
├── CONTRIBUTING.md            # (85%) boilerplate about conventional commits + pre-commit
├── UPGRADING.md               # (35%) required if there are breaking changes
└── LICENSE                    # (96%) Apache 2.0
```

**Rules:**

- Use `terraform.tf` **not** `versions.tf`. 81% of modules already use `terraform.tf`; the 10% on `versions.tf` are the older/less-maintained set. New modules and any module being touched MUST use `terraform.tf`.
- Use `providers.tf` for provider *configuration* blocks **only when a module needs aliased providers**. 99% of modules omit it because provider config belongs in the root caller, not inside a reusable module.
- Do not create empty files. No `locals.tf` if you have no locals.
- For multi-resource modules with >~40 variables, split `variables.tf` by domain: `variables.networking.tf`, `variables.share.tf`, etc. Keep `variables.tf` for the core set.

---

## 2. `terraform.tf` — version pinning

```hcl
terraform {
  required_version = ">= 1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.0, < 7.0"
    }
  }
}
```

**Rules:**

The exact floor number is not important — what matters is the **bounds**: a floor-only constraint for Terraform and most providers (no upper bound), and a major-version range for AzureAD, Azurerm, and Datadog (floor + upper bound at the next major). Don't bikeshed the minor; just ensure the constraint shape is correct.

- `required_version` — set a **minimum** with `>=`, no upper bound on Terraform itself. Any floor is acceptable (e.g. `">= 1.9"`).
- Provider `version` — floor-only for most providers; floor + upper bound at the next major for AzureAD, Azurerm, and Datadog. Do NOT pin to an exact version in a module.
- AWS: `>= 6` (no upper bound).
- AzureAD: `>= 3, < 4`. Azurerm: `>= 4, < 5`. Datadog: `>= 3, < 4`. Upper bound at the next major.
- Every provider block lists `source` explicitly, even for hashicorp providers.

---

## 3. Variables

```hcl
variable "name" {
  type        = string
  description = "The name of the bucket. If omitted, Terraform will assign a random unique name. Conflicts with `name_prefix`."
  default     = null
}

variable "object_lock_mode" {
  type        = string
  default     = null
  description = "The default object Lock retention mode to apply to new objects."
  nullable    = true

  validation {
    condition     = var.object_lock_mode == null || contains(["GOVERNANCE", "COMPLIANCE"], coalesce(var.object_lock_mode, "GOVERNANCE"))
    error_message = "object_lock_mode must be one of GOVERNANCE or COMPLIANCE."
  }
}
```

**Rules:**

- **Every** variable has a `description`. No exceptions.
- **Every** variable has an explicit `type`.
- Order of arguments inside the block: `type`, `default`, `description`, `sensitive`, `nullable`, `validation`. This is the order seen in ~80% of recently-touched modules.
- Prefer **complex typed objects** with `optional(..., <default>)` over dozens of flat variables. S3 / Aurora / Fargate modules are good examples — their nested `object({ ... })` signatures let callers stay terse.
- Use `validation` blocks for anything with an enumerated set of valid values, regex constraints, or cross-field invariants. 54% of modules already have at least one validation; aim for 100% on new variables with non-obvious constraints.
- Use `sensitive = true` on secrets, tokens, passwords. Never default a sensitive variable to a real value.
- Use `nullable = false` when `null` is genuinely not a valid value for the caller. 23% of modules use this today — under-used, because `null` often sneaks through as a silent default.
- Use `default = null` (not `default = ""`) to express "not provided". This lets `null`-aware conditionals like `var.x == null ? ... : ...` work cleanly.
- Naming: `snake_case`, descriptive, not abbreviated. Boolean flags read as statements: `versioning` (not `enable_versioning`), `force_destroy`, `bucket_key_encryption_enforced`.

---

## 3.5 Style & naming conventions

The style rules below are extracted from what the corpus actually does, not from HashiCorp's generic style guide. They're the ones CI doesn't enforce but reviewers should.

### Resource/data/module label convention

Each provider family has ONE canonical single-resource label:

| Provider | Convention | Evidence |
|---|---|---|
| `aws`, `github`, `datadog`, `tfe`, `gitlab` | `"default"` | 217 occurrences, 0 outside this set |
| `azure` | `"this"` | 114 occurrences, 0 `"default"` |

```hcl
# AWS — use "default"
resource "aws_s3_bucket" "default" { ... }
data   "aws_caller_identity" "default" {}

# Azure — use "this"
resource "azurerm_storage_account" "this" { ... }
data     "azurerm_client_config" "current" {}   # exception: data for caller identity uses "current"
```

- For additional instances of the same resource type, use a descriptive label (`"logging"`, `"replica"`, `"cmk"`) — not `"default2"` or `"this_extra"`.
- For resources created via `for_each`/`count`, the single canonical label still applies (`for_each` is what expresses multiplicity).

### Variable block internal order

```hcl
variable "x" {
  type        = …       # 1. type first
  default     = …       # 2. default (if present)
  description = "…"     # 3. description (always)
  nullable    = false   # 4. nullable (if non-default)
  sensitive   = true    # 5. sensitive (if non-default)
  validation { … }      # 6. validation blocks last
}
```

This is the order in `terraform-aws-mcaf-s3` and every reference module. Respect it.

### Variable source-file ordering

The corpus is split: older modules are alphabetical, newer ones group related variables. **Either is acceptable**, because CI renders the README with `terraform-docs --sort-by required`, so the user-facing order is normalised regardless.

- If you choose **alphabetical**, keep it strict (the `terraform_docs` pre-commit hook will reorder on drift).
- If you choose **logical grouping**, put identifying variables first (`name`, `resource_group_name`/`region`, `location`), then related feature clusters, then the catch-all `tags` at the end.
- For very large modules (>40 variables), split `variables.tf` into `variables.<domain>.tf` and apply ordering within each file.

### Output ordering

Outputs should be ordered by **usefulness to the caller**, not alphabetically. The canonical head of `outputs.tf` for any resource module is:

```hcl
output "id"   { … }  # or "name" for Azure (which mostly uses name as ID)
output "arn"  { … }  # AWS only
output "name" { … }
```

Then downstream outputs that expose IDs/ARNs other modules reference (VPC IDs, subnet IDs, role ARNs, etc.).

### Naming

- All identifiers (variables, outputs, locals, resource labels) are `snake_case`. No camelCase, no kebab-case. No exceptions.
- Boolean variables read as declarative statements about the desired state: `versioning`, `force_destroy`, `bucket_key_encryption_enforced`. Avoid `enable_` / `disable_` prefixes when the variable name already implies a state.
- Avoid redundant prefixes that repeat the module's purpose. In `terraform-aws-mcaf-s3`, the variable is `versioning`, not `s3_versioning`; the output is `arn`, not `bucket_arn`.
- Module names in `module "foo"` blocks follow the same snake_case rule and should describe what the module *is*, not what it is *for* (`module "logging_bucket"`, not `module "create_logging"`).

### Resource argument ordering

Inside a `resource` block, arrange arguments in this order. Empty lines separate each group:

1. `count` / `for_each` — meta-args first; even when written as a block, keep on top.
2. `provider`.
3. `region`, identifier (`name`, `role`, `bucket`, `resource_group_name`, …), then **alphabetically sorted** other fields, then `tags`.
4. Nested blocks (each separated by empty lines).
5. Meta-argument blocks: `depends_on`, `lifecycle`.

```hcl
resource "aws_s3_bucket" "default" {
  bucket              = var.name
  bucket_prefix       = var.name_prefix
  force_destroy       = var.force_destroy
  object_lock_enabled = var.object_lock_mode != null
  tags                = var.tags
}
```

### Module argument ordering

Inside a `module` block, arrange arguments in this order. Empty lines separate each group:

1. `count` / `for_each`.
2. `source`, `version`.
3. `providers`.
4. `region`, identifier (`name`, …), then **alphabetically sorted** other fields, then `tags`.
5. Nested blocks (each separated by empty lines).
6. Meta-argument blocks: `depends_on`, `lifecycle`.

### README section order

The `terraform-docs` template in use (see `.terraform-docs.yml`) fixes this order between the markers:

```
Requirements → Providers → Modules → Resources → Inputs → Outputs
```

Do not introduce new headings inside the `<!-- BEGIN_TF_DOCS --> / <!-- END_TF_DOCS -->` block — it will be overwritten. Prose feature sections go **above** the block; `## Licensing` goes **below** it.

### File section ordering inside `main.tf`

When a module keeps data/locals/resources all in `main.tf` (i.e. doesn't split into `data.tf` / `locals.tf`), the internal order is:

1. `data "…" "default"` blocks (AWS) / `data "…" "current"` (Azure)
2. `locals { … }` block
3. `module "…"` blocks (dependency parents first)
4. `resource "…"` blocks, with the primary resource first, then supporting resources in dependency order

### Terraform-docs specifics

- CI runs `terraform-docs` with `--sort-by required` (so required inputs render above optional ones).
- A checked-in `.terraform-docs.yml` is optional — only 2/91 modules ship one. Ship it when you need per-repo deviation (e.g. recursive docs for `modules/`), otherwise rely on the default template baked into the `terraform-docs/gh-actions` step.

### Anti-patterns

- `resource "aws_s3_bucket" "bucket"` — redundant, use `"default"`.
- `resource "azurerm_storage_account" "default"` — Azure convention is `"this"`.
- Variable block with `description` on top, then `type`, then `default` — reverse the order.
- `enable_versioning = bool` — rename to `versioning`.
- Alphabetised outputs where `arn`/`id`/`name` aren't first.
- Sorting variables alphabetically *and* adding `# Core` / `# Networking` comment headers — pick one system.

---

## 4. Outputs

```hcl
output "arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.default.arn
}
```

**Rules:**

- Every output has a `description` and a `value`.
- Expose the minimum useful surface: `id`, `arn`, `name`, and any ID your callers need to reference from other modules. Do not re-export every attribute of every resource.
- Mark sensitive outputs with `sensitive = true`.

---

## 5. Tags (AWS / Azure)

```hcl
resource "aws_s3_bucket" "default" {
  ...
  tags = var.tags
}
```

**Rules:**

- Expose `variable "tags"` with `type = map(string)` and `default = {}`. This should be universal.
- Every taggable resource references `var.tags`. No `try(var.tags)` cargo-cult. No `local.tags` indirection unless the module genuinely needs to inject extra tags.
- Do not hard-code tag keys inside individual resources.

---

## 6. Examples

**Rules:**

- `examples/` is required (90% have it). Every module MUST have at least `examples/default/` that exercises sensible defaults.
- Add one example per major scenario (encrypted, replication, public, private-endpoint, …).
- Examples **do not pin module versions** — they reference `source = "../../"` or `source = "schubergphilis/<name>/<provider>"` without a `version =`. Recommend pinning in the README's `IMPORTANT` banner only.
- Examples are the surface that `terraform-validation.yaml` lints/validates in CI, so every example must be runnable with `terraform init && terraform validate`.

---

## 7. Tests — native `terraform test`

The corpus has **zero terratest** (historical — was dropped) and **17%** native `terraform test` adoption, growing fast. Native tests are the MCAF standard.

```
tests/
├── main.tftest.hcl
└── setup/
    └── main.tf     # optional fixture resources the test depends on
```

```hcl
# tests/main.tftest.hcl
mock_provider "aws" {
  mock_data "aws_region" {
    defaults = { region = "eu-central-1" }
  }
}

run "setup" {
  module {
    source = "./tests/setup"
  }
}

run "default" {
  command = plan
  module  { source = "./" }

  assert {
    condition     = aws_s3_bucket.default.region == "eu-central-1"
    error_message = "Expected region eu-central-1, got: ${aws_s3_bucket.default.region}"
  }
}
```

**Rules:**

- Use `mock_provider` so tests run without AWS/Azure credentials. This is how modules get validated in PR CI.
- First `run` is `setup` (fixtures). Then one `run` per behaviour branch: `default`, `with_logging`, `with_kms`, `invalid_input`, etc.
- For invalid-input paths, use `expect_failures = [var.foo]` to assert the validation fires.
- Do not assert on raw resource fields that are identical to the input variable — test *derived* values and *conditional* resources.
- Tests MUST live under `tests/` (no `test/`, no `terratest/`).

---

## 8. CI — `mcaf-github-workflows`

85% of modules reuse the shared workflows from `schubergphilis/mcaf-github-workflows`. The files under `.github/workflows/` are **copied verbatim** and carry the header:

```yaml
# DO NOT CHANGE THIS FILE DIRECTLY
# Source: https://github.com/schubergphilis/mcaf-github-workflows
```

**Standard workflow set (each ≥85% adoption):**

| File | Purpose |
|---|---|
| `pr-validation.yaml` | PR title lint (conventional commits), PR label check, release-drafter autolabeler. |
| `terraform-validation.yaml` | `terraform fmt -check -recursive`, `tflint` on root + every example, `terraform validate` per example, `terraform test` (unless `SKIP_TERRAFORM_TESTS` var set), terraform-docs injection into README, checkov scan. |
| `label-synchronization.yaml` | Keeps repo labels in sync with the standard set. |
| `release-drafter.yaml` | Maintains draft release notes based on merged PR titles/labels. |
| `update-changelog.yaml` | Writes CHANGELOG.md on publish. |
| `terraform-test.yaml` | (16 modules so far) Runs `task test` via Taskfile — new-style test runner, complementing the one baked into `terraform-validation.yaml`. |

**Rules:**

- Do not modify these workflow files. If you need different behaviour, propose the change upstream in `mcaf-github-workflows`.
- Do not add ad-hoc workflows. Lambda-specific modules may add one targeted workflow (seen with `build-lambda.yml`), but the core five above remain.
- Required repo labels (enforced by `label-checker` job): `breaking`, `bug`, `chore`, `documentation`, `enhancement`, `feature`, `fix`, `security`. At least one must be on the PR.
- PR titles MUST follow **conventional commits**. Allowed types: `breaking`, `bug`, `chore`, `docs`, `documentation`, `enhancement`, `feat`, `feature`, `fix`, `security`.

---

## 9. Pre-commit

The canonical config is maintained in [`mcaf-github-workflows/sync-root/.pre-commit-config.yaml`](https://github.com/schubergphilis/mcaf-github-workflows/blob/main/sync-root/.pre-commit-config.yaml). Read the repository's copy for exact hooks and versions. Do not hardcode or duplicate the config here.

**Skipped checkov checks (by policy):**

- `CKV_GIT_5` / `CKV_GLB_1` — "≥2 approving reviews". MCAF policy is "≥1 approval".
- `CKV_TF_1` — "module sources must use commit hash". MCAF uses semantic versioning.

---

## 10. Taskfile

New-style modules ship a `Taskfile.yaml`:

```yaml
version: "3"
env: { TF_IN_AUTOMATION: 1 }
tasks:
  default:
    cmds: [{ cmd: "task --list", ignore_error: true }]
    silent: true
  clean:
    desc: Clean lock files and cache directories
    cmds:
      - rm -rf .terraform.lock.hcl .terraform
      - rm -rf **/.terraform.lock.hcl **/.terraform
    silent: true
  test:
    desc: Run Terraform tests
    cmds: ["terraform init", "terraform test"]
    silent: true
  verbose-test:
    desc: Run verbose Terraform tests
    cmds: ["terraform init", "terraform test -verbose"]
    silent: true
```

**Rules:**

- Prefer `Taskfile.yaml` (not `.yml`). The emerging standard.
- At minimum expose `default`, `clean`, `test`, `verbose-test`.
- CI's `terraform-test.yaml` calls `task test`, so Taskfile and CI stay in lockstep.

---

## 11. README

```markdown
# terraform-aws-mcaf-<name>

<One-line purpose.>

IMPORTANT: We do not pin modules to versions in our examples. We highly recommend that in your code you pin the version to the exact version you are using so that your infrastructure remains stable.

## <Feature section(s) — prose about non-obvious behaviour>

<!-- BEGIN_TF_DOCS -->
<!-- auto-injected by terraform-docs via the CI workflow; DO NOT EDIT -->
<!-- END_TF_DOCS -->

## Licensing

100% Open Source and licensed under the Apache License Version 2.0. See [LICENSE](...) for full details.
```

**Rules:**

- First H1 = repo name. First paragraph = one-line purpose.
- The version-pinning `IMPORTANT` banner is mandatory.
- Add prose sections for anything a reader cannot infer from the auto-generated inputs table (e.g. gotchas, AWS-specific caveats, lifecycle warnings, compatibility notes).
- The `BEGIN_TF_DOCS` / `END_TF_DOCS` markers are required (86% of modules have them). CI injects inputs/outputs/resources.
- End with a `## Licensing` section pointing at the LICENSE file.
- Do not add a `## Usage` section with hand-written HCL snippets — point people to `examples/` instead. (Only 15% have a Usage section; it rots.)

---

## 12. Release flow

- `release-drafter` maintains a draft release based on merged PR labels. Label → section mapping is defined in `release-drafter-config.yaml` (comes from `mcaf-github-workflows`).
- Version bump rules (driven by labels on merged PRs):
  - `breaking` → **major**
  - `feature`, `enhancement` → **minor**
  - `fix`, `bug`, `security`, `documentation`, `chore` → **patch**
- `no-changelog` on a PR excludes it from the draft.
- Only `MCAF Contributors` publish releases (click pencil on draft → Update release).
- If the release contains breaking changes, an `UPGRADING.md` entry is mandatory. 35% of modules have one; anything that ever broke should.

---

## 12.5 Lifecycle / currency targets

Modules drift behind Terraform, provider, and action releases. The targets below are the currency bar; anything older is technical debt to close on next touch. The `review-mcaf` skill flags LCM findings per module.

| Dependency | Current (2026-04) | MCAF minimum | Pinning style in module |
|---|---|---|---|
| Terraform | `1.14` | no upper bound (must allow newest) | `required_version = ">= 1.9"` (floor only) |
| `hashicorp/aws` | `6.x` | major `6` | `">= 6.0, < 7.0"` or `"~> 6.0"` |
| `hashicorp/azurerm` | `4.x` | major `4` | `">= 4, < 5.0"` |
| `hashicorp/azuread` | `3.x` | major `3` | `">= 3, < 4.0"` |
| `datadog/datadog` | `3.x` | major `3` | `">= 3.39, < 4.0"` |
| `integrations/github` | `6.x` | major `6` | `">= 6.0, < 7.0"` |
| `okta/okta` | `5.x` | major `5` | `">= 5.0, < 6.0"` |
| `hashicorp/tls` | `4.x` | major `4` | `">= 4.0, < 5.0"` |
| `hashicorp/random` | `3.x` | major `3` | `">= 3.0, < 4.0"` |
| `hashicorp/null` | `3.x` | major `3` | `">= 3.0, < 4.0"` |
| `hashicorp/http` | `3.x` | major `3` | `">= 3.0, < 4.0"` |
| `hashicorp/archive` | `2.x` | major `2` | `">= 2.0, < 3.0"` |
| `hashicorp/time` | `0.x` | major `0` | `">= 0.9, < 1.0"` |
| `hashicorp/tfe` | `0.x` | major `0` | `">= 0.50, < 1.0"` |

### Rules

- **Never hard-pin providers in a module.** `version = "= 6.1.2"` forbids the caller from bumping — it propagates module debt outward.
- **Avoid patch-tight pins** (`~> 6.1.2`). Pinning to the patch level (vs minor) blocks routine security patches and is almost never what the module author actually wanted. 3 modules in the corpus have this; all azure.
- **Avoid pre-1.3 Terraform floors**. `>= 0.13` / `>= 1.0.0` cuts off `terraform test` (1.6+) and optional-attrs-with-defaults (1.3+). 5 modules in the corpus are still pre-1.3.
- **No `required_version` missing** — 7 modules in the corpus are unset. The `terraform-validation` workflow cannot reason about version compatibility without it.

### Deprecated patterns to remove on next touch

- `resource "aws_s3_bucket_object"` → `aws_s3_object` (corpus: 0 left).
- Inline `versioning`/`server_side_encryption_configuration`/`lifecycle_rule` blocks inside `aws_s3_bucket` (removed in aws v4) → separate resources (corpus: 0 left).
- `resource "null_resource"` → `terraform_data` (Terraform ≥ 1.4). Corpus: 0 (already clean).
- `list("a","b")` / `map("k","v")` constructor calls → `["a","b"]` / `{k="v"}` literals (corpus: 0 left).

### Outdated workflow action pins (corpus hotspots)

- `hashicorp/setup-terraform@v2` → `@v3` (23 modules).
- `actions/checkout@master` / `@v2` / `@v3` → `@v4` (≥8 modules).
- `actions/github-script@v6` → `@v7`.
- `terraform-docs/gh-actions@v1.1.0` / `@v1.2.0` → `@v1.3.0`.
- Legacy security scanners (`aquasecurity/tfsec`, `triat/terraform-security-scan`) → replaced by the `bridgecrewio/checkov-action@v12` step that already exists in `terraform-validation.yaml`.
- Legacy label-checker (`danielchabr/pr-labels-checker`) → replaced by `docker://agilepathway/pull-request-label-checker` in mcaf-github-workflows.

Fixing these is not per-module work — it's upstream work in `mcaf-github-workflows`, which then flows out via the `DO NOT CHANGE` sync. **If a module still has v2 action pins, it has drifted from the shared workflows — re-sync it first.**

---

## 12.6 Supply chain

Terraform modules execute CI workflows and, in a few cases, bundle Lambda source. That gives two concrete supply-chain surfaces: **GitHub Actions** and **Lambda dependency manifests**. The `review-mcaf` skill flags supply-chain findings per module.

### GitHub Actions — pinning & trust

**Pin types, ordered safest-first:**

1. **SHA** (`uses: org/repo@<40-char-hex>`) — immutable. Recommended for any action not in MCAF's trusted set.
2. **Exact tag** (`@v1.3.0`) — immutable in practice; a retag would be noticed.
3. **Minor tag** (`@v1.3`) — floating, patch bumps silently; acceptable for trusted publishers.
4. **Major tag** (`@v3`) — floating across minors; acceptable for trusted publishers, not for others.
5. **Branch** (`@master`, `@main`) — **never**. Allows arbitrary code injection via a push to that branch.

Corpus today: **1 SHA-pinned**, 7 exact-tag, 1 minor-tag, 23 major-tag, **3 branch-pinned** (from 3 old modules).

**Trusted publishers** — major-tag is acceptable:

`actions`, `github`, `hashicorp`, `terraform-docs`, `terraform-linters`, `bridgecrewio`, `arduino`, `release-drafter`, `amannn`, `marocchino`, `agilepathway`, `crazy-max`, `stefanzweifel`.

**Flagged publishers** — remove from any MCAF module workflow on next touch:

- `Dirrk/terraform-docs` — abandoned fork; use `terraform-docs/gh-actions@v1.3.0`.
- `triat/terraform-security-scan` — unmaintained; the checkov step already scans.
- `danielchabr/pr-labels-checker` — non-standard; `mcaf-github-workflows` uses `agilepathway/pull-request-label-checker`.
- `anothrNick/github-tag-action` — one-person repo.
- `jessfraz/*` — personal.

**Docker image actions** (`uses: docker://org/image:tag`) should ideally pin by digest (`image@sha256:...`). The shared workflow pins `agilepathway/pull-request-label-checker:v1.6.55` by tag — fix upstream.

### Lambda dependency manifests

Only modules that bundle Lambda source have these:

- Python: use `requirements.txt` with `==X.Y.Z` exact pins (corpus: all 5 Python manifests are compliant).
- Node: use `package.json` + `package-lock.json` (committed). Caret/tilde ranges without a lockfile are not reproducible (corpus: 1 module — `cloudfront` auth lambda — fails this).

### Supply-chain review — blocking findings

The following are blocking findings in a PR review. No other supply-chain category stops a merge, but each of these must be addressed:

- Any action using `@master` / `@main` (mutable branch ref).
- Any action from a flagged publisher (see lists above).
- Any Python package in a Lambda `requirements.txt` without `==X.Y.Z`.
- Any `package.json` without a committed lockfile (`package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`).
- Any action from an untrusted publisher pinned by anything other than a 40-char SHA.

---

## 13. Secondary conventions worth adopting

These are underused in the corpus but recommended for new/maintained modules:

- **CODEOWNERS** — 0% adoption. Add one so PRs get auto-routed to the owning team.
- **Renovate/Dependabot** config in repo — 0% adoption (managed centrally). If central management goes away, add `renovate.json` with the MCAF preset.
- **`.tflint.hcl`** — 1% adoption. A root-level tflint config with the provider ruleset lets local `pre-commit` match CI exactly.
- **Nullable/validation coverage** — raise the 54% validation coverage and 23% `nullable=false` coverage to 100% on new modules.

---

## 14. Module skeleton — copy/paste starting point

```
terraform-<provider>-mcaf-<name>/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tf
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── Taskfile.yaml
├── .pre-commit-config.yaml
├── .github/workflows/
│   ├── label-synchronization.yaml
│   ├── pr-validation.yaml
│   ├── release-drafter.yaml
│   ├── terraform-test.yaml
│   ├── terraform-validation.yaml
│   └── update-changelog.yaml
├── examples/
│   └── default/
│       └── main.tf
└── tests/
    ├── main.tftest.hcl
    └── setup/
        └── main.tf
```

Use `terraform-aws-mcaf-s3` as the reference implementation for AWS and `terraform-azure-mcaf-storage-account` for Azure.

---

## 15. Recurring anti-patterns

Ten things that the structural checklist does not catch but which appear across the corpus. Use this list as the qualitative checklist when reviewing a module.

1. **Whole-resource outputs that leak state** — `output "resource" { value = aws_kubernetes_cluster.this }` re-exports every attribute including sensitive ones (`kube_admin_config`, `admin_password`). Always expose a curated set of named outputs. Mark any credential/token output `sensitive = true`.
2. **`try(var.tags)` cargo-culted** — `var.tags` defaults to `{}`; a `try()` around it is noise, and worse, masks real type errors. Drop it and use `var.tags` directly (§5).
3. **Two sources of truth for resource group** — Azure modules that take both `var.resource_group_name` AND `var.<obj>.resource_group_name` and `count`-toggle an internal `azurerm_resource_group.this`. Standardise on caller-owned RG; never create one inside a reusable module.
4. **Hard-pinned child-module refs** — `source = "github.com/schubergphilis/...?ref=vX.Y.Z"` inside a module propagates that version to every consumer. Use registry semver ranges (`schubergphilis/<name>/<provider>` + `version = "~> X.Y"`) instead.
5. **Missing `outputs.tf` entirely** — several modules ship no outputs and become black boxes. Every module producing a resource MUST expose at least `id`/`arn`/`name` (§4).
6. **Missing `sensitive = true` on credentials** — master passwords, storage access keys, API keys, kubeconfig outputs. Mechanical to audit; consistently missed.
7. **Floating `:latest` / `:main` image/version defaults** — makes the module silently non-idempotent and is a supply-chain risk. Default to a known-good version and document `"latest"` as opt-in.
8. **Dead variables / locals / files** — declared but never read, or referenced after being removed. Delete on the next touch instead of renaming.
9. **File-naming drift** — `functionApp.tf` / `storageAccount.tf` (camelCase), `Taskfile.yml` vs `Taskfile.yaml`, `backend.tf` / `module.tf` / `versions.tf` in place of the canonical names in §1. Fix before CI drifts further.
10. **Deeply nested `ternary`/`coalesce` over `optional(..., default)`** — if a variable body is 80% `X != null ? X : default`, your type is wrong. Move defaults into the type with `optional(field, default)`.

Bug classes worth explicit spot-checks during review (observed in the corpus at least once):

- Swapped output wiring (VPC endpoint IDs wired to the wrong endpoint).
- `each.value.*` vs `var.*` copy-paste bugs inside `for_each` blocks (node-pool scaling inheriting from system pool).
- `aws_sqs_queue_policy`-style conditions using `.name` where `.arn` is required.
- Relative paths in `archive_file.output_path` that write to the caller's CWD instead of `path.module`.
- Modules broken at plan time because they reference a resource (`azurerm_resource_group.this`) that isn't defined anywhere.
- Cron expressions with the wrong number of fields (AWS needs 7, Linux needs 5).

---

## Reference modules

Clone the structure of these when starting something new:

- **AWS**: `terraform-aws-mcaf-s3` (full-surface), `terraform-aws-mcaf-kms` (thin wrapper).
- **Azure**: `terraform-azure-mcaf-storage-account` (full-surface), `terraform-azure-mcaf-container-app-environment` (correct `var.tags` usage + native tests).
- **GitHub/TFE/GitLab**: `terraform-github-mcaf-repository` (the highest-quality module in the corpus).
