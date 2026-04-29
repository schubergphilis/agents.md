---
name: review-mcaf
description: Perform a qualitative MCAF module review covering best practices, usability, lifecycle currency, supply chain, security defaults, and design smells — and produce a good/bad/verdict markdown report. Use when the user asks for an "MCAF review", wants to assess whether a module is ship-ready, wants to triage multiple MCAF modules, asks "is this module any good?", or references `REVIEW.md`. For a single repo the skill produces one markdown section; for many it dispatches parallel subagents and stitches them into one file.
---

# review-mcaf

Qualitative review for Schuberg Philis MCAF Terraform modules. This is the judgement layer on top of the structural checklists in the [`terraform`](../terraform/SKILL.md) and [`mcaf-module`](../mcaf-module/SKILL.md) skills — what the eye catches that a rubric cannot:

- whether abstractions are right-sized,
- whether security defaults are safe,
- whether the README actually teaches,
- whether tests are meaningful or token,
- whether the module has correctness bugs or dead code,
- whether LCM / supply-chain rot is visible.

The ground truth for every rule lives in [`../mcaf-module/GUIDE.md`](../mcaf-module/GUIDE.md). This skill is the playbook for applying it.

## When to use this skill

Trigger on any of:

- "review this MCAF module" / "do an MCAF review" / "check it against MCAF best practices"
- "is `terraform-<provider>-mcaf-<name>` good?"
- "review all MCAF modules in `repos/`"
- "assess these modules for ship-readiness"
- After substantive changes to an MCAF module, before creating the PR or cutting a release
- User references `REVIEW.md` in conversation

For small one-rule structural questions (e.g. "does this look MCAF-compliant?"), use `mcaf-module` instead — it's lighter-weight.

## Target discovery (where "the modules" actually live)

The skill does not assume a fixed directory. Work out the target set from what the user said:

- **"review this module"** / no path / inside a repo → target is the **current working directory**. Confirm it looks like an MCAF module (`terraform-<provider>-mcaf-<name>` name, a `main.tf` or `terraform.tf` at the root) before proceeding.
- **Explicit single path** ("review `~/code/terraform-aws-mcaf-s3`") → that directory.
- **Container directory** ("review all MCAF modules in `./repos`", "review the modules under `~/git/schuberg/`") → recurse one or two levels and collect every directory whose **basename** matches `^terraform-[a-z]+-mcaf-` and which contains a `.tf` file at its root. Do not descend into `examples/`, `modules/`, `tests/`, `.terraform/`, `.git/`.
- **Org-wide** ("review all MCAF modules", no local path) → enumerate with `gh api orgs/schubergphilis/repos --paginate -q '.[] | select(.archived==false) | select(.name|test("^terraform-[a-z]+-mcaf-")) | {name, ssh_url, pushed_at}'`. Clone what's missing shallowly (`git clone --depth 1`) into a working dir the user picked (or `./repos/<provider>/<name>/` by default). Ask before cloning ~90 repos unprompted.

Derive `<provider>` from the second token of the repo name (`terraform-aws-…` → `aws`, `terraform-azure-…` → `azure`, etc.; anything else → `other`). Use this for the output grouping and for applying provider-specific conventions (AWS label `"default"` vs Azure label `"this"`, taggable-provider rule, etc.).

If exactly **one** target resolves, produce a single section. If **≥2**, follow the "Many-module review procedure" at the bottom of this file.

## What to read for each module

**Always** (cheap and essential):
- `main.tf`
- `variables.tf` (and `variables.*.tf` if domain-split)
- `outputs.tf`
- `README.md` (prose sections; the `BEGIN_TF_DOCS` block is auto-generated — skim only)

**If present**:
- `tests/*.tftest.hcl` and `tests/setup/` — test depth matters more than test presence
- `.github/workflows/*.y*ml` — look for stale action pins and flagged publishers
- `locals.tf`, `data.tf` — locals that recompute vs locals that extract invariants
- `modules/*/` — sub-module quality is part of the review
- `CHANGELOG.md`, `UPGRADING.md` — evidence of deliberate lifecycle management
- `package.json` / `requirements.txt` if the module ships Lambda — supply-chain check
- `terraform.tf` — currency of floors and pins

