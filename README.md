# sbp-skills

> "Agents today are brilliant, but they lack expertise."
> — Barry Zhang & Mahesh Murag, Anthropic — [AI Engineer Code Summit](https://www.youtube.com/watch?v=CEvIs9y1uog)

The industry is converging on a single insight: **stop building specialized agents — build Skills instead.** Intelligence without domain expertise is entertainment. The difference between a mediocre agent and an extraordinary one isn't the model — it's the knowledge you feed it.

Skills are folders with markdown files that encode your workflows, your conventions, your hard-won expertise. One generic agent + the right skills beats dozens of specialized agents. This works across all AI coding tools — Claude Code, GitHub Copilot, OpenCode, and any agent that reads markdown from the filesystem.

**sbp-skills is our skills library.** It turns every AI coding agent into a coworker that thinks like a senior SBP engineer — challenging assumptions, reviewing for failure modes, and teaching mission-critical practices through daily interaction. Same skills, every tool, one standard.

Works with **Claude Code**, **GitHub Copilot**, and **OpenCode**. Compatible with [skills.sh](https://skills.sh) and the [agentskills.io](https://agentskills.io) standard.

---

## Getting started

### Option A: One-liner install

```bash
curl -sSL https://raw.githubusercontent.com/schuberg/sbp-skills/main/install.sh | bash
```

Then in any project:

```bash
sbp-skills init
```

Done. Your AI agent now thinks mission-critical. It auto-detects your stack and activates the right conventions.

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

**3. Add skills** (copy to your user-level skills directory):

```bash
# Copy any skill you want
cp -r skills/threat-model ~/.claude/skills/
cp -r skills/deploy-checklist ~/.claude/skills/
```

That's it. No tool required. The product is the content, not the CLI.

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
| **operations-skills** | architecture-review, deploy-checklist, incident-review, observability-check, runbook-author, safe-change |
| **security-skills** | threat-model, secure-code-review, dependency-audit |
| **engineering-skills** | explain-codebase, agent-architecture-review, why-we-do-this |
| **brand-skills** | sbp-brandbook (SBP visual identity — colors, typography, logo, assets) |

This is the preferred path for non-engineers and business users on Claude Code / Claude.ai who just want the skills without touching a terminal.

### Using skills from other sources

sbp-skills follows the [agentskills.io](https://agentskills.io) standard. You can use skills from [skills.sh](https://skills.sh), from colleagues, or your own — just put them in `~/.claude/skills/` alongside these. Everything coexists.

```bash
# skills.sh example
npx skills add vercel-labs/agent-skills

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
| `/pre-deploy` | Quick GO/NO-GO deployment check — lighter than the full deploy-checklist skill |
| `/what-if-this-fails` | Trace failure cascades — direct failure, downstream impact, recovery, the 3 AM test |
| `/new-pack` | Scaffold a new domain pack for the team |
| `/new-skill` | Scaffold a new skill |

### Domain packs — conventions for your stack

Packs activate automatically based on your project's files. They encode *how SBP builds mission-critical systems with this technology* — not generic best practices.

| Pack | Auto-detected by | What it covers |
|------|-----------------|----------------|
| **python** | `pyproject.toml`, `setup.py`, `requirements.txt` | uv, ruff, pyright, pytest — auditable, testable Python for production |
| **supply-chain** | `.github/workflows/*.yml` | Pin GitHub Actions to SHA — prevent compromised dependencies in CI/CD |

More packs coming: terraform, kubernetes, docker, github-actions.

### Skills — deeper workflows for when you need them

Skills load on demand — they're not in context unless you invoke them. Pick what helps your work.

**Planning:**

| Skill | What it does |
|-------|-------------|
| **architecture-review** (default) | Review systems for single points of failure, blast radius, rollback paths, observability gaps, operational readiness |
| **threat-model** | Structured threat modeling — assets, threat actors, attack surfaces, mitigations, prioritized actions |
| **agent-architecture-review** | Review multi-agent system designs against a three-layer reference model (guardian/orchestration/worker) |

**Building:**

| Skill | What it does |
|-------|-------------|
| **secure-code-review** | Security-focused review — auth, injection, secrets, dependencies, OWASP Top 10 |
| **dependency-audit** | Analyze dependencies for bloat, supply-chain risk, and unused packages |
| **explain-codebase** | Deep explanation of unfamiliar code — traces data flow, names patterns, explains design decisions |
| **why-we-do-this** | Explain the reasoning behind SBP conventions — connects rules to real failure modes |

**Running:**

| Skill | What it does |
|-------|-------------|
| **deploy-checklist** (default) | Full pre-deployment verification — rollback readiness, monitoring, communication, GO/NO-GO decision |
| **safe-change** | Guided walkthrough for high-risk production changes — step-by-step with verification and rollback triggers |
| **incident-review** | Blameless post-incident analysis — timeline, root cause (5 whys), contributing factors, concrete action items |
| **runbook-author** | Generate operational runbooks from code and infrastructure — optimized for the 3 AM scenario |
| **observability-check** | Verify monitoring, alerting, and logging coverage across the four pillars |

**Brand:**

| Skill | What it does |
|-------|-------------|
| **sbp-brandbook** | Apply the SBP visual brand identity — colors, typography, logo, stylization, grids. Auto-triggers on any UI, HTML, slide, or design asset for Schuberg Philis. Bundles 22 brand SVGs (logos, slashes, squares, corners, buttons). |

Enable a skill:

```bash
# With the CLI
sbp-skills enable threat-model

# Or manually — just copy the folder
cp -r skills/threat-model ~/.claude/skills/
```

---

## CLI reference

If you're using the CLI (optional), these are the commands:

| Command | What it does |
|---------|-------------|
| `sbp-skills init` | Detect tools and stack, render AGENTS.md + commands, link default skills |
| `sbp-skills update` | Pull latest, re-detect, re-render, report what changed |
| `sbp-skills list` | Show available packs, skills, and commands with status |
| `sbp-skills add <pack>` | Add a domain pack explicitly |
| `sbp-skills remove <pack>` | Remove a pack (won't be auto-detected again) |
| `sbp-skills enable <skill>` | Enable a skill for this project (or `--global`) |
| `sbp-skills disable <skill>` | Disable a skill |
| `sbp-skills doctor` | Health check — Python, git, AI tools, repo status |
| `sbp-skills validate <path>` | Validate a pack or skill |
| `sbp-skills dev --pack <name>` | Scaffold a new domain pack |
| `sbp-skills dev --skill <name>` | Scaffold a new skill |

### Adding your own content

After `sbp-skills init`, your project has an `AGENTS.md`. Everything above the `---` separator is managed by sbp-skills (updated when you run `sbp-skills update`). Add your team's own rules below:

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
sbp-skills dev --pack my-new-pack
# Edit packs/my-new-pack/ — fill in manifest.toml, AGENTS.md, README.md
sbp-skills validate packs/my-new-pack
# Open a PR
```

**Pack rules:**
- `AGENTS.md` is plain markdown, under 300 words — tight and focused
- Imperative voice: "Run X." not "You should consider running X."
- Every instruction verifiable with a command
- Frame for mission-critical: not "best practice" but "what protects the customer"
- Add detection patterns to `detection.toml` for auto-activation

### Add a skill

Skills are deeper workflows that engineers opt into.

```bash
sbp-skills dev --skill my-new-skill
# Edit skills/my-new-skill/SKILL.md
sbp-skills validate skills/my-new-skill
# Open a PR
```

**Skill rules:**
- SKILL.md with YAML frontmatter: `name`, `description` (50-1024 chars), `metadata.domain`, `metadata.lifecycle`
- Name matches directory, lowercase with hyphens
- Write as if briefing a smart colleague — specific, actionable, opinionated
- Include output format so the agent knows how to structure its response
- Follows the [agentskills.io](https://agentskills.io) spec — compatible with skills.sh

### Add a command

Commands are slash commands for quick access to workflows.

Just write a markdown file and place it in `baseline/commands/` (for everyone) or a pack's `commands/` directory (for a specific stack). No special format needed — the file content is the prompt.

---

## Requirements

- Python 3.11+ (for the CLI; manual setup needs nothing)
- Git
- An AI coding tool: Claude Code, GitHub Copilot, or OpenCode

## Philosophy

- **A coworker, not a cop.** The agent asks "have you thought about...?" — it doesn't block your work.
- **Teaching through interaction.** When the agent asks "what's your rollback path?", you learn to think about rollback. Over time, you internalize it.
- **Freedom, not straitjackets.** The baseline encodes judgment, not mandates. Add your own rules, remove what doesn't fit, pick skills that match your work.
- **Easy use accelerates adoption.** If it takes 30 seconds, people tell their teammates. If it takes 30 minutes, they don't.

## License

MIT
