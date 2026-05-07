---
name: sbp-test-planning
description: Use when designing test coverage before writing code, or when adding tests to existing untested code — especially in mission-critical systems where coverage gaps become incidents.
metadata:
  domain: cross-cutting
  lifecycle: plan
---

# Test Planning

This skill helps you design test coverage before you write tests. Starting implementation or writing tests without a plan leads to two failure modes: coverage of the happy path only (because that is the case you built), or coverage of everything you can think of at the time (bloated, slow, duplicative).

The goal: decide *what* to test and *how* to test each thing, before the pressure of implementation narrows your thinking.

## Step 1: Name the behaviors

Start from the outside. What does this feature need to do, from the perspective of its caller or user?

List behaviors in plain language, not implementation terms:

- "When a user submits a valid form, they see a confirmation page."
- "When the payment API times out, the order is retained and the user sees a retry option."
- "When a duplicate email is submitted, the existing account is returned, not a new one."

Each behavior is a test you will eventually write. The list is the skeleton of your test suite.

If you cannot list behaviors without describing internal implementation ("calls the validator, then the persister"), the requirements are not clear yet. Go back to requirements before planning tests.

## Step 2: Enumerate the cases

For each behavior, think about the shapes of input and state that could hit it.

**Golden path**: the common, expected case. This is the case the feature was built for. Always test it.

**Boundary cases**:

- Empty input: empty string, empty list, null.
- Minimum and maximum values: one, many, max length, zero.
- Edge of the valid range: just inside, just outside.
- Unicode, whitespace, special characters in strings.
- Concurrent or interleaved operations, if concurrency matters.

**Failure modes**:

- External dependencies fail: database down, API times out, network error.
- Invalid input: malformed, missing required fields, wrong type.
- Unauthorized access: wrong credentials, insufficient permissions, expired session.
- Resource exhaustion: disk full, memory limit, rate limit hit.
- Race conditions: two writers, stale reads, lost updates.

**State-dependent cases**:

- First time vs. repeated calls.
- Cold cache vs. warm cache.
- Fresh database vs. populated database.
- Feature flag on vs. off.

Not every category applies to every feature. Go through the list deliberately and mark which ones matter for this feature. A feature with no external dependencies does not need "API timeout" tests; a feature with five external dependencies has at least five.

## Step 3: Pick the right test type for each case

Not every case needs the same kind of test. Using the wrong type wastes runtime, hides bugs, or both.

**Unit test**: a single function or small piece of logic, tested in isolation.

- Best for: pure functions, complex business logic, calculations, parsers, state machines.
- Cheap to write, fast to run, gives precise failure signals.
- Weakness: lies about integration. A unit test with a mocked collaborator says nothing about whether the real collaborator works.

**Integration test**: two or more real components talking to each other.

- Best for: verifying that your code and the thing it depends on actually agree — your ORM and the database, your HTTP client and the API, your serializer and the consumer.
- Catches bugs that unit tests cannot: schema mismatches, protocol disagreements, misconfigured clients.
- Slower than unit tests, but much more trustworthy for boundary behavior.

**End-to-end test**: full system from the outside, exercising the real runtime paths.

- Best for: critical user journeys, regressions that cross component boundaries, "does the deploy actually work" smoke tests.
- Slowest, most brittle, most expensive to maintain.
- Use sparingly. One or two per critical journey is usually enough.

**Contract test**: verifies your side of an agreement with another system.

- Best for: team boundaries, versioned APIs, event schemas.
- Catches: breaking changes before they reach the consumer.

Rule of thumb: most coverage at the unit level, real boundaries covered by integration tests, critical journeys covered end-to-end. Invert the pyramid and your test suite becomes slow and flaky.

## Step 4: Plan the data and state

For each test, think about what setup it needs and what state it leaves behind.

- **Test data**: specific inputs, realistic but minimal. Avoid lorem ipsum-style filler data that obscures intent — name the fixture after what it represents ("customer_with_overdue_invoices", not "test_customer_1").
- **Fixtures vs. factories**: fixtures are fast but brittle; factories are flexible but slower. Choose per test category.
- **Isolation**: each test should be runnable alone, in any order, repeatedly. Shared state between tests is a source of flakiness and slow debugging.
- **Teardown**: what state does this test create in the database, the file system, the external service? It must be cleaned up or isolated so subsequent tests do not see it.

If the feature touches external state (databases, message queues, files), decide now whether each test uses the real thing (integration) or a faithful stub (unit). Write it down so you are not making this choice 30 tests deep.

## Step 5: Decide the non-functional targets

Performance and reliability are testable too. Decide up front which ones matter for this feature.

- **Speed**: individual tests should run in under a second. The full suite should stay fast enough that developers run it before every push. If a test is slow, know why.
- **Reliability**: zero flakiness target. A test that fails once in twenty runs is worse than no test — it trains the team to ignore failures.
- **Determinism**: no dependence on real time, real network, or real random values. Seed or inject them.

If this feature has specific performance or throughput requirements, add tests for those too. A "it must handle 1000 requests/second" requirement needs a test, not a comment.

## Step 6: Write the plan down

Keep it short. A bulleted list is usually enough. The plan is for yourself and your reviewers, not for permanent documentation.

```
## Test plan: user profile update

Unit tests
- Valid update returns the updated profile
- Missing required fields raise ValidationError
- Fields beyond max length raise ValidationError
- Unicode in name and bio round-trips correctly

Integration tests
- Update writes through to the database
- Concurrent updates on the same profile: last write wins, no data loss
- Update with stale version token is rejected

End-to-end
- Happy path: user logs in, edits profile, sees updated profile

Not covered (and why)
- Performance under load: no specific requirement; defer to load test suite
- Profile image upload: separate feature, separate plan
```

The "not covered, and why" section is as important as the covered list. It makes deliberate the decision to skip something, and gives future readers a way to evaluate whether the scope was right.

## Step 7: Review before you build

A good test plan catches problems early. Before starting implementation:

- **Read the plan as if you were reviewing it**: do the tests actually prove the behavior works, or just that the code compiles?
- **Check for missing failure modes**: walk through the list of dependencies and ask, "if this fails, what do I expect?" If there is no test for it, either add one or explicitly call out that you are not testing it.
- **Check for over-testing**: are three unit tests actually testing three different things, or variations of the same case? Redundant tests slow the suite without catching more bugs.
- **Challenge the test types**: is this unit test carrying more weight than a unit test should? Does this e2e test really need to be e2e?

The reviewer can be a colleague, a rubber duck, or yourself the next day. Fresh eyes on the plan save days of rework on the implementation.

## Common anti-patterns to avoid

- **Plan-free testing**: writing tests as you go, based on whatever you just implemented. You end up testing what you built, not what the feature should do.
- **Testing implementation, not behavior**: "calls the validator" is not a useful assertion. "Rejects invalid input" is.
- **Exhaustive coverage of the happy path, nothing else**: the most common real failure mode. Failures live in the unhappy paths.
- **Mocking everything**: mocks that return whatever you tell them always pass. They prove nothing.
- **Ignoring flakiness**: "it's flaky but it usually passes" is a bug you are choosing not to fix. It will bite later.
- **Over-reliance on e2e**: slow, brittle, hard to diagnose. Reach for unit and integration first.

## Closing notes

A test plan is cheap to write and expensive to skip. Fifteen minutes of planning saves hours of implementation thrashing and catches scope gaps before they become production gaps.

The plan is also the first useful artifact for code review: "here is what I intend to build and verify." Reviewers can push back on the plan before a single line of code is written.
