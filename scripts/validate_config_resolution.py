#!/usr/bin/env python3
"""Validate the complete NegritaOS project-to-agent configuration chain.

The active resolution path is:

    .codex/project.yaml
      -> projects/<project_id>.yaml
      -> skill_profiles / mode_map / agents
      -> integrator.yaml agent block
      -> skills, rules, rubrics, templates, codex_skills
      -> skills/catalog.yaml profile and wrapper entries

This is intentionally stricter than a path-only check. It catches cases where
an agent is technically present in the environment but is not reachable from
the active project registry or cannot load one of its declared assets.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    from .validate_skill_catalog import (
        CATALOG,
        ROOT,
        _load_yaml,
        validate_catalog,
        validate_project,
    )
except ImportError:
    from validate_skill_catalog import CATALOG, ROOT, _load_yaml, validate_catalog, validate_project

sys.path.insert(0, str(ROOT / "src"))

from negrita_brain.errors import ProfileResolutionError  # noqa: E402
from negrita_brain.profiles import resolve_project_profiles  # noqa: E402


ASSET_KEYS = ("skills", "rules", "rubrics", "templates", "codex_skills")
PROFILE_AGENT_REQUIREMENTS = {
    "academic-tfm-review": {"tfm_evaluator_agent"},
    "academic-tfm-research": {"tfm_research_advisor_agent"},
    "git-tree-governance": {"git_tree_governance_agent"},
}


def _resolve(root: Path, raw: str) -> Path:
    """Resolve an absolute or repository-relative path."""
    path = Path(raw).expanduser()
    return path if path.is_absolute() else root / path


def _as_strings(value: Any) -> list[str]:
    """Return scalar or list values as a list of strings."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    if isinstance(value, dict):
        return [item for item in value.values() if isinstance(item, str)]
    return []


def _load_agent_manifests(root: Path) -> dict[str, Path]:
    """Index standalone agent manifests by their declared agent id."""
    manifests: dict[str, Path] = {}
    for path in root.glob("**/agent.yaml"):
        if ".git" in path.parts:
            continue
        try:
            data = _load_yaml(path)
        except Exception:
            continue
        agent = data.get("agent", {})
        agent_id = agent.get("id") if isinstance(agent, dict) else None
        if isinstance(agent_id, str):
            manifests[agent_id] = path
    return manifests


def _check_asset_paths(
    root: Path,
    agent_id: str,
    agent: dict[str, Any],
    errors: list[str],
) -> None:
    """Check every file declared by an active integrator agent."""
    for key in ASSET_KEYS:
        for reference in _as_strings(agent.get(key)):
            target = _resolve(root, reference)
            if not target.exists():
                errors.append(
                    f"agent {agent_id}: missing {key} reference {reference}"
                )


