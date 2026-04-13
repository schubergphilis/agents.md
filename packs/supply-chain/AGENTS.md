<!-- BEGIN pack: supply-chain -->
## Supply-Chain Hardening

**Rule:** Pin every GitHub Actions `uses:` reference to a full 40-character commit SHA. Add a version comment for humans.

```yaml
# Correct — pinned to SHA with version comment:
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

# Wrong — mutable tag, can be moved after compromise:
uses: actions/checkout@v4
```

**Why:** A compromised or moved tag can inject malicious code into your CI pipeline. SHA pinning ensures you run exactly the code you reviewed.

**Finding the SHA:** Run `gh api repos/{owner}/{repo}/git/ref/tags/{version} --jq .object.sha` — if the result is a tag object, dereference it with `gh api repos/{owner}/{repo}/git/tags/{sha} --jq .object.sha`.

**Scope:** All `uses:` lines in `.github/workflows/*.yml` and reusable workflow calls. Does not apply to `run:` steps.

**Acceptance criteria:**
- [ ] Every `uses:` line is pinned to a 40-char SHA
- [ ] Every pinned line has a `# vX.Y.Z` comment
- [ ] No `uses:` lines reference branch names or mutable tags
<!-- END pack: supply-chain -->
