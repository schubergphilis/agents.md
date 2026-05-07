---
name: sbp-safe-change
description: Use when planning a high-risk production change — classifies the change, assesses risk, runs pre-flight checks, builds an execution plan with rollback triggers, and verifies after completion.
metadata:
  domain: platform
  lifecycle: run
---

# Safe Change

This is a structured walkthrough for production changes that carry real risk. If you are nervous about a change, that instinct is correct — channel it into preparation, not avoidance.

The goal: turn anxiety into a checklist, execute methodically, and know exactly when to stop and roll back.

## Step 1: Classify the change

Name what you are doing. Different change types carry different risks.

- **Configuration change**: feature flags, environment variables, rate limits, routing rules.
- **Code deployment**: new application version, bug fix, dependency update.
- **Infrastructure change**: Terraform apply, Kubernetes resource modification, network policy, DNS.
- **Data migration**: schema change, backfill, data transformation, index creation.
- **Access change**: IAM policy, RBAC role, certificate rotation, secret rotation.

State clearly: what is changing, why, and what the expected outcome is. If you cannot state the expected outcome in one sentence, the change is not well enough understood to proceed.

## Step 2: Risk assessment

Answer each question honestly. The point is not to prove the change is safe — it is to understand exactly how it could go wrong.

**Blast radius**:
- If this goes wrong, what breaks? List every affected system and customer segment.
- Is the impact bounded (one service, one region) or unbounded (global, all customers)?
- Can the failure cascade into other systems?

**Reversibility**:
- Can this change be fully rolled back? How long does rollback take?
- Is there any part of this change that is irreversible? (Database column drops, data deletions, published API changes)
- Has rollback been tested, or is it theoretical?

**Data loss potential**:
- Could this change cause data loss or corruption under any scenario?
- Are backups current and tested? When was the last restore test?

**Timing risk**:
- Is this being done during peak traffic? During a maintenance window? On a Friday afternoon?
- Are the right people available if something goes wrong?

Assign an overall risk level:
- **HIGH**: irreversible components, wide blast radius, or untested rollback. Consider whether this change needs a maintenance window.
- **MEDIUM**: reversible but with significant blast radius or complexity. Proceed with extra caution.
- **LOW**: narrow blast radius, fully reversible, well-tested. Standard caution.

## Step 3: Pre-flight checks

Complete every item before executing the change. Skip nothing.

- [ ] **Backup verified**: relevant data is backed up and the backup has been validated (not just "backups are configured" but "I verified today's backup exists and is restorable").
- [ ] **Rollback tested**: rollback procedure has been executed in a non-production environment or is a known-good procedure from prior use.
- [ ] **Monitoring in place**: dashboards are open, you know which metrics to watch, alerts are active.
- [ ] **Communication sent**: on-call team knows the change is happening, dependent teams have been notified if applicable, status page is prepared if customer-facing.
- [ ] **Change window confirmed**: timing is appropriate, right people are available, no conflicting changes in progress.
- [ ] **Dry run completed**: if the tooling supports it (terraform plan, kubectl diff, migration --dry-run), the dry run output has been reviewed.
- [ ] **Peer review**: another engineer has reviewed the change and the execution plan.

If any item cannot be completed, stop and assess whether the change should proceed. Document why you are proceeding without it.

## Step 4: Execution plan

Write the exact steps you will follow. This is not a summary — it is the script you execute.

For each step:
1. **Action**: exactly what command, click, or change to make.
2. **Expected result**: what you should see after this step succeeds.
3. **Verification**: how to confirm the step worked correctly (specific command, metric, log entry).
4. **Abort condition**: what would you see that means "stop, do not proceed to the next step."

Example:

```
Step 1: Apply database migration
  Action: kubectl exec -it deploy/app -- python manage.py migrate --database=primary
  Expected: "Applying 0042_add_index... OK" with exit code 0
  Verify: SELECT count(*) FROM pg_indexes WHERE indexname = 'idx_orders_customer_id'; — should return 1
  Abort if: migration fails, takes longer than 5 minutes, or lock wait timeout appears in logs
```

Leave time between steps. Rushing through a plan defeats the purpose of having one.

## Step 5: Rollback triggers

Define the specific signals that mean "stop and roll back" before you start. Deciding this under pressure leads to bad decisions.

- **Error rate**: if error rate exceeds X% for Y minutes, roll back.
- **Latency**: if p99 latency exceeds X ms for Y minutes, roll back.
- **Availability**: if health checks fail on more than X% of instances, roll back.
- **Customer impact**: if any customer reports impact that correlates with the change, roll back.
- **Gut check**: if something feels wrong and you cannot explain why, pause. Investigate before proceeding. It is always cheaper to pause than to roll back.

Write these triggers down and share them with whoever is watching with you. During the change, you are executing — your partner is watching for triggers.

## Step 6: Post-change verification

After the change is complete and you believe it succeeded:

1. **Smoke test**: run the core user journeys. Do not trust "no errors" — actively verify correct behavior.
2. **Metric comparison**: compare error rate, latency, and throughput to the same time window yesterday or last week. Any significant deviation needs explanation.
3. **Log review**: check for new errors, warnings, or unexpected patterns in the logs.
4. **Alert silence period**: watch for at least 15 minutes after the change (longer for high-risk changes). Do not declare success and walk away.
5. **Dependent systems**: verify that downstream systems are healthy and processing normally.

When verification is complete, communicate the outcome:
- **Success**: confirm to stakeholders that the change is complete and verified.
- **Partial success**: state what worked and what still needs attention.
- **Rolled back**: state that the change was rolled back, why, and what happens next.

## Closing notes

Feeling nervous about a production change is a feature, not a bug. It means you understand the stakes. This walkthrough exists to channel that awareness into methodical execution.

The engineer who follows a checklist is not being slow — they are being professional. The fastest incident response is the one that never happens.
