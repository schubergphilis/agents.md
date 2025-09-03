# Context Intake

**Tags**: #context_intake #analysis  
**Purpose**: Systematically gather and understand all relevant context before starting work  
**Configurable**: Yes - Information sources and analysis approaches

## Quick Usage

```
Use #context_intake to thoroughly understand [task/problem/requirement] before proceeding
```

## Full Prompt

Systematically gather and analyze all relevant context:

**1. Problem/Task Understanding**
- Read and understand the complete request or problem statement
- Identify the core objective and expected outcomes
- Note any constraints, deadlines, or special requirements
- Clarify ambiguous requirements or assumptions

**2. Current State Analysis**
- Assess existing system state and relevant functionality
- Review recent changes that might affect the work
- Understand dependencies and integration points
- Document what currently works vs. what needs change

**3. Stakeholder Context**
- Identify who is affected by this work (users, team members, systems)
- Understand user needs and business requirements
- Consider impact on different user types and use cases
- Gather relevant feedback or input from stakeholders

**4. Technical Context**
- Review relevant code, documentation, and system architecture
- Understand technology stack and framework patterns
- Identify technical constraints and opportunities
- Consider performance, security, and scalability implications

**5. Success Criteria Definition**
- Define clear, measurable success criteria
- Identify what "done" looks like for this work
- Plan how progress and completion will be validated
- Consider both immediate and longer-term success measures

Project-specific information sources: See prompts_config/project_context.md  
Technical context sources: See prompts_config/tech_stack.md

## Configuration Points

- **Information Sources**: Where to find requirements, specifications, and system documentation
- **Stakeholder Communication**: How to gather input from users, product owners, and team members
- **System Analysis**: Tools and approaches for understanding current system state
- **Requirements Format**: How to document and validate understanding of requirements
- **Context Documentation**: How to record and share context for future reference

## Related Prompts

**Prerequisites**: None - This is typically the first step in any workflow  
**Complements**: #clarify_requirements - When requirements need further elaboration  
**Follows**: #test_plan, #feature_dev, #debug_bug - Inform all subsequent work

## Examples

**New Feature Request**: "Add user notification preferences"
- Understand what types of notifications exist and are planned
- Review current user management and settings functionality  
- Identify user experience expectations and business requirements
- Consider technical implementation approaches and constraints

**Bug Report**: "Users report checkout process failing intermittently"
- Gather detailed bug reports and reproduction scenarios
- Analyze current checkout flow and recent changes
- Review error logs and monitoring data
- Understand business impact and user experience effects

**Performance Issue**: "Dashboard loading slowly for some users"
- Understand which users are affected and under what conditions
- Review dashboard implementation and data sources
- Analyze performance monitoring data and user feedback
- Consider acceptable performance thresholds and user expectations
