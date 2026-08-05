"""Skill profile inheritance and deterministic closure resolution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .errors import ProfileResolutionError


@dataclass(frozen=True)
class ProfileClosure:
    """Ordered profile and skill closure for one project."""

    profiles: tuple[str, ...]
    skills: tuple[str, ...]


def _as_ids(value: Any, label: str) -> list[str]:
    """Validate and normalize one profile id list."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ProfileResolutionError(f"{label} must be a string or list of strings")


def resolve_profiles(catalog: dict[str, Any], requested: list[str]) -> ProfileClosure:
    """Resolve profiles parent-first with stable de-duplication and cycle checks."""
    definitions = catalog.get("profiles")
    if not isinstance(definitions, dict):
        raise ProfileResolutionError("catalog.profiles must be a mapping")
    ordered_profiles: list[str] = []
    ordered_skills: list[str] = []
    resolved: set[str] = set()
    visiting: list[str] = []

    def visit(profile_id: str) -> None:
        if profile_id in resolved:
            return
        if profile_id in visiting:
            cycle = " -> ".join([*visiting, profile_id])
            raise ProfileResolutionError(f"Profile inheritance cycle: {cycle}")
        profile = definitions.get(profile_id)
        if not isinstance(profile, dict):
            raise ProfileResolutionError(f"Unknown profile: {profile_id}")
        visiting.append(profile_id)
        for parent_id in _as_ids(profile.get("extends"), f"profiles.{profile_id}.extends"):
            visit(parent_id)
        visiting.pop()
        resolved.add(profile_id)
        ordered_profiles.append(profile_id)
        for skill_id in _as_ids(profile.get("skills", []), f"profiles.{profile_id}.skills"):
            if skill_id not in ordered_skills:
                ordered_skills.append(skill_id)

    defaults = catalog.get("defaults", {})
    default_profiles = (
        _as_ids(defaults.get("profiles"), "catalog.defaults.profiles")
        if isinstance(defaults, dict)
        else []
    )
    for requested_id in [*default_profiles, *requested]:
        visit(requested_id)
    return ProfileClosure(tuple(ordered_profiles), tuple(ordered_skills))


def resolve_project_profiles(
    catalog: dict[str, Any], project: dict[str, Any]
) -> ProfileClosure:
    """Resolve the defaults and declared profiles for one project."""
    requested = _as_ids(project.get("skill_profiles", []), "project.skill_profiles")
    return resolve_profiles(catalog, requested)
