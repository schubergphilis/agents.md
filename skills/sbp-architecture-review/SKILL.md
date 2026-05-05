---
name: sbp-architecture-review
description: Review system architecture for mission-critical concerns — single points of failure, blast radius, rollback paths, observability gaps, and operational readiness. Use when designing new systems or reviewing existing ones.
metadata:
  domain: platform
  lifecycle: plan
---

# Architecture Review for Mission-Critical Systems

Review the system or proposed change against these mission-critical criteria. For each area, state whether it's covered, partially covered, or missing — with specifics.

## Single points of failure

- Identify every component where failure means full system outage.
- For each: is there redundancy? Failover? Degraded mode?
- Check: databases, message queues, external APIs, DNS, auth providers, load balancers.

## Blast radius

- If this component fails, what else breaks?
- Can the failure cascade? Are there circuit breakers or bulkheads?
- Is the blast radius bounded by design (isolated services) or unbounded (shared state)?

## Rollback

- Can every deployment be rolled back within 15 minutes?
- Are database migrations reversible?
- Is there a known-good state to return to?
- Has rollback been tested, or is it theoretical?

## Observability

- Are health checks in place? Do they check actual functionality, not just "process is running"?
- Are error rates, latency, and saturation monitored?
- Will alerts fire before customers notice?
- Can on-call diagnose issues without the original author?

## Operational readiness

- Is there a runbook? Does it cover the 3 AM scenario?
- Are secrets rotatable without downtime?
- What happens during a dependency upgrade? During a cloud provider incident?
- Is capacity planning documented? What's the headroom?

## Output format

Summarize findings as:
1. **Strengths** — what's well-handled (be specific)
2. **Risks** — what's missing or weak, with severity (HIGH/MEDIUM/LOW)
3. **Recommendations** — concrete actions to address each risk, ordered by severity
