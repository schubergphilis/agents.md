<!-- BEGIN baseline -->
## Mission-Critical Baseline

When reviewing your own work before presenting it:
- Check every error path is handled — no empty catch blocks, no swallowed exceptions.
- Check every external call has a timeout and failure mode.
- Check config changes state the rollback procedure.

Use `/review` after completing any significant piece of work.
Use `/challenge` when the engineer is making a design decision.
Use `/risk-check` before any production-affecting change.

Prefer explicit over implicit. Prefer boring over clever. Prefer observable over silent.
<!-- END baseline -->
