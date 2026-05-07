---
name: sbp-threat-model
description: Use when preparing for a design review or when evaluating security posture — identifies assets, maps attack surfaces, assesses risks, and produces a prioritized threat matrix with concrete mitigations.
metadata:
  domain: security
  lifecycle: plan
---

# Threat Modeling

Walk through this structured threat model for the system or change under review. The goal is a prioritized list of real risks with concrete mitigations — not a compliance exercise.

## Step 1: Identify what you are protecting

Start here. If you do not know what matters, you cannot reason about threats.

- **Data assets**: customer data, credentials, secrets, PII, financial records, audit logs.
- **Access assets**: admin consoles, CI/CD pipelines, cloud accounts, DNS, certificate management.
- **Availability assets**: services with SLAs, data stores that cannot tolerate downtime, integration points.
- **Reputation assets**: anything where a breach makes the news or breaks customer trust.

For each asset, state: who owns it, where it lives, what classification level it carries, and what the impact of compromise would be (confidentiality, integrity, availability).

## Step 2: Identify threat actors

Consider who would attack this system and why. Be specific — "hackers" is not a threat actor.

- **External attackers**: opportunistic (automated scanners, credential stuffing) and targeted (APT, ransomware operators).
- **Insider threats**: disgruntled employee, compromised developer account, overprivileged service account.
- **Supply-chain actors**: compromised dependency, malicious package maintainer, hijacked build tool.
- **Automated threats**: bots, scrapers, DDoS, cryptominers exploiting exposed compute.

For each actor, state: motivation, capability level, and likely attack vector.

## Step 3: Map attack surfaces

Enumerate every boundary where an attacker can interact with the system.

- **APIs and endpoints**: public, internal, admin. Auth mechanisms on each.
- **Authentication and authorization**: how identity is established, how permissions are enforced, where tokens live.
- **Data stores**: databases, object storage, caches, message queues. Who can read/write, how access is controlled.
- **CI/CD pipeline**: who can trigger builds, what secrets are available during build, who can modify pipeline definitions.
- **Infrastructure**: cloud accounts, IAM roles, network boundaries, DNS, certificate issuance.
- **Human interfaces**: admin UIs, support tooling, SSH/console access, VPN.
- **Third-party integrations**: webhooks, OAuth flows, shared credentials, data feeds.

## Step 4: Analyze each surface

For each attack surface identified above, answer:

1. **What could go wrong?** Describe specific attack scenarios, not generic categories. "Attacker uses stolen API key to exfiltrate customer records via the export endpoint" not "unauthorized access."
2. **Likelihood**: How easy is this to exploit? Does it require insider access, zero-days, or just a Google search? Rate: HIGH (actively exploited in the wild), MEDIUM (requires moderate skill or access), LOW (theoretical or requires significant effort).
3. **Impact**: What happens if this succeeds? Rate: CRITICAL (data breach, full compromise, extended outage), HIGH (significant data exposure or service degradation), MEDIUM (limited exposure, recoverable), LOW (minimal impact).
4. **Severity**: Combine likelihood and impact. This drives prioritization.

Focus on what actually gets exploited in real-world incidents:
- Exposed secrets in repositories or logs
- Overprivileged service accounts and IAM roles
- Missing rate limiting on authentication endpoints
- Unpatched dependencies with known CVEs
- SSRF and injection in internal services assumed to be "trusted"
- CI/CD pipeline poisoning
- Misconfigured cloud storage permissions

## Step 5: Assess mitigations

For each threat identified:

- **What exists today?** Name the specific control (not "we have security"). WAF rule? Network policy? Secrets rotation? MFA?
- **Is it effective?** A WAF that is in monitoring mode does not block attacks. An alarm that nobody responds to is not a mitigation.
- **What is missing?** Be specific: "No rate limiting on /api/auth/token endpoint" not "need better security."
- **What compensating controls exist?** If the primary mitigation is weak, what else limits the blast radius?

## Output: Threat matrix

Produce a table summarizing findings:

| # | Attack surface | Threat scenario | Likelihood | Impact | Severity | Existing mitigation | Gap | Recommended action |
|---|---------------|-----------------|------------|--------|----------|--------------------|----|-------------------|
| 1 | Example | Example | HIGH | CRITICAL | CRITICAL | None | Full | Implement X by Y |

Below the table, provide:

1. **Critical findings** — must be addressed before deployment or within days.
2. **High-priority actions** — address within the current sprint or iteration.
3. **Advisory notes** — improvements to consider, lower urgency.

Each action item must be concrete, assignable, and testable. "Improve security" is not an action item. "Add rate limiting of 10 req/min to /api/auth/token and alert on threshold breach" is.
