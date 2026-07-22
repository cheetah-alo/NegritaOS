"""Validate file references in NegritaOS registry and governance files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SYSTEM_EXTENSIONS = ("md", "yaml", "yml", "docx", "pptx")
ADAPTER_RELATIVE_PREFIXES = (
    ".codex/",
    ".claude/",
)
ROOT_RELATIVE_PREFIXES = (
    "academic-layer/",
    "agents/",
    "archetypes/",
    "brands/",
    "business-layer/",
    "core/",
    "docs/",
    "intelligence-layer/",
    "projects/",
    "rubrics/",
    "rules/",
    "skills/",
    "strategic-layer/",
    "technical-layr/",
    "templates/",
)
CODEX_RELATIVE_PREFIXES = (
    "profiles/",
    "rules/",
    "skills/",
)
PATH_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_-])(?P<path>(?:"
    + "|".join(
        re.escape(prefix)
        for prefix in (
            ADAPTER_RELATIVE_PREFIXES + ROOT_RELATIVE_PREFIXES + CODEX_RELATIVE_PREFIXES
        )
    )
    + r")[A-Za-z0-9_./ -]+?\.(?:"
    + "|".join(SYSTEM_EXTENSIONS)
    + r"))"
)

OPTIONAL_REFERENCE_MARKERS = (
    "if exists",
    "if present",
    "per-project",
    "create ",
    "created/",
    "created or updated",
    "created/updated",
    "write ",
    "writes ",
    "output",
    "placeholder",
    "template_name",
    "yyyy",
    "<",
    ">",
)

REFERENCE_ONLY_SOURCE_PREFIXES = (
    "skills/skills_engram/",
    "skills/skill_nate/",
)


def iter_source_files(root: Path) -> list[Path]:
    """Return governance files whose path references should be validated."""
    files: list[Path] = []
    for extension in ("*.yaml", "*.yml", "*.md"):
        files.extend(root.glob(extension))
        for directory in (
            ".codex",
            "academic-layer",
            "agents",
            "archetypes",
            "business-layer",
            "core",
            "docs",
            "intelligence-layer",
            "projects",
            "rubrics",
            "rules",
            "skills",
            "strategic-layer",
            "technical-layr",
            "templates",
        ):
            files.extend((root / directory).rglob(extension))
    return sorted({path for path in files if path.is_file()})


def resolve_reference(root: Path, source_path: Path, reference: str) -> Path:
    """Resolve a reference against the repo root or canonical .codex root."""
    if reference.startswith(".claude/"):
        return root / ".codex" / reference.removeprefix(".claude/")
    if reference.startswith(".codex/"):
        return root / reference
    if source_path.relative_to(root).parts[:1] == (".codex",):
        codex_candidate = root / ".codex" / reference
        if codex_candidate.exists():
            return codex_candidate
    root_candidate = root / reference
    if root_candidate.exists():
        return root_candidate
    if reference.startswith(CODEX_RELATIVE_PREFIXES):
        codex_candidate = root / ".codex" / reference
        if codex_candidate.exists():
            return codex_candidate
    return root_candidate


def is_optional_or_placeholder_reference(
    source_path: Path, line: str, reference: str
) -> bool:
    """Return whether a missing reference is an example, placeholder, or output path."""
    line_lower = line.lower()
    reference_lower = reference.lower()
    if any(marker in line_lower for marker in OPTIONAL_REFERENCE_MARKERS):
        return True
    if "template_name" in reference_lower:
        return True
    if source_path.name == "prompt_examples_catalog.md" and reference.startswith(
        ("projects/", "templates/")
    ):
        return True
    if reference == "templates/analytical_report_template.md":
        return True
    if reference == "docs/task_tracker.md":
        return True
    return False


def collect_missing_paths(root: Path) -> list[tuple[Path, int, str]]:
    """Collect missing path references with source file and line number."""
    missing: list[tuple[Path, int, str]] = []
    for source_path in iter_source_files(root):
        relative_source = source_path.relative_to(root).as_posix()
        if relative_source.startswith(REFERENCE_ONLY_SOURCE_PREFIXES):
            continue
        try:
            text = source_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in PATH_PATTERN.finditer(line):
                reference = match.group("path").strip().rstrip(".,;:)")
                if not resolve_reference(root, source_path, reference).exists():
                    if is_optional_or_placeholder_reference(
                        source_path, line, reference
                    ):
                        continue
                    missing.append((source_path, line_number, reference))
    return missing


def main() -> int:
    """Run the registry path validation command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=Path.cwd(),
        type=Path,
        help="Repository root to validate. Defaults to the current directory.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    missing = collect_missing_paths(root)
    if missing:
        print("Missing path references:")
        for source_path, line_number, reference in missing:
            print(f"- {source_path.relative_to(root)}:{line_number} -> {reference}")
        return 1

    print("All registry path references resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
