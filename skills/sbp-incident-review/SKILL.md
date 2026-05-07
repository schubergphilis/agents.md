---
name: sbp-incident-review
description: Use when a production incident has occurred — structured blameless post-incident analysis that reconstructs timeline, assesses impact, finds root causes, and produces concrete action items.
metadata:
  domain: platform
  lifecycle: run
---

# Incident Review

Conduct a blameless post-incident review. The purpose is learning, not blame. Systems fail; the question is what we change so they fail less or recover faster.

## Timeline reconstruction

Build a detailed, timestamped sequence of events. This is the foundation — get it right before analyzing anything.

- **Detection**: When did the problem start? When was it detected? How was it detected — alert, customer report, engineer noticed?
- **Response**: Who responded? When? What was the first action taken?
- **Diagnosis**: What was investigated? What hypotheses were tested? Which were wrong and why?
- **Mitigation**: What action stopped or reduced the impact? When?
- **Recovery**: When was the system fully restored? How was "fully restored" verified?

Use UTC timestamps. Note the gap between each phase — long gaps reveal process problems.

Format the timeline as:

```
HH:MM UTC — [Event description] (Source: alert/person/log)
```

Call out any point where information was missing, misleading, or delayed. These are as important as the events themselves.

## Impact assessment

Quantify the impact. Vague impact statements lead to vague prioritization of fixes.

- **Duration**: total time from start of impact to full recovery.
- **Customer impact**: how many customers affected, what they experienced, whether they noticed.
- **Data implications**: any data loss, corruption, or exposure? If yes, scope it precisely.
- **SLA/SLO impact**: did this breach any commitments? Which error budgets were consumed?
- **Financial impact**: if quantifiable or estimable.
- **Downstream effects**: did this cause incidents or degradation in other systems?

## Root cause analysis

Use the "5 Whys" approach. Keep asking why until you reach a systemic cause, not a human action.

**Distinguish between**:
- **Trigger**: the immediate event that started the incident (a deploy, a config change, a traffic spike).
- **Root cause**: the underlying condition that made the trigger dangerous (missing validation, no circuit breaker, untested failover).
- **Contributing factors**: everything that made the incident worse or longer (see next section).

Bad root cause: "Engineer deployed a bad config."
Good root cause: "Config validation did not check for invalid values in the rate-limit field, allowing a zero value that caused all requests to be rejected. The deploy pipeline had no canary stage to catch this before full rollout."

The root cause should point to a system or process to fix, never to a person to blame.

## Contributing factors

What conditions made this incident possible, worse, or longer to resolve beyond the direct root cause?

Consider each category:

- **Monitoring gaps**: Was the right thing being measured? Did alerts fire promptly? Were they actionable?
- **Runbook quality**: Did the runbook exist? Was it accurate? Did it cover this scenario?
- **Deployment process**: Was there a canary? Was rollback easy? Was the change reviewed?
- **Communication**: Did the right people know? Was the escalation path clear? Was the status page updated?
- **Knowledge distribution**: Could only one person diagnose this? Was tribal knowledge involved?
- **System complexity**: Did the interaction between components make diagnosis harder?
- **Time pressure**: Was this change rushed? Was it deployed during a high-risk window?

## What went well

Explicitly capture what worked during the incident response. This is not optional — it is how you protect and reinforce good practices.

- What was detected or responded to quickly?
- What runbooks or automation helped?
- What communication or coordination worked well?
- What prior investment in resilience limited the blast radius?

Be specific. "Good teamwork" is not useful. "On-call engineer used the database runbook to identify the lock contention within 8 minutes of the alert" is.

## Action items

Every action item must be:
- **Concrete**: specific enough that someone can start working on it immediately.
- **Assigned**: an owner, not a team. A team is where action items go to die.
- **Time-bound**: a target date, even if it is approximate.
- **Prioritized**: P1 (prevents recurrence), P2 (improves detection/response), P3 (general improvement).

Format:

| # | Action item | Priority | Owner | Target date |
|---|------------|----------|-------|-------------|
| 1 | Add config validation for rate-limit field (reject zero/negative values) | P1 | @name | YYYY-MM-DD |
| 2 | Add canary stage to deploy pipeline for config changes | P1 | @name | YYYY-MM-DD |
| 3 | Update runbook with rate-limit incident scenario | P2 | @name | YYYY-MM-DD |

Avoid vague items:
- Bad: "Improve monitoring"
- Good: "Add alert for request rejection rate exceeding 5% over 2 minutes on the API gateway, routing to #incidents Slack channel"

## Output format

The final document should follow this structure, suitable for sharing with stakeholders:

1. **Summary** — 2-3 sentences: what happened, how long, what was the impact.
2. **Timeline** — timestamped events.
3. **Impact** — quantified.
4. **Root cause and contributing factors** — analysis.
5. **What went well** — reinforcement.
6. **Action items** — table with owners and dates.

Write in third person, past tense, blameless framing. Replace personal names in the narrative with roles ("the on-call engineer") unless the person specifically wants to be named. Keep names only in the action item owner column.
