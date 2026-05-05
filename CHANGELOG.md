# Changelog

## [1.0.0] — 2026-05-05

### Breaking changes

All skills have been renamed with an `sbp-` prefix.

This makes SBP skills immediately distinguishable from community skills, personal skills, or skills from other sources when they coexist in `~/.claude/skills/`. Name collisions (e.g., `deploy-checklist` from two different repos) become impossible.

**Migration:** Update any direct references to the old names.

| Old name | New name |
|----------|----------|
| `agent-architecture-review` | `sbp-agent-architecture-review` |
| `architecture-review` | `sbp-architecture-review` |
| `debug-investigation` | `sbp-debug-investigation` |
| `dependency-audit` | `sbp-dependency-audit` |
| `deploy-checklist` | `sbp-deploy-checklist` |
| `explain-codebase` | `sbp-explain-codebase` |
| `feature-development` | `sbp-feature-development` |
| `incident-review` | `sbp-incident-review` |
| `observability-check` | `sbp-observability-check` |
| `refactor` | `sbp-refactor` |
| `runbook-author` | `sbp-runbook-author` |
| `safe-change` | `sbp-safe-change` |
| `secure-code-review` | `sbp-secure-code-review` |
| `test-authoring` | `sbp-test-authoring` |
| `test-planning` | `sbp-test-planning` |
| `threat-model` | `sbp-threat-model` |
| `why-we-do-this` | `sbp-why-we-do-this` |

`sbp-brandbook` was already correctly named and is unchanged.

If you installed skills manually, remove the old directories and copy the renamed ones:

```bash
# Remove old
rm -rf ~/.claude/skills/threat-model ~/.claude/skills/deploy-checklist  # etc.

# Re-copy from the updated repo
cp -r skills/sbp-threat-model ~/.claude/skills/
cp -r skills/sbp-deploy-checklist ~/.claude/skills/

# Or just re-run init to sync everything
sbp-skills init
```

### Other changes

- Fixed install script and README one-liner to point to the correct repo (`schubergphilis/agents.md`)
- Skill authoring convention updated: new skills must use the `sbp-` prefix

---

## [0.1.0] — initial release

- CLI (`sbp-skills`) with `init`, `update`, `list`, `add`, `remove`, `enable`, `disable`, `doctor`, `validate`, `dev`
- Baseline mission-critical thinking model (`baseline/AGENTS.md`)
- Slash commands: `/review`, `/challenge`, `/risk-check`, `/explain`, `/pre-deploy`, `/what-if-this-fails`, `/new-pack`, `/new-skill`
- Domain packs: `python`, `supply-chain`
- 18 skills across planning, building, running, and brand categories
