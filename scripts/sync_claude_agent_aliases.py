#!/usr/bin/env python3
"""Generate Claude-native aliases for NegritaOS router modes.

NegritaOS agents are canonical registry entries, but Claude Code discovers
subagents from local `.codex/agents/*.md` or `.claude/agents/*.md` files. This
script creates thin aliases so the same operational modes are invocable from
Claude without duplicating the real agent contracts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path
from typing import Any

try:
    from .validate_skill_catalog import ROOT, _load_yaml
except ImportError:
    from validate_skill_catalog import ROOT, _load_yaml


MANAGED_MARKER = "<!-- NEGRITAOS_CLAUDE_AGENT_ALIAS:START -->"
DEFAULT_MODEL = "sonnet"
MODE_ORDER = [
    "ASTRA",
    "LP",
    "AE",
    "TD",
    "MR",
    "MCARD",
    "CR",
    "PRR",
    "DEP",
    "FQA",
    "LQA",
    "QG",
    "PA",
    "EP",
    "DQ",
    "RT",
    "HOURS",
]
MODE_ACTIONS = {
    "ASTRA": "astra_review",
    "LP": "planning",
    "AE": "academic_review",
    "TD": "technical_documentation",
    "MR": "model_review",
    "MCARD": "model_governance_card",
    "CR": "code_review",
    "PRR": "pull_request_review",
    "DEP": "deployment",
    "FQA": "functional_qa",
    "LQA": "lifecycle_qa",
    "QG": "quality_bar_gauntlet",
    "PA": "plot_analysis",
    "EP": "deck",
    "DQ": "data_incident",
    "RT": "research",
    "HOURS": "tracking_hours",
}


def _as_list(value: Any) -> list[str]:
    """Return a string list from scalar/list values."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _project_scope(mode: dict[str, Any], mode_id: str) -> list[str]:
    """Return a strictly typed optional project scope."""
    value = mode.get("project_scope")
    if value is None:
        return []
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, list) and all(
        isinstance(item, str) and item.strip() for item in value
    ):
        return [item.strip() for item in value]
    raise ValueError(f"router mode {mode_id}: project_scope must be a string list")


def _load_modes(root: Path, project_id: str | None = None) -> list[dict[str, Any]]:
    """Return router modes enriched with integrator agent metadata."""
    router = _load_yaml(root / "core/orchestration/metaagent_router.yaml")
    integrator = _load_yaml(root / "integrator.yaml")
    modes = router.get("metaagent_router", {}).get("modes", {})
    agents = integrator.get("negrita_os", {}).get("agents", {})
    rows: list[dict[str, Any]] = []
    for mode_key, mode in modes.items():
        if not isinstance(mode, dict):
            continue
        mode_id = mode.get("id")
        agent_id = mode.get("agent")
        if not isinstance(mode_id, str) or not isinstance(agent_id, str):
            continue
        project_scope = _project_scope(mode, mode_id)
        if project_id is not None and project_scope and project_id not in project_scope:
            continue
        native_alias = mode.get("native_alias", mode_id.lower())
        if not isinstance(native_alias, str) or not native_alias.strip():
            raise ValueError(f"router mode {mode_id}: native_alias must be a string")
        agent = agents.get(agent_id, {})
        rows.append(
            {
                "mode_key": mode_key,
                "mode_id": mode_id,
                "alias": native_alias.strip(),
                "label": mode.get("label", mode_key.replace("_", " ").title()),
                "agent_id": agent_id,
                "global_agent": mode.get("global_agent") is True,
                "agent_description": agent.get("description", ""),
                "trigger_signals": _as_list(mode.get("trigger_signals")),
                "output_types": _as_list(mode.get("output_types")),
                "codex_skills": _as_list(agent.get("codex_skills")),
                "rules": _as_list(agent.get("rules")),
                "quality_gate": _as_list(agent.get("quality_gate")),
                "action": MODE_ACTIONS.get(mode_id, mode_key),
            }
        )
    order = {mode_id: index for index, mode_id in enumerate(MODE_ORDER)}
    aliases = [row["alias"] for row in rows]
    if len(aliases) != len(set(aliases)):
        raise ValueError("router modes define duplicate native_alias values")
    return sorted(rows, key=lambda row: order.get(row["mode_id"], 999))


