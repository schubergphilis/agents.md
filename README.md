# sbp-skills

> "Agents today are brilliant, but they lack expertise."
> — Barry Zhang & Mahesh Murag, Anthropic — [AI Engineer Code Summit](https://www.youtube.com/watch?v=CEvIs9y1uog)

The industry is converging on a single insight: **stop building specialized agents — build Skills instead.** Intelligence without domain expertise is entertainment. The difference between a mediocre agent and an extraordinary one isn't the model — it's the knowledge you feed it.

Skills are folders with markdown files that encode your workflows, your conventions, your hard-won expertise. One generic agent + the right skills beats dozens of specialized agents. This works across all AI coding tools — Claude Code, GitHub Copilot, OpenCode, and any agent that reads markdown from the filesystem.

**sbp-skills is our skills library.** It turns every AI coding agent into a coworker that thinks like a senior SBP engineer — challenging assumptions, reviewing for failure modes, and teaching mission-critical practices through daily interaction. Same skills, every tool, one standard.

Works with **Claude Code**, **GitHub Copilot**, and **OpenCode**. Compatible with [skills.sh](https://skills.sh) and the [agentskills.io](https://agentskills.io) standard.

---

## Getting started

### Option A: `npx skills` (recommended)

Install skills with the [skills.sh](https://skills.sh) CLI. Nothing to clone, no custom installer. Set `DISABLE_TELEMETRY=1` so installs are not reported to skills.sh.

```bash
# Pick skills interactively
DISABLE_TELEMETRY=1 npx skills add schubergphilis/agents.md

# Or install specific skills globally for Claude Code
DISABLE_TELEMETRY=1 npx skills add schubergphilis/agents.md -g -a claude-code \
  --skill sbp-architecture-review sbp-deploy-checklist

# Keep them current
DISABLE_TELEMETRY=1 npx skills update
```

Then add the baseline and the packs for your stack by hand (Option B, steps 1 and 2). `npx skills` handles skills only.

### Option B: Manual setup (no tool needed)

Everything is just markdown files. Copy what you need:

**1. Get the baseline** (every project should have this):

```bash
# Copy the mission-critical thinking model into your project
cp baseline/AGENTS.md your-project/AGENTS.md

# For Claude Code — copy tool-specific hints
cp baseline/CLAUDE.md your-project/CLAUDE.md

# Copy the default commands
mkdir -p your-project/.claude/commands
cp baseline/commands/*.md your-project/.claude/commands/
```

**2. Add domain packs** (append the ones that match your stack):

```bash
# Python project? Append Python conventions
cat packs/python/AGENTS.md >> your-project/AGENTS.md

# GitHub Actions? Append supply-chain hardening
cat packs/supply-chain/AGENTS.md >> your-project/AGENTS.md
```

**3. Add skills** (or use `npx skills add`, see Option A):

```bash
# Copy any skill you want
cp -r skills/sbp-threat-model ~/.claude/skills/
cp -r skills/sbp-deploy-checklist ~/.claude/skills/
```

That's it. No tool required. The product is the content.

### Option C: Claude Code plugin marketplace

If you live in Claude Code, you can install skills as plugins — no CLI, no clone, no filesystem hop:

```
/plugin marketplace add schubergphilis/agents.md
/plugin install operations-skills@sbp-skills
/plugin install security-skills@sbp-skills
/plugin install engineering-skills@sbp-skills
/plugin install brand-skills@sbp-skills
```

Plugin groups available:

| Plugin | Skills |
|--------|--------|
| **operations-skills** | sbp-architecture-review, sbp-deploy-checklist, sbp-incident-review, sbp-observability-check, sbp-runbook-author, sbp-safe-change |
| **security-skills** | sbp-threat-model, sbp-secure-code-review, sbp-dependency-audit |
| **engineering-skills** | sbp-explain-codebase, sbp-agent-architecture-review, sbp-why-we-do-this |
| **brand-skills** | sbp-brandbook (SBP visual identity — colors, typography, logo, assets) |

This is the preferred path for non-engineers and business users on Claude Code / Claude.ai who just want the skills without touching a terminal.

### Using skills from other sources

sbp-skills follows the [agentskills.io](https://agentskills.io) standard. You can use skills from [skills.sh](https://skills.sh), from colleagues, or your own — just put them in `~/.claude/skills/` alongside these. Everything coexists.

```bash
# skills.sh example
DISABLE_TELEMETRY=1 npx skills add vercel-labs/agent-skills

# Your own skill — just a folder with a SKILL.md
mkdir -p ~/.claude/skills/my-custom-skill
echo "---\nname: my-custom-skill\n..." > ~/.claude/skills/my-custom-skill/SKILL.md
```

---

## What's inside

### Baseline — the mission-critical thinking model

The baseline changes how your AI agent *thinks*. It's not a checklist — it's the judgment of a senior SBP engineer encoded into every interaction.

After setup, your agent will:
- **Challenge before building** — "What's the blast radius? Who gets paged? What's the rollback?"
- **Auto-review its own work** — checks for silent failures and missing error handling before presenting code
- **Scale rigor to risk** — production gets scrutiny, a local script gets clean code without interrogation
- **Confirm good work** — "You've covered the database failure mode — solid"
- **Explain reasoning** — teaches, doesn't just instruct

Lives in: `baseline/AGENTS.md` (~300 words, always in context)

### Commands — quick access to mission-critical workflows

Slash commands you can use in any conversation:

| Command | What it does |
|---------|-------------|
| `/review` | Review current work against mission-critical standards — failure modes, rollback, observability, blast radius |
| `/challenge` | Challenge your approach like a senior engineer — worst case, assumptions, 3 AM scenario |
| `/risk-check` | Full blast radius analysis with LOW/MEDIUM/HIGH/CRITICAL rating and rollback assessment |
| `/explain` | Explain unfamiliar code, infrastructure, or patterns — teaches, doesn't just describe |
| `/pre-deploy` | Quick GO/NO-GO deployment check — lighter than the full sbp-deploy-checklist skill |
| `/what-if-this-fails` | Trace failure cascades — direct failure, downstream impact, recovery, the 3 AM test |
| `/new-pack` | Scaffold a new domain pack for the team |
| `/new-skill` | Scaffold a new skill |

### Domain packs — conventions for your stack

Append the packs that match your project's files to its `AGENTS.md`. They encode *how SBP builds mission-critical systems with this technology* — not generic best practices.

| Pack | Use when the repo has | What it covers |
|------|-----------------|----------------|
| **python** | `pyproject.toml`, `setup.py`, `requirements.txt` | uv, ruff, pyright, pytest — auditable, testable Python for production |
| **terraform** | `*.tf`, `terraform.tf`, `versions.tf` | Module layout, version ranges, `optional(…)`, curated outputs, native `terraform test` |
| **supply-chain** | `.github/workflows/*.yml` | Pin GitHub Actions to SHA — prevent compromised dependencies in CI/CD |

More packs coming: kubernetes, docker, github-actions.

### Skills — deeper workflows for when you need them

Skills load on demand — they're not in context unless you invoke them. All SBP skills are prefixed with `sbp-` so they're easy to distinguish from community or personal skills in your `~/.claude/skills/` directory.

**Planning:**

| Skill | What it does |
|-------|-------------|
| **sbp-architecture-review** (default) | Review systems for single points of failure, blast radius, rollback paths, observability gaps, operational readiness |
| **sbp-threat-model** | Structured threat modeling — assets, threat actors, attack surfaces, mitigations, prioritized actions |
| **sbp-agent-architecture-review** | Review multi-agent system designs against a three-layer reference model (guardian/orchestration/worker) |
| **sbp-test-planning** | Design comprehensive test coverage before implementation — behaviors, boundary cases, failure modes, right test type for each |

**Building:**

| Skill | What it does |
|-------|-------------|
| **sbp-feature-development** | Build a new feature using test-driven development — clarify requirements, plan test coverage, drive through red/green/refactor, integrate, and verify |
| **sbp-debug-investigation** | Systematically investigate, reproduce, and fix software bugs — frame symptoms, reliably reproduce, isolate the root cause, write a regression test, then fix |
| **sbp-refactor** | Improve code structure without changing observable behavior — establish a safety net, plan small reversible steps, execute iteratively, validate no regressions |
| **sbp-test-authoring** | Write tests that prove functionality works and catch regressions — structure each test clearly, exercise real behavior, keep the suite fast and reliable |
| **sbp-secure-code-review** | Security-focused review — auth, injection, secrets, dependencies, OWASP Top 10 |
| **sbp-dependency-audit** | Analyze dependencies for bloat, supply-chain risk, and unused packages |
| **sbp-explain-codebase** | Deep explanation of unfamiliar code — traces data flow, names patterns, explains design decisions |
| **sbp-why-we-do-this** | Explain the reasoning behind SBP conventions — connects rules to real failure modes |

**Running:**

| Skill | What it does |
|-------|-------------|
| **sbp-deploy-checklist** (default) | Full pre-deployment verification — rollback readiness, monitoring, communication, GO/NO-GO decision |
| **sbp-safe-change** | Guided walkthrough for high-risk production changes — step-by-step with verification and rollback triggers |
| **sbp-incident-review** | Blameless post-incident analysis — timeline, root cause (5 whys), contributing factors, concrete action items |
| **sbp-runbook-author** | Generate operational runbooks from code and infrastructure — optimized for the 3 AM scenario |
| **sbp-observability-check** | Verify monitoring, alerting, and logging coverage across the four pillars |

**Terraform / MCAF:**

| Skill | What it does |
|-------|-------------|
| **terraform** | Generic Terraform/OpenTofu authoring — module structure, variable + output design, block ordering, version pinning, native `terraform test`, CI/CD, security scanning, and state hygiene |
| **mcaf-module** | Schuberg Philis MCAF-specific deltas (filenames, provider floors, `mcaf-github-workflows` reuse, release flow). Bundles `GUIDE.md`, the authoritative source |
| **review-mcaf** | Qualitative MCAF module review that produces a good/bad/verdict markdown report; for many modules, dispatches parallel subagents and stitches one file |

**Brand:**

| Skill | What it does |
|-------|-------------|
| **sbp-brandbook** | Apply the SBP visual brand identity — colors, typography, logo, stylization, grids. Auto-triggers on any UI, HTML, slide, or design asset for Schuberg Philis. Bundles 22 brand SVGs (logos, slashes, squares, corners, buttons). |

Enable a skill:

```bash
DISABLE_TELEMETRY=1 npx skills add schubergphilis/agents.md --skill sbp-threat-model

# Or manually — just copy the folder
cp -r skills/sbp-threat-model ~/.claude/skills/
```

---

## Terraform & MCAF

Three-layer coverage for anything Terraform at Schuberg Philis — a daily-context pack plus three opt-in skills that stack on top of each other. You reach for whichever layer matches what you're doing.

### How the layers stack

```
┌───────────────────────────────────────────────────────────────┐
│  packs/terraform/    always-on context (AGENTS.md, CLAUDE.md) │
│                      → append when the repo has *.tf files   │
└───────────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────────┐
│  skills/terraform/     generic Terraform / OpenTofu baseline  │
│          ↑ layered on top                                     │
│  skills/mcaf-module/   MCAF-specific deltas (+ GUIDE.md)      │
│          ↑ layered on top                                     │
│  skills/review-mcaf/   qualitative good/bad/verdict review    │
└───────────────────────────────────────────────────────────────┘
```

- The **pack** lives in `AGENTS.md` / `CLAUDE.md`, so baseline rules (file layout, version ranges, curated outputs) are always in context when editing a Terraform repo.
- The **skills** load on demand when the agent decides they apply, or when you explicitly invoke them. They contain the long-form reference material the pack points at.

### What each piece covers

| Piece | Type | Triggers on | What you get |
|---|---|---|---|
| **`packs/terraform`** | pack | `*.tf`, `terraform.tf`, `versions.tf` | Tight 276-word AGENTS.md fragment — layout, pinning, variable/output rules, tag pattern, acceptance criteria |
| **`skills/terraform`** | skill | Any Terraform/OpenTofu authoring or review | Module structure, block ordering, `optional(…)`, testing decision matrix, CI/CD shape, security scanning, state hygiene. Includes `references/`: `module-patterns.md`, `code-patterns.md`, `testing.md`, `ci-cd.md`, `security-compliance.md`, `quick-reference.md` |
| **`skills/mcaf-module`** | skill | `terraform-<provider>-mcaf-<name>` repos | MCAF deltas: `terraform.tf` not `versions.tf`, provider floors (AWS ≥6, Azurerm ≥4, …), `mcaf-github-workflows` reuse, native `terraform test` with `mock_provider`, conventional-commit labels, release-drafter flow, corpus-specific anti-patterns. Bundles **`GUIDE.md`** — the authoritative way-of-working distilled from 91 MCAF modules |
| **`skills/review-mcaf`** | skill | "review this MCAF module", "is `terraform-<provider>-mcaf-<name>` any good?" | Qualitative review producing a good/bad/verdict markdown report. For multiple modules, dispatches parallel subagents and stitches one file |

### Common workflows

**Editing a Terraform repo (any org):**

```bash
# Inside a repo with *.tf files
cat /path/to/agents.md/packs/terraform/AGENTS.md >> AGENTS.md
DISABLE_TELEMETRY=1 npx skills add schubergphilis/agents.md --skill terraform   # optional: deep reference skill
```

**Authoring or reviewing an MCAF module:**

```bash
DISABLE_TELEMETRY=1 npx skills add schubergphilis/agents.md --skill terraform mcaf-module
# Now the agent knows the generic rules AND the MCAF-specific overlay,
# with GUIDE.md bundled for citation.
```

Then in the agent: "create a new `terraform-aws-mcaf-<thing>` module" or "review this PR against MCAF rules". The `mcaf-module` skill applies automatically when it sees an MCAF repo name or file.

**Running a qualitative MCAF review (single repo or many):**

```bash
DISABLE_TELEMETRY=1 npx skills add schubergphilis/agents.md --skill review-mcaf
```

Then in the agent: `review this MCAF module` (current dir), or `review all MCAF modules in ./repos` (dispatches subagents and stitches a single report).

### Layering rules

- The pack contains the *minimum* set of rules every Terraform repo needs. Don't duplicate its content in the skills.
- `mcaf-module` references `terraform` for anything generic — only the MCAF-specific *delta* lives there.
- `review-mcaf` cites `../mcaf-module/GUIDE.md §N` for every rule it applies. It doesn't re-state rules; it tells the agent how to *apply* them.
- `GUIDE.md` is the single source of truth for MCAF rules. Any new rule lands there first, then the skills reference it.

### Keeping content current

The Terraform + MCAF skills, including `GUIDE.md`, are edited directly in this repo. Update them with `npx skills update`.

---

### Adding your own content

Your project's `AGENTS.md` is the baseline plus the packs you appended. Keep that part in sync with this repo, and add your team's own rules below a `---` separator:

```markdown
...managed baseline and pack content...

---

## Our team additions

- Always check with the DBA before migration changes.
- Production deploys only on Tuesday-Thursday.
- Use #team-platform for deployment notifications.
```

---

## Contributing

### Add a pack

Packs encode how SBP builds mission-critical systems with a specific technology.

```bash
mkdir packs/my-new-pack
# Write packs/my-new-pack/AGENTS.md and README.md
wc -w packs/my-new-pack/AGENTS.md   # must be under 300
# Open a PR
```

**Pack rules:**
- `AGENTS.md` is plain markdown, under 300 words — tight and focused
- Imperative voice: "Run X." not "You should consider running X."
- Every instruction verifiable with a command
- Frame for mission-critical: not "best practice" but "what protects the customer"
- List the files that indicate the pack applies in the pack's README and in the packs table above

### Add a skill

Skills are deeper workflows that engineers opt into.

```bash
DISABLE_TELEMETRY=1 npx skills init skills/sbp-my-new-skill
# Edit skills/sbp-my-new-skill/SKILL.md
DISABLE_TELEMETRY=1 npx skills add ./ --list   # confirm it's discovered
# Add it to a plugin group in .claude-plugin/marketplace.json
# Open a PR
```

**Skill rules:**
- SKILL.md with YAML frontmatter: `name`, `description` (50-1024 chars), `metadata.domain`, `metadata.lifecycle`
- Name matches directory, lowercase with hyphens, prefixed with `sbp-`
- Write as if briefing a smart colleague — specific, actionable, opinionated
- Include output format so the agent knows how to structure its response
- Follows the [agentskills.io](https://agentskills.io) spec — compatible with skills.sh

### Add a command

Commands are slash commands for quick access to workflows.

Just write a markdown file and place it in `baseline/commands/` (for everyone) or a pack's `commands/` directory (for a specific stack). No special format needed — the file content is the prompt.

---

## Requirements

- Node.js (for `npx skills`; manual setup needs nothing)
- An AI coding tool: Claude Code, GitHub Copilot, or OpenCode

## Philosophy

- **A coworker, not a cop.** The agent asks "have you thought about...?" — it doesn't block your work.
- **Teaching through interaction.** When the agent asks "what's your rollback path?", you learn to think about rollback. Over time, you internalize it.
- **Freedom, not straitjackets.** The baseline encodes judgment, not mandates. Add your own rules, remove what doesn't fit, pick skills that match your work.
- **Easy use accelerates adoption.** If it takes 30 seconds, people tell their teammates. If it takes 30 minutes, they don't.

## License

Apache License 2.0 — see [LICENSE](./LICENSE).

**Exception:** `skills/sbp-brandbook/` is proprietary to Schuberg Philis and is **not** covered by the Apache 2.0 license. It has its own terms at [`skills/sbp-brandbook/LICENSE`](./skills/sbp-brandbook/LICENSE). The Schuberg Philis logo, wordmark, color palette, typography, and SVG brand assets may not be redistributed or used outside of work for Schuberg Philis. See [NOTICE](./NOTICE) for full details.
