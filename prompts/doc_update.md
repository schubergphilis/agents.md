# Documentation Update

**Tags**: #doc_update #maintenance  
**Purpose**: Update project documentation to reflect current system state and changes  
**Configurable**: Yes - Documentation standards, update triggers, and maintenance workflows

## Quick Usage

```
Use #doc_update to update documentation for [specific change or area]
```

## Full Prompt

Update documentation systematically to maintain accuracy and usefulness:

**1. Documentation Scope Assessment**
- Identify which documentation is affected by recent changes
- Review current documentation accuracy and completeness
- Determine documentation audience and usage patterns
- Assess urgency of updates based on user impact

**2. Content Review and Analysis**
- Compare current documentation against actual system state
- Identify outdated information, broken links, and missing content
- Review user feedback and questions indicating documentation gaps
- Validate examples, code samples, and procedure accuracy

**3. Update Strategy**
- Prioritize updates by user impact and documentation importance
- Plan content organization and structure improvements
- Consider documentation format and accessibility requirements
- Coordinate updates across related documentation sections

**4. Content Updates**
- Update technical specifications, API documentation, and feature descriptions
- Refresh installation guides, configuration instructions, and troubleshooting sections
- Update examples, code samples, and walkthrough tutorials
- Revise architectural diagrams and system overview documentation

**5. Quality Assurance**
- Review updates for accuracy, clarity, and completeness
- Test procedures, code examples, and configuration instructions
- Ensure consistent tone, style, and formatting across documentation
- Validate documentation works for intended audience skill levels

Documentation standards and templates: See prompts_config/documentation.md  
Content review and maintenance workflows: See prompts_config/workflows.md

## Configuration Points

- **Documentation Standards**: Style guides, formatting rules, and content templates
- **Update Triggers**: When documentation updates are required (code changes, feature releases)
- **Review Processes**: How documentation changes are reviewed and approved
- **Publication Workflows**: How updated documentation is deployed and distributed
- **Maintenance Schedule**: Regular review and update cycles for documentation

## Related Prompts

**Prerequisites**: #impl_change, #feature_dev - Changes that trigger documentation needs  
**Complements**: #backlog_update, #stakeholder_update - Coordinate related communication  
**Follows**: #governance_gates - Ensure documentation meets quality standards

## Examples

**Feature Release**: "Update API documentation for new authentication endpoints"
- Document new endpoint specifications, request/response formats
- Update authentication flow diagrams and integration examples
- Revise SDK documentation and code samples
- Test all examples and ensure they work with current API version

**Architecture Change**: "Update system architecture documentation after microservices migration"
- Revise high-level architecture diagrams and service boundaries
- Update deployment guides and infrastructure requirements
- Document new inter-service communication patterns and APIs
- Update troubleshooting guides for distributed system issues

**Process Change**: "Update development workflow documentation after CI/CD improvements"
- Revise developer onboarding and setup instructions
- Update code review and deployment process documentation
- Document new automated testing and quality gate procedures
- Update troubleshooting guides for build and deployment issues
