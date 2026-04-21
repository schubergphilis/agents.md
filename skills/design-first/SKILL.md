---
name: design-first
description: Understand what you are building before you build it — clarify the problem, explore alternatives, assess blast radius, and get alignment. Use before starting any non-trivial feature, system change, or architecture decision where building the wrong thing is more expensive than thinking first.
metadata:
  domain: cross-cutting
  lifecycle: plan
---

# Design First

The most expensive line of code is the one that solves the wrong problem. This skill is a thinking discipline — not a process, not a template, not a gate. It ensures you understand what you are building, why, and what alternatives exist before you write code.

## When to use this

- Building a feature that touches multiple components.
- Making an architecture decision that is hard to reverse.
- Solving a problem where the solution is not obvious.
- Starting work where the requirements are fuzzy or assumptions are untested.

Skip this for trivial changes, bug fixes with clear root causes, or mechanical refactors. Not everything needs a design phase — but everything that can go expensively wrong does.

## Step 1: State the problem, not the solution

Before proposing how to build something, answer:

- **What problem are we solving?** State it as a user or system need, not as an implementation.
- **Why now?** What is the cost of not solving it? What triggered this work?
- **What is the blast radius?** Which systems, teams, and customers are affected if this goes wrong?
- **What are the non-goals?** What are you explicitly *not* doing? Boundaries prevent scope creep.

If any answer is "I'm not sure," that is the thing to resolve first — not in code, but in conversation.

## Step 2: Explore alternatives

When the path forward is not obvious, propose 2-3 approaches before committing to one.

For each approach:

- **What does it look like?** One paragraph describing the approach.
- **What does it give us?** The main benefit.
- **What does it cost?** Complexity, risk, time, dependencies.
- **What could go wrong?** The failure mode specific to this approach.

You do not need a formal document. A bulleted list in the PR description, a thread in Slack, or a conversation with a colleague is enough. The point is to think before building, not to produce paperwork.

If only one approach is viable, say so and explain why the alternatives do not work. That reasoning is the design.

## Step 3: Identify what you do not know

Every design has assumptions. Name them:

- **Technical assumptions**: "The database can handle this query volume." "This API is idempotent." "The message queue preserves ordering."
- **Domain assumptions**: "Users always provide an email." "This process runs once per day." "The upstream service is available."
- **Organizational assumptions**: "The other team will accept this interface." "We can deploy independently." "This does not need a change request."

For each assumption, decide: can you verify it now (and should you), or is it safe to proceed and validate later?

Assumptions you cannot verify and cannot afford to be wrong about are the highest-risk items. Address those first.

## Step 4: Get alignment

Before writing code, confirm your understanding with the people who will be affected:

- Does the person who requested this agree with the problem statement?
- Does the team agree on the approach (or at least understand the trade-offs)?
- Does the on-call engineer know what changes are coming to their system?

Alignment does not require a meeting. A message saying "I'm planning to do X because Y, with approach Z — does that sound right?" is often enough.

The goal is not consensus. The goal is that no one is surprised by what you build or how you build it.

## What this is not

- **Not a design document template.** Write what is useful, skip what is not.
- **Not a gate.** There is no approval process. This is a thinking habit, not a workflow.
- **Not for everything.** A one-line config change does not need a design phase. Use judgment.

## Closing notes

Senior engineers do this instinctively — they think through the problem, consider alternatives, check assumptions, and align with stakeholders before writing code. This skill makes that instinct explicit so it happens consistently, especially under pressure when the temptation to "just start building" is strongest.

The time spent understanding the problem is never wasted. The time spent building the wrong solution always is.
