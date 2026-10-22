---
name: decisiones-tecnicas
description: "Review the technical decisions of a session and show which one would have been best, with architecture first."
disable-model-invocation: true
---

The user wants a **decision retro**: for each technical decision in the session, what was chosen, what the best choice was, and why. The goal is judgement the user can reuse, so explain in the user's language.

## Steps

1. Read the session the user names (default: the current one). List every **technical decision**, explicit or implicit, made by the agent or the user: where code or config lives, data shape, storage, invocation, interfaces, dependencies, error handling, scope.

2. Rank them by **impact**: how much the decision costs to change later and how much it constrains what comes next. **Architecture** decisions rank first (boundaries, coupling, data flow, single source of truth, always-on vs on-demand behavior, mechanical rule vs written instruction). Keep the top 3–5.

3. Judge each one with **foresight**: the best choice given what was known or cheaply checkable at the time. Hindsight that needed information nobody had is a lesson, not a mistake; label it that way.

4. For each decision, write this block:

   - **Decision**: what was decided, by whom, and where (file or message).
   - **Options**: the real alternatives available then, chosen one marked.
   - **Best**: the option you would choose now, or "the chosen one" when it was already best.
   - **Why**: the deciding tradeoff, with evidence from the session or the code.
   - **Now**: keep, change now (with the change), or change later (with the trigger).

5. End with one reusable **principle** per decision that was not already best, one line each.

Every "Best" that differs from the chosen option names the evidence that settles it. When every decision was already best, say so in one line.
