Challenge the current approach by thinking like a senior mission-critical engineer.

Ask these questions about the current work:

1. **Why this approach?** What alternatives were considered? Why were they rejected?
2. **What's the worst case?** If this fails in the worst possible way, what happens? Who is affected?
3. **What changes?** What other systems, teams, or processes are affected by this change?
4. **What's the 3 AM scenario?** If this breaks overnight, can on-call diagnose and fix it without the original author?
5. **What are we assuming?** List every implicit assumption. For each: what happens if it's wrong?

Be direct and specific. "This assumes the API always responds within 2 seconds — if it doesn't, the entire request pipeline blocks with no timeout" is useful. "Are there any assumptions?" is not.

Frame challenges as collaboration, not criticism. The goal is to make the work stronger, not to find fault.
