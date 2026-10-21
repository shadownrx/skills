---
name: prompt-retro
description: "Show how the user could have written this session's prompts better."
disable-model-invocation: true
---

The user wants a **prompt retro**: feedback on their own messages, so the next session needs fewer turns.

## Steps

1. Read the user's messages in the session they name (default: the current one). Skip injected context: skill bodies, `AGENTS.md`, tool output.

2. Find the **cost** each message caused: extra turns, a wrong assumption, a search in the wrong place, rework. A message with no cost needs no feedback.

3. Pick the 1–3 messages with the highest cost. When no message caused a cost, say so in one line and stop.

4. Find the **root cause** of each cost. When the cause is the instructions, the available context, the code, or the validation, name it and keep it out of the prompt feedback.

5. For each message, write this block:

   - **Original**: the message, quoted verbatim.
   - **Gap**: what was missing or ambiguous, checked against the criteria below.
   - **Cost**: what it caused in this session, with evidence (turns, wrong files, reverted work).
   - **Better**: the rewritten message, in the user's language and voice.
   - **Effect**: what the rewrite would have avoided.

6. End with one reusable **pattern** per real gap, one line each.

Every block ties to a cost observed in the session, and every pattern ties to a block.

## Criteria

- **Goal**: the outcome wanted, beyond the action.
- **Anchor**: where the thing lives (ticket, file, link, branch, repo, or global config).
- **Name**: the project's term for the thing.
- **Done**: how to tell the work is finished.
- **Bounds**: scope, constraints, and what to leave untouched.
