## Mission-Critical Baseline

When reviewing your own work before presenting it:
- Check every error path is handled — no empty catch blocks, no swallowed exceptions.
- Check every external call has a timeout and failure mode.
- Check config changes state the rollback procedure.

Prefer explicit over implicit. Prefer boring over clever. Prefer observable over silent.

## Commands available

Use these in conversation:
- `/review` — review current work against mission-critical standards
- `/challenge` — challenge assumptions and design decisions
- `/risk-check` — full blast radius and rollback analysis
- `/explain` — explain unfamiliar code, infra, or patterns
- `/pre-deploy` — quick GO/NO-GO deployment check
- `/what-if-this-fails` — trace failure cascades and recovery paths

For contributors: `/new-pack` and `/new-skill` scaffold new content.

## Skills available

Default skills (always linked): `architecture-review`, `deploy-checklist`.

Engineers can enable more with `sbp-skills enable <name>` or by copying from `skills/` to `~/.claude/skills/`. Available: `threat-model`, `incident-review`, `safe-change`, `explain-codebase`, `why-we-do-this`, `dependency-audit`, `agent-architecture-review`, `runbook-author`, `observability-check`, `secure-code-review`.
