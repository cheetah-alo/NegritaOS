#!/usr/bin/env python3
"""Check PR-introduced commits against a project's corporate identity policy."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from negrita_brain.commit_identity import (  # noqa: E402
    commit_identities,
    identity_violations,
    load_commit_identity_policies,
    resolve_policy,
)
from negrita_brain.config import load_project  # noqa: E402
from negrita_brain.errors import BrainError  # noqa: E402


ZERO_SHA = "0" * 40


def github_range(repo: Path, env: dict[str, str]) -> tuple[str, str]:
    """Resolve a PR or push range from GitHub Actions metadata."""
    event_path = env.get("GITHUB_EVENT_PATH")
    if event_path:
        payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
        pull_request = payload.get("pull_request")
        if isinstance(pull_request, dict):
            base = pull_request.get("base", {}).get("sha")
            head = pull_request.get("head", {}).get("sha")
            if isinstance(base, str) and base and isinstance(head, str) and head:
                return base, head
        before = payload.get("before")
        after = payload.get("after")
        valid_push_range = all(
            (
                isinstance(before, str),
                bool(before),
                before != ZERO_SHA,
                isinstance(after, str),
                bool(after),
            )
        )
        if valid_push_range:
            assert isinstance(before, str)
            assert isinstance(after, str)
            return before, after

    head = env.get("GITHUB_HEAD_SHA") or env.get("GITHUB_SHA") or "HEAD"
    base_branch = env.get("GITHUB_BASE_REF", "")
    if env.get("GITHUB_EVENT_NAME") == "pull_request" and base_branch:
        return f"origin/{base_branch}", head
    before = env.get("GITHUB_EVENT_BEFORE", "")
    if before and before != ZERO_SHA:
        return before, head
    raise ValueError("cannot resolve introduced commit range from GitHub metadata")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse checker arguments without guessing a local PR base."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--github-actions", action="store_true")
    parser.add_argument("--exclude-reachable", action="append", default=[])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Resolve policy, inspect the exact range, and return a CI-safe result."""
    args = parse_args(argv)
    repo = args.repo.expanduser().resolve()
    try:
        context = load_project(repo, ROOT)
        resolved = resolve_policy(
            context.project,
            load_commit_identity_policies(ROOT),
        )
        if resolved is None:
            print(f"Commit identity guard: SKIP ({context.project_id} has no policy)")
            return 0
        policy_id, policy = resolved
        if args.github_actions:
            base, head = github_range(repo, dict(os.environ))
        else:
            if not args.base:
                raise ValueError("--base is required outside GitHub Actions")
            base, head = args.base, args.head
        commits = commit_identities(repo, base, head, args.exclude_reachable)
        violations = identity_violations(commits, policy)
    except (BrainError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Commit identity guard: BLOCKED ({exc})", file=sys.stderr)
        return 2

    print(f"Policy: {policy_id}")
    print(f"Range: {base}..{head}")
    print(f"Commits checked: {len(commits)}")
    if violations:
        print("Commit identity guard: FAIL", file=sys.stderr)
        for violation in violations:
            print(
                f"- {violation.sha[:12]} {violation.role} "
                f"{violation.redacted_email} | {violation.subject}",
                file=sys.stderr,
            )
        return 1
    print("Commit identity guard: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
