# Incident Response

**Tags**: #incident_resp #ops  
**Purpose**: Restore service quickly and safely during production incidents while preserving data integrity and learning to prevent recurrence  
**Configurable**: Yes - Severity levels, escalation policies, runbooks, monitoring/alerting stack, communication channels, and workflows

## Quick Usage

```
Use #incident_resp to handle [incident description] and restore service safely while preserving data integrity
```

## Full Prompt

Coordinate and execute incident response from detection to recovery with clear roles, rapid stabilization, and thorough follow-up:

**1. Detection and Triage**
- Acknowledge alerts and initiate incident process immediately
- Apply #context_intake to capture current signals: symptoms, affected components, timeframe, blast radius, and user impact
- Classify severity (SEV level) based on impact and urgency; declare an incident if thresholds are met
- Assign roles and create shared context:
  - Incident Commander (leads and prioritizes), Communications Lead (stakeholder updates), Operations (hands-on responders), Scribe (timeline, decisions)
  - Open an incident channel, ticket, and timeline document
- Apply #route_task to categorize the incident type (availability, performance, data integrity, security, dependency outage) and determine specialized playbooks/runbooks
- Stabilize the situation operationally:
  - Pause risky deployments, freeze non-essential changes, and enable maintenance banners where applicable
  - Identify recent changes (deploys, migrations, config toggles) that could correlate with onset
- Establish update cadence (e.g., every 15–30 minutes internally, as needed externally) and stakeholder list (internal leadership, support, customers if appropriate)

**2. Stabilization and Mitigation**
- Prioritize restoring service and protecting data over identifying root cause
- Choose low-risk, reversible mitigations to reduce impact quickly:
  - Roll back recent releases or configs; consider progressive rollback or canary reductions
  - Toggle feature flags to disable problematic functionality
  - Reduce load: rate limiting, queue backpressure, circuit breakers, shed non-critical traffic
  - Scale resources or fail over to healthy region/replica if available
  - Quarantine problematic jobs, halt destructive batch operations, or switch systems to read-only if data integrity risk exists
- Gather evidence to guide action:
  - Inspect dashboards: error rates, latency, saturation; review logs, traces, and metrics for anomalies
  - Check dependency status pages and recent maintenance activities
- If feasible, reproduce symptoms in a safe environment using #reproduce_bug; otherwise use low-risk probes in production with tight blast-radius control
- Communicate status, actions taken, and next steps at agreed intervals; record decisions and outcomes in the timeline

**3. Cause Isolation and Fix**
- Narrow the fault domain using #isolate_cause:
  - Bisect recent changes, toggle components, or isolate traffic to identify failing path
  - Compare healthy vs affected instances; examine diffs in config, versions, and environment
- Implement the minimal safe fix:
  - Use #impl_change or #quick_fix for hotfixes behind appropriate risk controls
  - Add characterization or regression tests with #write_tests to lock in corrected behavior
  - Validate changes using #run_all_tests and smoke tests in staging or a safe subset of production
- If a full solution requires broader work, stabilize with mitigations and schedule follow-up under #feature_dev or #refactor
- Maintain heightened monitoring after applying fixes; be prepared to roll back if metrics regress

**4. Communication and Coordination**
- Keep stakeholders informed:
  - Internal updates on impact, mitigation status, and ETA to recovery
  - External communications when customer-facing impact occurs (status page, support macros)
- Ensure a single source of truth (incident doc) capturing:
  - Timeline of events, hypotheses tested, actions taken, outcomes, and current status
  - Roles, decisions, artifacts (logs, screenshots, dashboards)
- Coordinate cross-team and third-party efforts; track requests and responses (tickets, vendor contacts)
- Manage handoffs if incident spans shifts; ensure context continuity with a structured briefing

**5. Recovery and Verification**
- Confirm restoration:
  - Verify SLO/SLA metrics stable (error rates, latency, throughput) and user journeys functional
  - Reconcile data: audit for duplication, loss, or inconsistency; repair or backfill as needed
  - Ensure queues drain, jobs catch up, and caches warm as expected
