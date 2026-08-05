#!/usr/bin/env python3
"""Synchronize federated skill profiles into the canonical AGENTS guide."""

from __future__ import annotations

import argparse
import sys

try:
    from .validate_skill_catalog import CATALOG, ROOT, _load_yaml, validate_catalog
except ImportError:
    from validate_skill_catalog import CATALOG, ROOT, _load_yaml, validate_catalog

sys.path.insert(0, str(ROOT / "src"))

from negrita_brain.profiles import resolve_profiles  # noqa: E402


AGENTS = ROOT / ".codex" / "skills" / "AGENTS.md"
START = "## Federated Skill Profiles"
END = "## Auto-invoke Skills"


def render_profiles(catalog: dict) -> str:
    """Render a deterministic profile section from the catalog."""
    lines = [
        START,
        "",
        "Generated from `skills/catalog.yaml`; update the catalog first.",
        "",
        "| Profile | Skills |",
        "|---|---|",
    ]
    for profile_id in sorted(catalog["profiles"]):
        closure = resolve_profiles(catalog, [profile_id])
        skills = ", ".join(f"`{skill}`" for skill in closure.skills)
        lines.append(f"| `{profile_id}` | {skills or 'No automatic skills'} |")
    lines.extend(["", ""])
    return "\n".join(lines)


def update_agents(text: str, section: str) -> str:
    """Replace or insert the generated profile section."""
    if START in text:
        before, remainder = text.split(START, 1)
        if END in remainder:
            _, after = remainder.split(END, 1)
            return before + section + END + after
    if END not in text:
        raise ValueError(f"{END!r} heading missing from {AGENTS}")
    before, after = text.split(END, 1)
    return before.rstrip() + "\n\n" + section + END + after


def main() -> int:
    """Validate and optionally write the generated section."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    catalog = _load_yaml(CATALOG)
    errors = validate_catalog(catalog)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    current = AGENTS.read_text(encoding="utf-8")
    updated = update_agents(current, render_profiles(catalog))
    if updated == current:
        print(f"[OK] {AGENTS} already synchronized")
        return 0
    if args.write:
        AGENTS.write_text(updated, encoding="utf-8")
        print(f"[OK] synchronized {AGENTS}")
    else:
        print(f"[DRY-RUN] would synchronize {AGENTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
