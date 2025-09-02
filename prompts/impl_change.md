# Implementation Change

**Tags**: #impl_change #coding  
**Purpose**: Make targeted code changes while maintaining quality and system integrity  
**Configurable**: Yes - Programming languages, frameworks, and coding standards

## Quick Usage

```
Use #impl_change to implement [specific change description] with proper quality safeguards
```

## Full Prompt

Implement code changes systematically while maintaining system quality:

**1. Change Planning**
- Understand exactly what behavior change is needed
- Identify all code locations that require modification
- Plan the sequence of changes to maintain working state
- Consider impact on existing functionality and tests

**2. Safe Implementation Approach**
- Start with smallest change that moves toward the goal
- Make incremental changes that can be validated independently  
- Keep the system in a working state at each step
- Apply #run_all_tests frequently to catch regressions early

**3. Code Quality Standards**
- Follow established patterns and conventions for the codebase
- Write clear, readable code with meaningful names and structure
- Add appropriate comments for non-obvious logic or decisions
- Ensure new code integrates cleanly with existing architecture

**4. Testing Integration**
- Apply #write_tests to cover new functionality being implemented  
- Update existing tests that are affected by changes
- Verify tests pass after each significant change
- Add edge case coverage for new code paths

**5. Change Validation**
- Verify the implementation achieves the intended behavior
- Test both normal operation and error conditions
- Check performance impact of changes
- Ensure no unintended side effects or regressions

Technology-specific patterns: See prompts_config/tech_stack.md  
Code quality standards: See prompts_config/quality_standards.md

## Configuration Points

- **Programming Languages**: Language-specific idioms and best practices
- **Framework Patterns**: Framework-specific architectural patterns and conventions
- **Code Organization**: File structure, naming conventions, and module organization
- **Quality Tools**: Linting, formatting, and static analysis tool configuration
- **Performance Standards**: Performance requirements and optimization guidelines

## Related Prompts

**Prerequisites**: #test_plan, #write_tests - Have failing tests that guide implementation  
**Complements**: #run_all_tests, #debug_bug - Validate changes and fix issues  
**Follows**: #code_review, #doc_update - Review and document changes

## Examples

**Bug Fix Implementation**: "Fix calculation error in payment processing"
- Identify exact location and cause of the calculation error
- Implement minimal fix that addresses root cause  
- Update tests to cover the error scenario and validate fix
- Verify fix doesn't break other payment processing functionality

**Feature Addition**: "Add user profile photo upload capability"  
- Implement file upload handling with appropriate validation
- Add database schema changes for storing photo references
- Create UI components for photo upload and display
- Test various file types, sizes, and error conditions

**Refactoring**: "Extract common validation logic into reusable module"
- Identify all locations using similar validation patterns
- Create new module with generic validation functions
- Replace duplicated logic with calls to new module
- Ensure all existing functionality continues to work correctly
