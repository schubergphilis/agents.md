---
name: sbp-runbook-author
description: Use when generating operational runbooks from code and infrastructure — produces runbooks that work at 3 AM, covering common failure scenarios with specific diagnosis and resolution steps, copy-pasteable commands, and clear escalation paths.
metadata:
  domain: platform
  lifecycle: run
---

# Operational Runbook Author

Generate a runbook for the system under review by reading the actual codebase: configs, deployment files, monitoring setup, error handling patterns, and dependency declarations. The runbook must be usable by an on-call engineer at 3 AM under pressure — no vague instructions, no assumptions about tribal knowledge.

## Step 1: System overview

Start with what matters when you get paged.

- **What is this system?** One paragraph. What it does, why it exists.
- **What depends on it?** Upstream consumers, downstream dependencies, data flows.
- **What does it depend on?** Databases, message queues, external APIs, other internal services.
- **Where does it run?** Infrastructure, regions, deployment topology.
- **Who owns it?** Team, contact channels, escalation chain.

Source this from: README files, deployment configs (Kubernetes manifests, Terraform, CloudFormation), service mesh configs, dependency declarations (package.json, requirements.txt, go.mod).

## Step 2: Health checks and key metrics

Document how to tell if the system is healthy right now.

- **Health check endpoints**: exact URLs, expected responses, what each check validates.
- **Key metrics and normal ranges**: error rate (normal < X%), latency p50/p95/p99 (normal < Xms), throughput (normal ~X req/s), resource saturation (CPU, memory, disk, connections).
- **Dashboards**: links or names of monitoring dashboards.
- **Log locations**: where to find logs, useful log queries for common problems.

Source this from: health check implementations in code, monitoring configs (Prometheus rules, Datadog monitors, Grafana dashboards), logging configuration, alerting rules.

## Step 3: Common failure scenarios

For each scenario below, provide the full incident response flow. Only include scenarios that are relevant to the system — skip what does not apply, add system-specific scenarios found in the code.

### Scenario template

For each scenario, document:

1. **Symptoms** — What alerts fire. What users see. What dashboards show.
2. **Diagnosis steps** — Specific commands to run, specific dashboards to check, specific log queries to execute. Every command must be copy-pasteable.
3. **Resolution steps** — Exact commands to fix the issue. Not "restart the service" but the actual restart command with the correct service name, namespace, and any flags.
4. **Verification** — How to confirm the fix worked. What metrics should return to normal and in what timeframe.
5. **Escalation** — When to wake someone else up. Who to contact. What information to include in the escalation.

### Standard scenarios to evaluate

- **Service completely down**: process crashed, container not starting, deployment failed.
- **High latency**: slow responses, timeouts, upstream impact.
- **Disk full**: log volume growth, temp file accumulation, database growth.
- **Certificate expiry**: TLS cert expired or about to expire, cert renewal failure.
- **Dependency failure**: database unreachable, external API down, message queue unavailable.
- **Data inconsistency**: out-of-sync replicas, stale caches, failed migrations, corrupted state.
- **Resource exhaustion**: memory leak, connection pool exhaustion, thread pool saturation, file descriptor limits.
- **Authentication/authorization failure**: token expiry, secret rotation gone wrong, permission changes.

Source scenario details from: error handling code, retry logic, circuit breaker configs, fallback implementations, health check failure modes, known issues in commit history.

## Step 4: Recent changes

On-call needs to know what changed recently because changes cause incidents.

- **Where to check for recent deployments**: CI/CD system, deployment logs, git history.
- **How to identify what changed**: specific commands to diff recent releases, view deployment history, check feature flag changes.
- **How to roll back**: exact rollback commands for the deployment system in use.

Source this from: CI/CD configs (GitHub Actions, GitLab CI, Jenkins, ArgoCD), deployment scripts, release processes.

## Step 5: Contact list and escalation

- **Primary on-call**: how to find who is on call right now (PagerDuty, OpsGenie link or command).
- **Escalation path**: who to contact if the primary cannot resolve, with timeframes (e.g., escalate after 30 minutes without progress).
- **Domain experts**: who knows this system best, for specific subsystems.
- **External contacts**: vendor support numbers, cloud provider support, third-party API contacts.

## Output format

Produce a single structured markdown document with:

- Clear headings for each section — scannable under stress.
- All commands in fenced code blocks, copy-pasteable without modification.
- Normal ranges stated next to every metric so the on-call can compare immediately.
- No jargon without explanation — assume the reader knows the tech stack but not this specific system.
- A "Quick Reference" section at the top with the five most common actions (restart, rollback, check logs, check health, escalate) and their exact commands.

A runbook that cannot be followed under pressure at 3 AM is useless. Optimize for clarity and actionability over completeness.
