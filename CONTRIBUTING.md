# Contributing to Schuberg Philis AGENTS.md

Welcome! This repository captures Schuberg Philis engineering best practices as agent-readable instructions. We're excited to share our practices with the broader community and welcome contributions that improve functionality, clarity, security, and operational excellence.

## Quick Start

1. **Fork and clone** this repository
2. **Find an existing examples**
3. **Submit a pull request** following our guidelines below

## What We're Looking For

**High-impact contributions:**
- New AGENTS.md files for popular stacks and frameworks
- Improved security practices and operational guidance
- Clear introduction manuals
- Clearer, more testable instructions for agents

## Content Standards

### Writing Style
- **Imperative voice**: "Use Prettier" not "You should use Prettier"
- **Be explicit**: "Do X. Do not do Y." over vague recommendations
- **Be testable**: Include commands agents can verify
- **Short sentences**: Aim for clarity over cleverness

### Security Requirements
- **No secrets**: Use placeholders like `<API_KEY>` or `${SECRET_FROM_VAULT}`
- **Pin versions**: Specify minimum versions for tools and dependencies
- **Secure defaults**: Least privilege, scanners enabled, safe configurations
- **Document risks**: Call out security implications of choices

## Pull Request Guidelines

### Branch Naming
Use the pattern: `<type>/<short-description>`
- `feat/golang-gin-agents`
- `fix/terraform-modules-security`
- `docs/contributing-guidelines`

### Commit Messages
Follow Conventional Commits format:
```
<type>(scope): <description>

feat(catalog/python): add Django AGENTS.md with security defaults
fix(catalog/terraform): correct provider version pinning
docs(readme): clarify acceptance criteria examples
```

**Types:** feat, fix, docs, test, chore, refactor, perf, build, ci

### PR Description Template
```markdown
## What
Brief description of changes

## Why
Problem being solved or value being added

## How
Technical approach and key decisions

## Testing
- [ ] Commands in Setup Commands are tested
- [ ] Acceptance criteria are verifiable
- [ ] No secrets or sensitive data included

## Checklist
- [ ] Uses imperative, testable language
- [ ] Includes security best practices
- [ ] Links are valid and stable
- [ ] YAML front matter is complete
```

## Review Process

### What We Look For
- **Clarity**: Can an agent follow these instructions unambiguously?
- **Security**: Are defaults secure? Any missing security considerations?
- **Testability**: Are acceptance criteria objective and measurable?
- **Alignment**: Does this match the Schuberg Philis way of working?
- **Completeness**: Are all template sections addressed appropriately?

## Community Guidelines

### Code of Conduct
- **Be respectful** in discussions and feedback
- **Assume good intent** from contributors
- **Focus on technical merit** over personal preferences
- **Help newcomers** understand our standards

### Getting Help
- **Questions about standards**: Open a GitHub issue with the `question` label
- **Technical problems**: Include error messages and environment details
- **Unclear requirements**: Reference specific sections that need clarification


## Advanced Contributions

### Documentation Enhancements
- Additional examples for complex scenarios
- Integration guides for popular AI coding assistants
- Best practices documentation beyond the template
- Video tutorials for authoring AGENTS.md files

## Recognition

Contributors will be:
- **Acknowledged** in release notes for significant contributions
- **Added as collaborators** for sustained, high-quality contributions
- **Featured** in our engineering blog for innovative practices

## License and Attribution

By contributing, you agree that your contributions will be licensed under the same license as this project. When referencing external sources or adapting existing patterns, please include appropriate attribution in your AGENTS.md file.

---

## Questions?

- **General questions**: Open a GitHub issue
- **Security concerns**: Check one of us directly (@jverhoeks, @fbuters, @iheitlager)
- **Complex contributions**: Consider opening a discussion first to align on approach

Thank you for helping us build better, more secure, and more operable systems through standardized agent instructions! 🚀
