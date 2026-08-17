#!/usr/bin/env python3
"""Quick validation for NegritaOS skill folders."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


PATH_PREFIXES = (".", "brands/", "rules/", "skills/", "templates/")
SHELL_MARKERS = (" ", "\t", "\n", "$", "|", ";", "&", ">", "<")
GLOB_MARKERS = "*?[]"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
      if ":" not in line:
        continue
      key, value = line.split(":", 1)
      data[key.strip()] = value.strip()
    return data


def is_verifiable_path_reference(value: str) -> bool:
    """Return true for single path-like code spans, not shell commands."""
    if not value.startswith(PATH_PREFIXES) or "/" not in value:
        return False
    return not any(marker in value for marker in SHELL_MARKERS)


def validate_skill(root: pathlib.Path) -> list[str]:
    failures: list[str] = []
    skill = root / "SKILL.md"
    if not skill.exists():
        return [f"{root}: missing SKILL.md"]
    text = skill.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    if "name" not in frontmatter:
        failures.append("SKILL.md frontmatter missing name")
    if "description" not in frontmatter:
        failures.append("SKILL.md frontmatter missing description")
    body_lines = text.splitlines()
    if len(body_lines) > 520:
        failures.append(f"SKILL.md too long: {len(body_lines)} lines")
    if (root / "references").exists():
        refs = list((root / "references").rglob("*.md"))
        if not refs:
            failures.append("references/ exists but has no markdown references")
    if (root / "scripts").exists():
        scripts = list((root / "scripts").iterdir())
        if not scripts:
            failures.append("scripts/ exists but is empty")
        for script in scripts:
            if script.is_file() and script.suffix not in {".mjs", ".js", ".py", ".sh"}:
                failures.append(f"unexpected script suffix: {script}")
    workspace = pathlib.Path.cwd()
    linked_paths = re.findall(r"`([^`\n]+)`", text)
    for linked in linked_paths:
        if not is_verifiable_path_reference(linked):
            continue
        if any(marker in linked for marker in GLOB_MARKERS):
            if not list(workspace.glob(linked)):
                failures.append(f"referenced path pattern has no matches: {linked}")
            continue
        candidate = (workspace / linked).resolve()
        if not candidate.exists():
            failures.append(f"referenced path missing: {linked}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Skill folder to validate")
    args = parser.parse_args()
    root = pathlib.Path(args.path)
    failures = validate_skill(root)
    if failures:
        print(f"[FAIL] quick validation failed for {root}", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"[OK] quick validation passed for {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
