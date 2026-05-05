---
name: sbp-agent-architecture-review
description: Review multi-agent system designs for correctness, resilience, and safety — map components to the three-layer reference model, evaluate against responsibility checklists, check cross-cutting concerns, and flag common anti-patterns. Use when designing or reviewing agentic systems.
metadata:
  domain: data-ai
  lifecycle: plan
---

# Agent Architecture Review

Review a multi-agent system design against the three-layer reference model. The goal is to verify that the architecture is correct, resilient, safe, and operationally ready — not just that it works in the happy path.

## The three-layer reference model

Every multi-agent system should be decomposable into three layers. If a layer is missing, that is a finding.

### Guardian layer

The safety envelope. This layer exists to prevent the system from causing harm, exceeding boundaries, or operating without oversight.

Responsibilities:
- **Safety enforcement**: hard limits that cannot be overridden by lower layers (budget caps, rate limits, scope boundaries).
- **Policy enforcement**: organizational rules applied consistently (data classification, access controls, compliance requirements).
- **Budget controls**: spending limits, token limits, compute limits — with hard stops, not just warnings.
- **Human escalation**: clear triggers for when the system must stop and involve a human. Not optional, not advisory.
- **Audit logging**: every significant decision, delegation, and action recorded in tamper-resistant logs.

### Orchestration layer

The coordination brain. This layer decomposes work, delegates to workers, and verifies results.

Responsibilities:
- **Task decomposition**: breaking complex goals into manageable, well-scoped sub-tasks.
- **Delegation**: assigning tasks to appropriate workers with clear instructions and success criteria.
- **Result verification**: checking worker output for correctness, completeness, and safety before accepting it.
- **Retry logic**: handling worker failures with bounded retries, backoff, and eventual escalation.
- **Dependency tracking**: understanding which tasks depend on which results, and sequencing accordingly.
- **Progress reporting**: providing visibility into what is happening, what is complete, and what is blocked.

### Worker layer

The execution hands. These agents perform specific, scoped tasks and report results.

Responsibilities:
- **Scoped execution**: each worker has a clearly defined capability boundary. It does one thing and does it well.
- **Structured status reporting**: workers report success, failure, or partial results in a structured format the orchestrator can parse.
- **Permission boundaries**: workers have only the permissions they need for their specific task. No ambient authority.
- **No self-modification**: workers do not modify their own instructions, permissions, or scope.

## Review procedure

### 1. Map components to layers

Create a table mapping every component in the architecture to its layer:

| Component | Layer | Responsibilities | Notes |
|-----------|-------|-----------------|-------|
| PolicyGuard | Guardian | Rate limiting, budget enforcement | Missing audit logging |
| TaskPlanner | Orchestration | Task decomposition, delegation | No retry logic visible |
| CodeWriter | Worker | Code generation | Has file system write access — scope too broad? |

If a component spans multiple layers, that is a design smell. Note it.
If a layer has no components mapped to it, that is a critical finding.

### 2. Evaluate each layer against its responsibility checklist

For each layer, walk through its responsibilities and assess:

- **Present and effective**: the responsibility is clearly implemented and tested.
- **Present but weak**: implemented but with gaps (e.g., rate limiting exists but has no hard cap).
- **Missing**: not implemented. State the risk.

**Guardian layer checklist**:
- [ ] Can any agent exceed budget limits? What happens when limits are reached?
- [ ] Can any agent take actions outside its defined scope?
- [ ] Are there hard stops that cannot be bypassed by the orchestrator or workers?
- [ ] When does the system escalate to a human? Is this tested?
- [ ] Are all significant decisions and actions audit-logged?

**Orchestration layer checklist**:
- [ ] How are tasks decomposed? Is the decomposition strategy appropriate for the domain?
- [ ] How does the orchestrator verify worker results? Does it check, or does it trust?
- [ ] What happens when a worker fails? How many retries? What is the escalation path?
- [ ] Can the orchestrator get stuck in an infinite loop? What bounds exist?
- [ ] Is progress visible to operators and users?

