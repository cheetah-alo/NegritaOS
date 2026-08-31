#!/usr/bin/env python3
"""Validate governed browser routing across registered NegritaOS projects."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    from .validate_skill_catalog import ROOT, _load_yaml
except ImportError:
    from validate_skill_catalog import ROOT, _load_yaml

sys.path.insert(0, str(ROOT / "src"))

from negrita_brain.browser_routing import (  # noqa: E402
    load_browser_routing_config,
    validate_browser_routing_config,
    validate_project_browser_context,
    verify_local_brave_profiles,
)


def _project_mapping(data: dict[str, Any]) -> dict[str, Any] | None:
    project = data.get("project")
    if isinstance(project, dict):
        return project
    legacy = data.get("project_registry")
    if isinstance(legacy, dict) and isinstance(legacy.get("project_id"), str):
        return {"id": legacy["project_id"], **legacy}
    return None


def validate_all(
    root: Path = ROOT, *, verify_local_profiles: bool = False
) -> tuple[list[str], int]:
    """Return errors and number of project registries checked."""
    errors: list[str] = []
    config = load_browser_routing_config(root)
    errors.extend(validate_browser_routing_config(config))
    checked = 0
    for registry in sorted((root / "projects").glob("*.yaml")):
        data = _load_yaml(registry)
        project = _project_mapping(data)
        if project is None:
            continue
        checked += 1
        errors.extend(validate_project_browser_context(project, config))
    if verify_local_profiles:
        errors.extend(verify_local_brave_profiles(config))
    return errors, checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify-local-profiles",
        action="store_true",
        help="Also verify Brave profile directories and display names on this host.",
    )
    args = parser.parse_args()
    try:
        errors, checked = validate_all(
            ROOT, verify_local_profiles=args.verify_local_profiles
        )
    except Exception as exc:
        print(f"[FAIL] browser profile routing could not be loaded: {exc}")
        return 1
    if errors:
        print("Browser profile routing validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    suffix = " with local Brave metadata" if args.verify_local_profiles else ""
    print(f"[OK] browser profile routing: {checked} projects{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
