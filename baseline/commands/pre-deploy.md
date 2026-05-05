Run a quick pre-deployment sanity check for the current change.

Answer each question concisely. Skip items that clearly don't apply (say why).

1. **What's changing?** One sentence.
2. **Rollback plan?** How do you undo this? How long does it take?
3. **Blast radius?** What breaks if this is wrong?
4. **Tests green?** Are all relevant tests passing?
5. **Monitoring ready?** Will you know if this breaks in production?
6. **Anyone need to know?** On-call, dependent teams, customers?

## Verdict

Based on the answers: **GO** or **NO-GO** with the blocking reason.

Keep this fast — if deeper analysis is needed, use the `sbp-deploy-checklist` skill instead.
