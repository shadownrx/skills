---
name: prompt-coach
description: "Rewrite the user's draft prompt before they send it, so the agent gets it right the first time."
disable-model-invocation: true
---

The user passes a **draft prompt** as the argument. They want a better version to send, not the task done. Do not execute the draft.

## Steps

1. Read the draft. When there is no argument, ask for the draft and stop.

2. Fill what you can find yourself before asking: the current repo, branch, open ticket, files and terms from the conversation, and the skills available (e.g. `/fast-pr`, `/example`). A gap you can fill from context goes into the rewrite, not into a question.

3. Check the draft against the criteria below. When it already meets them, say so in one line and stop.

4. Write the result:

   - **Better**: the rewritten prompt in a code block, ready to copy. Keep the user's language and voice. Same length or shorter when possible; add only what closes a gap.
   - **Changes**: one line per change, naming the criterion it fixes.
   - **Questions**: up to 3, only for gaps the context cannot fill (e.g. the expected result). Mark their place in the rewrite with `<...>`.

## Criteria

- **Goal**: the outcome wanted, beyond the action.
- **Anchor**: where the thing lives (ticket, file, link, branch, repo, or global config).
- **Name**: the project's term for the thing.
- **Done**: how to tell the work is finished.
- **Bounds**: scope, constraints, and what to leave untouched.
- **One ask**: one task per prompt; split unrelated tasks into separate prompts, in order.
- **Skill**: when an available skill fits the task, start the prompt with it.

Cut what the agent already knows (greetings, repeated context, instructions from `CLAUDE.md`).
