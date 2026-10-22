---
name: stage-no-tests
description: "Leave test files unstaged when staging work for review or a commit. Use when staging files, presenting developed code, or preparing a commit or PR."
---

The user reviews staged files and skips tests, so tests stay **unstaged**. This overrides any repo rule that asks to stage tests; the rest of that rule still applies.

## Steps

1. Pick the files to stage as the repo's rules say.

2. Drop every **test file** from that list (see Reference), then stage the rest.

3. Check: `git diff --cached --name-only` lists no test file you staged. Test files the user staged stay as they are.

4. Tell the user which test files you left unstaged. A commit takes only staged files, so those tests stay out of the commit and the PR until the user stages them.

## Reference

Test files:

- Any path under a `test/` or `tests/` folder, `conftest.py` included.
- `test_*.py`, `*_test.py`, `*_test.go`.
- `*.test.*` and `*.spec.*` (`.ts`, `.tsx`, `.js`, `.jsx`).
- Snapshots and fixtures that only tests use (`__snapshots__/`, `fixtures/` inside a test folder).
