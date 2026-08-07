"""Read-only Git identity snapshots for concurrent Brain sessions."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import Any

from .models import iso_timestamp


def _run_git(root: Path, *args: str) -> tuple[bool, str]:
    """Run one read-only Git command and return success plus trimmed output."""
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, result.stdout.strip()


def _hashed_identifier(value: str) -> str:
    """Hash a local Git path so runtime ledgers do not expose it."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_git_path(root: Path, value: str) -> str:
    """Resolve a Git path relative to the worktree without returning it."""
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    return str(candidate.resolve())


def _is_temporary_root(root: Path) -> bool:
    """Identify conventional temporary worktree roots without globbing files."""
    normalized = root.resolve().as_posix()
    return normalized.startswith(("/tmp/", "/private/tmp/"))


def classify_worktree(root: Path, branch: str | None, head: str | None) -> str:
    """Classify a worktree for dashboard filtering and handoff warnings."""
    if not head:
        return "unknown"
    if branch is None:
        return "detached"
    if _is_temporary_root(root):
        return "temporary"
    if branch in {"main", "master"}:
        return "main"
    if branch.startswith("feature/"):
        return "feature"
    return "unknown"


def _status_counts(status_output: str) -> dict[str, Any]:
    """Count staged, unstaged, and untracked entries from porcelain status."""
    staged = 0
    unstaged = 0
    untracked = 0
    lines = [line for line in status_output.splitlines() if line]
    for line in lines:
        code = line[:2]
        if code == "??":
            untracked += 1
            continue
        if len(code) >= 1 and code[0] != " ":
            staged += 1
        if len(code) >= 2 and code[1] != " ":
            unstaged += 1
    return {
        "dirty": bool(lines),
        "staged_count": staged,
        "unstaged_count": unstaged,
        "untracked_count": untracked,
    }


def _base_ref(root: Path, upstream: str | None) -> str | None:
    """Resolve an upstream or the conventional origin/main fallback."""
    if upstream:
        return upstream
    available, _ = _run_git(root, "rev-parse", "--verify", "refs/remotes/origin/main")
    return "origin/main" if available else None


def _ahead_behind(root: Path, base_ref: str | None, head: str | None) -> tuple[int | None, int | None]:
    """Return commits behind and ahead of the selected base reference."""
    if not base_ref or not head:
        return None, None
    available, output = _run_git(root, "rev-list", "--left-right", "--count", f"{base_ref}...HEAD")
    if not available:
        return None, None
    values = output.split()
    if len(values) != 2 or not all(value.isdigit() for value in values):
        return None, None
    return int(values[0]), int(values[1])


def snapshot_git(root: Path) -> dict[str, Any]:
    """Return a privacy-preserving, read-only Git worktree snapshot."""
    work_root = root.expanduser().resolve()
    captured_at = iso_timestamp()
    base: dict[str, Any] = {
        "is_git": False,
        "git_valid": False,
        "repo_id": None,
        "worktree_id": None,
        "root_path_policy": "hashed",
        "worktree_class": "unknown",
        "branch": None,
        "head": None,
        "upstream": None,
        "base_ref": None,
        "merge_base": None,
        "ahead": None,
        "behind": None,
        "dirty": False,
        "staged_count": 0,
        "unstaged_count": 0,
        "untracked_count": 0,
        "captured_at": captured_at,
    }
    if not (work_root / ".git").exists():
        return base

    base["is_git"] = True
    common_ok, common_dir = _run_git(work_root, "rev-parse", "--git-common-dir")
    git_ok, git_dir = _run_git(work_root, "rev-parse", "--git-dir")
    branch_ok, branch = _run_git(work_root, "branch", "--show-current")
    head_ok, head = _run_git(work_root, "rev-parse", "HEAD")
    upstream_ok, upstream = _run_git(
        work_root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"
    )
    status_ok, status_output = _run_git(work_root, "status", "--porcelain=v1")

    common_path = _canonical_git_path(work_root, common_dir) if common_ok else None
    git_path = _canonical_git_path(work_root, git_dir) if git_ok else None
    branch_value = branch if branch_ok and branch else None
    head_value = head if head_ok and head else None
    upstream_value = upstream if upstream_ok and upstream else None
    base_ref = _base_ref(work_root, upstream_value) if head_value else None
    merge_base_ok, merge_base = (
        _run_git(work_root, "merge-base", "HEAD", base_ref)
        if base_ref
        else (False, "")
    )
    behind, ahead = _ahead_behind(work_root, base_ref, head_value)
    status = _status_counts(status_output) if status_ok else {}

    base.update(
        {
            "git_valid": bool(common_path and git_path and head_value),
            "repo_id": _hashed_identifier(common_path) if common_path else None,
            "worktree_id": (
                _hashed_identifier(f"{common_path}\n{git_path}")
                if common_path and git_path
                else None
            ),
            "worktree_class": classify_worktree(work_root, branch_value, head_value),
            "branch": branch_value,
            "head": head_value,
            "upstream": upstream_value,
            "base_ref": base_ref,
            "merge_base": merge_base if merge_base_ok and merge_base else None,
            "ahead": ahead,
            "behind": behind,
            **status,
        }
    )
    return base
