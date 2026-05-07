---
name: sbp-dependency-audit
description: Use when conducting a security review, reducing dependency surface, or when dependencies may pose supply-chain, bloat, or maintainability risks.
metadata:
  domain: security
  lifecycle: build
---

# Dependency Audit

Audit project dependencies for bloat, risk, and supply-chain concerns. The goal is a clear picture of what you depend on, why, and whether each dependency is worth the risk it carries.

Work incrementally — one category at a time. Do not try to fix everything at once.

## Step 1: Discovery

Build a complete inventory of dependencies and actual usage.

**List all direct dependencies**:
- Python: parse `pyproject.toml`, `requirements.txt`, `setup.py`, `setup.cfg`.
- JavaScript/TypeScript: parse `package.json` (both `dependencies` and `devDependencies`).
- Go: parse `go.mod`.
- Note the declared version constraints (pinned, range, latest).

**Identify what is actually imported**:
- Search the codebase for actual import statements and usage of each dependency.
- Flag dependencies that are declared but never imported — these are removal candidates.
- Note which specific functions or classes are used from each dependency. A project that imports one function from a 50,000-line library is a candidate for inlining.

**Map transitive dependencies**:
- Use the lockfile (`uv.lock`, `package-lock.json`, `go.sum`) to count transitive dependencies.
- Each transitive dependency is an attack surface you did not choose. High transitive counts deserve scrutiny.

## Step 2: Classification

Classify each direct dependency into one of five categories:

### Keep

Large, well-maintained, complex libraries where writing your own would be foolish.

Criteria: actively maintained (commits in last 6 months), multiple maintainers, solves a genuinely hard problem (HTTP server, cryptography, database driver, ML framework), widely used and battle-tested.

### Inline

Tiny packages that do one simple thing in under 100 lines of code.

Criteria: the functionality is trivial to implement, the package has few or no updates, and depending on it adds supply-chain risk disproportionate to its value. Copy the implementation (respecting the license), add a comment noting the origin, and remove the dependency.

Examples: left-pad-style packages, simple string utilities, single-function math helpers.

### Replace with native

Packages that provide functionality now available in the language's standard library or in a dependency you already have.

Criteria: the functionality exists natively in the current language version or in a library already in your dependency tree. Common cases: backport packages for features now in the stdlib, polyfill packages for APIs now widely available.

### Vendor

Narrow-purpose, stable packages where you want to lock the exact code but the package is too complex to inline.

Criteria: the package is stable (no updates needed), you use it for a specific purpose, and you want to decouple from the package registry. Copy the package into a `vendor/` or `3rdparty/` directory, preserving its license.

### Remove

Packages that are not imported anywhere, or that are imported but the functionality is unused (dead code paths).

Criteria: no import found in the codebase, or the import exists but the code path is never reached. Remove the dependency and run the test suite to confirm nothing breaks.

## Step 3: Supply-chain risk assessment

For each dependency classified as "keep," evaluate supply-chain risk:

**Maintenance status**:
- When was the last release? Last commit?
- How many maintainers have commit access? (Single-maintainer packages are higher risk)
- Is there a bus factor problem?

**Known vulnerabilities**:
- Check against vulnerability databases (OSV, GitHub Advisory Database, Snyk).
- Note any unpatched CVEs, especially in dependencies that handle untrusted input (parsers, serializers, network libraries).

**Trust indicators**:
- Is the package from a known organization or verified publisher?
- Does the package use 2FA for publishing?
- Has the package ever been involved in a supply-chain incident?

**Attack surface analysis for mission-critical systems**:
- Does this dependency have install-time hooks (setup.py with custom install commands, postinstall scripts)? These execute arbitrary code during `pip install` or `npm install`.
- Does this dependency download additional code at runtime?
- Does this dependency require network access to function?
- Could a compromised version of this dependency access secrets, credentials, or customer data in your environment?

Flag any dependency that is: unmaintained (no updates in 12+ months), single-maintainer, has known vulnerabilities, or has install-time code execution.

## Step 4: Action plan

Produce a prioritized list of actions. Work through these one category at a time, running the full test suite after each change.

**Priority 1 — Remove** (lowest effort, immediate risk reduction):
- Remove unused dependencies. Run tests. Commit.

**Priority 2 — Replace with native** (low effort, reduces surface area):
- Replace backport/polyfill packages with native equivalents. Run tests. Commit.

**Priority 3 — Inline** (moderate effort, meaningful risk reduction):
- For each inline candidate: copy the relevant code, respect the license, add an origin comment, remove the dependency. Run tests. Commit.

**Priority 4 — Vendor** (moderate effort, supply-chain protection):
- For each vendor candidate: copy the package, preserve the license, update import paths. Run tests. Commit.

**Priority 5 — Address vulnerabilities** (effort varies):
- For each vulnerability: update to a patched version if available, or evaluate whether the vulnerability is exploitable in your usage.

**Priority 6 — Monitor** (ongoing):
- Set up automated vulnerability scanning (Dependabot, Renovate, Snyk).
- Review new dependencies at PR time — every new dependency is a new trust decision.

## Output

Produce two artifacts:

### Summary table

| Package | Version | Category | Risk | Action | Effort | Notes |
|---------|---------|----------|------|--------|--------|-------|
| requests | 2.31.0 | Keep | Low | None | - | Well-maintained, widely used |
| left-pad | 1.0.0 | Inline | Medium | Copy 3-line implementation | 15 min | Single maintainer, trivial function |
| typing-extensions | 4.8.0 | Replace | Low | Remove (Python 3.11+) | 5 min | Backport no longer needed |

### Detailed recommendations

For each action item, provide:
- What to do (specific steps or code snippet).
- What to watch out for (license implications, breaking changes).
- How to verify (which tests to run, what to check).

## Important reminders

- **Always respect licenses.** When inlining or vendoring, include the original license and attribution.
- **Always run the full test suite after each change.** Do not batch removals — one at a time, verified.
- **Do not remove devDependencies used in CI.** Check CI pipeline configuration, not just application code.
- **Some "unused" imports are used dynamically.** Check for plugin systems, lazy imports, and conditional imports before removing.
- **Coordinate with the team.** Dependency changes affect everyone. Communicate before making sweeping changes.
