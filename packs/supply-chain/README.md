# Supply-Chain Hardening Pack

Prevent compromised dependencies from reaching your CI/CD pipeline.

## What this activates

- Pin all GitHub Actions to full commit SHA (not mutable tags)
- Version comments for human readability

## Auto-detected by

- `.github/workflows/*.yml`
- `.github/workflows/*.yaml`

## Why this matters

A compromised or moved tag on a GitHub Action can inject code into every pipeline that uses it. SHA pinning is the only reliable defence — it ensures you run exactly the code you reviewed.
