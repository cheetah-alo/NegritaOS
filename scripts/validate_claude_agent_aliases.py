#!/usr/bin/env python3
"""Validate Claude-native aliases for NegritaOS router modes."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from .sync_claude_agent_aliases import MANAGED_MARKER, discover_project_repos
    from .validate_skill_catalog import ROOT, _load_yaml
except ImportError:
    from sync_claude_agent_aliases import MANAGED_MARKER, discover_project_repos
    from validate_skill_catalog import ROOT, _load_yaml


def _expected_aliases(root: Path) -> list[dict[str, str]]:
    """Return expected alias metadata from the router."""
    router = _load_yaml(root / "core/orchestration/metaagent_router.yaml")
    modes = router.get("metaagent_router", {}).get("modes", {})
    aliases: list[dict[str, str]] = []
    for mode in modes.values():
        if not isinstance(mode, dict):
            continue
        mode_id = mode.get("id")
        agent_id = mode.get("agent")
        if isinstance(mode_id, str) and isinstance(agent_id, str):
            aliases.append(
                {
                    "alias": mode_id.lower(),
                    "mode_id": mode_id,
                    "agent_id": agent_id,
                }
            )
    return sorted(aliases, key=lambda row: row["alias"])


def _read(path: Path) -> tuple[str | None, str | None]:
    """Read a file and return `(text, error)`."""
    try:
        return path.read_text(encoding="utf-8", errors="ignore"), None
    except OSError as exc:
        return None, str(exc)


def validate_repo(repo: Path, root: Path) -> list[str]:
    """Validate aliases for one project adapter."""
    errors: list[str] = []
    agents_root = repo / ".codex" / "agents"
    if not agents_root.is_dir():
        return [f"{repo}: missing .codex/agents directory"]
    for expected in _expected_aliases(root):
        path = agents_root / f"{expected['alias']}.md"
        if not path.exists():
            errors.append(f"{repo}: missing Claude alias {path.relative_to(repo)}")
            continue
        text, error = _read(path)
        if error:
            errors.append(f"{repo}: unreadable {path.relative_to(repo)}: {error}")
            continue
        assert text is not None
        if MANAGED_MARKER not in text:
            errors.append(f"{repo}: {path.relative_to(repo)} is not a managed NegritaOS alias")
        if not re.search(rf'^name:\s*"{re.escape(expected["alias"])}"', text, re.MULTILINE):
            errors.append(f"{repo}: {path.relative_to(repo)} has wrong Claude agent name")
        if f"canonical_mode: {expected['mode_id']}" not in text:
            errors.append(f"{repo}: {path.relative_to(repo)} has wrong canonical_mode")
        if f"canonical_agent: {expected['agent_id']}" not in text:
            errors.append(f"{repo}: {path.relative_to(repo)} has wrong canonical_agent")
    return errors


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, action="append", default=[])
    parser.add_argument("--all-projects", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Run alias validation."""
    args = _parse_args()
    repos = [ROOT]
    repos.extend(args.repo)
    if args.all_projects:
        repos.extend(discover_project_repos(ROOT))

    errors: list[str] = []
    seen: set[Path] = set()
    for repo in repos:
        resolved = repo.expanduser().resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        errors.extend(validate_repo(resolved, ROOT))

    if errors:
        print("Claude agent alias validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"[OK] Claude agent aliases valid for {len(seen)} project(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
