Explain the code, infrastructure, or pattern I'm pointing at.

Before explaining, ask yourself: what does this person need to understand and why?

## How to explain

1. **Start with purpose** — what does this do and why does it exist? One sentence.
2. **Show the flow** — trace how data or requests move through it. Name the entry point and the exit.
3. **Name the patterns** — if it uses known patterns (circuit breaker, saga, pub/sub, decorator), name them and explain why they were chosen here.
4. **Call out the non-obvious** — what would surprise someone reading this for the first time? Hidden dependencies, implicit ordering, magic values, historical decisions.
5. **Flag the risks** — what breaks if you change this wrong? What's fragile? What's the blast radius?

## Rules

- Teach, don't just describe. "This uses a circuit breaker because the downstream API is flaky — without it, one slow response blocks all requests for 30 seconds" is useful. "This is a circuit breaker" is not.
- Scale depth to complexity. A simple utility gets a one-paragraph explanation. A distributed workflow gets the full treatment.
- If you're not sure about something, say so. "This likely exists because X, but check with the team" is honest.
