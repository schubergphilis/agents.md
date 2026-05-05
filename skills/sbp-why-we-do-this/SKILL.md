---
name: sbp-why-we-do-this
description: Explain the reasoning behind SBP engineering conventions — connect rules to real failure modes, show the trade-offs, and make the case with concrete examples. Use when an engineer asks why a convention exists or when onboarding new team members.
metadata:
  domain: cross-cutting
  lifecycle: cross-cutting
---

# Why We Do This

When an engineer asks "why do we do it this way?", give them the real answer — not "because the rules say so" but "because here is what goes wrong without it."

Every convention at SBP exists because something broke, something almost broke, or the cost of it breaking in a mission-critical environment is unacceptable. Explain the reasoning honestly, including the trade-offs.

## How to explain a convention

Follow this structure:

1. **What the convention is**: state it clearly and concisely.
2. **What it prevents**: describe the specific failure mode, incident, or risk it addresses.
3. **What the trade-off is**: acknowledge the cost — slower workflow, more boilerplate, extra steps. Be honest.
4. **Why it is worth it**: explain why the prevention outweighs the cost in a mission-critical context.
5. **What breaks without it**: give a concrete, specific example. Not hypothetical — what has actually happened or what realistically would happen.

## Common conventions and their reasoning

### Pin dependencies to exact versions or SHA hashes

**What it prevents**: A dependency update introducing breaking changes or malicious code into a production system without explicit review.

**What breaks without it**: A package maintainer pushes a compromised version. Every build that runs `pip install package>=1.0` picks it up automatically. Your next deploy ships malicious code to production without any engineer reviewing or approving the change. This is not theoretical — the `event-stream`, `ua-parser-js`, and `colors.js` incidents all exploited version ranges.

**Trade-off**: You have to manually update dependencies and test them. Dependabot or Renovate can automate the PR creation, but a human still reviews it.

**Why it is worth it**: In mission-critical systems, predictability beats convenience. You want to know exactly what is running in production, and you want every change to be deliberate.

### Use uv, not pip

**What it prevents**: Slow, non-reproducible dependency resolution that produces different results on different machines.

**What breaks without it**: pip resolves dependencies at install time with no lockfile by default. Two engineers run `pip install -r requirements.txt` on the same day and get different transitive dependency versions. One works, one does not. CI produces a different result than local. You spend hours debugging "works on my machine" problems that are actually dependency resolution differences.

**Trade-off**: Engineers need to learn a new tool. The uv CLI is deliberately similar to pip, so the learning curve is minimal.

**Why it is worth it**: uv is deterministic, fast (10-100x faster than pip), and produces lockfiles that guarantee reproducibility. In mission-critical systems, "it worked on my machine" is not an acceptable deployment strategy.

### Use ruff, not black + isort + flake8

**What it prevents**: Inconsistent formatting, linting gaps, slow CI feedback, and configuration drift between multiple tools.

**What breaks without it**: With three separate tools, each has its own configuration file, its own version, and its own opinion. They occasionally conflict (black reformats something that isort then reformats back). CI takes 30+ seconds to run all three. Engineers disable one tool because it is slow and miss real issues.

**Trade-off**: Ruff is newer and has fewer edge-case rules than the combined ecosystem. Some very niche flake8 plugins do not have ruff equivalents yet.

**Why it is worth it**: One tool, one config file, sub-second execution, consistent results. Engineers actually run it because it is fast. The best linter is the one that runs, not the one with the most rules.

### Require type hints in Python

**What it prevents**: Runtime type errors in production, unclear interfaces, and costly debugging sessions.

**What breaks without it**: A function accepts a dict but someone passes a list. In a typed codebase, the IDE and mypy catch this before the code leaves the engineer's machine. In an untyped codebase, it passes review, passes tests that happen to use the right type, and crashes at 2 AM when a rare code path runs for the first time.

**Trade-off**: Writing type hints takes time, especially for complex types. Some dynamic Python patterns are hard to type correctly.

**Why it is worth it**: Types are documentation that the machine verifies. In mission-critical systems, "I think this function takes a string" is not good enough. Types make code reviewable, refactorable, and debuggable by engineers who did not write it.

### Require rollback plans for every deployment

**What it prevents**: Deploying changes that cannot be undone when they cause problems.

**What breaks without it**: An engineer deploys a database migration that drops a column. The new code has a bug. You need to roll back the code, but the old code depends on the column that no longer exists. Now you have a broken production system with no clear path to recovery. A 5-minute rollback becomes a 4-hour emergency.

**Trade-off**: Writing and testing rollback plans takes time. Some changes require creative rollback strategies (forward-fix instead of revert, compatibility windows for schema changes).

**Why it is worth it**: The rollback plan is your insurance policy. You hope you never need it, but when you do, it is the difference between a 5-minute recovery and a multi-hour incident. In mission-critical systems, "we will figure it out if something goes wrong" is not a plan.

### Analyze blast radius before changes

**What it prevents**: Making changes that affect more systems, customers, or data than intended.

**What breaks without it**: An engineer updates a shared library and deploys it. They tested it with their service. But the library is used by 12 other services, three of which use an API that changed subtly. Those three services start returning errors. The engineer who made the change does not even know those services exist.

**Trade-off**: Blast radius analysis takes time and requires understanding the system topology. For large changes, it can take as long as the change itself.

**Why it is worth it**: Blast radius analysis is how you find out what you do not know before production finds out for you. Most major incidents start with "we did not realize this would affect X."

## For the skeptic

If an engineer thinks a convention is unnecessary overhead:

1. Do not dismiss their concern. They might be right that the implementation is too heavy-handed, even if the principle is sound.
2. Give the concrete example. Not "this could happen" but "this happened at X" or "this happens in Y% of cases."
3. Acknowledge the cost honestly. "Yes, this adds 10 minutes to every deploy. The alternative is that 1 in 50 deploys turns into a 2-hour incident."
4. Distinguish the principle from the implementation. The principle (verify before deploy) might be non-negotiable. The implementation (this specific checklist) can be improved.
5. Invite improvement. "If you can see a way to get the same safety with less overhead, propose it. The goal is safety, not bureaucracy."

## For the new joiner

If an engineer is new to SBP and encountering these conventions for the first time:

1. Start with context. "SBP runs mission-critical systems for customers who depend on 100% availability. Our conventions reflect that responsibility."
2. Explain the stakes. "When our systems go down, real business operations stop. This is not a social media app where users can retry in 5 minutes."
3. Connect to their experience. "You have probably worked in environments with lighter process. That works when the cost of failure is low. Here, the cost of failure is high, so we invest more in prevention."
4. Be welcoming. "These conventions might feel heavy at first. After a few weeks, they become second nature, and you will start to appreciate having the safety net."
5. Point to the wins. "Last quarter, our rollback plan saved us three times. Each time, a 5-minute rollback prevented what would have been a multi-hour incident."

## When a convention is genuinely annoying

Some conventions are annoying and still necessary. Be honest about it.

"Yes, writing a rollback plan for a one-line config change feels like overkill. And 99% of the time, it is. But the 1% where the config change breaks authentication and you need to revert in 30 seconds — that is the scenario the rollback plan exists for. The annoyance is the cost; the insurance is the benefit."

Honesty about trade-offs builds more trust than pretending everything is perfectly efficient.
