---
name: sbp-refactor
description: Use when existing code needs to change shape before a feature, or when code drift is making further work expensive — improves structure and readability without changing observable behavior.
metadata:
  domain: cross-cutting
  lifecycle: build
---

# Refactor

This skill walks you through refactoring safely. A refactor is a contract with yourself: observable behavior does not change. Inputs, outputs, side effects, error cases, and performance bounds stay the same; the shape of the code underneath is what moves.

Violating that contract — even accidentally — turns a refactor into a bug delivery vehicle. This walkthrough keeps the contract intact.

## Step 1: Establish why

Refactoring without a clear objective drifts into "just tidying up." That kind of diff is hard to review, hard to justify, and often introduces risk with no upside.

Name the specific goal:

- **Unblock a feature**: existing code shape makes an upcoming feature hard to add cleanly.
- **Reduce coupling**: two things that change for different reasons are currently tangled together.
- **Improve testability**: the code has hidden dependencies or side effects that prevent testing.
- **Reduce duplication**: the same logic appears in three places and they have started to drift.
- **Clarify intent**: future readers (including future you) will misread this code.
- **Remove dead weight**: unreachable code, unused exports, obsolete compatibility shims.

If you cannot state the objective in one sentence, pause. Refactoring without a target is how weekends disappear.

If you catch yourself wanting to change behavior during the refactor, stop. Scope that out as a separate change with its own tests.

## Step 2: Establish the safety net

You cannot refactor safely without tests. Period.

Before touching code:

- **Run the full test suite** and confirm it passes on the current code. The baseline is green.
- **Assess coverage around the target**: are the paths you are about to reshape actually tested? Do the tests exercise the real behavior, or just the types?
- **If coverage is inadequate**: write characterization tests first. These are not tests of desired behavior — they are tests that lock in *current* behavior, whatever that is, so you notice if you change it.
- **Capture external contracts**: public APIs, data formats, error shapes, log lines consumers might depend on, performance budgets. These are the things that must not change.

Characterization tests can feel like busy-work. They are the only thing standing between your refactor and a silent regression. Do not skip.

## Step 3: Plan small, reversible steps

A refactor executed in one huge diff is hard to review and hard to back out of. Plan a sequence of small, safe edits that each keep tests green.

Typical safe edits, roughly in order of risk:

- Rename symbols for clarity.
- Extract a method or function from a long block.
- Inline a method that adds no value.
- Move a method or class to a better location.
- Introduce a parameter object or struct to group related arguments.
- Replace a temporary variable with a direct query.
- Replace magic values with named constants.
- Extract an interface or port to decouple from an implementation.
- Introduce an adapter or facade to isolate a volatile dependency.
- Split a class or module along a real seam.

For each step, ask: if this step went wrong, how hard is it to undo? Small, reversible steps mean you can move fast without fear.

Avoid large rewrites. If the target is "replace this entire subsystem," that is not a refactor — that is a rewrite, with different risks and a different plan.

## Step 4: Execute iteratively

Loop through the planned steps. After each one:

- Run the tests. Must stay green.
- If tests fail, revert immediately and investigate. Do not try to fix forward through a failing refactor.
- Commit atomically with a descriptive message. Small commits make rollback and review easy.
- Check formatting, linting, and type checks still pass.

Do not batch multiple steps into one commit because they "feel related." Related steps that fail together are harder to diagnose than independent steps that either both passed or one failed.

If a step turns out larger than planned, stop and split it. A step that takes more than one commit to get right was not actually one step.

## Step 5: Preserve what must be preserved

Throughout the refactor, verify the contract:

- **Public APIs**: routes, function signatures, response schemas, thrown error types — unchanged.
- **Side effects**: log lines, metric names, event emissions, database writes — unchanged in kind and shape.
- **Performance**: the hot path should not get meaningfully slower. Measure if you are unsure.
- **Concurrency behavior**: if the original handled concurrent access a certain way, the new code must too. Race conditions introduced during refactoring are particularly nasty because no one is looking for them.
- **Error paths**: if the old code threw X on condition Y, the new code must too. Consumers may depend on it.

When in doubt, write the behavior down as a test before you change the code.

## Step 6: Validate at integration

With unit tests green, check the whole system:

- **Full suite**: not just your tests. Other teams' tests may exercise seams you moved.
- **Realistic runs**: exercise the refactored code through the actual paths users and callers take, not just through tests.
- **Performance**: if the refactor touched a hot path, measure before and after. Budget variance is defined by the system's requirements, not by your intuition.
- **Observability**: logs, metrics, traces should still carry the same signal. A refactor that silences a useful log line is a regression in operability.

## Step 7: Document what changed structurally

If the refactor moved module boundaries, introduced new abstractions, or reshaped the architecture:

- Update any internal documentation or architecture notes that describe the old shape.
- Add a short note to the PR description explaining the new structure and why.
- If the project has ADRs (architecture decision records), consider whether this warrants one.

Skip: commenting the code to explain the shape. The code should read as its own explanation. If it does not, the refactor is not done.

## Common anti-patterns to avoid

- **"Refactor" that changes behavior**: if you changed what the code does, it is not a refactor — it is a feature or a bug fix in disguise. Split it.
- **No tests, refactoring anyway**: you are not refactoring, you are rewriting and hoping. Add characterization tests first.
- **One giant diff**: impossible to review, impossible to roll back. Small commits, each green.
- **Pursuing perfect architecture**: refactors have diminishing returns. Stop when the original objective is met, not when the code is aesthetically pleasing.
- **Refactoring under deadline pressure**: the temptation to skip the safety net is highest when you should least skip it. If you have no time for tests, you have no time for a refactor.
- **Letting the refactor grow**: "while I'm in here..." — note it down, move on. Separate change, separate PR.

## Closing notes

A good refactor is invisible from the outside and obvious on the inside. Behavior unchanged, code clearer.

The best refactor is one you can ship in small pieces over time, with the system green at every step. That way, if you are interrupted — and you will be — the code is never in a half-transformed state.
