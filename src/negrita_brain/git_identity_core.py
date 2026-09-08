"""Portable, standard-library-only Git identity checks for hooks and CI."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Mapping


DOMAIN = re.compile(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+\Z")
OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


def git(repo: Path, *args: str, env: Mapping[str, str] | None = None) -> str:
    """Run a bounded Git command without echoing arguments or raw failures."""
    result = subprocess.run(
        ["git", "--no-replace-objects", "-C", str(repo), *args],
        capture_output=True, text=True, env=env, timeout=60, check=False,
    )
    if result.returncode:
        raise ValueError("Git operation failed; verify refs, repository and access")
    return result.stdout.strip()


def normalize_email(value: str) -> str:
    """Reject malformed addresses rather than accepting a corporate suffix."""
    email = value.strip().lower()
    if email.count("@") != 1 or any(c.isspace() or ord(c) < 32 for c in email):
        raise ValueError("Invalid identity email")
    local, domain = email.split("@")
    if not local or not DOMAIN.fullmatch(domain) or any(c in local for c in '<>'):
        raise ValueError("Invalid identity email")
    return email


def allowed(email: str, policy: dict) -> bool:
    """Match an explicit address list, or an approved team domain policy."""
    try:
        normalized = normalize_email(email)
    except ValueError:
        return False
    exact = policy.get("ci_allowed_emails", policy.get("allowed_emails"))
    if exact is not None:
        return normalized in [normalize_email(item) for item in exact]
    domain = normalized.split("@")[1]
    return any(
        domain == item or (policy.get("allow_subdomains") is True and domain.endswith("." + item))
        for item in policy.get("allowed_email_domains", [])
    )


def validate_policy(policy: dict) -> None:
    """Require a usable policy even when a revision range contains zero commits."""
    if not isinstance(policy, dict):
        raise ValueError("Contributor policy must be an object")
    if "allowed_emails" in policy:
        emails = policy["allowed_emails"]
        if not isinstance(emails, list) or not emails:
            raise ValueError("Exact email allowlist is empty")
        for email in emails:
            normalize_email(email)
    else:
        domains = policy.get("allowed_email_domains")
        if not isinstance(domains, list) or not domains:
            raise ValueError("Corporate domain allowlist is empty")
        if not all(isinstance(domain, str) and DOMAIN.fullmatch(domain) for domain in domains):
            raise ValueError("Invalid corporate domain")
        if not isinstance(policy.get("allow_subdomains"), bool):
            raise ValueError("Subdomain policy must be explicit")


def masked(email: str) -> str:
    """Expose only a validated domain in reports."""
    try:
        return "***@" + normalize_email(email).split("@")[1]
    except ValueError:
        return "<invalid-email>"


def effective_violations(repo: Path, expected: str) -> list[dict]:
    """Inspect Git's effective author and committer, including environment overrides."""
    policy = {"allowed_emails": [normalize_email(expected)]}
    failures = []
    for role in ("author", "committer"):
        identity = git(repo, "var", "GIT_" + role.upper() + "_IDENT")
        match = re.fullmatch(r".* <([^<>]+)> -?\d+ [+-]\d{4}", identity)
        email = match[1] if match else ""
        if not allowed(email, policy):
            failures.append({"role": role, "email": masked(email)})
    return failures


def commit_oid(repo: Path, ref: str) -> str:
    """Resolve one commit without permitting option or revision-range injection."""
    value = git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}")
    if not OID.fullmatch(value):
        raise ValueError("Expected one commit object")
    return value


def scan(repo: Path, head: str, bases: list[str], policy: dict) -> dict:
    """Inspect all introduced commits; ignore mailmap and replacement objects."""
    validate_policy(policy)
    if git(repo, "rev-parse", "--is-shallow-repository") == "true":
        raise ValueError("Shallow history cannot certify the commit range; fetch full history")
    tip = commit_oid(repo, head)
    excluded = [commit_oid(repo, base) for base in bases]
    # NUL is forbidden in Git metadata. Three fixed fields avoid subject parsing.
    raw = git(repo, "log", "--format=%H%x00%ae%x00%ce%x00", tip, *["^" + b for b in excluded], "--")
    fields = raw.split("\0")
    if fields[-1].strip():
        raise ValueError("Incomplete commit identity record")
    fields.pop()
    if len(fields) % 3:
        raise ValueError("Incomplete commit identity record")
    failures = []
    for index in range(0, len(fields), 3):
        sha, author, committer = fields[index:index + 3]
        for role, email in (("author", author), ("committer", committer)):
            if not allowed(email, policy):
                failures.append({"commit": sha.strip(), "role": role, "email": masked(email)})
    return {"status": "FAIL" if failures else "PASS", "commits_checked": len(fields) // 3,
            "head": tip, "bases": excluded, "violations": failures}


def push_scan(repo: Path, remote: str, stdin: str, policy: dict) -> list[dict]:
    """Check every pushed ref; new refs exclude only advertised remote history."""
    results = []
    remote_bases = None
    for line in stdin.splitlines():
        parts = line.split()
        if len(parts) != 4 or not OID.fullmatch(parts[1]) or not OID.fullmatch(parts[3]):
            raise ValueError("Invalid pre-push input")
        _, local_sha, _, remote_sha = parts
        if set(local_sha) == {"0"}:
            continue  # A deletion introduces no commit identity.
        if set(remote_sha) != {"0"}:
            bases = [remote_sha]
        else:
            if remote_bases is None:
                advertised = git(repo, "ls-remote", "--heads", "--", remote)
                remote_bases = sorted({row.split()[0] for row in advertised.splitlines()})
            bases = remote_bases
        results.append(scan(repo, local_sha, bases, policy))
    return results


def ci_range(event: dict, event_name: str, new_branch_base: str | None = None) -> tuple[str, list[str]]:
    """Use event SHAs, never a synthetic PR merge commit or inferred HEAD parent."""
    if event_name in {"pull_request", "pull_request_target"}:
        pr = event.get("pull_request", {})
        base, head = pr.get("base", {}).get("sha"), pr.get("head", {}).get("sha")
    elif event_name == "push":
        base, head = event.get("before"), event.get("after")
    else:
        raise ValueError("Unsupported CI event")
    if not isinstance(head, str) or not OID.fullmatch(head) or not isinstance(base, str) or not OID.fullmatch(base):
        raise ValueError("Missing event commit SHAs")
    if set(head) == {"0"}:
        return head, []
    if set(base) == {"0"}:
        if not new_branch_base:
            raise ValueError("New-branch CI requires an explicit trusted base")
        return head, [new_branch_base]
    return head, [base]


def main() -> int:
    """Run the neutral CI entrypoint with a checked-in policy."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--github-actions", action="store_true")
    parser.add_argument("--new-branch-base")
    args = parser.parse_args()
    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"))
        if args.github_actions:
            event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
            head, bases = ci_range(event, os.environ["GITHUB_EVENT_NAME"], args.new_branch_base)
            if set(head) == {"0"}:
                print(json.dumps({"status": "PASS", "commits_checked": 0, "reason": "ref deletion"}))
                return 0
        else:
            if not args.base:
                raise ValueError("An explicit base is required")
            head, bases = args.head, [args.base]
        result = scan(args.repo, head, bases, policy)
        print(json.dumps(result, sort_keys=True))
        return 1 if result["violations"] else 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.SubprocessError):
        print("BLOCKED: invalid configuration, unavailable refs or incomplete history", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
