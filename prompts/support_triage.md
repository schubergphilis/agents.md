# Support Triage and Issue Processing

**Tags**: #support_triage #customer_support  
**Purpose**: Systematically process user feedback, bug reports, and support requests  
**Configurable**: Yes - Support workflows, escalation rules, and communication templates

## Quick Usage

```
Use #support_triage to process and prioritize [user feedback/bug report/support request]
```

## Full Prompt

Process user feedback and support requests systematically to ensure appropriate response and resolution:

**1. Initial Intake and Classification**
- Apply #context_intake to understand the complete issue scope and impact
- Classify issue type: bug report, feature request, user confusion, or system issue
- Assess severity: critical (system down), high (major functionality affected), medium (minor issues), low (enhancements)
- Identify affected user segments and potential business impact

**2. Issue Reproduction and Validation**
- Apply #create_repro to reproduce reported issues in controlled environment
- Validate issue exists and gather additional technical context
- Document reproduction steps and environmental factors
- Confirm issue affects other users or is isolated incident

**3. Impact Assessment and Prioritization**
- Evaluate number of users affected and frequency of occurrence
- Assess business impact: revenue effects, user experience degradation, operational costs
- Consider timing factors: peak usage periods, upcoming releases, external deadlines
- Apply project-specific prioritization criteria and escalation rules

**4. Solution Pathway Determination**
- For bugs: Apply #debug_bug workflow for systematic investigation and resolution
- For feature requests: Apply #product_strategy to evaluate against roadmap priorities
- For user confusion: Apply #docs_knowledge to improve documentation or user guidance
- For quick fixes: Apply #quick_fix for rapid resolution of simple issues

**5. Communication and Follow-up**
- Apply #stakeholder_update to communicate status to affected users and internal teams
- Document issue in appropriate tracking system with clear status and timeline
- Schedule follow-up communications and progress reviews
- Close loop with original reporter once issue is resolved

Customer communication templates: See prompts_config/support_templates.md  
Escalation rules and SLA definitions: See prompts_config/support_workflows.md

## Configuration Points

- **Support Channels**: Where user feedback is collected and how it's processed
- **Classification Rules**: Criteria for categorizing different types of issues  
- **Severity Definitions**: How to assess impact and urgency of different issues
- **Escalation Procedures**: When and how to escalate issues to different teams
- **Communication Standards**: How to respond to users and maintain ongoing communication

## Related Prompts

**Prerequisites**: #context_intake - Understand issue completely before processing  
**Complements**: #debug_bug, #feature_dev, #quick_fix - Route to appropriate resolution workflow  
**Follows**: #stakeholder_update, #doc_update - Communicate resolution and prevent recurrence

## Examples

**Critical Bug Report**: "Payment processing is failing for all users"
- Immediate escalation to incident response team
- Apply #incident_resp workflow for system-wide issue
- Coordinate with business team on customer communication
- Apply #debug_bug for urgent root cause analysis and fix

**Feature Request**: "Can we add bulk export functionality to the dashboard?"
- Apply #product_strategy to evaluate against current roadmap
- Assess user demand and business value of proposed feature
- Coordinate with product team for prioritization decision
- Communicate timeline and decision back to requesting user

**User Confusion**: "I can't find how to update my payment method"
- Apply #create_repro to walk through user experience
- Identify UX issues or missing documentation
- Apply #docs_knowledge to improve help documentation
- Consider #quick_fix for immediate UX improvements if needed
