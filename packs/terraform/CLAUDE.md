## Terraform — Claude Code

For deeper guidance, invoke the skills:

- `terraform` — generic Terraform/OpenTofu authoring (module structure, `optional(…)`, block ordering, testing decision matrix, CI/CD shape).
- `mcaf-module` — Schuberg Philis MCAF deltas (shared workflows, native tests with `mock_provider`, corpus-specific anti-patterns). Bundles `GUIDE.md`, the authoritative source for every MCAF rule.
- `review-mcaf` — qualitative MCAF module review that produces a good/bad/verdict markdown report.

Prefer `terraform test` (native) over Terratest — runs without cloud credentials via `mock_provider`. Tests live under `tests/`, never `test/` or `terratest/`.

When asked for an MCAF review of one or more `terraform-<provider>-mcaf-<name>` repos, use the `review-mcaf` skill — for many repos it dispatches parallel subagents and stitches a single report.