**Skip**:
- Every other module in the corpus; do not try to cross-reference.
- The auto-generated portion of `README.md`.
- Lock files, `.terraform/`.

## The review dimensions

Walk each dimension for every module. Note concrete findings — cite variable/resource/file names. Generic bullets fail the review.

1. **Repository hygiene** — canonical filenames (`terraform.tf`, `main.tf`, `Taskfile.yaml`); no camelCase file names; no stray `VERSION` / `INFO.md` / `example.tfvars`; `README copy.md` or other accidental commits.
2. **Variable design** —
   - Every `variable` has `description` + `type` in the canonical arg order (per `../mcaf-module/GUIDE.md §3`): `type` → `default` → `description` → `nullable` / `sensitive` → `validation`. `description` before `type` or `validation` before `type`/`description` are the common violations.
   - Complex shapes use `object({ ... optional(..., default) ... })` rather than flat var sprawl.
   - Constrained values have `validation` with an actionable `error_message`.
   - `sensitive = true` on credentials; `nullable = false` on truly-required inputs.
   - `default = null` (not `""`) for "unset".
   - No flat-variable passthroughs that duplicate a child module's surface.
3. **Resource / logic quality** —
   - Provider-canonical labels (`"default"` on AWS/GitHub/Datadog/TFE/GitLab; `"this"` on Azure).
   - No copy-paste bugs inside `for_each` blocks (very common: `var.x` where `each.value.x` was meant).
   - Preconditions (`lifecycle { precondition { ... } }`) used for cross-field invariants.
   - `moved {}` blocks for refactors — state-preserving renames.
   - No dead variables / locals / files.
   - No `null_resource` / deprecated resources (`aws_s3_bucket_object`, `azurerm_function_app`).
   - Resource group ownership is caller's responsibility on Azure — flag any internal `azurerm_resource_group.this` with a `count` toggle.
4. **Outputs** —
   - `description` on every output; first are `id` / `arn` / `name`.
   - No whole-resource dumps (`output "resource" { value = aws_x.this }`).
   - Sensitive values marked `sensitive = true`.
   - Minimum useful surface — not every attribute re-exported.
5. **Tags** —
   - `variable "tags"` defaults to `{}` (not `null`).
   - Every taggable resource references `var.tags`. No `local.tags` indirection unless the module genuinely needs to inject extra tags.
   - No `try(var.tags)` cargo-cult.
   - No hard-coded tag keys buried inside individual resources.
6. **Examples** — `examples/default/` present; additional examples cover major feature branches; each is valid HCL; no ad-hoc `## Usage` HCL blob in README.
7. **Tests** — native `terraform test` with `mock_provider`; multiple `run` blocks per behaviour; `expect_failures` for negative paths; tests assert on *derived* values (not just re-echoing defaults).
8. **CI & pre-commit** — five standard workflows from `mcaf-github-workflows` with the `DO NOT CHANGE` header intact; no hand-edits; pre-commit config includes the core hooks.
9. **Lifecycle / currency** —
   - Terraform `required_version` allows the newest Terraform (no upper bound). The exact floor is not important — just verify the constraint shape.
   - AWS `>= 6` (no upper bound). AzureAD `>= 3, < 4`, Azurerm `>= 4, < 5`, Datadog `>= 3, < 4` (upper bound at next major). Don't bikeshed the minor; focus on whether the bounds are correct.
   - No exact or patch-tight provider pins.
   - No deprecated HCL or deprecated provider resources.
   - No action pins older than current (`setup-terraform@v3`, `checkout@v4`, `github-script@v7`, `terraform-docs/gh-actions@v1.3.0`).
   - Child MCAF modules referenced via registry + `version = "~> X.Y"`, not `?ref=vX.Y.Z`.
