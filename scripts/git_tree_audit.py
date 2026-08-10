#!/usr/bin/env python3
"""Read-only branch and worktree audit for NegritaOS projects."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


def _run(root: Path, *args: str) -> tuple[bool, str]:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=False
    )
    return result.returncode == 0, result.stdout.rstrip()


def _status(root: Path) -> dict[str, int | bool]:
    _, output = _run(root, "status", "--porcelain=v1")
    staged = unstaged = untracked = 0
    for line in output.splitlines():
        if line.startswith("??"):
            untracked += 1
            continue
        if line[:1] and line[0] != " ":
            staged += 1
        if len(line) > 1 and line[1] != " ":
            unstaged += 1
    return {
        "dirty": bool(staged or unstaged or untracked),
        "staged": staged,
        "unstaged": unstaged,
        "untracked": untracked,
    }


def _branch_name(root: Path) -> str | None:
    ok, value = _run(root, "branch", "--show-current")
    return value if ok and value else None


def _counts(root: Path, base: str, branch: str = "HEAD") -> tuple[int | None, int | None]:
    ok, value = _run(root, "rev-list", "--left-right", "--count", f"{base}...{branch}")
    if not ok:
        return None, None
    parts = value.split()
    if len(parts) != 2 or not all(part.isdigit() for part in parts):
        return None, None
    return int(parts[0]), int(parts[1])


def _worktrees(root: Path) -> list[dict[str, Any]]:
    ok, output = _run(root, "worktree", "list", "--porcelain")
    if not ok:
        return []
    records: list[dict[str, Any]] = []
    current: dict[str, Any] = {}
    for line in output.splitlines() + [""]:
        if not line:
            if current:
                path = Path(str(current["path"]))
                current["branch"] = _branch_name(path)
                current["status"] = _status(path)
                records.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        if key == "worktree":
            current["path"] = value
        elif key == "HEAD":
            current["head"] = value
        elif key == "branch":
            current["ref"] = value
        elif key == "detached":
            current["detached"] = True
    return records


def _resolve_integration_branch(repo: Path, explicit: str | None) -> str | None:
    if explicit:
        return explicit
    project_yaml = repo / ".codex" / "project.yaml"
    if not project_yaml.is_file():
        return None
    try:
        try:
            import yaml

            adapter = yaml.safe_load(project_yaml.read_text(encoding="utf-8")) or {}
        except (ImportError, ModuleNotFoundError):
            output = subprocess.check_output(
                [
                    "ruby",
                    "-e",
                    "require 'yaml'; require 'json'; puts JSON.generate(YAML.load_file(ARGV.fetch(0)))",
                    str(project_yaml),
                ],
                text=True,
            )
            adapter = json.loads(output) or {}
        registry = Path(str(adapter.get("negrita_registry", ""))).expanduser()
        if not registry.is_absolute():
            registry = repo / registry
        try:
            import yaml

            data = yaml.safe_load(registry.read_text(encoding="utf-8")) or {}
        except (ImportError, ModuleNotFoundError):
            output = subprocess.check_output(
                [
                    "ruby",
                    "-e",
                    "require 'yaml'; require 'json'; puts JSON.generate(YAML.load_file(ARGV.fetch(0)))",
                    str(registry),
                ],
                text=True,
            )
            data = json.loads(output) or {}
        project = data.get("project", {})
        branch = project.get("integration_branch") if isinstance(project, dict) else None
        return branch if isinstance(branch, str) and branch.strip() else None
    except (OSError, ImportError, ModuleNotFoundError, AttributeError, TypeError, ValueError, subprocess.SubprocessError):
        return None


def _classify(
    branch: str,
    ahead: int | None,
    behind: int | None,
    status: dict[str, Any],
    integration_available: bool,
    max_commits: int,
) -> str:
    if not integration_available:
        return "BLOCKED_CONFIG_RESOLUTION"
    if status.get("dirty"):
        return "RECOVERY_REQUIRED"
    if branch is None:
        return "DETACHED_BASELINE"
    if ahead is not None and ahead > max_commits:
        return "PR_REQUIRED"
    if ahead == 0 and behind is not None and behind > 0:
        return "STALE_REVIEW"
    return "ACTIVE_NO_PR"


def audit_repo(repo: Path, integration_branch: str | None = None, max_commits: int = 5) -> dict[str, Any]:
    """Return a read-only audit without mutating the repository."""
    root = repo.expanduser().resolve()
    ok, top = _run(root, "rev-parse", "--show-toplevel")
    if not ok:
        return {"repository": str(root), "state": "NOT_GIT", "branches": [], "worktrees": []}
    root = Path(top)
    branch = _branch_name(root)
    integration = _resolve_integration_branch(root, integration_branch)
    base_ref = f"origin/{integration}" if integration else None
    base_ok = bool(base_ref and _run(root, "rev-parse", "--verify", base_ref)[0])
    status = _status(root)
    ahead, behind = _counts(root, base_ref) if base_ok and base_ref else (None, None)
    current_class = _classify(branch, ahead, behind, status, base_ok, max_commits)
    return {
        "repository": str(root),
        "state": "READY" if integration and base_ok else "BLOCKED_CONFIG_RESOLUTION",
        "integration_branch": integration,
        "integration_ref": base_ref if base_ok else None,
        "current": {
            "branch": branch,
            "head": _run(root, "rev-parse", "HEAD")[1] or None,
            "ahead": ahead,
            "behind": behind,
            "status": status,
            "classification": current_class,
        },
        "branches": _branch_rows(root, base_ref if base_ok else None, max_commits),
        "worktrees": _worktrees(root),
    }


def _branch_rows(root: Path, base_ref: str | None, max_commits: int) -> list[dict[str, Any]]:
    ok, output = _run(
        root,
        "for-each-ref",
        "--format=%(refname:short)\t%(upstream:short)\t%(objectname:short)\t%(committerdate:iso-strict)\t%(subject)",
        "refs/heads",
    )
    if not ok:
        return []
    rows: list[dict[str, Any]] = []
    for line in output.splitlines():
        values = line.split("\t", 4)
        if len(values) != 5:
            continue
        name, upstream, head, committed_at, subject = values
        ahead, behind = _counts(root, base_ref, name) if base_ref else (None, None)
        upstream_exists = bool(upstream and _run(root, "rev-parse", "--verify", upstream)[0])
        rows.append(
            {
                "branch": name,
                "upstream": upstream or None,
                "upstream_exists": upstream_exists,
                "head": head,
                "committed_at": committed_at,
                "subject": subject,
                "ahead": ahead,
                "behind": behind,
                "classification": _classify(
                    name,
                    ahead,
                    behind,
                    {"dirty": False},
                    bool(base_ref),
                    max_commits,
                ),
            }
        )
    return rows


def _print_table(report: dict[str, Any]) -> None:
    print(f"Repository: {report['repository']}")
    print(f"State: {report['state']}")
    print(f"Integration: {report.get('integration_branch') or 'MISSING'}")
    print("\nBranches")
    print("branch | upstream | behind | ahead | classification | last commit")
    for row in report.get("branches", []):
        print(
            f"{row['branch']} | {row['upstream'] or '-'} | {row['behind'] if row['behind'] is not None else '-'} | "
            f"{row['ahead'] if row['ahead'] is not None else '-'} | {row['classification']} | {row['head']} {row['subject']}"
        )
    print("\nWorktrees")
    for item in report.get("worktrees", []):
        status = item.get("status", {})
        print(
            f"{item['path']} | {item.get('branch') or 'DETACHED'} | "
            f"dirty={status.get('dirty')} staged={status.get('staged')} "
            f"unstaged={status.get('unstaged')} untracked={status.get('untracked')}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--integration-branch")
    parser.add_argument("--max-unmerged-commits", type=int, default=5)
    parser.add_argument("--format", choices=("table", "json"), default="table")
    args = parser.parse_args()
    report = audit_repo(args.repo, args.integration_branch, args.max_unmerged_commits)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        _print_table(report)
    return 0 if report.get("state") != "NOT_GIT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
