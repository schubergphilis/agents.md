# Write Tests

**Tags**: #write_tests #tdd  
**Purpose**: Create comprehensive test coverage for functionality using test-driven development principles  
**Configurable**: Yes - Testing frameworks, patterns, and organization

## Quick Usage

```
Use #write_tests to create comprehensive test coverage for [functionality description]
```

## Full Prompt

Write comprehensive tests that prove functionality works correctly:

**1. Test Design from Requirements**
- Start with clear understanding of what behavior needs to be validated
- Apply #test_plan approach to identify all scenarios to cover
- Design tests that read like specifications and user stories
- Plan both positive (happy path) and negative (error) test cases

**2. Test-Driven Development Cycle**
- **Red**: Write failing test that describes desired behavior first
- Write test assertions for expected outcomes and side effects
- Run test to confirm it fails appropriately (not due to syntax errors)
- Ensure test failure message clearly indicates what's missing

**3. Test Implementation**
- Use appropriate testing framework patterns and conventions
- Create minimal test data needed to exercise functionality
- Write clear, descriptive test names that explain the scenario
- Organize tests logically with setup, action, and assertion sections

**4. Comprehensive Coverage**
- **Happy Paths**: All successful user workflows and use cases
- **Edge Cases**: Boundary conditions and unusual but valid inputs
- **Error Cases**: Invalid inputs, system failures, and exceptional conditions  
- **Integration**: How functionality works with related system components

**5. Test Quality Validation**
- Ensure tests actually prove the intended functionality works
- Verify tests would fail if functionality were broken or missing
- Check tests run quickly (target <1 second each) and reliably
- Review test readability and maintainability

Testing framework specifics: See prompts_config/tech_stack.md  
Test organization patterns: See prompts_config/quality_standards.md

## Configuration Points

- **Testing Framework**: Language and platform-specific testing libraries
- **Test Organization**: File structure, naming conventions, and test grouping  
- **Data Setup**: Test fixtures, factories, and database management
- **Assertions**: Preferred assertion patterns and error messages
- **Test Categories**: How to organize unit, integration, and end-to-end tests

## Related Prompts

**Prerequisites**: #test_plan - Design comprehensive test strategy first  
**Complements**: #impl_change, #debug_bug - Tests guide implementation and debugging  
**Follows**: #run_all_tests, #code_review - Validate and review test quality

## Examples

**User Authentication Feature**: "Test user login functionality"
- Happy path: Valid credentials result in successful login and session creation
- Error cases: Invalid email, wrong password, account lockout scenarios
- Edge cases: Empty fields, SQL injection attempts, concurrent login attempts
- Integration: Login redirects, session persistence, logout functionality

**API Endpoint**: "Test order creation endpoint"  
- Happy path: Valid order data creates order and returns confirmation
- Validation: Required fields, data format validation, business rule checks
- Error handling: Payment failures, inventory issues, server errors
- Security: Authorization checks, data sanitization, rate limiting

**Background Job**: "Test email notification job"
- Happy path: Job processes successfully and sends email  
- Error cases: Invalid email addresses, service outages, template errors
- Retry logic: Failed jobs are retried appropriately with backoff
- Monitoring: Job completion and failure tracking works correctly
