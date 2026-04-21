# Why sbp-skills exists

## The problem

AI coding agents are powerful. They write code, generate infrastructure, review pull requests, and build entire features. But they have no idea what mission-critical means.

A generic AI agent will happily write a deployment script with no rollback path. It'll create a Terraform module that can't be safely reverted. It'll add a dependency without considering supply-chain risk. It'll build the happy path and forget what happens at 3 AM when the on-call gets paged.

At Schuberg Philis, that's not acceptable.

We deliver 100% customer satisfaction and 100% quality on systems that run healthcare, finance, energy, and government. Our engineers don't just build software — they plan, build, and run it. The same person who writes the code is the one who gets paged when it breaks. That creates a way of thinking that no AI model has been trained on.

## The industry is catching up

At the AI Engineer Code Summit, Anthropic's Barry Zhang and Mahesh Murag told the industry to stop building agents and start building Skills. Their computing stack analogy: models are processors, agent runtimes are operating systems, and skills are applications. The application layer is where domain expertise lives — and it's portable across tools.

This isn't just an Anthropic idea. Claude Code, GitHub Copilot, and OpenCode all read markdown skills from the filesystem. The [agentskills.io](https://agentskills.io) spec is becoming the common format. Write a skill once, use it in every tool.

Their three categories of skills map directly to what we've built:
- **Foundational skills** — general capabilities (our baseline)
- **Partner skills** — technology-specific (our domain packs)
- **Enterprise skills** — your organization's knowledge (our mission-critical thinking model)

The key insight: institutional knowledge accumulates. When one engineer writes a skill or improves a pack, every agent in the organization gets better — regardless of which AI tool that engineer uses. Day 30 is measurably better than day 1.

We didn't wait for the industry to tell us this. sbp-skills has been encoding SBP's mission-critical expertise into portable, composable skills from the start. But it's good to know we're on the right track.

## What we believe

**The senior engineer's judgment should be portable.** When a senior SBP engineer reviews code, they ask questions that generic tools don't: "What's the blast radius? Who gets paged? Can we roll this back in 15 minutes? What happens when this dependency is unavailable?" That judgment shouldn't live only in people's heads. It should be available to every engineer, in every project, in every AI interaction.

**AI should teach, not just execute.** When an agent asks "what's your rollback path?", the engineer learns to think about rollback paths. When it confirms "you've handled the database failure mode — solid", the engineer learns what good looks like. Over months of daily interaction, engineers sharpen their instincts — not because they read a wiki, but because they practiced it.

**Compliance should be invisible.** ISO 27001, ISO 9001 — these aren't checkbox exercises. They describe how good engineering works: traceability, change management, risk assessment, evidence. If the agent naturally documents decisions, states impact before changes, and plans for failure modes, compliance outcomes follow. No one needs to "do compliance."

**Freedom beats control.** We don't want to build straitjackets. Teams need autonomy to move fast and make decisions. But autonomy without shared judgment leads to inconsistency — one team pins dependencies, another doesn't; one team thinks about rollback, another ships and hopes. sbp-skills provides the baseline judgment so teams can be autonomous *and* reliable.

**Easy beats comprehensive.** A system that takes 30 minutes to set up won't spread. A system that takes 30 seconds will. We deliberately keep the tool minimal and the content tight. The baseline is ~300 words. Packs auto-detect. Skills are opt-in. Engineers shouldn't need to configure their way to safety.

## Plan / Build / Run

SBP engineers plan, build, and run with the same team. sbp-skills supports the full lifecycle.

### Plan

The agent challenges before you've written a line. "What's the blast radius? Who gets paged? What's the rollback?" It pushes you to think about operability from the start — not after the code is written.

| | |
|---|---|
| `/challenge` | Stress-test your approach |
| `architecture-review` | Single points of failure, observability, operational readiness |
| `threat-model` | Attack surfaces, mitigations, risk matrix |
| `agent-architecture-review` | Multi-agent system design against the three-layer model |
| `design-first` | Understand the problem, explore alternatives, get alignment before building |

### Build

The agent auto-reviews its own output — silent failures, missing error handling, implicit assumptions. It follows your stack's conventions automatically. You focus on the problem, not on remembering the rules.

| | |
|---|---|
| `/review` | Mission-critical review of current work |
| `/explain` | Understand unfamiliar code or infrastructure |
| `secure-code-review` | Security-focused analysis: auth, injection, secrets, dependencies |
| `dependency-audit` | Supply-chain risk, bloat, unused packages |
| `explain-codebase` | Deep dive into architecture, patterns, design decisions |
| `why-we-do-this` | The reasoning behind SBP conventions |
| `verify-before-done` | Prove it works before claiming it — evidence, not assertions |

### Run

The same team that builds it runs it. The agent thinks about what happens after deployment — monitoring, incidents, the 3 AM scenario.

| | |
|---|---|
| `/pre-deploy` | Quick GO/NO-GO |
| `/what-if-this-fails` | Failure cascades, recovery, the 3 AM test |
| `/risk-check` | Full blast radius and rollback analysis |
| `deploy-checklist` | Complete pre-deployment verification |
| `safe-change` | Guided walkthrough for high-risk production changes |
| `incident-review` | Blameless post-incident analysis |
| `runbook-author` | Generate operational runbooks from the codebase |
| `observability-check` | Verify monitoring, alerting, and logging coverage |

### Learn

When you're new to a team, a codebase, or SBP itself — the agent is your onboarding partner. It teaches SBP thinking through every interaction. The questions it asks ("what's the blast radius?", "who gets paged?") are the questions senior engineers ask. After a month, you ask them instinctively — not because you read a wiki, but because you practiced it.

| | |
|---|---|
| `/explain` | Quick orientation on unfamiliar code or infra |
| `explain-codebase` | Deep dive — data flow, patterns, design decisions |
| `why-we-do-this` | The reasoning behind SBP conventions |

### Contribute

Your experience becomes a shared asset. Write a pack or skill, and every engineer on the team benefits.

| | |
|---|---|
| `/new-pack` | Scaffold a domain convention pack |
| `/new-skill` | Scaffold a new skill |

## What it's not

**It's not a linter.** Linters check syntax. sbp-skills teaches thinking.

**It's not a compliance tool.** It doesn't generate audit reports or check boxes. It works in a way that naturally produces compliant outcomes.

**It's not mandatory.** Everything is opt-in. The baseline is guidance, not a gate. Packs can be removed. Skills can be ignored. Teams that don't want it can skip it entirely.

**It's not AI-specific.** The thinking model in the baseline is how senior SBP engineers work, period. The AI agent just makes it scalable.

## The name

"Cognitive autonomy" — the ability to think independently and make good decisions. That's what we're building for our engineering teams. Not dependence on rules, not blind compliance, but the judgment to operate mission-critical systems with confidence.

sbp-skills is the vehicle. The content is the product. The outcome is engineers who build systems that don't break, and know what to do when they do.
