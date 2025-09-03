# Feature Development

**Tags**: #feature_dev #tdd  
**Purpose**: Implement new features using test-driven development methodology  
**Configurable**: Yes - Technology stack, testing frameworks, and project workflows

## Quick Usage

```
Use #feature_dev to implement [feature description] following TDD principles
```

## Full Prompt

Implement a new feature using test-driven development:

**1. Preparation Phase**
- Apply #context_intake to thoroughly understand requirements and acceptance criteria
- Understand how this feature fits into the overall system architecture
- Apply #test_plan to design comprehensive test coverage strategy
- Consider whether to first apply #refactor to make implementation easier
- Identify integration points with existing functionality and potential conflicts

**2. TDD Implementation Cycle**
- **🔴 RED**: Write a failing test that describes desired behavior
- **🟢 GREEN**: Write minimal code to make the test pass
- **🔵 REFACTOR**: Improve code quality while keeping tests green
- Repeat for each aspect of the feature

**3. Feature Completion**
- Apply #run_all_tests to ensure all user journeys work end-to-end
- Add comprehensive error handling and edge cases using #write_tests
- Verify feature meets original requirements from #context_intake phase
- Apply #doc_update to update relevant documentation

**4. Integration Validation**
- Apply #run_all_tests to check for regressions across entire system
- Manually test feature in realistic application context
- Verify feature works with related functionality and doesn't break existing flows
- Confirm performance meets standards defined in prompts_config/quality_standards.md
- Apply #code_review to ensure code quality before integration

Apply technology-specific patterns from: prompts_config/tech_stack.md  
Follow project quality standards from: prompts_config/quality_standards.md  
Integrate with project workflows from: prompts_config/workflows.md

## Configuration Points

- **Technology Stack**: Framework-specific development patterns
- **Testing Approach**: Testing libraries, assertion patterns, data setup
- **Code Organization**: File structure, naming conventions, architectural patterns  
- **Quality Gates**: Code formatting, linting, compilation standards
- **Documentation**: Where and how to update project documentation

## Related Prompts

**Prerequisites**: #context_intake, #test_plan, #clarify_requirements  
**Complements**: #write_tests, #impl_change, #code_review  
**Follows**: #run_all_tests, #doc_update, #merge_deploy

## Examples

**User Interface Feature**: "Implement user profile editing"
- Plan tests for form validation, data submission, success/error states
- Implement UI components with proper data binding
- Add backend validation and database updates  
- Test complete user journey from click to confirmation

**API Feature**: "Implement search endpoint"
- Design tests for query parsing, filtering, result formatting
- Implement search logic with performance considerations
- Add input validation and error handling  
- Test with realistic data volumes and edge cases

**Background Process**: "Implement data synchronization job"
- Plan tests for data transformation, error recovery, completion status
- Implement job logic with proper error handling
- Add monitoring and observability
- Test with various data scenarios and failure conditions
