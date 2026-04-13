# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Test

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run a single test file
python3 -m pytest tests/test_fragment.py -v

# Run a single test
python3 -m pytest tests/test_fragment.py::test_insert_baseline -v
```

## Architecture

Single-file Python CLI at `cli/sbp-skills` (stdlib only, Python 3.11+). Content lives in `baseline/`, `packs/`, `skills/`. Tests import the CLI via importlib in `tests/conftest.py`.

## Key conventions

- CLI must use only Python standard library — no pip dependencies
- Pack AGENTS.md fragments must be under 300 words
- All fragments use HTML comment section markers: `<!-- BEGIN ... -->` / `<!-- END ... -->`
- Imperative voice in all agent-facing content
- SKILL.md files follow the agentskills.io spec (YAML frontmatter + markdown body)
