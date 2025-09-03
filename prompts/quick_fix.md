# Quick Fix Implementation

**Tags**: #quick_fix #maintenance  
**Purpose**: Implement small, low-risk changes with fast validation and minimal overhead  
**Configurable**: Yes - Change approval processes, testing requirements, and risk thresholds

## Quick Usage

```
Use #quick_fix to implement [small change description] with appropriate validation
```

## Full Prompt

Implement small changes efficiently while maintaining quality and safety:

**1. Change Scope Validation**
- Apply #context_intake to understand the complete scope and impact
- Verify the change is truly small and low-risk
- Identify all affected systems, users, and processes
- Confirm change aligns with existing architecture and patterns

**2. Risk Assessment**
- Evaluate potential impact on existing functionality
- Identify rollback procedures if change causes issues
- Consider timing and coordination with other changes
- Assess need for coordination with stakeholders

**3. Minimal Testing Strategy**
- Apply #write_tests for any new logic or behavior changes
- Apply #run_all_tests to ensure no regressions introduced  
- Test the specific change in realistic scenarios
- Validate change works as intended in target environment

**4. Implementation and Validation**
- Apply #impl_change to make targeted modifications
- Keep changes focused and avoid scope creep
- Document the change rationale and approach
- Verify change meets original requirements

**5. Deployment and Monitoring**
- Apply #merge_deploy following fast-track approval if appropriate
- Apply #post_deploy_checks to validate change in production
- Apply #monitoring_watch for any unexpected impacts
- Have rollback plan ready if issues arise

Change approval workflows: See prompts_config/workflows.md  
Technology-specific quick change patterns: See prompts_config/tech_stack.md

## Configuration Points

- **Risk Thresholds**: What constitutes a "quick fix" vs. requiring full development process
- **Approval Processes**: Fast-track approval workflows for low-risk changes
- **Testing Requirements**: Minimum testing standards for different types of changes
- **Deployment Patterns**: How quick fixes are deployed and monitored
- **Documentation**: What documentation is required for small changes

## Related Prompts

**Prerequisites**: #context_intake - Understand change requirements and impact  
**Complements**: #impl_change, #run_all_tests - Execute change with quality safeguards  
**Follows**: #post_deploy_checks, #monitoring_watch - Validate change in production

## Examples

**Configuration Change**: "Update API rate limits for premium users"
- Verify current rate limiting configuration and impact
- Test new limits with realistic user scenarios
- Deploy with monitoring for rate limit violations
- Document change and rationale for future reference

**Copy/Content Fix**: "Update error message text for better user clarity"
- Review current error message and user feedback
- Test new message in various error scenarios
- Validate message displays correctly across different devices
- Monitor for reduced support requests after change

**Bug Hotfix**: "Fix calculation error in tax computation"
- Create focused test case that reproduces the calculation error
- Implement minimal fix that addresses root cause
- Validate fix with edge cases and boundary conditions
- Deploy with careful monitoring of financial calculations