def _router_modes(router: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index router modes by their short mode id."""
    modes = router.get("metaagent_router", {}).get("modes", {})
    if not isinstance(modes, dict):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for mode in modes.values():
        if isinstance(mode, dict) and isinstance(mode.get("id"), str):
            result[mode["id"]] = mode
    return result


def validate_resolution(
    root: Path = ROOT,
    project_yaml: Path | None = None,
) -> tuple[list[str], list[str], str]:
    """Return errors, warnings, and the resolved project id."""
    errors: list[str] = []
    warnings: list[str] = []
    project_yaml = project_yaml or root / ".codex" / "project.yaml"

    try:
        adapter = _load_yaml(project_yaml)
    except Exception as exc:
        return [f"cannot load {project_yaml}: {exc}"], [], "unknown"

    project_id = adapter.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        errors.append(f"{project_yaml}: project_id is missing or empty")
        return errors, warnings, "unknown"

    raw_registry = adapter.get("negrita_registry")
    if not isinstance(raw_registry, str) or not raw_registry.strip():
        raw_registry = f"projects/{project_id}.yaml"
    registry_path = _resolve(root, raw_registry)
    expected_registry = root / "projects" / f"{project_id}.yaml"
    if registry_path.resolve() != expected_registry.resolve():
        errors.append(
            f"{project_yaml}: registry resolves to {registry_path}, "
            f"expected {expected_registry}"
        )
    if not registry_path.is_file():
        errors.append(f"missing project registry: {registry_path}")
        return errors, warnings, project_id

    try:
        registry_data = _load_yaml(registry_path)
        catalog = _load_yaml(CATALOG)
        integrator_data = _load_yaml(root / "integrator.yaml")
        router_data = _load_yaml(root / "core" / "orchestration" / "metaagent_router.yaml")
    except Exception as exc:
        return [f"configuration load failed: {exc}"], warnings, project_id

    project = registry_data.get("project", {})
    if not isinstance(project, dict):
        errors.append(f"{registry_path}: project must be a mapping")
        return errors, warnings, project_id
    if project.get("id") != project_id:
        errors.append(
            f"{registry_path}: project.id={project.get('id')!r} does not match "
            f".codex/project.yaml project_id={project_id!r}"
        )

    catalog_errors = validate_catalog(catalog)
    errors.extend(f"catalog: {error}" for error in catalog_errors)
    errors.extend(
        f"project registry: {error}"
        for error in validate_project(catalog, registry_path)
    )
    profiles = catalog.get("profiles", {})
    skills_by_id = {
        item.get("id"): item
        for item in catalog.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    integrator = integrator_data.get("negrita_os", {})
    agents = integrator.get("agents", {})
    if not isinstance(agents, dict):
        errors.append("integrator.yaml: negrita_os.agents must be a mapping")
        return errors, warnings, project_id
    project_agents = set(_as_strings(project.get("agents")))
    declared_profiles = _as_strings(project.get("skill_profiles"))
    capabilities = set(_as_strings(project.get("capabilities")))

    if "bigquery" in capabilities:
        data_source = project.get("data_source")
        if not isinstance(data_source, dict):
            warnings.append(
                "BigQuery capability has no data_source declaration; provider, dialect, "
                "source-of-truth, and access remain unresolved"
            )
        elif data_source.get("provider") != "bigquery":
            errors.append(
                f"project {project_id}: BigQuery capability conflicts with "
                f"data_source.provider={data_source.get('provider')!r}"
            )
        if "data-source-bigquery" not in declared_profiles:
            warnings.append(
                "BigQuery capability has no data-source-bigquery skill profile; "
                "canonical BigQuery analysis governance is not activated"
            )

    for agent_id in sorted(project_agents):
        agent = agents.get(agent_id)
        if not isinstance(agent, dict):
            errors.append(
                f"project {project_id}: agent {agent_id!r} is not registered in integrator.yaml"
            )
            continue
        _check_asset_paths(root, agent_id, agent, errors)

    for profile_id in declared_profiles:
        profile = profiles.get(profile_id)
        if not isinstance(profile, dict):
            errors.append(
                f"project {project_id}: skill profile {profile_id!r} is missing "
                "from skills/catalog.yaml"
            )
            continue
        for required_agent in PROFILE_AGENT_REQUIREMENTS.get(profile_id, set()):
            if required_agent not in project_agents:
                errors.append(
                    f"project {project_id}: profile {profile_id} requires "
                    f"agent {required_agent}, but it is not declared"
                )
    try:
        resolved_skills = resolve_project_profiles(catalog, project).skills
    except ProfileResolutionError as exc:
        errors.append(f"project {project_id}: {exc}")
        resolved_skills = ()
    for skill_id in resolved_skills:
        entry = skills_by_id.get(skill_id)
        if not isinstance(entry, dict):
            errors.append(
                f"project {project_id}: resolved profile closure references "
                f"unknown skill {skill_id}"
            )
            continue
        for key in ("path", "native_path"):
            raw_path = entry.get(key)
            if isinstance(raw_path, str) and not _resolve(root, raw_path).exists():
                errors.append(f"catalog skill {skill_id}: missing {key} {raw_path}")

    modes = _router_modes(router_data)
    mode_map = project.get("mode_map", {})
    if isinstance(mode_map, dict):
        for intent, mode_id in mode_map.items():
            mode = modes.get(str(mode_id))
            if mode is None:
                errors.append(
                    f"project {project_id}: mode_map.{intent}={mode_id!r} "
                    "does not resolve to a router mode"
                )
                continue
            resolved_agent = mode.get("agent")
            if isinstance(resolved_agent, str) and resolved_agent not in project_agents:
                errors.append(
                    f"project {project_id}: mode_map.{intent} resolves to "
                    f"{resolved_agent}, which is not in agents"
                )

    manifests = _load_agent_manifests(root)
    for agent_id in sorted(project_agents):
        if agent_id not in manifests:
            errors.append(
                f"agent {agent_id}: no standalone agent.yaml manifest was found"
            )

    if "academic-tfm-research" in declared_profiles:
        local_paths = project.get("local_paths", {})
        if not isinstance(local_paths, dict) or not local_paths.get("tfm_proposal_corpus"):
            warnings.append(
                "academic-tfm-research: tfm_proposal_corpus is not configured; "
                "differentiation must be reported as unverified"
            )

    return errors, warnings, project_id


def main() -> int:
    """Run the configuration resolution validator."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-yaml",
        type=Path,
        help="Adapter project YAML. Defaults to .codex/project.yaml.",
    )
    args = parser.parse_args()
    errors, warnings, project_id = validate_resolution(
        ROOT, args.project_yaml.resolve() if args.project_yaml else None
    )
    if errors:
        print(f"[FAIL] configuration resolution for project {project_id}")
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"[WARN] {warning}")
        return 1

    print(f"[OK] configuration resolution: .codex/project.yaml -> {project_id}")
    print("[OK] project registry -> profiles/mode_map/agents")
    print("[OK] agents -> integrator skills/rules/rubrics/templates/wrappers")
    print("[OK] profiles -> skills/catalog.yaml -> canonical skill paths")
    for warning in warnings:
        print(f"[WARN] {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