10. **Supply chain** —
    - No `@master` / `@main` action refs.
    - No `uses:` with no `@ref` at all (unpinned).
    - No "weird" ref shapes (non-SHA, non-semver, non-branch) — flag and investigate.
    - No flagged publishers (`Dirrk`, `triat`, `danielchabr`, `anothrNick`, `jessfraz`).
    - Non-trusted publishers → SHA-pinned (40-char hex).
    - Lambda Python deps `==X.Y.Z`; Node deps have a committed lockfile.
    - No floating `:latest` / `:main` image defaults.
11. **README usefulness** — explains gotchas a caller cannot infer from the inputs table (multi-account aliased providers, operational caveats, lifecycle warnings); no hand-written inputs table; has the version-pinning `IMPORTANT` banner; has `## Licensing` footer.
12. **Security defaults** — encryption on by default; public access off; TLS ≥ 1.2; secrets not logged; IAM principle-of-least-privilege; broad `0.0.0.0/0` only where explicitly justified.
13. **Recency** — derive last-push from `git log -1 --format=%cI` (or the cloned repo's HEAD date). Treat **>24 months** with no push as a strong push toward `deprecate-or-consolidate` unless the module is clearly "done" (stable, small, no drift). **>12 months** is a soft signal — weigh alongside the other dimensions, don't let it drive the verdict alone.

## Recurring anti-patterns to hunt for

Each of these appears across the corpus. Check every module for them:

1. **Whole-resource outputs** leaking sensitive attributes.
2. **`try(var.tags)`** cargo-cult.
3. **Two sources of truth for resource group** on Azure.
4. **Hard-pinned child-module `?ref=vX.Y.Z`** inside a module.
5. **Empty `outputs.tf`** — module is a black box.
6. **Missing `sensitive = true`** on passwords/keys/tokens/kubeconfig.
7. **Floating `:latest` / `:main`** image/version defaults.
8. **Dead variables / locals / files / commented-out blocks**.
9. **File-naming drift** (camelCase, `backend.tf`, `module.tf`, `versions.tf`, `Taskfile.yml`).
10. **Nested ternaries over `optional(field, default)`** — wrong type shape.

Also spot-check for the concrete bug classes observed in the corpus:

- Swapped output wiring.
- `each.value.*` vs `var.*` copy-paste inside `for_each`.
- Policy conditions comparing `.name` to an ARN.
- `archive_file.output_path` as a relative path.
- References to `azurerm_resource_group.this` that is never declared.
- Cron expressions with the wrong number of fields.

## Output format

**One module** → one markdown section, exactly this shape:

```markdown
### `<module-name>`

**Last pushed:** YYYY-MM-DD  <!-- optional, only if quickly derivable -->

**Good:**
- Concrete bullet citing `variable_name` / `resource "..." "..."` / file path.
- 3–6 bullets total.

**Bad:**
- Concrete bullet with specifics.
- 3–6 bullets total.

**Verdict:** One sentence. Pick one tag:
- `keep-as-is` — reference quality, clone when starting a new module.
- `minor-cleanup` — healthy design, small fixes (descriptions, pin bumps, tag merge, output polish).
- `major-refactor` — real design or correctness issues; reshape, fix bugs, rewrite sections.
- `deprecate-or-consolidate` — empty shell, abandoned, or duplicate with a better sibling.
```

Hard rules on the review prose:

- **≤180 words per module**. Terse is better.
- **Concrete, not generic.** "Missing `sensitive = true` on `variable "api_key"`" beats "sensitive values not marked". If you cannot cite a name, you have not read carefully enough.
- **Do not repeat structural checklist items** unless they are the headline issue. The `mcaf-module` skill handles "missing Taskfile" etc.; this skill adds the judgement layer.
- **Modules that fail most of the structural checklist**: be blunt about whether they are worth rescuing. If the repo is a README-only scaffold, `deprecate-or-consolidate` is the honest answer.
- **No preamble, no trailing summary** per section.

**Many modules** → concatenate sections in this order:

1. H1 title + one-paragraph intro.
2. "Verdict distribution" table (counts per tag).
3. Per-tag headline lists:
   - 🥇 `keep-as-is` — named bullets with module + static %.
   - 🗑️ `deprecate-or-consolidate` — named bullets with one-line reason.
   - 🔧 `major-refactor` — table with headline issue per module.
4. "Cross-corpus standout findings" — systemic patterns you saw recurring.
5. All per-module sections grouped roughly by provider (AWS → Azure → Other), alphabetical within group.

## Single-module review procedure

1. Confirm the target path. Assume `repos/<provider>/<name>/` or a direct repo path supplied by the user.
2. Read the files listed under "What to read" above.
3. Walk the 13 review dimensions and the 10 anti-pattern hunts.
4. Draft the section in the exact format.
5. Keep ≤180 words. Trim generic bullets first.

## Many-module review procedure

When reviewing more than ~5 modules at once:

1. List the target modules. If last-pushed dates are easy to derive (e.g. from `git log`), include them in the section header for grounding.
2. Bucket into groups of ~10. Dispatch **parallel subagents** (one per bucket) via the `Task` / `Agent` tool. Each subagent gets:
   - The review dimensions + anti-pattern hunts (link to this skill or inline them).
   - The list of module paths for its bucket.
   - The exact output format.
   - Explicit instruction to return ONLY concatenated markdown sections, no preamble.
3. As each agent finishes, stash its output to a scratch file (e.g. `/tmp/review-bucket-<N>.md`).
4. Once all complete, stitch into a single file. Compute the verdict distribution. Write the headline tables. Extract **cross-corpus findings** — only include a pattern if it appeared in **≥3 modules** (or ≥3 buckets, whichever is stricter). Single-module oddities belong in their own section, not the cross-corpus roll-up.
5. Save to `REVIEW.md` at the repo root (or a user-specified path).

Parallel-dispatch tips:

- Each subagent should be briefed to skim `../mcaf-module/GUIDE.md` §3/§5/§7/§11 first and reference it as source of truth.
- Tell each subagent the provider-specific conventions: AWS label `"default"`, Azure label `"this"`; Azure gold standard is `terraform-azure-mcaf-storage-account`, AWS gold standard is `terraform-aws-mcaf-s3`.
- When the first agent returns, validate its format before the rest finish — catches prompt-level drift early.
- Do not tail the agent transcript files — they are JSONL and will blow context. Save the final output only.

## Edge cases

- **Repo with no Terraform code** (LICENSE + README only) → `deprecate-or-consolidate`. Do not pretend there is substance to review.
- **Repo that fails `terraform validate`** (missing resources, empty `terraform.tf`) → lead the **Bad** bullets with the plan-breaking issue, verdict `major-refactor` or `deprecate-or-consolidate`.
- **Non-AWS/Azure providers** (gitlab, tfe, datadog) — do not penalise for AWS/Azure conventions that don't apply (e.g. no `tags` on GitLab). Use `terraform-github-mcaf-repository` as the cross-provider reference.
- **Private providers** (`schubergphilis/mcaf`, etc.) — note in the review if undocumented.
- **Module that embeds `provider "x" { ... }`** — always a **Bad** bullet and usually `major-refactor`; providers belong in the root caller.

## Don't

- Do not run automated scorers or write Python scripts to produce this report. This skill is prose judgement; mechanical checks are the other skill's job.
- Do not duplicate the structural checklist line-by-line — that is the `mcaf-module` skill's job.
- Do not generate generic bullets. Every bullet cites a concrete name.
- Do not add a "Neutral" or "Observations" section — Good / Bad / Verdict only.
- Do not invent findings. If you did not read the file, do not write a bullet about it.

## Related

- [`../mcaf-module/GUIDE.md`](../mcaf-module/GUIDE.md) — the source of truth for every rule cited above.
- [`terraform`](../terraform/SKILL.md) skill — generic Terraform/OpenTofu baseline.
- [`mcaf-module`](../mcaf-module/SKILL.md) skill — structural checklist for authoring and PR review.
