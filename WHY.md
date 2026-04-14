# Why sbp-skills exists

## The problem

AI coding agents are powerful. They write code, generate infrastructure, review pull requests, and build entire features. But they have no idea what mission-critical means.

A generic AI agent will happily write a deployment script with no rollback path. It'll create a Terraform module that can't be safely reverted. It'll add a dependency without considering supply-chain risk. It'll build the happy path and forget what happens at 3 AM when the on-call gets paged.

At Schuberg Philis, that's not acceptable.

We deliver 100% customer satisfaction and 100% quality on systems that run healthcare, finance, energy, and government. Our engineers don't just build software — they plan, build, and run it. The same person who writes the code is the one who gets paged when it breaks. That creates a way of thinking that no AI model has been trained on.

## What we believe

**The senior engineer's judgment should be portable.** When a senior SBP engineer reviews code, they ask questions that generic tools don't: "What's the blast radius? Who gets paged? Can we roll this back in 15 minutes? What happens when this dependency is unavailable?" That judgment shouldn't live only in people's heads. It should be available to every engineer, in every project, in every AI interaction.

**AI should teach, not just execute.** When an agent asks "what's your rollback path?", the engineer learns to think about rollback paths. When it confirms "you've handled the database failure mode — solid", the engineer learns what good looks like. Over months of daily interaction, junior engineers start thinking like senior ones — not because they read a wiki, but because they practiced it.

**Compliance should be invisible.** ISO 27001, ISO 9001 — these aren't checkbox exercises. They describe how good engineering works: traceability, change management, risk assessment, evidence. If the agent naturally documents decisions, states impact before changes, and plans for failure modes, compliance outcomes follow. No one needs to "do compliance."

**Freedom beats control.** We don't want to build straitjackets. Teams need autonomy to move fast and make decisions. But autonomy without shared judgment leads to inconsistency — one team pins dependencies, another doesn't; one team thinks about rollback, another ships and hopes. sbp-skills provides the baseline judgment so teams can be autonomous *and* reliable.

**Easy beats comprehensive.** A system that takes 30 minutes to set up won't spread. A system that takes 30 seconds will. We deliberately keep the tool minimal and the content tight. The baseline is ~300 words. Packs auto-detect. Skills are opt-in. Engineers shouldn't need to configure their way to safety.

## Who it's for

Every engineer at SBP — but not all in the same way.

**The new joiner** who doesn't know what "mission-critical" means here yet. The agent teaches SBP thinking through every interaction. After a month, they ask the right questions instinctively — not because they read documentation, but because they practiced it daily.

**The anxious engineer** who's scared of breaking production. The agent catches what they might miss, confirms their good instincts, and gives them structured approaches for risky changes. It builds confidence through competence.

**The curious engineer** who wants to understand why. They pull in skills like `threat-model` and `architecture-review`, explore `/challenge`, and use the agent to deepen their craft. Every convention has an explanation. Every rule has a reason.

**The skeptic** who thinks AI tools are overhyped. They run `init`, the agent gets smarter, and they notice it asking better questions. No onboarding flow, no "AI is your new best friend" messaging. Value proves itself through work.

**The rushed engineer** under deadline pressure. The agent doesn't slow them down — it catches problems invisibly through auto-review and gives quick answers via `/pre-deploy` and `/review`. Fewer bugs in production means fewer 3 AM pages means more time.

**The senior engineer** who already thinks this way. The advanced skills amplify their expertise. And they contribute: writing packs and skills that encode their judgment for the rest of the team. The system turns individual experience into a shared asset.

## What it's not

**It's not a linter.** Linters check syntax. sbp-skills teaches thinking.

**It's not a compliance tool.** It doesn't generate audit reports or check boxes. It works in a way that naturally produces compliant outcomes.

**It's not mandatory.** Everything is opt-in. The baseline is a suggestion, not a gate. Packs can be removed. Skills can be ignored. Teams that don't want it can skip it entirely.

**It's not AI-specific.** The thinking model in the baseline is how senior SBP engineers work, period. The AI agent just makes it scalable.

## The name

"Cognitive autonomy" — the ability to think independently and make good decisions. That's what we're building for our engineering teams. Not dependence on rules, not blind compliance, but the judgment to operate mission-critical systems with confidence.

sbp-skills is the vehicle. The content is the product. The outcome is engineers who build systems that don't break, and know what to do when they do.
