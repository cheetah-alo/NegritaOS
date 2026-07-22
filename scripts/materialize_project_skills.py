#!/usr/bin/env python3
"""Link canonical profile skills into a NegritaOS sibling adapter."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path

try:
    from .validate_skill_catalog import CATALOG, ROOT, _load_yaml
except ImportError:
    from validate_skill_catalog import CATALOG, ROOT, _load_yaml


def _registry_path(adapter: dict, repo: Path) -> Path:
    """Resolve the canonical project registry from an adapter."""
    raw = adapter.get("negrita_registry")
    if not isinstance(raw, str) or not raw:
        raise ValueError(f"{repo / '.codex/project.yaml'} has no negrita_registry")
    path = Path(raw).expanduser()
    return path if path.is_absolute() else (repo / path).resolve()


def selected_skills(catalog: dict, project: dict) -> list[str]:
    """Return unique canonical skill IDs in declared profile order."""
    selected: list[str] = []
    for profile_id in project.get("skill_profiles", []):
        profile = catalog["profiles"].get(profile_id)
        if profile is None:
            raise ValueError(f"Unknown project skill profile: {profile_id}")
        for skill_id in profile.get("skills", []):
            if skill_id not in selected:
                selected.append(skill_id)
    return selected


def materialize(repo: Path, dry_run: bool) -> int:
    """Materialize selected canonical skills into a project adapter."""
    adapter_path = repo / ".codex" / "project.yaml"
    if not adapter_path.is_file():
        raise ValueError(f"missing adapter: {adapter_path}")
    adapter = _load_yaml(adapter_path)
    registry_path = _registry_path(adapter, repo)
    registry = _load_yaml(registry_path).get("project", {})
    if not isinstance(registry, dict):
        raise ValueError(f"invalid project registry: {registry_path}")
    catalog = _load_yaml(CATALOG)
    selected = selected_skills(catalog, registry)
    if not selected:
        print(f"[OK] {repo}: no skill_profiles declared; nothing to materialize")
        return 0

    skills_by_id = {entry["id"]: entry for entry in catalog["skills"]}
    target_root = repo / ".codex" / "skills"
    if not target_root.exists() and dry_run:
        print(f"[DRY-RUN] would create {target_root}")
    elif not target_root.exists():
        target_root.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    for skill_id in selected:
        entry = skills_by_id[skill_id]
        source_file = (ROOT / entry["path"]).resolve()
        source = source_file.parent
        destination = target_root / source.name
        if destination.is_symlink() and destination.resolve() == source:
            print(f"[OK] {skill_id}: already linked")
            continue
        backup = destination.with_name(f"{destination.name}.preCanonical.{timestamp}")
        if destination.exists() or destination.is_symlink():
            if dry_run:
                print(f"[DRY-RUN] {skill_id}: backup {backup} then link {source}")
                continue
            shutil.move(str(destination), str(backup))
            print(f"[BACKUP] {destination} -> {backup}")
        if dry_run:
            print(f"[DRY-RUN] {skill_id}: link {destination} -> {source}")
            continue
        destination.symlink_to(source, target_is_directory=True)
        print(f"[LINK] {skill_id}: {destination} -> {source}")
    return 0


def main() -> int:
    """Parse arguments and materialize the project profile."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return materialize(args.repo.expanduser().resolve(), args.dry_run)
    except (OSError, ValueError, KeyError) as exc:
        print(f"[FAIL] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
