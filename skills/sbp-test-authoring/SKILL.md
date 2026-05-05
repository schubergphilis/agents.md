---
name: sbp-test-authoring
description: Write tests that prove functionality works and catch regressions — structure each test clearly, exercise real behavior, cover happy paths and failure modes, and keep the suite fast and reliable. Use when writing new tests, adding coverage to existing code, or fixing flaky or low-value tests.
metadata:
  domain: cross-cutting
  lifecycle: build
---

# Test Authoring

This skill is about writing tests that earn their keep. A test that passes when the code is broken is worse than no test: it creates a false sense of safety and trains the team to trust the wrong signal.

The goal: tests that read like a specification, fail when they should, run fast, and stay reliable.

## Step 1: Know what each test is for

Before writing a test, state in one sentence what it proves. If you cannot, the test is unfocused.

Examples of a clear purpose:

- "Valid credentials produce a session token."
- "An expired token is rejected with 401."
- "Concurrent updates to the same record do not lose data."
- "A duplicate email returns the existing user rather than creating a new one."

Examples of an unclear purpose:

- "Test the login function." — tests *what* about it?
- "Test happy path." — which happy path, and what does success mean?
- "End-to-end test of the feature." — which behavior of the feature?

If you have done test planning first, you already have this list. If not, pause and write it.

## Step 2: Structure each test for readability

A reader should understand a test in five seconds. That means a clear, consistent structure.

**Arrange, Act, Assert** (or Given, When, Then):

```
def test_expired_token_is_rejected():
    # Arrange
    token = issue_token(expires_in=timedelta(seconds=-1))
    
    # When
    result = authenticate(token)
    
    # Then
    assert result.status == "rejected"
    assert result.reason == "token_expired"
```

The three sections should be visually distinct. Setup noise, hidden mutations, and assertions scattered through the body are what make tests hard to debug years later.

**Name tests after the behavior**, not the function under test:

- `test_expired_token_is_rejected` (good) vs. `test_authenticate_1` (useless).
- `test_duplicate_email_returns_existing_user` (good) vs. `test_create_user_edge_case` (useless).

When a test fails, the name is the first diagnostic signal. A good name tells you what broke without reading the assertion.

**Keep each test focused on one behavior**. If a test has multiple asserts and they cover different scenarios, split it. One test per behavior makes failures specific.

## Step 3: Exercise real behavior, not implementation

A test should prove the feature works, not that the code is shaped a certain way.

**Assert on outcomes, not calls**:

- Good: `assert order.total == Decimal("42.00")`
- Bad: `assert calculator.calculate.called_once_with(...)`

Outcome assertions survive refactoring; call assertions break the moment you restructure internals, even when behavior is unchanged.

**Mock at the boundary, not inside the unit under test**:

- Mock external services (databases, APIs, message queues) at their adapter layer.
- Do not mock the thing you are testing. A function that has its internal calls mocked out is being "tested" against an imaginary version of itself.

**Prefer real dependencies when they are cheap**:

- A real in-memory SQLite, a real test double of the API, a real in-process queue — each gives more signal than a mock and costs little.
- Reach for mocks when the dependency is genuinely slow, expensive, or non-deterministic, and even then only at the boundary.

**Verify the test actually tests**: temporarily break the implementation (return a wrong value, skip a step) and confirm the test fails. A test that stays green when the code is broken is not a test.

## Step 4: Cover the cases deliberately

Use the test plan to guide coverage. If you do not have a plan, walk through these categories for each behavior:

**Golden path**: the common, expected case. Must be covered.

**Boundary cases**:

- Empty input, minimum, maximum, off-by-one.
- Unicode, whitespace, special characters.
- Repeated calls, idempotency.

**Failure modes**:

- External dependency fails (timeout, 500, network error).
- Invalid input (malformed, missing fields, wrong type).
- Unauthorized access.
- Resource exhaustion.

**State-dependent cases**:

- First call vs. repeated calls.
- Empty state vs. populated state.
- Feature flags on vs. off.

