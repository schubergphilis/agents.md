---
name: sbp-secure-code-review
description: Use when reviewing code in mission-critical systems — checks OWASP Top 10, authentication and authorization, input validation, secrets handling, dependency vulnerabilities, cryptography, and security logging, framing findings by blast radius and customer impact.
metadata:
  domain: security
  lifecycle: build
---

# Security-Focused Code Review

Review the code specifically for security concerns. This is not a general code quality review — focus exclusively on vulnerabilities, misconfigurations, and security design flaws. For mission-critical systems, every finding must be framed in terms of blast radius and customer impact.

## Authentication and authorization

- **Auth on every endpoint**: is authentication enforced on all endpoints that require it? Are there unprotected endpoints that should be protected?
- **Authorization enforcement**: is authorization checked (not just authentication)? Can a user with valid credentials access resources they should not? Check for IDOR (insecure direct object references).
- **Privilege escalation**: are there paths where a regular user can perform admin actions? Are role checks applied consistently?
- **Token handling**: are tokens validated properly? Are JWTs verified with the correct algorithm and key? Are token expiration and revocation handled?
- **Session management**: are sessions invalidated on logout? Are session tokens rotated? Is there protection against session fixation?

## Input validation

- **SQL injection**: is user input parameterized in all database queries? Search for string concatenation in SQL statements.
- **Command injection**: is user input passed to shell commands, system calls, or process execution? Check for exec, spawn, system, eval.
- **Path traversal**: can user input manipulate file paths? Check for ../ sequences, absolute paths in user-controlled input.
- **XSS (cross-site scripting)**: is user input rendered in HTML without escaping? Check templates, frontend code, API responses used in rendering.
- **XXE (XML external entities)**: if XML is parsed, are external entities disabled?
- **Insecure deserialization**: is untrusted data deserialized using unsafe mechanisms? (Python object serialization, Java native serialization, unsafe YAML load, eval of JSON-like strings)
- **Server-side request forgery (SSRF)**: can user input control URLs that the server fetches? Are there allow-lists for outbound requests?
- **Regex denial of service (ReDoS)**: are there complex regex patterns applied to user input that could cause catastrophic backtracking?

## Secrets management

- **Hardcoded credentials**: search for API keys, passwords, tokens, connection strings embedded in source code.
- **Secret loading**: are secrets loaded from environment variables, secret managers (Vault, AWS Secrets Manager, Azure Key Vault), or config files? Config files in the repo are a red flag.
- **Secret exposure in logs**: are secrets, tokens, or passwords printed in log output or error messages?
- **Secret exposure in URLs**: are credentials passed as query parameters (they end up in access logs and browser history)?
- **.gitignore coverage**: are secret files (.env, credentials.json, *.pem, *.key) excluded from version control?

## Dependencies

- **Known vulnerabilities**: are any dependencies on known-vulnerable versions? Check against CVE databases.
- **Version pinning**: are dependency versions pinned (exact or range-locked)? Unpinned dependencies can introduce vulnerabilities silently.
- **Dependency count**: are there unnecessary dependencies that expand the attack surface?
- **Supply chain risk**: are dependencies from reputable sources? Are lock files committed?

## Cryptography

- **Custom implementations**: is there any hand-rolled cryptography? This is almost always wrong — flag it as critical.
- **Algorithm selection**: are deprecated algorithms used for security purposes? Flag: MD5, SHA1 for integrity/signing, DES, RC4, ECB mode.
- **Key management**: how are encryption keys stored and rotated? Are they hardcoded?
- **TLS configuration**: is TLS enforced? Are insecure protocol versions allowed (TLS 1.0, 1.1, SSLv3)? Are certificates validated?
- **Random number generation**: is a cryptographically secure random number generator used where security matters? (not Math.random, not the standard random module for tokens)

## Security logging and error handling

- **Security event logging**: are authentication failures, authorization failures, and access to sensitive resources logged?
- **Sensitive data in errors**: do error messages returned to users expose internal details (stack traces, database schemas, file paths, version numbers)?
- **Sensitive data in logs**: are passwords, tokens, credit card numbers, or PII written to logs?
- **Error handling consistency**: are there catch-all handlers that swallow security exceptions silently?
- **Audit trail**: for sensitive operations (user creation, permission changes, data export), is there an audit log?

## OWASP Top 10 cross-check

After the detailed review above, verify coverage of the current OWASP Top 10:

1. **Broken access control** — covered in auth section above.
2. **Cryptographic failures** — covered in cryptography section above.
3. **Injection** — covered in input validation above.
4. **Insecure design** — are there architectural security flaws? Missing trust boundaries? Security decisions based on client-side logic?
5. **Security misconfiguration** — are default credentials, unnecessary features, or overly permissive configs present?
6. **Vulnerable and outdated components** — covered in dependencies above.
7. **Identification and authentication failures** — covered in auth section above.
8. **Software and data integrity failures** — are CI/CD pipelines protected? Are software updates verified? Is there protection against unsigned code?
9. **Security logging and monitoring failures** — covered in logging section above.
10. **Server-side request forgery** — covered in input validation above.

## Output: Security findings

Present findings grouped by severity:

### Critical

Findings that could lead to data breach, full system compromise, or unauthorized access to customer data. Include:
- **File and line**: exact location in the codebase.
- **Vulnerability**: what the issue is, concretely.
- **Blast radius**: what is at risk if exploited — which customers, which data, which systems.
- **Exploitation**: how an attacker would exploit this (be specific enough to demonstrate the risk without providing a complete attack script).
- **Remediation**: exact code change or configuration fix needed.

### High

Findings that could lead to partial compromise, privilege escalation, or significant data exposure. Same format as critical.

### Medium

Findings that represent defense-in-depth gaps or could be chained with other vulnerabilities. Same format as critical.

### Low

Findings that are best-practice violations or minor hardening opportunities. Same format as critical.

### Summary

- Total findings by severity.
- Top 3 areas of concern with rationale.
- Whether the code is acceptable for production deployment from a security perspective — YES, YES WITH CONDITIONS, or NO with the blocking issues stated.
