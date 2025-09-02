# Run All Tests

**Tags**: #run_all_tests #validation  
**Purpose**: Execute comprehensive test suite and validate all functionality works correctly  
**Configurable**: Yes - Test commands, frameworks, and reporting preferences

## Quick Usage

```
Use #run_all_tests to validate all functionality works after changes
```

## Full Prompt

Execute comprehensive test suite to ensure system integrity:

**1. Pre-Test Setup**
- Ensure test environment is clean and properly configured
- Reset test database and clear any cached state
- Verify all test dependencies are available
- Check that no other processes are interfering

**2. Test Execution**
- Run complete test suite using project's standard test command
- Monitor test execution for failures, errors, or timeouts
- Capture test output and any error messages
- Note execution time and performance characteristics

**3. Result Analysis** 
- Review all test failures and errors in detail
- Identify patterns in failures (specific modules, types of tests)
- Distinguish between genuine failures and flaky tests
- Check if failures are related to recent changes

**4. Failure Resolution**
- For each failing test, understand what behavior it validates
- Apply #debug_bug methodology to investigate root causes
- Fix underlying issues rather than just making tests pass
- Re-run specific tests to verify fixes work

**5. Quality Validation**
- Ensure test suite completes within reasonable time
- Verify test coverage meets project standards
- Check that tests actually validate intended functionality
- Confirm no warnings or deprecation notices

Test execution commands: See prompts_config/tech_stack.md  
Quality standards and thresholds: See prompts_config/quality_standards.md

## Configuration Points

- **Test Commands**: Framework-specific commands for running tests
- **Test Categories**: How to run different types of tests (unit, integration, e2e)
- **Reporting**: Test result formatting and where results are stored
- **Performance**: Expected test execution time and timeout settings
- **Coverage**: How to measure and report test coverage

## Related Prompts

**Prerequisites**: #write_tests - Tests must exist to run them  
**Complements**: #debug_bug - When tests fail unexpectedly  
**Follows**: #code_review, #merge_deploy - Validate before code integration

## Examples

**After Code Changes**: "Validate that new authentication feature doesn't break existing functionality"
- Run full test suite to check for regressions
- Pay attention to authentication-related and user management tests
- Verify performance hasn't degraded significantly

**Before Deployment**: "Ensure system is ready for production release"  
- Execute complete test suite including integration tests
- Verify all quality gates pass (formatting, linting, compilation)
- Check test coverage meets deployment requirements

**Debugging Session**: "Understand current system state after bug investigation"
- Run tests to establish baseline of what currently works
- Identify which specific functionality is broken
- Use test results to guide debugging priorities
