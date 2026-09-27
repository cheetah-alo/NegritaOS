"""Read-only local capability catalog for the NegritaOS 360 dashboard."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .config import load_yaml
from .dashboard_local_service import LocalCatalogError, LocalCatalogService
from .profiles import ProfileResolutionError, resolve_project_profiles


class LocalCapabilityError(ValueError):
    """Raised when an authorized capability source is malformed or inconsistent."""


class LocalCapabilityService:
    """Build a deterministic capability view from authorized local registries."""

    def __init__(self, work_root: Path, access_path: Path) -> None:
        if not isinstance(work_root, Path) or not isinstance(access_path, Path):
            raise LocalCapabilityError("work_root and access_path must be pathlib.Path values")
        self._work_root = work_root
        self._access_path = access_path

    def read_capabilities(
        self,
        requested_project_id: str | None = None,
        kind: str | None = None,
    ) -> dict[str, object]:
        """Return the authorized local capability view.

        Authorization is completed by ``LocalCatalogService`` before any
        capability source is read.  Only exact project YAML files for visible
        project IDs, plus the two canonical global registries, are inspected.
        """
        if requested_project_id is not None and not _valid_id(requested_project_id):
            raise LocalCapabilityError("requested_project_id is invalid")
        if kind is not None and kind not in {"agent", "skill", "rule"}:
            raise LocalCapabilityError("kind is invalid")

        try:
            visible_catalog = LocalCatalogService(
                self._work_root, self._access_path
            ).read_catalog()
        except LocalCatalogError as exc:
            raise LocalCapabilityError("local capability authorization failed") from exc

        visible = {project.project_id: project for project in visible_catalog.projects}
        if requested_project_id is not None:
            visible = {
                project_id: project
                for project_id, project in visible.items()
                if project_id == requested_project_id
            }
        if not visible:
            return _response(())

        try:
            skills_catalog = _load_exact_mapping(self._work_root / "skills" / "catalog.yaml")
            integrator = _load_exact_mapping(self._work_root / "integrator.yaml")
            global_rules = _global_rules(integrator)
            registered_agents = _registered_agents(integrator)
            items: list[dict[str, str]] = []
            for project_id in sorted(visible):
                project = _load_visible_project(self._work_root, project_id, visible[project_id])
                items.extend(
                    _project_capabilities(project_id, project, skills_catalog, registered_agents)
                )
                items.extend(
                    _rule_item(project_id, reference, "DECLARED")
                    for reference in global_rules
                )
        except LocalCapabilityError:
            raise
        except (OSError, TypeError, ValueError, ProfileResolutionError) as exc:
            raise LocalCapabilityError("local capability source is invalid") from exc

        deduplicated = {
            (item["project_id"], item["kind"], item["id"]): item for item in items
        }
        selected = tuple(
            deduplicated[key]
            for key in sorted(deduplicated)
            if kind is None or key[1] == kind
        )
        return _response(selected)


def _project_capabilities(
    project_id: str,
    project: Mapping[str, Any],
    skills_catalog: Mapping[str, Any],
    registered_agents: set[str],
) -> list[dict[str, str]]:
    if "project" in project:
        payload = project["project"]
        if not isinstance(payload, Mapping):
            raise LocalCapabilityError("project declaration is invalid")
        agents = _list_only(payload.get("agents", []), "project.agents")
        try:
            closure = resolve_project_profiles(dict(skills_catalog), dict(payload))
        except ProfileResolutionError as exc:
            raise LocalCapabilityError("skill profile resolution failed") from exc
        known_skills = _catalog_skill_ids(skills_catalog)
        if any(skill_id not in known_skills for skill_id in closure.skills):
            raise LocalCapabilityError("resolved skill is not registered")
        items = [
            _named_item(
                project_id, "agent", agent,
                "REGISTERED" if agent in registered_agents else "DECLARED",
            )
            for agent in agents
        ]
        items.extend(
            _named_item(project_id, "skill", skill_id, "RESOLVED")
            for skill_id in closure.skills
        )
        return items

    if "project_registry" not in project:
        raise LocalCapabilityError("project declaration is missing")
    payload = project["project_registry"]
    if not isinstance(payload, Mapping):
        raise LocalCapabilityError("legacy project declaration is invalid")
    items: list[dict[str, str]] = []
    agents = payload.get("agents", {})
    if not isinstance(agents, Mapping):
        raise LocalCapabilityError("legacy agents declaration is invalid")
    for group in ("primary", "secondary"):
        items.extend(
            _named_item(project_id, "agent", agent, "DECLARED")
            for agent in _list_only(agents.get(group, []), f"agents.{group}")
        )
    skills = payload.get("skills", {})
    if not isinstance(skills, Mapping):
        raise LocalCapabilityError("legacy skills declaration is invalid")
    items.extend(
        _legacy_skill_item(project_id, skill)
        for skill in _list_only(skills.get("required", []), "skills.required")
    )

    rules = payload.get("rules", {})
    if not isinstance(rules, Mapping):
        raise LocalCapabilityError("legacy rules declaration is invalid")
    for field in ("inherit", "domains", "project_specific"):
        values = rules.get(field, [])
        if isinstance(values, str):
            values = [values]
        if not isinstance(values, list):
            raise LocalCapabilityError(f"rules.{field} must be a list or string")
        items.extend(_rule_item(project_id, value, "DECLARED") for value in values)
    return items


def _load_visible_project(work_root: Path, project_id: str, visible: Any) -> dict[str, Any]:
    path = work_root / "projects" / f"{project_id}.yaml"
    raw = _load_exact_mapping(path)
    if "project" in raw:
        payload = raw["project"]
        raw_id = payload.get("id") if isinstance(payload, Mapping) else None
        metadata = payload.get("metadata", {}) if isinstance(payload, Mapping) else {}
        client = metadata.get("client_id") if isinstance(metadata, Mapping) else None
    elif "project_registry" in raw:
        payload = raw["project_registry"]
        raw_id = payload.get("project_id") if isinstance(payload, Mapping) else None
        client = None
    else:
        raise LocalCapabilityError("project source schema is invalid")
    if raw_id != project_id or getattr(visible, "client_id", None) != client:
        raise LocalCapabilityError("project source does not match authorization")
    return raw


def _load_exact_mapping(path: Path) -> dict[str, Any]:
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    except OSError as exc:
        raise LocalCapabilityError("local capability source is unavailable") from exc
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise LocalCapabilityError("local capability source is unavailable")
        os.close(descriptor)
        descriptor = -1
        # Parse through the canonical loader only after the exact file check.
        value = load_yaml(path)
    except LocalCapabilityError:
        raise
    except Exception as exc:
        # PyYAML and the optional Ruby fallback raise different parser errors.
        # Redact either family at this local source boundary.
        raise LocalCapabilityError("local capability source is invalid") from exc
    finally:
        if descriptor != -1:
            os.close(descriptor)
    if not isinstance(value, dict):
        raise LocalCapabilityError("local capability source must be a mapping")
    return value


def _catalog_skill_ids(catalog: Mapping[str, Any]) -> set[str]:
    skills = catalog.get("skills")
    if not isinstance(skills, list):
        raise LocalCapabilityError("skills catalog is invalid")
    ids: set[str] = set()
    for skill in skills:
        if not isinstance(skill, Mapping) or not _valid_id(skill.get("id")):
            raise LocalCapabilityError("skills catalog contains an invalid skill")
        ids.add(skill["id"])
    return ids


def _global_rules(integrator: Mapping[str, Any]) -> list[str]:
    negrita_os = integrator.get("negrita_os")
    if not isinstance(negrita_os, Mapping):
        raise LocalCapabilityError("integrator global rules are missing")
    return _list_only(negrita_os.get("global_rules", []), "negrita_os.global_rules")


def _registered_agents(integrator: Mapping[str, Any]) -> set[str]:
    negrita_os = integrator.get("negrita_os")
    if not isinstance(negrita_os, Mapping):
        raise LocalCapabilityError("integrator agents are unavailable")
    agents = negrita_os.get("agents", {})
    if not isinstance(agents, Mapping) or not all(_valid_id(agent) for agent in agents):
        raise LocalCapabilityError("integrator agents are invalid")
    return set(agents)


def _string_list(value: Any, label: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise LocalCapabilityError(f"{label} must contain strings")
    return [item.strip() for item in value]


def _list_only(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise LocalCapabilityError(f"{label} must be a list of strings")
    return [item.strip() for item in value]


def _named_item(project_id: str, kind: str, name: str, state: str) -> dict[str, str]:
    if not _valid_id(name):
        raise LocalCapabilityError("capability name is invalid")
    return {
        "id": name,
        "project_id": project_id,
        "kind": kind,
        "name": name,
        "configuration_state": state,
    }


def _legacy_skill_item(project_id: str, reference: str) -> dict[str, str]:
    basename = _basename(reference)
    if not basename:
        raise LocalCapabilityError("legacy skill reference is invalid")
    return {
        "id": basename,
        "project_id": project_id,
        "kind": "skill",
        "name": basename,
        "configuration_state": "DECLARED",
    }


def _rule_item(project_id: str, reference: str, state: str) -> dict[str, str]:
    if not isinstance(reference, str) or not reference.strip():
        raise LocalCapabilityError("rule reference is invalid")
    value = reference.strip()
    basename = _basename(value)
    if "/" in value or "\\" in value:
        item_id = f"rule-{hashlib.sha256(value.encode('utf-8')).hexdigest()}"
        name = basename
    else:
        item_id = value
        name = value
    return {
        "id": item_id,
        "project_id": project_id,
        "kind": "rule",
        "name": name,
        "configuration_state": state,
    }


def _basename(value: str) -> str:
    return value.replace("\\", "/").rstrip("/").split("/")[-1]


def _valid_id(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and all(
        char.isalnum() or char in "_-" for char in value
    ) and value[0].isalpha()


def _response(items: Sequence[dict[str, str]]) -> dict[str, object]:
    normalized = [dict(item) for item in items]
    digest = hashlib.sha256(
        json.dumps(
            normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")
    ).hexdigest()
    return {
        "state": "READY" if normalized else "EMPTY",
        "items": normalized,
        "provenance": {"snapshot_id": f"view-{digest[:20]}", "view_sha256": digest},
    }
