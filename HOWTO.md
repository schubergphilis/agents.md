# How to use sbp-skills

This guide shows how sbp-skills changes your daily work in Claude Code. It assumes you already use Claude Code and know what a skill is. The examples follow one scenario throughout: building an alerting pipeline for a mission-critical service.

---

## 1. Install

Open Claude Code and run:

```
/plugin marketplace add schubergphilis/agents.md
```

Then install the skill groups you want:

```
/plugin install operations-skills@sbp-skills
/plugin install security-skills@sbp-skills
/plugin install engineering-skills@sbp-skills
/plugin install brand-skills@sbp-skills
```

To verify it worked, ask Claude: *"What should I think about before adding a new service to our platform?"*

Without sbp-skills, you get a generic answer. With it, Claude asks about blast radius, rollback, who gets paged, and what happens at 3 AM. That difference is the point.

---

## 2. Plan: Reviewing a system architecture

**Context:** You want a mission-critical review of your system before the team starts building on top of it.

Type the skill name in Claude Code:

```
/sbp-architecture-review
```

The skill first explores the codebase autonomously — reading files, tracing dependencies, understanding what is actually there. Then it produces a structured review. Here is real output from a recent run:

---

**Architecture Review**

*Reviewed: 2026-05-05 / Reviewer: Claude Code / sbp-architecture-review*

**What's here**

| Component | Purpose | Status |
|-----------|---------|--------|
| SBP Framework | Claude Code commands + skills for mission-critical engineering | Dev / operational |
| vulnapp/ | Intentionally vulnerable Flask app for security education | Educational / local only |

---

**Strengths**

AGENTS.md is genuinely good engineering philosophy. The "3 AM question" framing, the explicit blast-radius-first thinking, and the requirement to explain *why* rather than just *what* — these are the right instincts, clearly stated.

vulnapp is well-contained for its purpose. It binds to 127.0.0.1 only, uses an ephemeral /tmp database, and ships a clear header listing every intentional vulnerability.

---

**Risks**

`HIGH` — Framework has no Claude API availability fallback

The entire command set is powered by the Claude API. If the API is unavailable, engineers lose all framework support with no degraded mode and no offline runbook substitute. Blast radius: all engineers lose decision-support tooling exactly when a production incident might also be occurring.

`HIGH` — No CI/CD pipeline or automated gate

Zero CI configuration. Changes to commands, skills, or vulnapp are merged with no automated verification. A broken skill ships silently — and if an engineer runs `/pre-deploy` during a production push and the command itself is broken, they get false confidence. That is the worst outcome for a tool designed to prevent exactly that.

`HIGH` — vulnapp has no deployment guard-rail beyond the warning comment

Nothing prevents the app from being deployed behind a public-facing reverse proxy. If deployed publicly, all six vulnerability classes become live attack surface.

`MEDIUM` — Rollback is theoretical only

No deployment pipeline means rollback is "revert the git commit and re-run." This has never been tested. For the framework specifically, breaking a command means manual intervention with no defined recovery time objective.

---

**Recommendations (ordered by severity)**

1. **[HIGH]** Add a Claude API circuit breaker / offline fallback. Define a minimal offline mode — a static Markdown checklist that covers the same surface as `/pre-deploy` and `/risk-check`. Engineers should be able to run a degraded-but-functional review without API access.

2. **[HIGH]** Add a CI pipeline. A GitHub Actions workflow that runs a syntax check and validates command/skill YAML on every PR. It does not need to be sophisticated — it needs to exist so broken changes are caught before merge.

3. **[HIGH]** Add a network-level guard for vulnapp. A comment is not a guard. Add an assertion that aborts if the app is not bound to localhost:
   ```python
   assert host == "127.0.0.1", "vulnapp must not be exposed beyond localhost"
   ```

4. **[MEDIUM]** Document a tested rollback procedure. "Revert the commit and re-run" is only a rollback if someone has verified it works. Write three steps, run them once, record that they were tested.

---

*Summary: The framework philosophy is strong. The operational scaffolding is absent: no CI, no API fallback, no tested rollback. For a framework engineers rely on during production incidents, that gap is the most urgent thing to close.*

---

You get a prioritised list of risks before any code changes. Each finding has a blast radius, a recommendation, and enough context to act on it immediately.

---

## 3. Build: Security review

**Context:** You want a security review of a codebase before it ships.

First, enable the skill from the CLI (or via the plugin install — same result):

```bash
sbp-skills enable sbp-secure-code-review
```

Then in Claude Code:

```
use sbp-secure-code-review
```

The skill explores the codebase first, then produces a structured review with severity ratings, blast radius for each finding, exploitation steps, and concrete remediation. Here is real output from a recent run on a Flask app:

---

**Security Review — vulnapp/app.py**

*Context: Intentionally vulnerable Flask app for local security education. Every finding below is a deliberate demonstration of a real vulnerability class. This review treats it as if it were production code.*

---

**Critical**

**C1 — SQL Injection: Authentication Bypass (app.py:90)**

```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```

Blast radius: Any unauthenticated actor can log in as any user — including admin — without knowing any credentials. Full authentication layer is bypassed.