def _short_csv(values: list[str], limit: int = 8) -> str:
    """Return a compact comma-separated value preview."""
    if not values:
        return "registered NegritaOS router triggers"
    clipped = values[:limit]
    suffix = ", ..." if len(values) > limit else ""
    return ", ".join(clipped) + suffix


def _bullet_list(values: list[str], empty: str) -> str:
    """Format values as Markdown bullets."""
    if not values:
        return f"- {empty}"
    return "\n".join(f"- `{value}`" for value in values)


def render_alias(row: dict[str, Any]) -> str:
    """Render one Claude agent alias file."""
    alias = row["alias"]
    mode_id = row["mode_id"]
    agent_id = row["agent_id"]
    description = (
        f"NegritaOS {mode_id} alias for {row['label']} -> {agent_id}. "
        "Use this Claude agent when the user asks for "
        f"{_short_csv(row['trigger_signals'])}. "
        "It resolves .codex/project.yaml before acting and must not claim the "
        f"{mode_id} agent is missing until canonical resolution has run."
    )
    codex_skills = _bullet_list(row["codex_skills"], "No direct Codex skill wrappers declared.")
    rules = _bullet_list(row["rules"], "Use the rules returned by Negrita Brain resolution.")
    outputs = _bullet_list(row["output_types"], "Use the output mode returned by Negrita Brain.")
    gates = _bullet_list(row["quality_gate"], "Use the agent quality gate from integrator.yaml.")
    action = row["action"]
    availability = (
        f"`{agent_id}` is globally routed and does not need to be duplicated\n"
        "in the active project's `agents` list."
        if row["global_agent"]
        else (
            f"If the active project registry does not declare `{agent_id}`, answer\n"
            "`ROUTING_UNAVAILABLE` and name the missing project registry entry."
        )
    )
    return f"""---
name: "{alias}"
description: "{description}"
model: {DEFAULT_MODEL}
memory: project
---

{MANAGED_MARKER}

# NegritaOS Claude Agent Alias: {mode_id}

canonical_mode: {mode_id}
canonical_agent: {agent_id}
canonical_label: {row['label']}
global_agent: {str(row['global_agent']).lower()}

This file is a Claude-native wrapper. The source of truth is NegritaOS:

- `.codex/project.yaml`
- `projects/<project_id>.yaml`
- `core/orchestration/metaagent_router.yaml`
- `integrator.yaml`
- `skills/catalog.yaml`

## Invocation

Use this alias in Claude Code as:

```text
--agent {alias}
```

Users may still write `{mode_id}: ...`, `@agent:{mode_id} ...`, or plain
language triggers. Treat those as requests for this same NegritaOS mode.

## Mandatory Bootstrap

Before answering or editing, run canonical resolution:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve \\
  --root "$PWD" \\
  --provider claude \\
  --action {action}
```

Then load the resolved project registry, profile closure, skills, rules,
rubrics, templates, artifact route, and gates. If resolution returns `BLOCK`,
answer `BLOCKED_CONFIG_RESOLUTION` and report the reason.

{availability}
Do not ask what `{mode_id}` means; it is the canonical router mode above.

## Canonical Skills

{codex_skills}

## Canonical Rules

{rules}

## Output Modes

{outputs}

## Quality Gate

{gates}

## Fallback When Tools Are Restricted

If Bash or AskUserQuestion is denied by Claude permissions, do not invent a
local substitute. State which canonical resolution command or user decision is
blocked, and continue only with read-only evidence that is already visible.
"""


def _write_text(path: Path, content: str, dry_run: bool) -> None:
    """Write content when it changed."""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        print(f"[OK] {path}: unchanged")
        return
    if dry_run:
        action = "update" if path.exists() or path.is_symlink() else "create"
        print(f"[DRY-RUN] {action} {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[WRITE] {path}")


