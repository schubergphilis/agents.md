# Bug Debugging Methodology

**Tags**: #debug_bug #troubleshooting  
**Purpose**: Systematically investigate, reproduce, and fix software bugs  
**Configurable**: Yes - Technology stack debugging tools and project-specific workflows

## Quick Usage

```
Use #debug_bug to systematically investigate and fix [bug description]
```

## Full Prompt

Systematically debug and resolve software issues:

**1. Issue Understanding**
- Apply #context_intake to gather complete problem description and business impact
- Identify specific symptoms, error messages, and occurrence patterns
- Collect relevant logs, stack traces, and monitoring data
- Determine scope: affected users, frequency, and business impact severity

**2. Reproduction Strategy**
- Apply #create_repro to create minimal test case that demonstrates the bug
- Document exact steps to reproduce the issue consistently  
- Test reproduction in different environments if needed
- Isolate variables to understand contributing factors

**3. Root Cause Investigation**
- Apply #isolate_cause to narrow down the problem systematically
- Examine relevant code sections and data flows
- Check recent changes that might have introduced the issue
- Use debugging tools appropriate to your technology stack

**4. Solution Implementation**
- Design fix that addresses root cause, not just symptoms
- Apply #write_tests to create regression test that would catch this bug
- Implement minimal change needed to resolve the issue
- Verify fix resolves the problem without introducing new issues

**5. Validation and Prevention**
- Apply #run_all_tests to ensure fix works and no regressions introduced
- Test fix in realistic scenarios with production-like data
- Apply #doc_update to document issue, root cause, and resolution for future reference
- Apply #code_review to validate fix quality and consider similar potential issues
- Update monitoring or alerting to catch similar issues earlier

Use technology-specific debugging tools from: prompts_config/tech_stack.md  
Follow project debugging workflows from: prompts_config/workflows.md

## Configuration Points

- **Debugging Tools**: Language and framework-specific debugging utilities
- **Log Analysis**: How to access and interpret application logs  
- **Environment Setup**: How to reproduce issues in development/staging
- **Error Tracking**: How to access error monitoring and crash reports
- **Communication**: How to report progress and coordinate with team

## Related Prompts

**Prerequisites**: #context_intake - Understand the bug report thoroughly  
**Complements**: #create_repro, #isolate_cause, #write_tests - Core debugging steps  
**Follows**: #run_all_tests, #code_review, #doc_update - Validate and document fix

## Examples

**User Interface Bug**: "Button doesn't respond on mobile devices"
- Reproduce on different mobile browsers and devices
- Check browser console for JavaScript errors
- Test with different user interaction patterns
- Fix responsive design or event handling issues

**Data Processing Bug**: "Calculation produces wrong results for large numbers"  
- Create test cases with known input/output pairs
- Trace through calculation logic step by step
- Check for overflow, precision, or rounding issues
- Implement fix with proper numeric handling

**Performance Bug**: "Page loads slowly under certain conditions"
- Identify conditions that trigger slow performance
- Profile application to find bottlenecks  
- Analyze database queries, network requests, or computation
- Optimize critical path while maintaining functionality
