---
name: sbp-debug-investigation
description: Systematically investigate, reproduce, and fix software bugs — frame the symptoms, reliably reproduce, isolate the root cause, write a regression test, then fix. Use when chasing a bug, especially in mission-critical systems where "works on my machine" is not an acceptable resolution.
metadata:
  domain: cross-cutting
  lifecycle: build
---

# Debug Investigation

This skill walks you through debugging methodically. The temptation when chasing a bug is to jump to hypotheses and start patching. Resist. A symptom that looks like X is often caused by Y, and the patch for X will leave Y lurking until it surfaces at 3 AM.

The goal: reproduce reliably, find the root cause, prove you found it, fix once.

## Step 1: Frame the problem

Before touching code, get the facts. Vague bug reports lead to vague fixes.

Collect:

- **Exact symptoms**: what was expected, what happened instead. "It is broken" is not a symptom.
- **Error messages and stack traces**: the complete text, not a paraphrase.
- **Logs**: from the affected system, around the time of the failure.
- **Scope**: which users, which requests, which environments. One user or all? One region or global?
- **Timing**: when did this start? What changed around that time — deploy, config change, traffic shift, external dependency?
- **Business impact**: what is the cost of this bug right now? That shapes how much investigation rigour is warranted.

If the report is fuzzy, go back to the reporter. Investigating a misstated bug burns time on the wrong problem.

## Step 2: Reproduce reliably

You cannot fix what you cannot reproduce. Chasing an intermittent bug without a repro is guessing.

Work toward a minimal, deterministic reproduction:

- Start with the steps the reporter gave. Verify they reproduce the bug.
- Strip away everything not needed to trigger it. What is the smallest input, the shortest path, the cleanest state?
- If it reproduces only in production: capture enough data (inputs, state, timing) that you can replay it in a test environment.
- If it is timing-dependent: introduce controlled delays, run it in a loop, stress the relevant resource.
- If it appears random: look for hidden state — cached values, database rows, feature flags, leader election, time of day.

A stable repro is often 80% of the fix. Once you can trigger it on demand, you can iterate fast.

## Step 3: Isolate the root cause

With a repro in hand, narrow down. Do not guess — bisect.

- **Bisect by version**: if it worked yesterday and not today, `git bisect` to find the commit that broke it.
- **Bisect by input**: which part of the input triggers the bug? Remove parts one at a time until the bug disappears.
- **Bisect by code path**: add logging, breakpoints, or print statements at decision points. Find where the actual behaviour diverges from the expected.
- **Check assumptions**: the first thing to verify is something you are sure of. "Of course the config is loaded" — is it? Actually?

Distinguish the *cause* from the *trigger*. The trigger is what makes it happen today. The cause is the underlying defect. A race condition triggered by traffic growth has "traffic growth" as the trigger and "missing lock" as the cause. Fix the cause.

Beware the first hypothesis that fits. Ask: does this explanation account for every symptom, including the ones that do not fit my first theory? If not, keep digging.

## Step 4: Write the regression test first

Before writing the fix, write a test that reproduces the bug and fails because of it.

- The test must fail on the current code.
- The test must pass after the fix.
- If the test is still green without the fix, the test does not actually exercise the bug.

This test is how you know you fixed it. It is also how future changes avoid reintroducing the bug. A bug without a regression test will come back.

## Step 5: Fix the root cause, minimally

Apply the smallest change that addresses the root cause.

- **Fix the cause, not the symptom**: patching the error message so it no longer appears is not a fix.
- **Avoid defensive coding everywhere**: add input validation at boundaries, not in every function. Scattering `if x is None:` checks obscures the real problem.
- **Keep the diff focused**: this is a bug fix. Not a refactor, not a cleanup. Separate concerns into separate changes.
- **Verify the fix in isolation**: run the new test, confirm it passes. Then run the full suite to catch regressions.

If the fix requires a significant change — new abstraction, architectural shift, migration — stop. The bug fix is one thing; the larger change is another. Ship the minimal fix, then plan the larger change separately.

## Step 6: Validate the full picture

Before marking this resolved:

- **Full test suite**: the new test passes, nothing else broke.
- **Realistic scenarios**: run the feature in a production-like environment with production-like data.
- **Adjacent bugs**: the investigation may have surfaced related issues. Note them — do not necessarily fix them now, but do not lose them either.
- **Observability**: if this bug went unnoticed, could better monitoring have caught it sooner? Add the signal.

## Step 7: Capture what you learned

Write it down. Future you, or future teammates, will face similar bugs.

- **Root cause**: one clear sentence. Not "the code was wrong" — the *specific* wrong thing.
- **How it was missed**: what allowed this to reach production? Test gap? Review miss? Monitoring gap? Unclear assumption?
- **How you would catch it sooner**: what signal, test, or review practice would flag this earlier next time?

For production-impacting bugs, this belongs in a post-incident review. For smaller bugs, a note in the PR description is enough.

## Common anti-patterns to avoid

- **"It works now, I don't know why"**: if you cannot explain why the fix works, you have not finished investigating. You have a different bug waiting.
- **Patching the symptom**: swallowing the exception, raising the timeout, retrying blindly. Each hides the cause for next time.
- **Fixing without a repro**: "I think this might be it" and shipping. You do not know you fixed anything.
- **Fixing without a test**: the bug will return. You just do not know when.
- **Scope creep**: "while I'm fixing this, let me also..." — stop. Fix the bug, open a separate issue for the rest.
- **Skipping the write-up**: the second team member to hit this bug wastes hours you could have saved them in five minutes.

## Closing notes

Good debugging is slow on purpose. Each step narrows the possibilities. Skipping steps feels faster but usually costs more — because a bug that is not fully understood is a bug that is not really fixed.

The reward for rigour is that the bug stays fixed.
