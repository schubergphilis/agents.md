# Terraform Convention Pack

Mission-critical Terraform/OpenTofu conventions for Schuberg Philis projects.

## What this activates

- **Module layout** — `terraform.tf` over `versions.tf`, examples under `examples/`, native tests under `tests/`
- **Version pinning** — floor-only `required_version`, provider version ranges (never exact or patch-tight)
- **Variable/output design** — `type` + `description` on every var, `optional(…)` over flat sprawl, curated outputs, `sensitive = true` on secrets
- **Tag hygiene** — `variable "tags"`. Referencing `var.tags` on every taggable resource.
- **Testing** — native `terraform test` with `mock_provider`
- **Security** — checkov in pre-commit + CI, no plaintext secret defaults

## Auto-detected by

- `*.tf`
- `terraform.tf`
- `versions.tf`

## Related skills

Enable with `sbp-skills enable <skill>`:

- `terraform` — generic Terraform/OpenTofu reference (with `references/` — module patterns, code patterns, testing, CI/CD, security, quick reference)
- `mcaf-module` — Schuberg Philis MCAF-specific rules (bundles the `GUIDE.md` way-of-working)
- `review-mcaf` — qualitative MCAF module review that produces good/bad/verdict reports