Do not test every permutation of every input. Pick representatives: one boundary per boundary class, one failure mode per dependency, one state variant per meaningful state.

When you skip a case deliberately, note it — in a comment on the test file or the PR description. "No test for concurrency: serial access enforced at call site" is a better signal than silence.

## Step 5: Manage test data carefully

Tests with opaque data are tests that lie. A fixture called `test_user_1` tells the reader nothing. Name data after what it represents.

- **Name fixtures by role**: `customer_with_overdue_invoice`, `expired_session`, `admin_user`.
- **Minimal realistic data**: include only the fields the test actually cares about. Extra data is noise that obscures intent.
- **Factories over shared fixtures**: let each test build its own data. Shared fixtures create invisible coupling between tests.
- **Avoid `sleep()`**: a test that sleeps is a test that is either flaky, slow, or both. Use deterministic control of time — inject a clock, advance it in the test.
- **No dependence on real network, real time, or real randomness**: inject or stub all three. A test that passes today and fails tomorrow because DNS changed is not a test.

## Step 6: Keep the suite fast and isolated

A slow suite is a suite developers stop running. A flaky suite is a suite developers stop trusting.

**Speed**:

- Individual unit tests should run in well under a second.
- Integration tests may take a few seconds; if they take longer, look for hidden setup cost (full database migration per test? regenerating fixtures from scratch?).
- End-to-end tests can be slow but should be few in number.

**Isolation**:

- Each test must be runnable alone, in any order, repeatedly. No hidden ordering dependencies.
- No shared mutable state across tests. Either create fresh state per test or reset explicitly in teardown.
- Parallel execution should be safe. If it is not, find and fix the shared state — do not force serial execution.

**Reliability**:

- A test that fails "sometimes" is already broken. Investigate immediately — do not accept "rerun and hope."
- Common flakiness sources: real time, real network, real filesystem, concurrency without synchronization, shared state.

## Step 7: Make tests useful when they fail

The test's job is to tell you something useful when it fails. Design for that.

- **Clear assertions**: use the testing framework's native assertion helpers. `assert.equal(actual, expected)` gives a better failure message than `assert actual == expected`.
- **One logical assertion per test**: so the failure line is precise.
- **Meaningful variable names in the test body**: the stack trace and failure message should read as prose, not as `x`, `y`, `result`.
- **Avoid deep call chains in the test itself**: a test that fails five helpers deep makes debugging harder. Keep test logic flat.

## Step 8: Review your tests like code

Tests are code. They rot, they accumulate, they need review.

Before shipping:

- **Are any tests doing the same thing?** Deduplicate.
- **Are any tests actually testing nothing?** A test that passes unconditionally is technical debt.
- **Can any tests be moved to a lower level?** An integration test covering logic that could be a unit test is slow and precise-less.
- **Do the test names still describe the behavior?** Names drift after refactors. Keep them honest.

When the feature ships, the tests become part of the asset and part of the liability. Treat them accordingly.

## Common anti-patterns to avoid

- **Asserting on internal calls**: brittle, breaks on refactor, proves nothing about behavior.
- **Mocking the unit under test**: the test tests the mock, not the code.
- **One big test covering the whole feature**: when it fails, you have no idea what broke.
- **`time.sleep()` as a synchronization mechanism**: always flaky, always slow.
- **Tests that are sometimes green, sometimes red**: a bug you have trained the team to ignore.
- **Copy-paste tests**: the bug you copy into the test is the bug you will not catch.
- **No negative tests**: "it works when everything is right" does not prove anything about resilience.
- **Testing what you just implemented, not what the feature requires**: the test validates the code, not the behavior.

## Closing notes

Tests are the specification of the system, written in a form a computer can check. A good test suite is worth more than the code it tests: the code can be rewritten, but the behavioral contract the tests encode is what the users and callers actually depend on.

Slow, flaky, or untrustworthy tests are worse than no tests. They train the team to ignore failure signals — and when a real regression appears, it passes unnoticed through a gate that people stopped watching.