**Worker layer checklist**:
- [ ] Are worker permissions scoped to their specific task?
- [ ] Do workers have access to resources they do not need?
- [ ] Do workers report results in a structured format the orchestrator can validate?
- [ ] Can a worker modify its own instructions or scope?
- [ ] Can a worker invoke other workers directly (bypassing orchestration)?

### 3. Cross-cutting concerns

Evaluate concerns that span all layers:

**Identity and memory**:
- How is agent identity maintained across interactions?
- Is conversation/task history stored? Where? Who can access it?
- Can one agent impersonate another?
- Is memory bounded, or can it grow without limit?

**Failure modes**:
- What happens when an external API is unavailable?
- What happens when an agent produces invalid output?
- What happens when the orchestrator itself fails? Is there a supervisor?
- Are failure modes tested, or are they theoretical?

**Security boundaries**:
- How are secrets managed? Do agents have direct access to credentials?
- Are network boundaries enforced between agents?
- Can a compromised worker escalate privileges?
- Is input from external sources (users, APIs) treated as untrusted?

**Observability**:
- Can operators see what every agent is doing in real time?
- Are there metrics for task completion rate, error rate, latency, and cost?
- Can operators intervene (pause, stop, redirect) during execution?
- Is there enough logging to reconstruct what happened after an incident?

### 4. Self-improvement boundaries

If the system has self-modification or self-improvement capabilities, assess the maturity level:

- **Level 0 — Static**: agents do not modify themselves. Configuration is external and human-controlled.
- **Level 1 — Tunable**: agents can adjust parameters within predefined ranges (e.g., temperature, retry count) but cannot change their own prompts or capabilities.
- **Level 2 — Prompt-adaptive**: agents can modify their own prompts or strategies within a guardian-defined envelope. Changes are logged and reversible.
- **Level 3 — Capability-expanding**: agents can acquire new tools or capabilities, subject to guardian approval and human oversight.
- **Level 4 — Autonomous evolution**: agents modify their own architecture. This level requires extraordinary safety controls and is rarely appropriate.

For levels 2+, verify:
- Are changes bounded and reversible?
- Is there a guardian-layer veto on self-modifications?
- Are changes logged and auditable?
- Can the system be rolled back to a known-good configuration?

### 5. Output

Produce findings organized by severity:

**Critical** — must be addressed before the system is deployed or allowed to operate:
- Missing guardian layer
- No budget or scope limits
- Workers with unbounded permissions
- No human escalation path

**Warning** — should be addressed before production use:
- Weak result verification (trust without verify)
- Unbounded retry logic
- Missing observability
- Insufficient audit logging

**Advisory** — improvements to consider:
- Opportunities to narrow worker permissions
- Observability enhancements
- Testing recommendations

For each finding, provide:
1. What was found (specific, not vague).
2. Why it matters (what could go wrong).
3. Recommended fix (concrete, actionable).

## Common anti-patterns

Flag these if found in the architecture:

- **God agent**: one agent that does everything — orchestrates, executes, and guards itself. No separation of concerns, no safety boundaries.
- **Trust cascade**: orchestrator trusts worker output without verification. Worker trusts external input without validation. Trust flows down with no checkpoints.
- **Infinite retry**: failed tasks are retried without bound, consuming budget and potentially causing side effects with each attempt.
- **Shared mutable state**: multiple agents read and write the same state without coordination. Race conditions and corrupt state follow.
- **Permission creep**: agents accumulate permissions over time, ending up with far more access than their task requires.
- **Phantom guardian**: a guardian layer exists in the architecture diagram but is not actually enforced in the implementation. Safety controls that can be bypassed are not safety controls.
- **Soul drift**: an agent's behavior diverges from its defined purpose over time, especially in systems with self-modification. The agent still runs, but it is no longer doing what you think it is doing.

Each anti-pattern should be flagged with a severity level and a specific recommendation for resolution.
