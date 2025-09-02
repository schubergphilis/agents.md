# Code Review

**Tags**: #code_review #quality  
**Purpose**: Systematically review code changes for quality, security, and maintainability  
**Configurable**: Yes - Review checklists, approval workflows, and quality standards

## Quick Usage

```
Use #code_review to evaluate [code changes/pull request/commit] for quality and compliance
```

## Full Prompt

Conduct thorough code review to ensure quality, security, and maintainability:

**1. Change Overview and Context**
- Understand the purpose and scope of the code changes
- Review related requirements, specifications, or issue descriptions
- Identify the type of change: feature, bug fix, refactoring, or maintenance
- Assess change complexity and potential system impact

**2. Functional Review**
- Verify code changes achieve the intended functionality
- Check that business logic correctly implements requirements
- Validate error handling covers expected failure scenarios
- Ensure edge cases and boundary conditions are properly addressed

**3. Technical Quality Assessment**
- Review code structure, organization, and readability
- Check adherence to established coding patterns and conventions
- Assess performance implications and resource usage
- Verify proper use of framework patterns and best practices

**4. Test Coverage Validation**
- Apply #run_all_tests to ensure all tests pass with changes
- Review test quality and coverage for new or modified code
- Verify tests actually validate the intended functionality
- Check for missing test scenarios or insufficient coverage

**5. Security and Compliance Review**
- Identify potential security vulnerabilities or data exposure risks
- Check input validation and sanitization practices
- Verify proper authentication and authorization handling
- Assess compliance with security guidelines and standards

**6. Documentation and Maintainability**
- Check that complex logic includes appropriate comments and documentation
- Verify API documentation and code comments are accurate and helpful
- Assess code maintainability and future extensibility
- Ensure changes align with architectural decisions and patterns

Technology-specific review criteria: See prompts_config/tech_stack.md  
Quality standards and checklists: See prompts_config/quality_standards.md

## Configuration Points

- **Review Checklists**: Technology and domain-specific items to check during review
- **Quality Standards**: Coding conventions, performance requirements, and security guidelines
- **Approval Workflows**: Who needs to approve different types of changes
- **Tool Integration**: How code review tools integrate with development workflow
- **Documentation Requirements**: What documentation updates are required for changes

## Related Prompts

**Prerequisites**: #impl_change, #write_tests - Code and tests exist to review  
**Complements**: #run_all_tests, #security_review - Validate functionality and security  
**Follows**: #merge_deploy, #doc_update - Approved changes ready for integration

## Examples

**Feature Implementation Review**: "Review new user authentication system"
- Verify authentication flow matches security requirements
- Check password handling and session management practices
- Review test coverage for authentication success and failure scenarios
- Validate integration with existing authorization system

**Bug Fix Review**: "Review fix for payment calculation error"
- Verify fix addresses root cause identified in bug analysis
- Check that fix doesn't introduce regressions in related functionality
- Review test coverage for the specific bug scenario and related edge cases
- Validate fix maintains existing performance characteristics

**Refactoring Review**: "Review code organization improvements"
- Verify refactoring maintains existing functionality without behavior changes
- Check that all tests still pass and cover refactored code paths
- Review improved code structure for readability and maintainability
- Ensure refactoring follows established architectural patterns
