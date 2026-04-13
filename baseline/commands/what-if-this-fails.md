Analyze what happens when the current component, service, or change fails.

Walk through these failure scenarios for what I'm working on:

## Direct failure
- What happens immediately when this fails? Error? Timeout? Silent corruption?
- Who notices first — monitoring, a human, or a customer?

## Cascade
- What depends on this? What breaks downstream?
- Is the blast radius bounded (isolated service) or unbounded (shared state, no circuit breaker)?

## Recovery
- Does it recover automatically? If so, how long?
- If manual intervention is needed, what does on-call do? Is there a runbook?
- Can you roll back, or is the state changed irreversibly?

## The 3 AM test
- If this fails at 3 AM, can the on-call engineer diagnose and fix it without the original author?
- What information do they need? Is it in logs, dashboards, or someone's head?

## Verdict
Rate each area: **COVERED** / **PARTIAL** / **MISSING** — with one sentence explaining why.
