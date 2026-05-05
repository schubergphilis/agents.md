# How to use sbp-skills

This guide shows how sbp-skills changes your daily work in Claude Code. It assumes you already use Claude Code and know what a skill is. The examples follow one scenario throughout: building an alerting pipeline for a mission-critical service.

---

## 1. Install

Open Claude Code and run:

```
/plugin marketplace add schubergphilis/agents.md
```

Then install the skill groups you want:

```
/plugin install operations-skills@sbp-skills
/plugin install security-skills@sbp-skills
/plugin install engineering-skills@sbp-skills
/plugin install brand-skills@sbp-skills
```

To verify it worked, ask Claude: *"What should I think about before adding a new service to our platform?"*

Without sbp-skills, you get a generic answer. With it, Claude asks about blast radius, rollback, who gets paged, and what happens at 3 AM. That difference is the point.

---

## 2. Plan: Designing a new system

**Context:** Your team needs a real-time alerting pipeline. Before writing a line of code, you want to think through the architecture.

```
Use sbp-architecture-review to review the design for our new alerting pipeline.
```

> **You:** We are adding a real-time alerting pipeline. It reads from Kafka, fans out to webhook endpoints, and retries on failure. I want to review the architecture before we start.
>
> **Claude:** Before we look at the design, a few things. What happens if the Kafka consumer falls behind by more than your SLA window? Is there a circuit breaker on the webhook fanout, or does one slow endpoint block the others? And when this fails at 3 AM, who gets paged and what can they do without a full rollback?
>
> **You:** No circuit breaker yet. On-call can restart the consumer but cannot reroute traffic.
>
> **Claude:** That is your first single point of failure. A slow webhook will block the entire fanout. Isolate each destination in its own worker pool before this goes to production. You also need a runbook that does not require a deploy to mitigate. Let's work through the rest.

You get the gaps before any code exists. That is cheaper to fix now than after the first incident.

---

## 3. Build: Developing a feature

**Context:** The architecture is signed off. You are implementing the webhook fanout logic.

```
Use sbp-feature-development to build the webhook fanout component.
```

The skill drives you through a TDD approach: write a failing test for the happy path first, then retry logic, then the circuit breaker. When the implementation is taking shape, switch to a security review:

```
Use sbp-secure-code-review on the webhook handler.
```

> **Claude:** The webhook URL is taken directly from the Kafka message payload and passed to the HTTP client without validation. An attacker who can write to the Kafka topic can make your service send requests to internal endpoints. Validate the URL against an allowlist of known destinations before any outbound request.

That finding came from the review, not from you remembering to check for SSRF. The skill catches the class of bug, not just the instance.

---

## 4. Run: Deploying safely

**Context:** The fanout component is ready and tested. It is Tuesday morning. You want a clean deploy.

```
Use sbp-deploy-checklist for the alerting pipeline deployment.
```

> **Claude:** Checking deployment readiness.
>
> **Rollback:** your deployment disables the feature flag and stops the new consumer. Rollback time is under 5 minutes. Good.
>
> **Monitoring:** no alert on fanout lag or dead-letter queue depth. If the fanout silently falls behind, you will not know until a customer tells you. Add those two metrics before deploying.
>
> **Communication:** has the on-call been notified? This component adds a new failure mode to the alerting path.
>
> **NO-GO** until the monitoring gaps are closed.

Add the metrics, notify on-call, run the checklist again.

---

## 5. Run: After something breaks

**Context:** Three weeks later, alert fanout silently dropped messages for two hours. The incident is over. Time to learn from it.

```
Use sbp-incident-review to run the post-incident review for the fanout outage.
```

The skill walks you through a blameless timeline and 5 whys. It does not let you stop at "the webhook timed out." It pushes until you find why the timeout was not caught by monitoring, why the retry logic did not surface the error, and what let a deployment go out without testing that failure mode.

The output is a structured report with action items, owners, and deadlines, ready to share with the team.

---

## What's next

Run `sbp-skills list` to browse everything available, or look through the `skills/` directory in this repo. If you find a workflow that is not covered, scaffold a new skill with:

```bash
sbp-skills dev --skill sbp-your-skill-name
```

Then open a PR.
