---
name: prompt-optimize
description: "Optimize a prompt that an app sends to an LLM: fewer tokens, less ambiguity, same or better output, with evidence."
disable-model-invocation: true
---

The user wants a prompt that their code sends to a model made shorter, clearer, and more reliable. The argument is a file, a symbol, or pasted text. When there is no argument, ask which prompt and stop.

## Steps

1. Find the prompt and how it runs: the model and parameters, the variables injected, the tools, and the code that parses the output. The parser is the output contract.

2. Find its job: the input, the expected output, and who consumes it. Collect 3–5 real inputs from tests, evals, fixtures, or logs; invent realistic ones only when none exist, and say so.

3. Check it against the criteria below. List each finding in one line with its criterion, split into **fixes** (wrong or risky behavior) and **cuts** (same behavior, fewer tokens).

4. Rewrite it. Keep the behavior unless a finding is a fix. Keep the user's language for customer-facing copy. Show the rewrite as a diff, plus the token count before and after (name the tokenizer, or say it is an estimate of characters / 4).

5. Validate: run the old and new prompt on the same inputs with the project's eval, test, or a short script, and compare the outputs. When you cannot run them (no API key, no harness), say so and hand over the inputs as a test plan. Never claim an improvement without this comparison.

6. Wait for the user's approval before editing the file: a prompt is production behavior.

## Criteria

- **Task first**: the job and the output in the first lines.
- **Output contract**: the format matches the parser exactly; use structured output or a tool schema when the API supports it, instead of prose rules.
- **One meaning**: no ambiguous terms, no contradictory rules, one term per thing.
- **No filler**: cut repeated rules, politeness, and what the model already does by default.
- **Edge cases**: say what to do with empty, invalid, or unclear input, and when unsure.
- **Examples**: few, varied, shaped like real input; drop the ones that only repeat a rule.
- **Cache order**: static text first, variable data last, so prompt caching hits.
- **Model fit**: flag a model or parameter that looks wrong for the task; do not change it without asking.

When a repo has its own prompt skill (e.g. `prompt-design` in macch-core), follow it for those prompts.
