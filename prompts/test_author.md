# Test Authoring and Coverage

**Tags**: #test_author #quality  
**Purpose**: Create comprehensive test coverage and improve testing strategy for system reliability  
**Configurable**: Yes - Testing frameworks, coverage standards, and quality requirements

## Quick Usage

```
Use #test_author to create comprehensive test coverage for [system/feature/component]
```

## Full Prompt

Design and implement comprehensive test coverage to ensure system reliability and quality:

**1. Test Strategy Design**
- Apply #context_intake to understand system requirements and user expectations
- Apply #test_plan to design comprehensive coverage across all functionality layers
- Identify critical user journeys and business logic that must be tested
- Assess current test coverage gaps and areas needing improvement

**2. Test Suite Architecture**
- Design test organization that mirrors system architecture
- Plan test data management, setup, and teardown procedures
- Establish test categorization: unit, integration, end-to-end, performance
- Create reusable test utilities and helper functions

**3. Comprehensive Test Implementation**
- Apply #write_tests to create tests covering all identified scenarios
- Focus on end-to-end user journey tests as primary validation
- Add integration tests for system boundaries and external dependencies
- Include unit tests for complex business logic and edge cases

**4. Test Quality and Maintainability**
- Ensure tests are readable and serve as documentation of system behavior
- Design tests for reliability and fast execution (target <1 second per test)
- Create realistic test data that reflects production usage patterns
- Implement test isolation to avoid dependencies between tests

**5. Coverage Validation and Improvement**
- Apply #run_all_tests to validate comprehensive test execution
- Measure test coverage and identify gaps in critical functionality
- Address flaky or unreliable tests that reduce confidence
- Continuously improve test performance and maintainability

Testing framework patterns: See prompts_config/tech_stack.md  
Coverage standards and quality requirements: See prompts_config/quality_standards.md

## Configuration Points

- **Testing Framework**: Language and platform-specific testing tools and patterns
- **Coverage Standards**: Required coverage percentages and quality metrics
- **Test Organization**: File structure, naming conventions, and categorization
- **Data Management**: Test fixtures, factories, and database management approaches  
- **Performance Requirements**: Test execution speed and reliability standards

## Related Prompts

**Prerequisites**: #context_intake, #test_plan - Understand requirements and design strategy  
**Complements**: #write_tests, #run_all_tests - Execute testing strategy  
**Follows**: #impl_change, #code_review - Validate implementation through comprehensive testing

## Examples

**New Feature Testing**: "Create comprehensive test coverage for user authentication system"
- Design tests covering registration, login, logout, and session management
- Test password requirements, account lockout, and security features
- Create tests for integration with existing authorization system
- Include performance tests for authentication under load

**Legacy System Testing**: "Add test coverage to existing payment processing system"
- Identify critical payment workflows and business rules to test
- Create tests that validate existing behavior before making changes
- Add integration tests for payment gateway interactions
- Implement regression tests for known issues and edge cases

**API Testing Strategy**: "Comprehensive testing for REST API endpoints"
- Create contract tests validating request/response formats
- Test authentication, authorization, and input validation
- Add integration tests for database operations and business logic
- Include performance and load testing for critical endpoints
