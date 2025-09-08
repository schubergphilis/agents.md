# Codebase Orientation and Discovery

**Tags**: #code_orient #discovery  
**Purpose**: Map and understand an unfamiliar codebase's architecture, patterns, and conventions  
**Configurable**: Yes - Technology stack, architectural patterns, and project structure

## Quick Usage

```
Use #code_orient to understand the structure and patterns of [codebase/module name]
```

## Full Prompt

Systematically explore and map an unfamiliar codebase:

**1. High-Level Architecture Discovery**
- Apply #context_intake to understand the project's purpose and domain
- Identify main directories and their organizational patterns
- Locate configuration files, dependencies, and build systems
- Find documentation, README files, and architectural decision records

**2. Code Structure Analysis**
- Map major modules, components, and their responsibilities
- Identify data models, schemas, and database interactions
- Understand routing patterns, API endpoints, and user interface organization
- Locate test files and understand testing patterns

**3. Pattern Recognition**
- Identify coding conventions, naming patterns, and style guidelines
- Understand error handling patterns and logging approaches
- Recognize authentication, authorization, and security patterns
- Note performance optimization patterns and architectural choices

**4. Entry Point Mapping**
- Find application entry points and initialization code
- Trace key user workflows through the codebase
- Identify external integrations and service boundaries
- Map data flow patterns and state management approaches

**5. Development Environment Understanding**
- Locate development setup instructions and dependencies
- Understand build processes, testing commands, and deployment procedures
- Identify development tools, linting rules, and formatting standards
- Find debugging approaches and common development workflows

Technology-specific exploration patterns: See prompts_config/tech_stack.md  
Project-specific architectural context: See prompts_config/project_context.md

## Configuration Points

- **Technology Stack**: Framework-specific patterns and file organization
- **Architectural Patterns**: Common design patterns and architectural styles used
- **Development Workflow**: How code is built, tested, and deployed
- **Documentation Standards**: Where to find and how to interpret project documentation
- **Domain Context**: Business logic patterns and domain-specific terminology

## Related Prompts

**Prerequisites**: #context_intake - Understand project purpose and goals  
**Complements**: #orient_code, #clarify_requirements - Deep-dive into specific areas  
**Follows**: #feature_dev, #debug_bug - Apply understanding to actual work

## Examples

**New Team Member**: "Understand the e-commerce platform codebase"
- Map user journey from product browsing to checkout completion
- Identify payment processing, inventory management, and user authentication
- Understand database schema and API endpoint organization
- Learn testing patterns and development workflow

**Legacy System Analysis**: "Orient to inherited financial application"
- Identify core business logic and regulatory compliance patterns
- Map data flow through calculation engines and reporting systems
- Understand security patterns and audit trail implementations
- Document technical debt and modernization opportunities

**Open Source Contribution**: "Navigate large React component library"
- Understand component architecture and prop patterns
- Identify build system, testing approach, and documentation generation
- Learn contribution guidelines and code review processes
- Map example applications and usage patterns
