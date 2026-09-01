#!/usr/bin/env python3
"""Materialize project-declared Codex custom agents into local adapters."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import tomllib
from pathlib import Path

try:
    from .sync_claude_agent_aliases import discover_project_repos
    from .validate_skill_catalog import ROOT, _load_yaml
except ImportError:
    from sync_claude_agent_aliases import discover_project_repos
    from validate_skill_catalog import ROOT, _load_yaml


AGENT_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
REQUIRED_FIELDS = (
    "name",
    "description",
    "model",
    "model_reasoning_effort",
    "developer_instructions",
)


def global_custom_agents(root: Path = ROOT) -> list[str]:
    """Return the canonical custom agents materialized for every project."""
    policy_path = root / "core" / "orchestration" / "model_escalation_policy.yaml"
    policy = _load_yaml(policy_path).get("model_escalation_policy", {})
    configured = (
        policy.get("global_codex_custom_agents", [])
        if isinstance(policy, dict)
        else []
    )
    if not isinstance(configured, list) or not all(
        isinstance(item, str) for item in configured
    ):
        raise ValueError("global_codex_custom_agents must be a string list")
    names: list[str] = []
    for raw_name in configured:
        name = raw_name.strip()
        if not AGENT_NAME.fullmatch(name):
            raise ValueError(f"invalid global custom agent name {raw_name!r}")
        if name not in names:
            names.append(name)
    return names


def _assert_valid_agent_toml(path: Path, expected_name: str) -> None:
    """Fail before distributing malformed canonical agent configuration."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"invalid canonical custom agent {path}: {exc}") from exc
    for field in REQUIRED_FIELDS:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{path}: {field} must be a non-empty string")
    if data.get("name") != expected_name:
        raise ValueError(f"{path}: name must match filename {expected_name!r}")


def _project_id(repo: Path) -> str:
    project_yaml = repo / ".codex" / "project.yaml"
    if not project_yaml.is_file():
        raise ValueError(f"missing adapter project file: {project_yaml}")
    adapter = _load_yaml(project_yaml)
    project_id = adapter.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        raise ValueError(f"missing project_id in {project_yaml}")
    return project_id.strip()


def configured_agents(repo: Path, root: Path = ROOT) -> list[str]:
    """Return the custom Codex agent names declared by a project registry."""
    project_id = _project_id(repo)
    registry = root / "projects" / f"{project_id}.yaml"
    if not registry.is_file():
        raise ValueError(f"missing project registry: {registry}")
    project = _load_yaml(registry).get("project", {})
    configured = project.get("codex_custom_agents", []) if isinstance(project, dict) else []
    if configured is None:
        return []
    if not isinstance(configured, list) or not all(isinstance(item, str) for item in configured):
        raise ValueError(f"project {project_id}: codex_custom_agents must be a string list")
    names: list[str] = global_custom_agents(root)
    for raw_name in configured:
        name = raw_name.strip()
        if not AGENT_NAME.fullmatch(name):
            raise ValueError(f"project {project_id}: invalid custom agent name {raw_name!r}")
        if name not in names:
            names.append(name)
    return names


def _link_agent(source: Path, destination: Path, dry_run: bool, timestamp: str) -> None:
    """Link one canonical TOML while preserving an existing local override."""
    if destination.is_symlink() and destination.resolve() == source.resolve():
        print(f"[OK] {destination}: already linked")
        return
    if destination.exists() or destination.is_symlink():
        if destination.is_file() and not destination.is_symlink():
            try:
                if destination.read_bytes() == source.read_bytes():
                    print(f"[OK] {destination}: byte-matches canonical agent")
                    return
            except OSError:
                pass
        backup = destination.with_name(f"{destination.name}.preCodexAgent.{timestamp}")
        if dry_run:
            print(f"[DRY-RUN] backup {destination} -> {backup}")
            print(f"[DRY-RUN] link {destination} -> {source}")
            return
        shutil.move(str(destination), str(backup))
        print(f"[BACKUP] {destination} -> {backup}")
    elif dry_run:
        print(f"[DRY-RUN] link {destination} -> {source}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.symlink_to(source)
    print(f"[LINK] {destination} -> {source}")


def sync_repo(repo: Path, root: Path = ROOT, dry_run: bool = True) -> None:
    """Materialize the configured custom agents for one project adapter."""
    repo = repo.expanduser().resolve()
    if repo == root.resolve():
        print(f"[OK] {repo}: canonical custom agents live in this repo")
        return
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    for name in configured_agents(repo, root):
        source = root / ".codex" / "agents" / f"{name}.toml"
        if not source.is_file():
            raise ValueError(f"missing canonical Codex custom agent: {source}")
        _assert_valid_agent_toml(source, name)
        _link_agent(source, repo / ".codex" / "agents" / source.name, dry_run, timestamp)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, action="append", default=[])
    parser.add_argument("--all-projects", action="store_true")
    parser.add_argument("--write", action="store_true", help="Apply changes. Default is dry-run.")
    return parser.parse_args()


def main() -> int:
    """Synchronize selected project adapters and return a process exit code."""
    args = _parse_args()
    repos = list(args.repo)
    if args.all_projects:
        repos.extend(discover_project_repos(ROOT))
    seen: set[Path] = set()
    for repo in repos:
        resolved = repo.expanduser().resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        sync_repo(resolved, ROOT, dry_run=not args.write)
    if not repos:
        print("[OK] no project adapters selected; pass --repo or --all-projects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
