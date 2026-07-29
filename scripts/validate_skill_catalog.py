#!/usr/bin/env python3
"""Validate the NegritaOS federated skill catalog and optional project profile."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "skills" / "catalog.yaml"
VALID_STATUSES = {"canonical", "adapted", "reference_only"}
VALID_PROVIDERS = {"bigquery", "postgresql", "files", "api", "other"}
VALID_ANALYSIS_PHASES = {"warn_first", "fail_closed"}


def _load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML with PyYAML and fall back to Ruby Psych when needed."""
    try:
        import yaml  # type: ignore[import-not-found]

        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (ImportError, ModuleNotFoundError):
        ruby = (
            "require 'yaml'; require 'json'; "
            "puts JSON.generate(YAML.load_file(ARGV.fetch(0)))"
        )
        output = subprocess.check_output(
            ["ruby", "-e", ruby, str(path)], text=True
        )
        value = json.loads(output)
    if not isinstance(value, dict):
        raise ValueError(f"Expected mapping in {path}")
    return value


def _frontmatter_name(path: Path) -> str | None:
    """Return a skill name from the first YAML frontmatter block."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^name:\s*([A-Za-z0-9_-]+)\s*$", line)
        if match:
            return match.group(1)
    return None


def _path(value: str) -> Path:
    """Resolve a catalog path relative to the repository root."""
    return ROOT / value


def validate_catalog(catalog: dict[str, Any]) -> list[str]:
    """Return validation errors for the catalog structure and files."""
    errors: list[str] = []
    profiles = catalog.get("profiles")
    skills = catalog.get("skills")
    if not isinstance(profiles, dict):
        errors.append("catalog.profiles must be a mapping")
        profiles = {}
    if not isinstance(skills, list):
        errors.append("catalog.skills must be a list")
        skills = []

    by_id: dict[str, dict[str, Any]] = {}
    canonical_paths: set[str] = set()
    for index, entry in enumerate(skills):
        if not isinstance(entry, dict):
            errors.append(f"catalog.skills[{index}] must be a mapping")
            continue
        skill_id = entry.get("id")
        path_value = entry.get("path")
        status = entry.get("status")
        if not isinstance(skill_id, str) or not skill_id:
            errors.append(f"catalog.skills[{index}] has no valid id")
            continue
        if skill_id in by_id:
            errors.append(f"duplicate skill id: {skill_id}")
        by_id[skill_id] = entry
        if status not in VALID_STATUSES:
            errors.append(f"{skill_id}: invalid status {status!r}")
        if not isinstance(path_value, str):
            errors.append(f"{skill_id}: path must be a string")
            continue
        if path_value in canonical_paths:
            errors.append(f"duplicate canonical path: {path_value}")
        canonical_paths.add(path_value)
        path = _path(path_value)
        if not path.is_file():
            errors.append(f"{skill_id}: missing canonical path {path_value}")
            continue
        if status in {"canonical", "adapted"} and path.name == "SKILL.md":
            if path.parent.name != skill_id:
                errors.append(
                    f"{skill_id}: directory {path.parent.name!r} does not match id"
                )
            frontmatter_name = _frontmatter_name(path)
            if frontmatter_name != skill_id:
                errors.append(
                    f"{skill_id}: frontmatter name {frontmatter_name!r} does not match"
                )
        native_path = entry.get("native_path")
        if native_path is not None and not _path(str(native_path)).is_file():
            errors.append(f"{skill_id}: missing native path {native_path}")
        source = entry.get("source")
        if isinstance(source, str) and source not in {"NegritaOS-native"}:
            if not _path(source).exists():
                errors.append(f"{skill_id}: missing source path {source}")

    for profile_id, profile in profiles.items():
        if not isinstance(profile, dict):
            errors.append(f"profile {profile_id}: must be a mapping")
            continue
        profile_skills = profile.get("skills", [])
        if not isinstance(profile_skills, list):
            errors.append(f"profile {profile_id}: skills must be a list")
            continue
        for skill_id in profile_skills:
            if skill_id not in by_id:
                errors.append(f"profile {profile_id}: unknown skill {skill_id}")
            elif profile_id not in by_id[skill_id].get("profiles", []):
                errors.append(
                    f"{skill_id}: missing reverse profile mapping {profile_id}"
                )

    source_mappings = catalog.get("source_mappings", {})
    if not isinstance(source_mappings, dict):
        errors.append("catalog.source_mappings must be a mapping")
    else:
        for source_id, mapping in source_mappings.items():
            if not isinstance(mapping, dict):
                errors.append(f"source mapping {source_id}: must be a mapping")
                continue
            root = mapping.get("root")
            if isinstance(root, str) and not _path(root).is_dir():
                errors.append(f"source mapping {source_id}: missing root {root}")
            normalized_to = mapping.get("normalized_to", {})
            if isinstance(normalized_to, dict):
                for source_skill, target_skills in normalized_to.items():
                    if not isinstance(target_skills, list):
                        errors.append(
                            f"source mapping {source_id}: normalized_to.{source_skill} must be a list"
                        )
                        continue
                    for target_skill in target_skills:
                        if target_skill not in by_id:
                            errors.append(
                                f"source mapping {source_id}: unknown normalized skill {target_skill}"
                            )

    return errors


def validate_project(catalog: dict[str, Any], project_path: Path) -> list[str]:
    """Validate one project's profile and data-source declarations."""
    errors: list[str] = []
    project = _load_yaml(project_path).get("project", {})
    if not isinstance(project, dict):
        return [f"{project_path}: project must be a mapping"]
    profiles = catalog.get("profiles", {})
    declared_profiles = project.get("skill_profiles", [])
    if not isinstance(declared_profiles, list):
        errors.append(f"{project_path}: skill_profiles must be a list")
    else:
        for profile_id in declared_profiles:
            if profile_id not in profiles:
                errors.append(f"{project_path}: unknown profile {profile_id}")
    if "data-source-bigquery" in declared_profiles and "analytical-eda" not in declared_profiles:
        # The provider profile is also useful for dashboards, but analysis
        # projects must opt into the provider-neutral EDA entry gate explicitly.
        if "elal-eda-governance" not in declared_profiles:
            errors.append(
                f"{project_path}: BigQuery analysis profile requires analytical-eda "
                "or an explicit ELAL EDA governance profile"
            )
    integration_branch = project.get("integration_branch")
    if integration_branch is not None and (
        not isinstance(integration_branch, str) or not integration_branch.strip()
    ):
        errors.append(f"{project_path}: integration_branch must be a non-empty string")
    data_source = project.get("data_source")
    if "data-source-bigquery" in declared_profiles and data_source is None:
        errors.append(
            f"{project_path}: data_source is required when data-source-bigquery is declared"
        )
    if data_source is not None:
        if not isinstance(data_source, dict):
            errors.append(f"{project_path}: data_source must be a mapping")
        else:
            provider = data_source.get("provider")
            if provider not in VALID_PROVIDERS:
                errors.append(
                    f"{project_path}: unsupported data_source.provider {provider!r}"
                )
            for key in ("dialect", "source_of_truth", "access"):
                if not data_source.get(key):
                    errors.append(f"{project_path}: data_source.{key} is required")
            for profile_id in declared_profiles:
                profile = profiles.get(profile_id, {})
                profile_source = profile.get("data_source")
                if not isinstance(profile_source, dict):
                    continue
                if profile_source.get("provider") != provider:
                    errors.append(
                        f"{project_path}: profile {profile_id} expects "
                        f"provider {profile_source.get('provider')!r}, got {provider!r}"
                    )
                dialects = profile_source.get("dialects", [])
                if dialects and data_source.get("dialect") not in dialects:
                    errors.append(
                        f"{project_path}: dialect {data_source.get('dialect')!r} "
                        f"is not allowed by profile {profile_id}"
                    )
    governance = project.get("analysis_governance")
    if governance is not None:
        if not isinstance(governance, dict):
            errors.append(f"{project_path}: analysis_governance must be a mapping")
        else:
            phase = governance.get("phase")
            if phase not in VALID_ANALYSIS_PHASES:
                errors.append(
                    f"{project_path}: analysis_governance.phase must be one of "
                    f"{sorted(VALID_ANALYSIS_PHASES)}"
                )
            scope = governance.get("scope")
            if not isinstance(scope, str) or not scope.strip():
                errors.append(f"{project_path}: analysis_governance.scope must be a non-empty string")
    return errors


def main() -> int:
    """Run catalog and optional project validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path)
    args = parser.parse_args()
    try:
        catalog = _load_yaml(CATALOG)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load catalog: {exc}")
        return 1
    errors = validate_catalog(catalog)
    if args.project is not None:
        errors.extend(validate_project(catalog, args.project.resolve()))
    if errors:
        print("Skill catalog validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"[OK] skill catalog: {len(catalog.get('skills', []))} skills, "
        f"{len(catalog.get('profiles', {}))} profiles"
    )
    if args.project is not None:
        print(f"[OK] project profile: {args.project.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
