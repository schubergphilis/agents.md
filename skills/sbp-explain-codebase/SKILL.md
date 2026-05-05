---
name: sbp-explain-codebase
description: Explain unfamiliar code, infrastructure, or architectural patterns in context — trace data flow, identify patterns, surface design decisions, and teach the reasoning behind the implementation. Use when onboarding, reviewing, or debugging.
metadata:
  domain: cross-cutting
  lifecycle: build
---

# Explain Codebase

Help an engineer understand unfamiliar code, infrastructure, or architecture. The goal is not just to describe what things do, but to teach why they were built this way and what to watch out for.

## Start with context

Before explaining anything, establish what the engineer is trying to accomplish:

- **Reviewing**: they need to understand enough to evaluate correctness and risk.
- **Debugging**: they need to trace a specific behavior through the system.
- **Onboarding**: they need the big picture first, then details on their area.
- **Extending**: they need to know the conventions and boundaries before adding code.

The right explanation depends on the purpose. A reviewer needs risk areas highlighted. A debugger needs data flow traced. A new joiner needs the mental model.

Ask: "What are you trying to understand, and what is the context — are you reviewing, debugging, onboarding, or building on top of this?"

## Architecture overview first

Start at the highest useful level before zooming in. For any system:

1. **What does this system do?** One sentence. What problem does it solve for whom?
2. **What are the major components?** Services, data stores, queues, external dependencies. Draw the boxes and arrows.
3. **How do requests/data flow through it?** Trace the primary path from entry point to result.
4. **What are the boundaries?** Where does this system end and others begin? What does it own vs. depend on?
5. **What are the operational characteristics?** How is it deployed, scaled, monitored? What does failure look like?

Only then zoom into the specific area of interest.

## Trace data and request flow

For the specific code or component being examined:

- **Entry point**: where does execution begin? HTTP handler, event consumer, scheduled job, CLI command.
- **Data transformation**: what happens to the data at each step? What format does it arrive in, how is it validated, transformed, stored?
- **Branching logic**: where does the code make decisions? What are the conditions and what happens on each branch?
- **External calls**: what other services, databases, or APIs are contacted? What happens if they are slow or unavailable?
- **Exit point**: where does execution end? What does the caller receive? What side effects have occurred?

Trace the happy path first, then the error paths. Most bugs live in error handling.

## Identify patterns and conventions

Name the patterns being used. Engineers learn faster when they can connect code to known concepts.

- **Design patterns**: "This uses the repository pattern to abstract data access, which means you add new queries here, not in the service layer."
- **Architectural patterns**: "This is an event-driven architecture with eventual consistency — the write service publishes events and the read service consumes them asynchronously."
- **Project conventions**: "This codebase puts all database queries in `*_repo.py` files and all HTTP handlers in `*_handler.py` files. Follow this convention when adding new endpoints."
- **Infrastructure patterns**: "This uses the sidecar pattern — the proxy container handles TLS termination so the application container does not need to manage certificates."

If a pattern is applied inconsistently, note it: "Most services use the repository pattern, but the billing service has queries scattered through the handler layer — this is tech debt, not a different convention."

## Explain design decisions

Go beyond "what" to "why." Engineers need to understand the reasoning to maintain and extend the code correctly.

- **"This uses a circuit breaker pattern because the downstream payment service has historically had latency spikes. Without it, a slow payment service would back up the entire request queue and take down the checkout flow."**
- **"This data is denormalized into both tables because the read path needs sub-millisecond response times and a join would add 50ms. The trade-off is that writes need to update both places, and the sync job handles eventual consistency."**
- **"This is implemented as a separate microservice rather than a library because the ML model requires GPU instances, and coupling it to the API service would force GPU allocation for every API pod."**

When the reason is not obvious from the code, say so: "I cannot determine why this was implemented this way from the code alone. Likely reasons include X or Y — check the ADR documents or git history for the original decision."

## Surface risks and tech debt

Point out areas that need extra care, especially for engineers who are new to the codebase.

- **Fragile code**: "This function has no input validation and will throw an unhandled exception if the payload is missing the `customer_id` field. This is a known gap."
- **Hidden coupling**: "This service reads directly from the orders database. If the orders team changes the schema, this service breaks. There is no contract or API boundary here."
- **Scaling limits**: "This processes items sequentially. It works fine at current volume but will become a bottleneck above approximately 10,000 events per minute."
- **Security concerns**: "This endpoint does not check authorization — it trusts that the API gateway has already validated the token. If the gateway routing changes, this endpoint could be exposed."
- **Operational gaps**: "There is no health check for the connection to the external API. If that API goes down, this service will appear healthy while silently failing."

## For infrastructure

When explaining infrastructure (Terraform, Kubernetes, cloud resources, CI/CD):

- **What does it provision?** Name the resources and their purpose in plain language.
- **What depends on it?** If this resource is deleted or misconfigured, what breaks?
- **What happens when it fails?** Is there redundancy? Automatic recovery? Manual intervention required?
- **What are the cost implications?** Especially for auto-scaling resources or resources billed by usage.
- **Where are the secrets?** How are credentials managed, rotated, and accessed?
- **What is the blast radius of a change?** Does `terraform apply` affect one resource or fifty?

## Teaching, not just describing

Frame explanations to build understanding, not just convey facts.

Instead of: "This is a circuit breaker."
Say: "This is a circuit breaker pattern. When the downstream service fails 5 times in 30 seconds, the circuit 'opens' and requests immediately return an error instead of waiting for a timeout. This prevents a failing dependency from consuming all your connection pool and taking down your service too. It resets after 60 seconds and tries again."

Instead of: "This uses Redis for caching."
Say: "This caches user session data in Redis to avoid hitting the database on every request. The TTL is 15 minutes, which means a user could see stale data for up to 15 minutes after a profile change. This is an intentional trade-off — the alternative was 3x database load during peak hours."

Connect concepts to consequences. Engineers remember "this prevents cascading failures" longer than they remember "this is a circuit breaker."
