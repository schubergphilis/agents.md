# Create Bug Reproduction Case

**Tags**: #create_repro #debugging  
**Purpose**: Create minimal, reliable test case that demonstrates a bug or issue  
**Configurable**: Yes - Testing frameworks and debugging approaches

## Quick Usage

```
Use #create_repro to create a failing test that demonstrates [bug description]
```

## Full Prompt

Create a minimal reproduction case that reliably demonstrates the issue:

**1. Issue Analysis**
- Understand the exact symptoms and when they occur
- Identify the minimal conditions needed to trigger the bug
- Note environmental factors (browser, device, data state, etc.)
- Determine what "success" would look like vs. current "failure"

**2. Test Case Design**
- Write a test that reproduces the exact user scenario
- Use minimal data and setup required to trigger the issue  
- Make test deterministic and reliable (runs consistently)
- Ensure test fails in the current buggy state

**3. Reproduction Validation**
- Run the test multiple times to confirm it fails consistently
- Test in different environments to verify it's not environment-specific
- Document exact conditions and steps in the test
- Verify that the test actually demonstrates the reported issue

**4. Test Documentation**
- Add clear test description explaining what should happen vs. what does happen
- Include comments about the expected behavior
- Note any specific setup or data requirements
- Mark test appropriately (e.g., `@tag :bug_repro` or similar)

**5. Debugging Readiness**
- Ensure test provides enough information to guide debugging
- Verify test isolates the issue from other functionality
- Check that test will pass once bug is fixed
- Consider adding assertions for related functionality that should remain working

Testing framework patterns: See prompts_config/tech_stack.md  
Bug tracking workflows: See prompts_config/workflows.md

## Configuration Points

- **Testing Framework**: Language and framework-specific test structure
- **Test Organization**: Where to put reproduction tests and how to tag them
- **Data Setup**: How to create minimal test data for reproduction
- **Assertions**: Preferred assertion patterns and failure messages
- **Environment**: How to ensure consistent test environment

## Related Prompts

**Prerequisites**: #context_intake - Understand the bug thoroughly first  
**Complements**: #isolate_cause, #debug_bug - Use repro to guide debugging  
**Follows**: #write_tests - Convert repro into proper regression test after fix

## Examples

**UI Interaction Bug**: "Form doesn't submit when validation fails"
- Create test that fills form with invalid data
- Attempt form submission and verify it fails appropriately  
- Check that error messages are displayed correctly
- Ensure form state is preserved for user correction

**Data Processing Bug**: "Calculation wrong for negative numbers"
- Create test with specific negative number inputs
- Call calculation function with those inputs
- Assert expected result vs. actual (incorrect) result
- Document what the correct calculation should be

**API Integration Bug**: "Third-party service call fails intermittently"  
- Mock the third-party service to simulate failure conditions
- Create test that reproduces the specific failure scenario
- Verify error handling behaves as expected
- Check that system recovers gracefully from the failure
