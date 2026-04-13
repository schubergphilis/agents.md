# sbp-skills

Mission-critical cognitive autonomy for Schuberg Philis engineering teams.

Turn every AI coding agent into a coworker that thinks like a senior SBP engineer — challenging assumptions, reviewing for failure modes, and teaching mission-critical practices through daily interaction.

## Install

```bash
curl -sSL https://raw.githubusercontent.com/schuberg/sbp-skills/main/install.sh | bash
```

## Quick start

```bash
# In your project directory:
sbp-skills init

# See what's available:
sbp-skills list

# Update to latest:
sbp-skills update
```

## How it works

Three layers, right context at the right time:

- **Baseline** — always-on thinking model that teaches mission-critical practices
- **Domain packs** — auto-detected conventions for your project's stack (Python, Terraform, etc.)
- **Skills & commands** — opt-in capabilities for deeper workflows (`/review`, `/challenge`, threat modeling, etc.)

## Requirements

- Python 3.11+
- Git
- An AI coding tool: Claude Code, GitHub Copilot, or OpenCode
