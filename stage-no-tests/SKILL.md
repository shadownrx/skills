---
name: stage-no-tests
description: "Install or explain the hook that keeps the agent from staging test files."
disable-model-invocation: true
---

The user reviews staged files and skips tests, so the agent leaves tests **unstaged**. `guard.py` (next to this file) enforces it as a Claude Code `PreToolUse` hook: before each Bash call it runs `git add --dry-run` for every `git add` in the command, following `cd` and `-C`, and denies the call when a test file would be staged. Tests the user stages by hand are untouched.

## Install

Add this to `hooks.PreToolUse` in `~/.claude/settings.json`, next to any existing `Bash` entry:

```json
{ "matcher": "Bash", "hooks": [{ "type": "command", "command": "python3 '<skill-dir>/guard.py'", "timeout": 10 }] }
```

Then check it: in a scratch repo with `tests/test_x.py`, the agent's `git add -A` is denied and `git add <non-test file>` passes.

## Test files

- Any path under a `test/` or `tests/` folder, plus `conftest.py` and `__snapshots__/`.
- `test_*.py`, `*_test.py`, `*_test.go`.
- `*.test.*` and `*.spec.*` for JS and TS files.

Change `TEST_PATH` in `guard.py` to add a pattern.
