#!/usr/bin/env bash
# Sync terraform/mcaf skills from mcaf-review (source of truth while under active
# development) into sbp-skills.
#
# Usage:
#   scripts/sync-terraform-skills.sh                    # uses $MCAF_REVIEW_DIR or default
#   MCAF_REVIEW_DIR=/path/to/mcaf-review scripts/sync-terraform-skills.sh
#   scripts/sync-terraform-skills.sh --check            # dry-run: diff only, no writes
#
# The mapping:
#   mcaf-review/.claude/skills/terraform/      -> sbp-skills/skills/terraform/
#   mcaf-review/.claude/skills/mcaf-module/    -> sbp-skills/skills/mcaf-module/
#   mcaf-review/.claude/skills/review-mcaf/    -> sbp-skills/skills/review-mcaf/
#   mcaf-review/GUIDE.md                       -> sbp-skills/skills/mcaf-module/GUIDE.md
#
# After copying, GUIDE.md references in review-mcaf/SKILL.md are rewritten to
# point at ../mcaf-module/GUIDE.md so cross-skill links resolve once installed.

set -euo pipefail

SRC="${MCAF_REVIEW_DIR:-$HOME/git/schuberg/mcaf-review}"
DST="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -d "$SRC/.claude/skills/terraform" ]; then
  echo "error: source skills not found at $SRC/.claude/skills/terraform" >&2
  echo "hint:  set MCAF_REVIEW_DIR to the mcaf-review checkout path" >&2
  exit 1
fi

CHECK=0
if [ "${1:-}" = "--check" ]; then
  CHECK=1
fi

sync_path() {
  local from="$1"
  local to="$2"
  if [ $CHECK -eq 1 ]; then
    if ! diff -qr "$from" "$to" >/dev/null 2>&1; then
      echo "DRIFT $to"
      diff -r "$from" "$to" || true
    else
      echo "OK    $to"
    fi
  else
    mkdir -p "$(dirname "$to")"
    rm -rf "$to"
    cp -R "$from" "$to"
    echo "synced $to"
  fi
}

sync_path "$SRC/.claude/skills/terraform"   "$DST/skills/terraform"
sync_path "$SRC/.claude/skills/mcaf-module" "$DST/skills/mcaf-module"
sync_path "$SRC/.claude/skills/review-mcaf" "$DST/skills/review-mcaf"

# GUIDE.md is the authoritative source for mcaf-module + review-mcaf.
# It lives at the mcaf-review repo root; we bundle it with mcaf-module.
if [ $CHECK -eq 1 ]; then
  if ! diff -q "$SRC/GUIDE.md" "$DST/skills/mcaf-module/GUIDE.md" >/dev/null 2>&1; then
    echo "DRIFT $DST/skills/mcaf-module/GUIDE.md"
  else
    echo "OK    $DST/skills/mcaf-module/GUIDE.md"
  fi
else
  cp "$SRC/GUIDE.md" "$DST/skills/mcaf-module/GUIDE.md"
  echo "synced $DST/skills/mcaf-module/GUIDE.md"
fi

# Rewrite GUIDE.md path references in review-mcaf so cross-skill links resolve
# once installed as siblings under ~/.claude/skills/ (or wherever the harness
# symlinks them).
if [ $CHECK -eq 0 ]; then
  RMD="$DST/skills/review-mcaf/SKILL.md"
  MMD="$DST/skills/mcaf-module/SKILL.md"

  # Portable in-place sed (BSD + GNU).
  sed_i() {
    if sed --version >/dev/null 2>&1; then sed -i "$@"; else sed -i '' "$@"; fi
  }

  # review-mcaf: rewrite every `GUIDE.md` codespan — covers `GUIDE.md`,
  # `GUIDE.md §3`, `GUIDE.md` §X/§Y, etc. Order matters: the trailing-space
  # variant runs first so the backtick-closed variant doesn't match it.
  sed_i 's|`GUIDE\.md |`../mcaf-module/GUIDE.md |g' "$RMD"
  sed_i 's|`GUIDE\.md`|`../mcaf-module/GUIDE.md`|g' "$RMD"
  sed_i 's|lives in `\.\./mcaf-module/GUIDE\.md`|lives in [`../mcaf-module/GUIDE.md`](../mcaf-module/GUIDE.md)|g' "$RMD"
  sed_i 's|- `\.\./mcaf-module/GUIDE\.md` — the source of truth|- [`../mcaf-module/GUIDE.md`](../mcaf-module/GUIDE.md) — the source of truth|g' "$RMD"

  # In mcaf-module, GUIDE.md is a sibling file — point link at it directly.
  sed_i 's|`GUIDE\.md` in this repo|[`GUIDE.md`](GUIDE.md) bundled with this skill|g' "$MMD"

  echo "rewrote GUIDE.md path references in review-mcaf + mcaf-module SKILL.md"
fi

if [ $CHECK -eq 0 ]; then
  echo
  echo "Validate with: python3 cli/sbp-skills validate packs/terraform skills/terraform skills/mcaf-module skills/review-mcaf"
fi
