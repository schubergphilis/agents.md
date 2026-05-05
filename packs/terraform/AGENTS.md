## Terraform / OpenTofu Conventions

Baseline rules for any Terraform/OpenTofu module. For MCAF specifics, enable the `mcaf-module` skill.

**Layout:** `main.tf`, `variables.tf`, `outputs.tf`, `terraform.tf` (not `versions.tf`). `locals.tf` / `data.tf` only when non-empty. Examples under `examples/<scenario>/`, native tests under `tests/`.

**Version pinning:** `required_version = ">= X.Y"` — floor only, no upper bound. Never pin providers exactly or patch-tight inside a reusable module.

**Variables:** every variable has `type` + `description`. Arg order: `type` → `default` → `description` → `nullable` → `sensitive` → `validation`. Prefer `optional(field, default)` over flat sprawl. `sensitive = true` on secrets. `default = null` (not `""`) for unset. Snake_case; booleans read as statements (`versioning`, not `enable_versioning`).

**Outputs:** every output has `description`. Lead with `id`, `arn`, `name`. Never `output "resource" { value = aws_x.default }` — curate. Mark credentials `sensitive = true`.

**Tags:** `variable "tags"`. Reference `var.tags` on every taggable resource. No `try(var.tags)` cargo-cult.

**Testing:** prefer native `terraform test` with `mock_provider` — no cloud credentials needed. Tests under `tests/`. Cover each conditional branch plus negative paths with `expect_failures`.

**State & secrets:** remote backend with locking and encryption. Modules take ARNs/IDs, not plaintext secrets. Run `checkov` in pre-commit + CI; skip rules only with an inline rationale.

**Acceptance criteria:**
- [ ] `terraform fmt -check -recursive` passes
- [ ] `tflint` passes on root + every example
- [ ] `terraform validate` passes per example
- [ ] `terraform test` passes (or justify why absent)
- [ ] `checkov` passes (skip rules only with inline rationale)
- [ ] No whole-resource outputs, no hard provider pins, no plaintext secret defaults
