Analyze the blast radius and risk profile of the current change.

For the change being made, assess:

## Blast radius
- What systems are directly affected?
- What systems are indirectly affected (downstream consumers, shared resources)?
- How many users/customers are in the impact zone?
- Is the impact zone bounded or could it cascade?

## Rollback path
- Can this change be rolled back? How?
- How long does rollback take?
- Is there data loss or state corruption risk during rollback?
- Has the rollback been tested or is it theoretical?

## Risk level
Rate as LOW / MEDIUM / HIGH / CRITICAL based on:
- LOW: Local change, easy rollback, no production impact
- MEDIUM: Affects shared systems, rollback possible but not instant
- HIGH: Production-facing, rollback complex, customer-visible if wrong
- CRITICAL: Data loss possible, multi-system impact, regulatory implications

## Recommendation
Based on the risk level, recommend:
- What additional review or testing is needed before proceeding
- What monitoring should be in place during and after the change
- What the rollback trigger should be (what metric or signal means "roll back now")
