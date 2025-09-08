# Refactoring
Tags: #refactor #code_quality
Purpose: Improve code structure, readability, performance, and maintainability without changing observable behavior
Configurable: Yes - Technology stack, testing frameworks, refactoring patterns, and project workflows

## Quick Usage
```
Use #refactor to improve [target area] without changing behavior
```

## Full Prompt
Refactor existing code safely and systematically while preserving behavior:

1. Preparation and Safety Net
- Apply #context_intake to understand current behavior, constraints, and motivation for refactoring
- Define explicit objectives: readability, modularity, testability, performance bounds, or risk reduction
- Establish a safety net:
  - Apply #run_all_tests to confirm current baseline passes
  - Assess coverage; if inadequate, apply #test_plan and #write_tests to add characterization tests that lock current behavior (inputs, outputs, side effects, error cases)
- Document external contracts and non-functional expectations (public APIs, data formats, SLAs)
- If any behavior change is desired, stop and route to #feature_dev or scope those changes separately with tests

2. Refactoring Strategy
- Map dependencies, seams, and coupling hotspots; identify safe entry points for change
- Choose strategy according to goals:
  - Simplify: extract/inline methods, remove duplication, clarify conditionals, rename for clarity
  - Restructure: move responsibilities, introduce interfaces/ports, modularize, isolate I/O and side effects
  - Stabilize: encapsulate volatile dependencies behind adapters/facades, introduce anti-corruption layers
  - Performance-safe: preserve algorithmic behavior while improving allocation/complexity within defined budgets
- Plan small, reversible steps with clear rollback points; prefer breadth-first improvements over large rewrites
- Consider internal feature flags or toggles for risky internal pivots while keeping external behavior unchanged

3. Iterative Refactor Cycle
- Select a small, coherent change
- Keep tests green at all times:
  - If needed, tighten or add characterization tests before touching code (#write_tests)
  - Apply #impl_change to perform the minimal safe edit
  - Run #run_all_tests frequently; maintain formatting, linting, and build standards per prompts_config/quality_standards.md
- Typical safe edits:
  - Rename symbols, extract/inline methods, extract classes/modules, move code, reduce branching, replace temp with query, introduce parameter objects, break long functions, eliminate dead code
  - Encapsulate collections/state, separate command from query, isolate side effects, consolidate duplicate logic
- After each step:
  - Ensure all tests pass; revert immediately if behavior deviates
  - Commit atomically with descriptive messages
- Repeat until objectives are met, continuously checking against goals and baseline behavior

4. Validation and Integration
- Apply #run_all_tests to validate no regressions across the entire system
- Manually sanity test key user journeys or API flows in a realistic context
- Verify:
  - Public contracts unchanged (routes, payloads, schemas, UI behavior)
  - Non-functional goals met (performance within baseline/budget, memory/latency stable or improved)
  - Concurrency and error-handling paths preserved
  - Observability intact (logs/metrics/traces still meaningful)
- Resolve integration concerns (module boundaries, dependency graphs, build times)
- Apply #code_review to ensure quality, adherence to patterns, and maintainability before integration
- Apply #doc_update to update architectural notes, internal diagrams, and code navigation where structure changed

Apply technology-specific patterns from: prompts_config/tech_stack.md
Follow project quality standards from: prompts_config/quality_standards.md
Integrate with project workflows from: prompts_config/workflows.md

## Configuration Points
- Refactoring Patterns: Preferred catalog of safe edits and architectural moves
- Testing Approach: Characterization test style, isolation level, fixtures, and assertions
- Code Organization: Module boundaries, naming conventions, layering rules
- Safety Gates: Build, lint, format, type checks, and coverage thresholds
- Performance Budgets: Allowed variance and measurement approach for critical paths
- Documentation: What internal docs to update (architecture overviews, ADRs, code maps)

## Related Prompts
Prerequisites: #context_intake, #test_plan, #code_orient
Complements: #write_tests, #impl_change, #code_review
Follows: #run_all_tests, #doc_update, #merge_deploy

## Examples
User Interface Refactor: "Refactor settings page state management"
- Add characterization tests for rendering states, interactions, and accessibility roles
- Extract reusable input components; separate presentation from state and effects
- Remove duplicate validation logic; clarify data flow and naming
- Validate that visual states and interactions remain unchanged

API Refactor: "Extract search logic into service layer"
- Write tests to lock current endpoint behavior (status codes, response schema, pagination, errors)
- Move parsing/filtering/sorting into a dedicated module with unit tests
- Introduce an interface to decouple controllers from persistence
- Confirm identical responses across sample and edge-case queries; check performance budgets

Background Process Refactor: "Simplify data synchronization job"
- Create characterization tests around idempotency, retries, and failure handling
- Break monolithic job into pipeline steps (extract transform, apply, report)
- Isolate external calls behind adapters; centralize error handling and backoff
- Validate identical outputs and side effects across realistic data scenarios and failure modes
