# HOWTO.md — Design Spec

**Date:** 2026-05-05
**Status:** Approved

## Goal

A practical guide that shows an existing SBP engineer (Claude Code user, not yet using sbp-skills) how skills change their daily workflow — from install to real use across the engineering lifecycle.

## Audience

Primary: SBP engineers who already use Claude Code. Assume they know what Claude Code is; minimal explanation of skills.

## Format

Hybrid: short install section + 5 lifecycle scenarios, each with a one-line context and a realistic conversation snippet showing the skill in action.

## Sections

1. **Install** — plugin marketplace path only (`/plugin marketplace add schubergphilis/agents.md`, install skill groups, verify with one prompt)
2. **Plan: Designing a new system** — `sbp-architecture-review` on a new alerting pipeline; agent probes blast radius, rollback, observability
3. **Build: Developing a feature safely** — `sbp-feature-development` for TDD thinking, `sbp-secure-code-review` catching a webhook injection risk
4. **Run: Deploying safely** — `sbp-deploy-checklist` walking rollback readiness and monitoring; agent issues GO or asks a hard question
5. **Run: After something breaks** — `sbp-incident-review` running blameless timeline, 5 whys, concrete action items
6. **Closing** — two sentences pointing to more skills and contribution

## Constraints

- Conversation snippets: realistic, not generic — use the alerting pipeline scenario throughout for coherence
- Tone: matches WHY.md — direct, SBP-opinionated, no fluff
- Length: ~400–600 words total; scannable
