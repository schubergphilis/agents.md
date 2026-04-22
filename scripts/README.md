# scripts/

Maintenance scripts.

## `sync-terraform-skills.sh`

One-way sync from `mcaf-review` (source of truth while skills are under active development) into this repo's `skills/`. Run whenever you've edited the skills or `GUIDE.md` in `mcaf-review`.

```bash
# Default source path: ~/git/schuberg/mcaf-review
scripts/sync-terraform-skills.sh

# Override source path
MCAF_REVIEW_DIR=/path/to/mcaf-review scripts/sync-terraform-skills.sh

# Dry-run — show drift without writing
scripts/sync-terraform-skills.sh --check
```

The script:

1. Copies `.claude/skills/{terraform,mcaf-module,review-mcaf}/` from `mcaf-review`.
2. Copies `mcaf-review/GUIDE.md` to `skills/mcaf-module/GUIDE.md` (bundled with the skill so its reference resolves once installed).
3. Rewrites `GUIDE.md` path references in `review-mcaf/SKILL.md` and `mcaf-module/SKILL.md` so cross-skill links resolve when the skills are symlinked as siblings under `~/.claude/skills/`.
4. Leaves the pack at `packs/terraform/` untouched — the pack is authored here, not synced from anywhere.

After running, always validate:

```bash
python3 cli/sbp-skills validate packs/terraform skills/terraform skills/mcaf-module skills/review-mcaf
```

### Source-of-truth rule

- Generic Terraform + MCAF content → edit in `mcaf-review/.claude/skills/…` and `mcaf-review/GUIDE.md`, then sync.
- The `terraform` **pack** (AGENTS.md, CLAUDE.md, manifest) → edit in this repo directly; it's not in `mcaf-review`.

If the mcaf-review repo eventually goes away or merges in, drop this script and edit the skills directly here.
