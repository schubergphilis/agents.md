---
name: sbp-observability-check
description: Use when verifying monitoring, alerting, and logging coverage — checks the four pillars (metrics, logs, traces, alerts), produces a coverage matrix with gaps, severity ratings, and recommended actions, and applies the 3 AM test to every component.
metadata:
  domain: platform
  lifecycle: run
---

# Observability Coverage Check

Review the system's observability posture across all four pillars. The goal is to answer one question: if this system breaks at 3 AM, can the on-call engineer diagnose and fix it from dashboards and logs alone, without reading source code?

## Pillar 1: Metrics

For each service or component, check:

- **Error rates**: are 4xx and 5xx rates tracked separately? Are they broken down by endpoint or operation?
- **Latency**: are p50, p95, and p99 measured? Are there latency budgets or thresholds defined?
- **Throughput**: is request rate tracked? Are there baselines to detect anomalies (sudden drops or spikes)?
- **Saturation**: are resource limits tracked — CPU, memory, disk, connection pools, thread pools, queue depth?
- **Business metrics**: are domain-specific signals measured (orders processed, messages delivered, jobs completed)?
- **Dashboards**: do dashboards exist? Are they useful (show context, not just raw numbers)? Can you see the system's health in 10 seconds?

Source from: monitoring configs (Prometheus rules, Datadog monitors, CloudWatch metrics), instrumentation in code (metric libraries, custom counters/gauges/histograms), dashboard definitions (Grafana JSON, Datadog dashboard configs).

## Pillar 2: Logs

For each service or component, check:

- **Error context**: when an error is logged, does it include enough information to diagnose the issue? (request ID, user context, input parameters, stack trace)
- **Structured logging**: are logs structured (JSON) or free-text? Can they be queried and aggregated?
- **Log levels**: are log levels used correctly? (ERROR for actual errors, not WARN for everything)
- **Sensitive data**: are passwords, tokens, PII, or secrets excluded from logs?
- **Retention**: how long are logs kept? Is it enough for incident investigation (minimum 30 days)?
- **Correlation**: can you trace a request across log entries? Is there a request ID or correlation ID?

Source from: logging configuration, log framework setup, log output examples in code, log shipping configs (Fluentd, Logstash, Vector).

## Pillar 3: Traces

For distributed systems, check:

- **Trace propagation**: is trace context propagated across service boundaries (HTTP headers, message metadata)?
- **Span coverage**: are key operations captured as spans? Database queries, external API calls, queue operations?
- **Sampling**: what is the sampling rate? Is it sufficient to capture errors (100% error sampling)?
- **Trace-to-log correlation**: can you jump from a trace span to the corresponding log entries?
- **Service map**: can you see the dependency graph from trace data?

For monolithic systems: note that distributed tracing is not applicable, but check whether internal operation tracing exists for performance diagnosis.

Source from: tracing library configuration (OpenTelemetry, Jaeger, Zipkin), middleware/interceptor setup, trace exporter configs.

## Pillar 4: Alerts

For each service or component, check:

- **Coverage**: will alerts fire before customers notice a problem? Are there alerts for the key metrics (error rate, latency, availability)?
- **Actionability**: does each alert tell the responder what is wrong and what to do? Or is it just "CPU high" with no context?
- **Thresholds**: are alert thresholds based on user impact (SLO burn rate) or arbitrary numbers? Are they tuned to avoid false positives?
- **Routing**: do alerts reach the right team? Is on-call rotation configured?
- **Escalation**: do alerts escalate if not acknowledged? Is there a path from page to incident?
- **Alert fatigue**: are there noisy alerts that get ignored? How many alerts fire per week? More than 1-2 per on-call shift indicates noise.
- **Gaps**: are there failure modes that would not trigger any alert? (slow degradation, partial failures, data corruption)

Source from: alerting rules (Prometheus alertmanager, PagerDuty, OpsGenie, Datadog monitors), alert routing configs, on-call schedules.

## Health checks

For each service, evaluate the health check:

- **Does it exist?** An endpoint that returns 200 when the process is running is not a health check.
- **Does it check real functionality?** Database connectivity, downstream dependency reachability, critical resource availability.
- **Liveness vs. readiness**: are they separate? Does a failed dependency take the service out of rotation (readiness) without killing it (liveness)?
- **Startup probes**: for slow-starting services, is there a startup probe to prevent premature kills?

Source from: health check endpoint implementations, Kubernetes probe configs, load balancer health check settings.

## SLOs and SLIs

- **Are SLOs defined?** What is the target availability, latency, and error rate?
- **Are SLIs measured?** Are the actual indicators being tracked against the objectives?
- **Error budgets**: is there a concept of error budget? Does the team know when they are burning through it?
- **SLO-based alerting**: do alerts fire based on SLO burn rate rather than static thresholds?

Source from: SLO definitions (Sloth, Nobl9, custom configs), SLI recording rules, error budget policies.

## Output: Coverage matrix

Produce a table:

| Component | Metrics | Logs | Traces | Alerts | Health Check | SLO |
|-----------|---------|------|--------|--------|-------------|-----|
| Service A | Full | Partial | None | Partial | Shallow | None |

Below the matrix, provide:

1. **Critical gaps** — missing observability that means incidents will be harder to diagnose or will go undetected. State the blast radius: what breaks if this gap is not addressed.
2. **High-priority improvements** — partial coverage that should be completed. Include specific actions (not "add more metrics" but "add p99 latency histogram to /api/orders endpoint").
3. **Advisory notes** — nice-to-have improvements, lower urgency.

### The 3 AM test verdict

For each component, answer: can an on-call engineer who did not build this system diagnose an issue at 3 AM using only dashboards, logs, and alerts? State YES, PARTIALLY, or NO — with the specific reason.
