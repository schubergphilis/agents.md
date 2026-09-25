# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Validate

```bash
# All skills must be discovered (count must match `ls skills | wc -l`)
DISABLE_TELEMETRY=1 NO_COLOR=1 npx -y skills add ./ --list

# Pack fragments must stay under 300 words
wc -w packs/*/AGENTS.md
```

## Architecture

Content only — no code. `baseline/`, `packs/`, `skills/`. Skills install via `npx skills` (skills.sh); plugin groups in `.claude-plugin/marketplace.json`. Always set `DISABLE_TELEMETRY=1` when running `npx skills`.

## Git workflow

- Always create a feature branch before making commits — never commit directly to `main`
- Branch naming: `feat/<topic>`, `fix/<topic>`, `chore/<topic>`
- Open a PR after committing; do not push to main directly

## Key conventions

- No custom scripts or code — use `npx skills` for install/update
- Pack AGENTS.md fragments must be under 300 words
- Pack AGENTS.md files are plain markdown, appended to a project's AGENTS.md by hand
- Imperative voice in all agent-facing content
- SKILL.md files follow the agentskills.io spec (YAML frontmatter + markdown body)
