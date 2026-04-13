Review the current work against mission-critical standards.

Check each of these and report findings:

1. **Failure modes** — What happens when each external dependency is unavailable? Is every error path handled? Are there silent failures?
2. **Rollback** — Can this change be safely rolled back? Is the rollback procedure documented or obvious?
3. **Observability** — Will we know this is working? Will we know when it breaks? Are logs, metrics, or alerts in place?
4. **Blast radius** — What is affected if this goes wrong? Is the scope of impact minimized?
5. **Assumptions** — What implicit assumptions exist? Are they documented? What happens if they're wrong?

For each finding:
- If it's solid, confirm it: "Failure mode for database connection is handled — good."
- If it's missing, be specific about what to add and why.

Do not add unnecessary process. A local utility script needs less scrutiny than a production deployment pipeline.
