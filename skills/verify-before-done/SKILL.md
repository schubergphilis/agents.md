---
name: verify-before-done
description: Prove your work is done before claiming it — run the command, read the output, show the evidence. Use before any completion claim, commit, or handoff in mission-critical systems where "it should work" is not an acceptable answer.
metadata:
  domain: cross-cutting
  lifecycle: build
---

# Verify Before Done

In mission-critical systems, "it should work" is not evidence. "Here is the test output with 0 failures" is evidence. This skill enforces a simple discipline: before claiming anything is done, prove it.

## The rule

Every completion claim must follow this sequence:

1. **Identify** — what command proves this claim? ("tests pass" → run the test suite. "Bug is fixed" → run the regression test. "Feature works" → exercise it end-to-end.)
2. **Run** — execute the full command. Not a partial run, not a cached result, not "it passed earlier." Fresh, complete, now.
3. **Read** — read the full output. Check exit codes. Count failures. Look for warnings you are about to ignore.
4. **Confirm** — does the output actually support the claim? "95 passed, 2 failed" does not support "tests pass."
5. **Show** — include the evidence with the claim. The output is the proof.

Only then make the claim.

## What counts as a claim

Any statement that work is complete:

- "Tests pass."
- "The bug is fixed."
- "The feature is working."
- "Ready for review."
- "Build succeeds."
- "No regressions."

Each requires its own evidence. "Tests pass" does not prove "no regressions" if you only ran unit tests and the integration suite exists.

## Words that signal you are guessing

If you catch yourself using these, stop and run the command:

- "should" — "tests *should* pass"
- "probably" — "this *probably* works"
- "seems to" — "it *seems to* be fixed"
- "looks good" — no it does not, you have not checked
- "I think" — thinking is not verifying

## Why this matters

A false completion claim is expensive in mission-critical systems:

- A "fixed" bug that is not fixed erodes trust and wastes the next person's time.
- A "passing" test suite that has failures trains the team to ignore red.
- A "ready for review" PR that does not build wastes the reviewer's time and yours.
- A "deployed" service that is not actually healthy pages someone at 3 AM.

The cost of running one more command is seconds. The cost of a false claim is hours, trust, or an incident.

## Common verification gaps

- **Ran unit tests, skipped integration tests.** If both exist, both must pass.
- **Checked the happy path, skipped the error path.** If the fix touches error handling, exercise the error.
- **Verified locally, not in CI.** Local and CI environments diverge. If CI matters, check CI.
- **Read the first line of output, not the last.** Failures often appear at the end. Read the whole thing.
- **Trusted a previous run.** Code changed since then. Run it again.

## Closing notes

This is not bureaucracy. This is the difference between "I believe it works" and "I know it works." In systems where people get paged, that difference matters.

Run the command. Read the output. Show the evidence. Then say it is done.