Exploitation: Submit `username = ' OR '1'='1' --` with any password.

Remediation:
```python
row = db.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (username, password)
).fetchone()
```

---

**C3 — IDOR + Plaintext Password Exposure (app.py:142)**

```python
return f"<h3>User #{row['id']}</h3><p>Username: {row['username']}<br>Password: {row['password']}</p>"
```

Blast radius: Any unauthenticated visitor can enumerate all user accounts and retrieve their plaintext passwords by iterating `/user/1`, `/user/2`, etc. Full credential dump in three HTTP requests.

Remediation: Require authentication, enforce users can only read their own profile, never return password fields from any endpoint. Passwords must be stored as salted hashes.

---

**C4 — Path Traversal: Arbitrary File Read (app.py:152)**

```python
path = os.path.join("/tmp/uploads", name)
with open(path) as f:
    content = f.read()
```

Blast radius: Any file readable by the process user can be exfiltrated — `/etc/passwd`, source code, environment files, SSH keys, cloud credentials. On a container running as root, this is a full filesystem read.

Remediation:
```python
base = os.path.realpath("/tmp/uploads")
candidate = os.path.realpath(os.path.join(base, name))
if not candidate.startswith(base + os.sep):
    return "Forbidden", 403
```

---

**High**

**H3 — Hardcoded Flask Secret Key (app.py:18)**

```python
app.secret_key = "supersecret123"
```

Blast radius: Anyone with repo access can forge valid session cookies for any user — including admin — without ever authenticating. This is a complete authentication bypass that survives SQL injection fixes.

Remediation:
```python
import os, sys
app.secret_key = os.environ.get("SECRET_KEY") or sys.exit("SECRET_KEY not set")
```

---

*(...4 medium findings, 3 low findings omitted for brevity)*

---

**Summary**

| Severity | Count |
|----------|-------|
| Critical | 4 |
| High | 4 |
| Medium | 4 |
| Low | 3 |
| **Total** | **15** |

Top concern: two independently exploitable SQL injection points, both unauthenticated, one giving full auth bypass and one giving a complete database dump. A single HTTP request yields admin access or all passwords.

**Production deployment verdict: NO**

This application has four critical vulnerabilities, any one of which allows full compromise by an unauthenticated attacker. The blocking issues are C1–C4; all four must be remediated before any broader deployment is considered.

---

Each finding includes the exact line, the blast radius, a working exploit, and a drop-in fix. The review does not stop at identifying the class of bug — it tells you how to exploit it and how to fix it.

---

## 4. Run: Deploying safely

**Context:** You are about to ship a change and want a quick GO/NO-GO before pushing.

```
/pre-deploy
```

Real output from a recent run:

---

**Pre-Deploy Check: vulnapp/ — Intentionally Vulnerable Flask App**

1. **What's changing?** Adding an intentionally vulnerable Flask app (SQL injection, XSS, IDOR, path traversal, hardcoded secret) for local security education.
2. **Rollback plan?** Delete the directory or git revert — immediate, no state to clean up (DB lives in /tmp and only exists after first run).
3. **Blast radius?** If deployed anywhere beyond localhost:5001, every route is exploitable and `debug=True` enables unauthenticated RCE on the host. Blast radius is catastrophic if network-exposed, zero if localhost-only.
4. **Tests green?** No tests exist — not applicable for an educational demo, but worth noting there are no guardrails preventing accidental production use.
5. **Monitoring ready?** N/A for a local tool. No production system is involved.
6. **Anyone need to know?** Anyone with access to the repo needs to understand this must never run on a shared or internet-facing host.

**Verdict: NO-GO for any networked environment / GO for local-only educational use**

Blocking reason for networked deploy: `debug=True` + no auth + path traversal = host compromise. The app has no defence-in-depth — the only control is the 127.0.0.1 binding.

Conditions for GO:
- Confirmed running locally or in an isolated, network-none container only.
- Repo visibility is private or the team is briefed that this is intentionally broken.
- No CI pipeline spins this up with a published port.

---

Notice what happened: the command did not just say "looks fine." It found the catastrophic blast radius, named the specific mechanism (`debug=True` + no auth), and gave you a concrete condition list to satisfy before it will flip to GO. That is the kind of review that stops the 3 AM page.

For a full deployment with rollback verification, monitoring checks, and communication planning, use `sbp-deploy-checklist` instead.

---

## 5. Run: After something breaks

**Context:** Three weeks later, alert fanout silently dropped messages for two hours. The incident is over. Time to learn from it.

```
Use sbp-incident-review to run the post-incident review for the fanout outage.
```

The skill walks you through a blameless timeline and 5 whys. It does not let you stop at "the webhook timed out." It pushes until you find why the timeout was not caught by monitoring, why the retry logic did not surface the error, and what let a deployment go out without testing that failure mode.

The output is a structured report with action items, owners, and deadlines, ready to share with the team.

---

## What's next

Run `sbp-skills list` to browse everything available, or look through the `skills/` directory in this repo. If you find a workflow that is not covered, scaffold a new skill with:

```bash
sbp-skills dev --skill sbp-your-skill-name
```

Then open a PR.
