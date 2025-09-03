# Task Routing and Classification

**Tags**: #route_task #classification  
**Purpose**: Analyze incoming work requests and route them to appropriate workflow prompts  
**Configurable**: Yes - Task categories, routing rules, and escalation patterns

## Quick Usage

```
Use #route_task to classify and route [work request or problem description]
```

## Full Prompt

Analyze and classify incoming work to determine the most appropriate handling approach:

**1. Request Analysis**
- Parse the work request to understand core objective and scope
- Identify key stakeholders, urgency, and business impact
- Extract technical context, constraints, and dependencies
- Note any specific requirements or compliance needs

**2. Work Type Classification**
Apply classification framework to categorize the work:

**Main Task Categories:**
- **#feature_dev** - New functionality implementation
- **#debug_bug** - Issue investigation and resolution  
- **#quick_fix** - Small, low-risk changes
- **#refactor** - Code quality improvements without functionality changes
- **#product_strategy** - Planning, prioritization, and roadmap decisions
- **#support_triage** - User feedback and issue processing
- **#security_privacy** - Security vulnerability or privacy compliance
- **#incident_resp** - Production incident or system failure
- **#perf_opt** - Performance analysis and optimization
- **#docs_knowledge** - Documentation creation or updates

**3. Complexity and Priority Assessment**
- Evaluate scope: Simple building block vs. complex workflow
- Assess urgency: Critical incident vs. planned improvement
- Determine expertise required: Specialized skills vs. general development
- Consider coordination needs: Individual work vs. team effort

**4. Routing Decision**
- Select primary prompt category based on work type
- Identify prerequisite building blocks (e.g., #context_intake)
- Suggest composition pattern for complex work
- Note any special handling requirements

**5. Escalation Rules**
- Identify work requiring management approval or broader coordination
- Flag security, compliance, or high-risk changes
- Note cross-team dependencies or external stakeholder involvement
- Suggest timeline and resource allocation considerations

Project-specific routing rules: See prompts_config/routing_rules.md  
Task category definitions: See prompts/prompt_network.md

## Configuration Points

- **Routing Rules**: Project-specific criteria for categorizing different types of work
- **Priority Frameworks**: How urgency and business impact are assessed
- **Escalation Triggers**: What types of work require special approval or coordination
- **Expertise Mapping**: Which team members or skills are needed for different work types
- **Tool Integration**: How routing decisions integrate with project management tools

## Related Prompts

**Prerequisites**: None - This is typically the first step in work processing  
**Complements**: All main task category prompts - Routes to appropriate workflows  
**Follows**: Specific task prompts based on routing decision

## Examples

**Bug Report**: "Users can't complete checkout on mobile devices"
- Classification: #debug_bug (critical user-facing issue)
- Priority: High (affects revenue and user experience)
- Routing: Apply #context_intake → #create_repro → #debug_bug workflow
- Escalation: Notify product and business teams due to revenue impact

**Feature Request**: "Add social media sharing to product pages"
- Classification: #feature_dev (new functionality)
- Priority: Medium (enhancement, not critical path)
- Routing: Apply #context_intake → #scope_shaping → #feature_dev workflow
- Coordination: Requires design input and marketing alignment

**Performance Complaint**: "Dashboard loads slowly during peak hours"
- Classification: #perf_opt (performance optimization)
- Priority: High (affects user experience during critical times)
- Routing: Apply #context_intake → #perf_profile → #perf_opt workflow
- Investigation: May require #observability setup for proper analysis
