"""Validate file references in NegritaOS registry and governance files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SYSTEM_EXTENSIONS = ("md", "yaml", "yml", "docx", "pptx")
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
    + "|".join(re.escape(prefix) for prefix in ROOT_RELATIVE_PREFIXES + CODEX_RELATIVE_PREFIXES)
    + r")[A-Za-z0-9_./ -]+?\.(?:"
    + "|".join(SYSTEM_EXTENSIONS)
    + r"))"
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
    """Resolve a reference against the repo root or .codex root."""
    if source_path.relative_to(root).parts[:1] == (".codex",):
        codex_candidate = root / ".codex" / reference
        if codex_candidate.exists():
            return codex_candidate
    return root / reference


def collect_missing_paths(root: Path) -> list[tuple[Path, int, str]]:
    """Collect missing path references with source file and line number."""
    missing: list[tuple[Path, int, str]] = []
    for source_path in iter_source_files(root):
        try:
            text = source_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in PATH_PATTERN.finditer(line):
                reference = match.group("path").strip().rstrip(".,;:)")
                if not resolve_reference(root, source_path, reference).exists():
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
