---
name: sbp-feature-development
description: Build a new feature using test-driven development — clarify requirements, plan test coverage, drive implementation through red/green/refactor, integrate, and verify. Use when starting any feature that will reach production, especially in mission-critical systems where untested code is a liability.
metadata:
  domain: cross-cutting
  lifecycle: build
---

# Feature Development

This skill walks you through building a new feature using test-driven development. The goal is not ceremony — it is to reach production with a feature that works, has a regression safety net, and does not break what already works.

TDD is particularly valuable in mission-critical systems: the test you write before the code is the test that will wake someone up if this feature regresses at 3 AM.

## Step 1: Understand what you are building

Before writing any code or tests, answer these questions in plain language:

- **What does the user or caller need to do that they cannot do today?** State this as a capability, not an implementation.
- **What is the acceptance criteria?** How will you know this feature works? Be specific enough that someone else could verify it.
- **What is the blast radius?** Which existing systems does this feature touch? What could break?
- **What is the non-goal?** What are you explicitly *not* doing in this iteration?

If any of these are unclear, stop and ask. Writing code against fuzzy requirements is the most expensive form of rework.

## Step 2: Plan the test coverage

Design the tests before writing the code. Think about what could go wrong, not just the happy path.

For each piece of the feature, identify:

- **Golden path**: the common, expected case.
- **Boundary cases**: empty input, max length, zero, one, many, negative.
- **Failure modes**: what happens when the database is down, the external API times out, input is malformed, the user is unauthorized?
- **Integration seams**: where does this feature meet existing code? What are the assumptions at that boundary?

Write the test plan down. It does not need to be formal — a bulleted list is enough. The point is to decide coverage *before* implementation pressure creates shortcuts.

## Step 3: Consider refactoring first

If the existing code makes the feature harder to add, refactor first — with its own tests — before starting the feature.

Signs refactoring should come first:
- You need to change an existing function's signature.
- You cannot test the feature without also changing unrelated behavior.
- You find yourself wanting to duplicate logic to avoid touching the original.

Refactoring before feature work keeps the feature diff clean and the review focused.

## Step 4: Drive implementation through red/green/refactor

Execute one loop per behavior, not per function:

- **Red**: write a failing test that describes the desired behavior. Run it. Confirm it fails for the *right reason* — not a syntax error, but because the behavior does not exist yet.
- **Green**: write the minimum code needed to make the test pass. Resist adding anything the test does not demand. "Minimum" includes hardcoded values if that is what the current test requires — subsequent tests will force generalization.
- **Refactor**: with tests green, improve the code. Remove duplication, clarify names, extract helpers. Run tests after each change.

Repeat for each behavior: golden path first, then boundary cases, then failure modes.

Do not skip the refactor step. Skipping it is how test-driven code ends up as messy as untested code — just more of it.

## Step 5: Add error handling and edge cases deliberately

Do not sprinkle defensive code everywhere. Decide explicitly where each class of error is handled.

- **Input validation**: at the boundary where input enters your system (API handler, CLI parser, message consumer). Not in every internal function.
- **External calls**: wrap with timeouts, retries where appropriate, and clear failure modes. Do not silently swallow.
- **Unexpected state**: fail fast and loud. An assertion that crashes is better than a silent wrong answer in production.

Every error path should have a test. If a failure mode is worth handling, it is worth proving with a test that it *is* handled.

## Step 6: Integration verification

With unit tests green, verify the feature in realistic context:

- **Run the full test suite**: not just the new tests. Regressions often live in code you did not think you touched.
- **Run the feature end-to-end**: against a real database, real network, real dependencies (or faithful stubs). Unit tests lie about integration.
- **Exercise adjacent flows**: if this feature changes shared code, use the adjacent features that touch it. Do not wait for the customer to discover the regression.
- **Check observability**: does the feature emit the metrics, logs, and traces you would need at 3 AM to diagnose a problem? If not, add them now. You will not add them later.

## Step 7: Prepare for code review

Before requesting review:

- **Self-review the diff**: read it as if you were seeing it for the first time. Remove commented-out code, debug logging, and TODO stubs.
- **Confirm the tests actually test**: a test that passes without the implementation is not a test. Temporarily break the implementation and confirm tests fail.
- **Write the PR description**: what changed, why, and what to focus review on. If you cannot explain the *why* in two sentences, the feature may be over-scoped.
- **Check the performance**: if this feature sits in a hot path, have you measured? Estimates are not measurements.

## Step 8: Documentation and hand-off

Update what must be updated, skip what is noise:

- **User-facing docs**: if this changes behavior users observe.
- **Runbook**: if this introduces a failure mode someone might be paged for.
- **API reference**: if this adds or changes a public interface.
- **Changelog**: if your project has one.

Skip: explaining the code in prose. The code, its name, and its tests are the documentation for the implementation.

## Common anti-patterns to avoid

- **"I'll write tests after"**: the tests written after are different tests. They test what the code does, not what the feature should do. Write first.
- **One big test that covers everything**: hard to read, hard to diagnose when it fails. Small, focused tests tell you exactly what broke.
- **Mocking the thing you are actually testing**: a mock returning `True` does not prove correctness. Mock at the boundary, not inside the unit under test.
- **Feature-creep during implementation**: "while I'm in here, I'll also..." — that is a separate PR. Finish the feature first.
- **Skipping the refactor step**: "it works, ship it" — the second feature on this code will be slower for it.

## Closing notes

TDD is not about tests. It is about a tight feedback loop that catches your mistakes while they are cheap. The tests are a byproduct. The feedback is the product.

A feature without tests is a feature that has never been proven to work — only observed to work once. In mission-critical systems, the difference matters.
