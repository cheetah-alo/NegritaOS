#!/usr/bin/env python3
"""Validate project-declared Codex custom agent TOML files and adapter links."""

from __future__ import annotations

import argparse
import subprocess
import tomllib
from pathlib import Path

try:
    from .sync_claude_agent_aliases import discover_project_repos
    from .sync_codex_custom_agents import (
        AGENT_NAME,
        configured_agents,
        global_custom_agents,
    )
    from .validate_skill_catalog import ROOT, _load_yaml
except ImportError:
    from sync_claude_agent_aliases import discover_project_repos
    from sync_codex_custom_agents import (
        AGENT_NAME,
        configured_agents,
        global_custom_agents,
    )
    from validate_skill_catalog import ROOT, _load_yaml


REQUIRED_FIELDS = (
    "name",
    "description",
    "model",
    "model_reasoning_effort",
    "developer_instructions",
)
ALLOWED_SANDBOX_MODES = ("read-only", "workspace-write", "danger-full-access")
FINANCIAL_CONTROL_MARKERS = (
    "explicit authorization for that exact operation",
    "BLOCKED_FINANCIAL_AUTHORIZATION",
)


def _model_policy(root: Path) -> dict:
    """Load the model policy mapping; structural validation runs separately."""
    path = root / "core" / "orchestration" / "model_escalation_policy.yaml"
    value = _load_yaml(path).get("model_escalation_policy", {})
    return value if isinstance(value, dict) else {}


def validate_toml(
    path: Path,
    expected_name: str,
    root: Path = ROOT,
) -> list[str]:
    """Validate the supported custom-agent contract."""
    errors: list[str] = []
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [f"{path}: invalid TOML: {exc}"]
    for field in REQUIRED_FIELDS:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}: {field} must be a non-empty string")
    if data.get("name") != expected_name:
        errors.append(f"{path}: name must match filename {expected_name!r}")
    policy = _model_policy(root)
    expected_tier = policy.get("custom_agent_tiers", {}).get(expected_name)
    tier = policy.get("tiers", {}).get(expected_tier, {})
    if not isinstance(expected_tier, str) or not isinstance(tier, dict):
        errors.append(f"{path}: no canonical model tier for agent {expected_name!r}")
    else:
        if data.get("model") != tier.get("model"):
            errors.append(
                f"{path}: model must be {tier.get('model')!r} for tier {expected_tier}"
            )
        if data.get("model_reasoning_effort") != tier.get("reasoning_effort"):
            errors.append(
                f"{path}: model_reasoning_effort must be "
                f"{tier.get('reasoning_effort')!r} for tier {expected_tier}"
            )
    sandbox_mode = data.get("sandbox_mode")
    if sandbox_mode is not None and sandbox_mode not in ALLOWED_SANDBOX_MODES:
        errors.append(f"{path}: unsupported sandbox_mode {sandbox_mode!r}")
    instructions = data.get("developer_instructions")
    if isinstance(instructions, str):
        normalized_instructions = " ".join(instructions.split())
        for marker in FINANCIAL_CONTROL_MARKERS:
            if marker not in normalized_instructions:
                errors.append(
                    f"{path}: developer_instructions missing financial control "
                    f"marker {marker!r}"
                )
    return errors


def validate_repo(repo: Path, root: Path = ROOT) -> list[str]:
    """Validate one adapter against its project registry declaration."""
    errors: list[str] = []
    repo = repo.expanduser().resolve()
    try:
        names = configured_agents(repo, root)
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        return [f"{repo}: cannot resolve custom agents: {exc}"]
    for name in names:
        source = root / ".codex" / "agents" / f"{name}.toml"
        if not source.is_file():
            errors.append(f"missing canonical Codex custom agent: {source}")
            continue
        errors.extend(validate_toml(source, name, root))
        if repo == root.resolve():
            continue
        destination = repo / ".codex" / "agents" / source.name
        if not destination.exists() and not destination.is_symlink():
            errors.append(f"{repo}: missing custom agent {destination.relative_to(repo)}")
            continue
        if destination.is_symlink():
            try:
                if destination.resolve() != source.resolve():
                    errors.append(f"{destination}: symlink does not resolve to {source}")
            except OSError as exc:
                errors.append(f"{destination}: broken symlink: {exc}")
        else:
            try:
                if destination.read_bytes() != source.read_bytes():
                    errors.append(f"{destination}: local copy drifts from canonical agent")
            except OSError as exc:
                errors.append(f"{destination}: unreadable: {exc}")
    return errors


def validate_registry_declarations(root: Path = ROOT) -> list[str]:
    """Validate canonical TOMLs referenced by every project registry."""
    errors: list[str] = []
    for registry in sorted((root / "projects").glob("*.yaml")):
        project = _load_yaml(registry).get("project", {})
        if not isinstance(project, dict):
            errors.append(f"{registry}: project must be a mapping")
            continue
        configured = project.get("codex_custom_agents", [])
        if configured is None:
            configured = []
        if not isinstance(configured, list) or not all(
            isinstance(item, str) for item in configured
        ):
            errors.append(f"{registry}: codex_custom_agents must be a string list")
            continue
        try:
            global_names = global_custom_agents(root)
        except (OSError, ValueError) as exc:
            errors.append(f"cannot resolve global custom agents: {exc}")
            global_names = []
        names = list(
            dict.fromkeys([*global_names, *(item.strip() for item in configured)])
        )
        for name in names:
            if not AGENT_NAME.fullmatch(name):
                errors.append(f"{registry}: invalid custom agent name {name!r}")
                continue
            source = root / ".codex" / "agents" / f"{name}.toml"
            if not source.is_file():
                errors.append(f"missing canonical Codex custom agent: {source}")
            else:
                errors.extend(validate_toml(source, name, root))
    return errors


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, action="append", default=[])
    parser.add_argument("--all-projects", action="store_true")
    parser.add_argument("--registry-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Validate registry declarations and selected materialized adapters."""
    args = _parse_args()
    errors = validate_registry_declarations(ROOT)
    repos = [] if args.registry_only else list(args.repo)
    if args.all_projects:
        repos.extend(discover_project_repos(ROOT))
    seen: set[Path] = set()
    for repo in repos:
        resolved = repo.expanduser().resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        errors.extend(validate_repo(resolved, ROOT))
    if errors:
        print("Codex custom agent validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    if args.registry_only:
        print("[OK] Codex custom agent registry declarations are valid")
    else:
        print(f"[OK] Codex custom agents valid for {len(seen)} adapter(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
