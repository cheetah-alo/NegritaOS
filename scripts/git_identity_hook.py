#!/usr/bin/env python3
"""Dispatch canonical identity checks and preserve existing Git hooks."""

import json
import os
import subprocess
import sys
from pathlib import Path

from git_identity_core import effective_violations, git, push_scan


def main() -> int:
    """Validate first, then invoke the prior hook with unchanged arguments/stdin."""
    try:
        if os.environ.get("GIT_IDENTITY_GUARD_ACTIVE"):
            raise ValueError("Recursive identity hook invocation")
        name, *arguments = sys.argv[1:]
        repo = Path(git(Path.cwd(), "rev-parse", "--show-toplevel"))
        common = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir"))
        state = json.loads((common / "identity-guard.json").read_text(encoding="utf-8"))
        if state.get("schema_version") != 1:
            raise ValueError("Invalid installation receipt")
        expected, policy = state["expected_email"], state["contributor_policy"]
        failures = effective_violations(repo, expected)
        data = None
        if name == "pre-push":
            data = sys.stdin.buffer.read()
            if len(arguments) != 2:
                raise ValueError("Invalid pre-push arguments")
            results = push_scan(repo, arguments[1], data.decode("utf-8"), policy)
            failures.extend(item for result in results for item in result["violations"])
        elif name != "pre-commit":
            raise ValueError("Unsupported identity hook")
        if failures:
            print(json.dumps({"status": "BLOCKED", "violations": failures}), file=sys.stderr)
            return 1
        previous = Path(state["previous_hooks"]) / name
        if previous.is_file() and os.access(previous, os.X_OK):
            return subprocess.run([str(previous), *arguments], input=data, check=False,
                                  env={**os.environ, "GIT_IDENTITY_GUARD_ACTIVE": "1"}).returncode
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.SubprocessError):
        print("BLOCKED: Git identity validation unavailable; run configure git-identity --check", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
