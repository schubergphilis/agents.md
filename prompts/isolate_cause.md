# Isolate Root Cause

**Tags**: #isolate_cause #debugging  
**Purpose**: Systematically narrow down the source of a problem through elimination and investigation  
**Configurable**: Yes - Debugging tools and investigation approaches

## Quick Usage

```
Use #isolate_cause to systematically identify the root source of [problem description]
```

## Full Prompt

Apply systematic elimination to identify the root cause of an issue:

**1. Problem Boundaries**
- Define what is working vs. what is broken
- Identify when the problem started occurring  
- Note environmental factors (version, configuration, data, timing)
- Determine scope of impact (all users, specific conditions, intermittent)

**2. Hypothesis Formation**  
- List potential causes based on symptoms and recent changes
- Prioritize hypotheses by likelihood and ease of testing
- Consider both obvious causes and systemic issues
- Account for timing, dependencies, and environmental factors

**3. Systematic Elimination**
- Test each hypothesis independently with controlled experiments
- Change one variable at a time to isolate effects
- Use binary search approach: divide problem space in half repeatedly
- Document what each test rules in or out

**4. Evidence Gathering**
- Collect relevant logs, error messages, and system state
- Compare working vs. non-working scenarios in detail  
- Look for patterns in failures (timing, data, conditions)
- Use appropriate debugging tools for your technology stack

**5. Root Cause Validation**  
- Verify the identified cause can explain all observed symptoms
- Test that fixing this cause resolves the original problem
- Ensure the cause is truly root (not just a symptom of something deeper)
- Consider why this cause wasn't caught earlier and how to prevent similar issues

Technology-specific debugging approaches: See prompts_config/tech_stack.md

## Configuration Points

- **Debugging Tools**: Platform-specific tools for investigation and analysis
- **Logging Systems**: How to access and analyze system logs and traces
- **Monitoring Data**: Available metrics and observability information
- **Testing Environment**: How to safely reproduce and test hypotheses
- **Documentation**: How to record investigation process and findings

## Related Prompts

**Prerequisites**: #create_repro - Have a reliable way to reproduce the issue  
**Complements**: #debug_bug, #instrumentation - Part of comprehensive debugging  
**Follows**: #write_tests, #impl_change - Implement fix based on findings

## Examples

**Performance Degradation**: "API responses became slow after deployment"
- Compare response times before/after deployment
- Test with different data sizes and user loads  
- Examine database query performance and resource usage
- Isolate specific endpoints or operations causing slowdown

**Intermittent Failures**: "Feature works sometimes but fails randomly"  
- Identify conditions that correlate with failures vs. successes
- Test for race conditions, timing issues, or resource contention
- Examine error patterns and frequency statistics
- Isolate specific user patterns or data conditions

**Integration Issues**: "Third-party service integration stopped working"
- Test service independently outside of application context
- Verify API credentials, endpoints, and request format  
- Check for service version changes or deprecated endpoints
- Isolate network, authentication, or data format issues