- Carefully revert temporary mitigations (rate limits, feature flags, maintenance modes) under observation
- Validate security posture and access changes if the incident touched credentials or permissions
- Confirm monitoring and alerting are back to normal and tuned to avoid alert storms or silencing critical signals

**6. Post-Incident Review and Improvements**
- Conduct a blameless post-incident review:
  - Summarize impact, user experience, root cause, contributing factors, detection and response timelines
  - Identify what worked well and opportunities to improve detection, tooling, and process
- Define and prioritize remediation actions with owners and due dates:
  - Permanent code fixes, test coverage additions, guardrails (rate limits, circuit breakers), and safer defaults
  - Monitoring/alerting enhancements, runbook updates, and chaos drills
- Apply #doc_update to update runbooks, architecture notes, and incident knowledge base
- Apply #code_review for remediation changes to ensure quality and prevent regressions
- Feed systemic improvements into prompts_config/workflows.md and prompts_config/tech_stack.md if process or patterns need adjustment
- Track follow-ups to completion; avoid closing the incident until critical remediations are scheduled and communicated

Apply technology-specific patterns from: prompts_config/tech_stack.md  
Follow project quality standards from: prompts_config/quality_standards.md  
Integrate with project workflows from: prompts_config/workflows.md

## Configuration Points

- Severity Levels and Criteria: SEV classification thresholds, impact definitions, and escalation triggers
- Escalation Policies: On-call rotations, paging rules, handoff procedures, and subject-matter expert directories
- Communication Protocols: Status page templates, stakeholder matrices, internal update cadence, and public messaging guidelines
- Runbooks and Playbooks: Standard mitigation steps for common failure modes (availability, latency, data, security, dependencies)
- Monitoring and Alerting: Signal sources, dashboards, alert thresholds, noise controls, and observability conventions
- Change Management: Deployment strategy, rollback procedures, feature flag policies, and maintenance windows
- Data Integrity Safeguards: Write-freeze procedures, backup/restore workflows, reconciliation patterns, and audit logging
- Security Considerations: Containment workflows, credential rotation, forensic data handling, and legal/compliance notifications
- Postmortem Process: Review format, artifact collection requirements, remediation tracking, and follow-up SLAs

## Related Prompts

**Prerequisites**: #route_task, #context_intake, #code_orient  
**Complements**: #reproduce_bug, #isolate_cause, #quick_fix, #impl_change, #write_tests, #run_all_tests  
**Follows**: #doc_update, #code_review, #refactor, #feature_dev, #product_strategy

## Examples

**Availability Incident**: "Spike in 5xx errors after deployment"
- Declare SEV, assign roles, freeze deploys
- Roll back recent release; toggle off new feature flag
- Inspect logs/traces, compare diffs; isolate a failing controller
- Hotfix null-check; add regression test; redeploy and monitor
- Update runbook with detection pattern and mitigation steps

**Performance Degradation**: "API latency doubled due to upstream dependency"
- Triage and inform stakeholders of degraded experience
- Apply circuit breakers and aggressive request timeouts
- Route read-heavy traffic to cache; reduce concurrency to protect DB
- Engage vendor; add fallback path; monitor until metrics stabilize
- Add alert for dependency latency; document fallback strategy

**Data Integrity Issue**: "Duplicate orders from retry loop"
- Halt order creation temporarily; quarantine affected messages
- Identify idempotency gap; deduplicate and reconcile records
- Implement idempotency keys and backoff; add tests
- Resume writes under observation; notify impacted customers via support
- Capture remediation tasks for broader resilience improvements

**Security Incident**: "Leaked API key discovered in logs"
- Rotate credentials immediately; restrict access; enable enhanced logging
- Assess blast radius and revoke affected tokens/sessions
- Review logs for suspicious activity; preserve forensic artifacts
- Patch code to prevent logging secrets; add detection rules
- Coordinate legal/compliance notifications as required

**Third-Party Outage**: "Payment provider unavailable"
- Degrade gracefully: queue transactions and inform users
- Increase retry backoff; fail over to secondary if available
- Communicate status page updates; monitor vendor recovery
- Reconcile queued transactions post-recovery; verify no double charges
- Add chaos drill to practice provider outages