def sync_canonical(root: Path, dry_run: bool) -> list[Path]:
    """Create canonical alias files under NegritaOS `.codex/agents`."""
    aliases: list[Path] = []
    for row in _load_modes(root):
        path = root / ".codex" / "agents" / f"{row['alias']}.md"
        _write_text(path, render_alias(row), dry_run)
        aliases.append(path)
    return aliases


def _is_generated_alias(path: Path) -> bool:
    """Return whether an existing file is a managed NegritaOS alias."""
    try:
        return MANAGED_MARKER in path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False


def _link_alias(source: Path, destination: Path, dry_run: bool, timestamp: str) -> None:
    """Link one canonical alias into a project adapter."""
    if destination.is_symlink() and destination.resolve() == source.resolve():
        print(f"[OK] {destination}: already linked")
        return
    if destination.exists() or destination.is_symlink():
        backup = destination.with_name(f"{destination.name}.preAlias.{timestamp}")
        if dry_run:
            print(f"[DRY-RUN] backup {destination} -> {backup}")
            print(f"[DRY-RUN] link {destination} -> {source}")
            return
        shutil.move(str(destination), str(backup))
        reason = "managed alias" if _is_generated_alias(backup) else "local file"
        print(f"[BACKUP] {destination} -> {backup} ({reason})")
    elif dry_run:
        print(f"[DRY-RUN] link {destination} -> {source}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.symlink_to(source)
    print(f"[LINK] {destination} -> {source}")


def sync_repo(
    repo: Path,
    root: Path,
    dry_run: bool,
    aliases: list[Path] | None = None,
) -> None:
    """Materialize canonical aliases into one project adapter."""
    repo = repo.expanduser().resolve()
    if repo == root.resolve():
        print(f"[OK] {repo}: canonical aliases live in this repo")
        return
    project_yaml = repo / ".codex" / "project.yaml"
    if not project_yaml.is_file():
        raise ValueError(f"missing adapter project file: {project_yaml}")
    target_root = repo / ".codex" / "agents"
    if target_root.exists() and target_root.resolve() == (root / ".codex" / "agents").resolve():
        print(f"[OK] {repo}: .codex/agents already points to canonical aliases root")
        return
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    source_aliases = aliases if aliases is not None else sync_canonical(root, dry_run=True)
    adapter = _load_yaml(project_yaml)
    project_id = adapter.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        raise ValueError(f"missing project_id in {project_yaml}")
    applicable_names = {
        f"{row['alias']}.md" for row in _load_modes(root, project_id.strip())
    }
    for source in source_aliases:
        if source.name not in applicable_names:
            continue
        destination = target_root / source.name
        _link_alias(source, destination, dry_run, timestamp)


def discover_project_repos(root: Path) -> list[Path]:
    """Return registered sibling project roots from `projects/*.yaml`."""
    repos: list[Path] = []
    for registry in sorted((root / "projects").glob("*.yaml")):
        data = _load_yaml(registry)
        project = data.get("project", {})
        primary = project.get("local_paths", {}).get("primary") if isinstance(project, dict) else None
        if not isinstance(primary, str):
            continue
        path = Path(primary).expanduser()
        repos.append(path if path.is_absolute() else (root / path).resolve())
    return repos


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, action="append", default=[])
    parser.add_argument("--all-projects", action="store_true")
    parser.add_argument("--canonical-only", action="store_true")
    parser.add_argument("--write", action="store_true", help="Apply changes. Default is dry-run.")
    return parser.parse_args()


def main() -> int:
    """Run alias synchronization."""
    args = _parse_args()
    dry_run = not args.write
    aliases = sync_canonical(ROOT, dry_run)
    if args.canonical_only:
        return 0
    repos = list(args.repo)
    if args.all_projects:
        repos.extend(discover_project_repos(ROOT))
    seen: set[Path] = set()
    errors: list[str] = []
    for repo in repos:
        resolved = repo.expanduser().resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        try:
            sync_repo(resolved, ROOT, dry_run, aliases)
        except (OSError, ValueError) as exc:
            errors.append(f"{resolved}: {exc}")
    for error in errors:
        print(f"[BLOCKED] {error}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
