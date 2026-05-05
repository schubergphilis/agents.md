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

## 2. Plan: Reviewing a system architecture

**Context:** You want a mission-critical review of your system before the team starts building on top of it.

Type the skill name in Claude Code:

```
/sbp-architecture-review
```

The skill first explores the codebase autonomously — reading files, tracing dependencies, understanding what is actually there. Then it produces a structured review. Here is real output from a recent run:

---

**Architecture Review**

*Reviewed: 2026-05-05 / Reviewer: Claude Code / sbp-architecture-review*

**What's here**

| Component | Purpose | Status |
|-----------|---------|--------|
| SBP Framework | Claude Code commands + skills for mission-critical engineering | Dev / operational |
| vulnapp/ | Intentionally vulnerable Flask app for security education | Educational / local only |

---

**Strengths**

AGENTS.md is genuinely good engineering philosophy. The "3 AM question" framing, the explicit blast-radius-first thinking, and the requirement to explain *why* rather than just *what* — these are the right instincts, clearly stated.

vulnapp is well-contained for its purpose. It binds to 127.0.0.1 only, uses an ephemeral /tmp database, and ships a clear header listing every intentional vulnerability.

---

**Risks**

`HIGH` — Framework has no Claude API availability fallback

The entire command set is powered by the Claude API. If the API is unavailable, engineers lose all framework support with no degraded mode and no offline runbook substitute. Blast radius: all engineers lose decision-support tooling exactly when a production incident might also be occurring.

`HIGH` — No CI/CD pipeline or automated gate

Zero CI configuration. Changes to commands, skills, or vulnapp are merged with no automated verification. A broken skill ships silently — and if an engineer runs `/pre-deploy` during a production push and the command itself is broken, they get false confidence. That is the worst outcome for a tool designed to prevent exactly that.

`HIGH` — vulnapp has no deployment guard-rail beyond the warning comment

Nothing prevents the app from being deployed behind a public-facing reverse proxy. If deployed publicly, all six vulnerability classes become live attack surface.

`MEDIUM` — Rollback is theoretical only

No deployment pipeline means rollback is "revert the git commit and re-run." This has never been tested. For the framework specifically, breaking a command means manual intervention with no defined recovery time objective.

---

**Recommendations (ordered by severity)**

1. **[HIGH]** Add a Claude API circuit breaker / offline fallback. Define a minimal offline mode — a static Markdown checklist that covers the same surface as `/pre-deploy` and `/risk-check`. Engineers should be able to run a degraded-but-functional review without API access.

2. **[HIGH]** Add a CI pipeline. A GitHub Actions workflow that runs a syntax check and validates command/skill YAML on every PR. It does not need to be sophisticated — it needs to exist so broken changes are caught before merge.

3. **[HIGH]** Add a network-level guard for vulnapp. A comment is not a guard. Add an assertion that aborts if the app is not bound to localhost:
   ```python
   assert host == "127.0.0.1", "vulnapp must not be exposed beyond localhost"
   ```

4. **[MEDIUM]** Document a tested rollback procedure. "Revert the commit and re-run" is only a rollback if someone has verified it works. Write three steps, run them once, record that they were tested.

---

*Summary: The framework philosophy is strong. The operational scaffolding is absent: no CI, no API fallback, no tested rollback. For a framework engineers rely on during production incidents, that gap is the most urgent thing to close.*

---

You get a prioritised list of risks before any code changes. Each finding has a blast radius, a recommendation, and enough context to act on it immediately.

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
