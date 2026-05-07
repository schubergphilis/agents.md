---
name: sbp-deploy-checklist
description: Use when deploying to production — verifies rollback readiness, monitoring, and change communication against mission-critical criteria and produces a go/no-go decision.
metadata:
  domain: platform
  lifecycle: run
---

# Mission-Critical Deploy Checklist

Walk through this checklist before deploying to production. Every item must be answered — "not applicable" is a valid answer if you explain why.

## Before deployment

- [ ] **Change documented** — What is changing, why, and what's the expected impact?
- [ ] **Rollback plan** — How do we roll back? How long does it take? Has it been tested?
- [ ] **Blast radius understood** — What systems are affected? What customers are in scope?
- [ ] **Tests passing** — All unit, integration, and smoke tests green?
- [ ] **Review completed** — Has another engineer reviewed this change?
- [ ] **Communication** — Does anyone need to know this is happening? (on-call, dependent teams, customers)

## During deployment

- [ ] **Monitoring open** — Are dashboards and alerts visible during the deploy?
- [ ] **Incremental rollout** — Can this be deployed to a subset first? (canary, blue-green, feature flag)
- [ ] **Rollback trigger defined** — What metric or signal means "roll back now"?

## After deployment

- [ ] **Smoke test** — Does the core functionality work in production?
- [ ] **Metrics stable** — Error rates, latency, and throughput within normal range?
- [ ] **No alert noise** — No new alerts firing?
- [ ] **Cleanup** — Any temporary changes (feature flags, extra logging) to revert?

## Go / No-Go

Based on the checklist above, state:
- **GO** — all items addressed, risks are acceptable
- **NO-GO** — state which items are blocking and what needs to happen before retrying
