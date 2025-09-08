# Test-First Development Planning

**Tags**: #test_plan #tdd  
**Purpose**: Plan comprehensive test coverage for any feature before implementation begins  
**Configurable**: Yes - Testing frameworks, patterns, and standards via prompts_config/

## Quick Usage

```
Use #test_plan to design test coverage for [feature name] before implementation
```

## Full Prompt

Plan comprehensive test coverage following test-driven development principles:

**1. Understand Requirements**
- Identify the core behavior this feature must provide
- List all user interactions and system responses  
- Define success criteria and acceptance conditions
- Note error conditions and edge cases

**2. Design Test Strategy**
- **End-to-End Tests**: Complete user journeys from UI to data layer
- **Integration Tests**: Component interactions and system boundaries  
- **Unit Tests**: Complex business logic and calculations (if needed)
- **Error Cases**: Invalid inputs, system failures, boundary conditions

**3. Test Structure Planning**
- Plan test data requirements and setup
- Identify test dependencies and prerequisites
- Design for test isolation and repeatability
- Ensure tests can run quickly (target: <1 second each)

**4. Coverage Validation**
- Verify all happy paths are covered
- Ensure all sad paths and error conditions are tested
- Check that tests actually prove the feature works
- Confirm tests would fail if feature was broken

Technology-specific testing patterns: See prompts_config/tech_stack.md
Quality standards and expectations: See prompts_config/quality_standards.md

## Configuration Points

- **Testing Framework**: Specific testing libraries and patterns
- **Test Organization**: File structure and naming conventions
- **Data Setup**: Test fixtures, factories, and database handling
- **Assertion Patterns**: Preferred assertion styles and helpers
- **Performance Standards**: Test execution time expectations

## Related Prompts

**Prerequisites**: #context_intake, #clarify_requirements - Understand what to test
**Complements**: #write_tests, #impl_change - Execute the testing plan
**Follows**: #run_all_tests, #debug_bug - Validate and maintain tests

## Examples

**Web Feature**: "Plan tests for user authentication flow"
- End-to-end: Login form submission, session handling, redirects
- Integration: Authentication service, database user lookup  
- Unit: Password validation, token generation
- Error cases: Invalid credentials, expired sessions, network failures

**API Feature**: "Plan tests for payment processing endpoint"  
- Integration: Payment gateway communication, database updates
- Unit: Payment calculation logic, validation rules
- Error cases: Payment failures, network timeouts, invalid data
- Security: Authorization checks, data sanitization
