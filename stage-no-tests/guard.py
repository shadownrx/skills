#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block an agent `git add` that would stage test files.

The user stages tests themselves, so the agent stages everything else and leaves tests out.
"""

import json
import os
import re
import shlex
import subprocess
import sys

TEST_PATH = re.compile(
    r"(^|/)tests?/"
    r"|(^|/)__snapshots__/"
    r"|(^|/)conftest\.py$"
    r"|(^|/)test_[^/]*\.py$"
    r"|_test\.(py|go)$"
    r"|\.(test|spec)\.[cm]?[jt]sx?$"
)
SEGMENT_SPLIT = re.compile(r"&&|\|\||[;|\n]")


def git_add_calls(command, cwd):
    """Yield (directory, git global options, add arguments) for each `git add` in a shell command.

    Follows `cd` segments, since the agent often runs `cd repo && git add ...`.
    """
    for segment in SEGMENT_SPLIT.split(command):
        try:
            tokens = shlex.split(segment)
        except ValueError:
            continue
        if len(tokens) == 2 and tokens[0] == "cd":
            cwd = os.path.join(cwd, os.path.expanduser(tokens[1]))
            continue
        for start, token in enumerate(tokens):
            if token != "git":
                continue
            index, global_options = start + 1, []
            while index < len(tokens) and tokens[index] in ("-C", "-c"):
                global_options += tokens[index : index + 2]
                index += 2
            if index < len(tokens) and tokens[index] == "add":
                yield cwd, global_options, tokens[index + 1 :]


def paths_to_stage(cwd, global_options, add_args):
    """Ask git which paths this `git add` would stage, without staging them."""
    if any(arg in ("-p", "--patch", "-i", "--interactive", "-e", "--edit") for arg in add_args):
        return []
    result = subprocess.run(
        ["git", *global_options, "add", "--dry-run", *add_args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return re.findall(r"^add '(.+)'$", result.stdout, re.MULTILINE)


def main():
    """Deny the Bash call when any `git add` in it would stage a test file."""
    payload = json.load(sys.stdin)
    command = (payload.get("tool_input") or {}).get("command") or ""
    tests = sorted(
        {
            path
            for directory, options, args in git_add_calls(command, payload.get("cwd") or os.getcwd())
            for path in paths_to_stage(directory, options, args)
            if TEST_PATH.search(path)
        }
    )
    if not tests:
        return
    reason = (
        "This git add would stage test files, and the user stages tests themselves: "
        + ", ".join(tests)
        + ". Stage the other files by name, or add the pathspec "
        "':(exclude)**/tests/**' ':(exclude)**/test_*.py' ':(exclude)**/*.test.*' "
        "':(exclude)**/*.spec.*' ':(exclude)**/conftest.py'. Then tell the user which tests stay unstaged."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


if __name__ == "__main__":
    main()
