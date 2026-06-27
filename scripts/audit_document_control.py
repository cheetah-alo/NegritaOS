"""Audit document-control placement and filename compliance.

This script is intentionally read-only. It reports deliverable artifacts that
are outside a `documents/` folder or whose filename does not include the
required `__updated_YYYYMMDD_HHMMSS` suffix.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DELIVERABLE_EXTENSIONS = {".md", ".pptx", ".ppt", ".pdf", ".docx", ".doc", ".html"}
TIMESTAMPED_NAME = re.compile(
    r"^[a-z0-9][a-z0-9_]*__updated_[0-9]{8}_[0-9]{6}"
    r"\.(md|pptx|ppt|pdf|docx|doc|html)$"
)
EXCLUDED_PARTS = {
    ".agents",
    ".claude",
    ".codex",
    ".cursor",
    ".git",
    "__pycache__",
    "core",
    "node_modules",
    "plots",
    "rules",
    "skills",
    "templates",
}
EXCLUDED_NAMES = {"README.md"}


def is_deliverable(path: Path, root: Path) -> bool:
    """Return whether a file should be governed as a deliverable."""
    if path.suffix.lower() not in DELIVERABLE_EXTENSIONS:
        return False
    if path.name in EXCLUDED_NAMES:
        return False
    relative_parts = path.relative_to(root).parts
    return not any(part in EXCLUDED_PARTS for part in relative_parts)


def audit(root: Path) -> tuple[list[Path], list[Path], list[Path]]:
    """Collect deliverables and non-compliant subsets."""
    deliverables: list[Path] = []
    outside_documents: list[Path] = []
    missing_timestamp: list[Path] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or not is_deliverable(path, root):
            continue
        deliverables.append(path)
        relative_parts = path.relative_to(root).parts
        if "documents" not in relative_parts[:-1]:
            outside_documents.append(path)
        if not TIMESTAMPED_NAME.match(path.name):
            missing_timestamp.append(path)

    return deliverables, outside_documents, missing_timestamp


def print_section(title: str, root: Path, paths: list[Path], limit: int) -> None:
    """Print a bounded list of relative paths."""
    print(f"\n{title}: {len(paths)}")
    for path in paths[:limit]:
        print(f"- {path.relative_to(root)}")
    if len(paths) > limit:
        print(f"- ... {len(paths) - limit} more")


def main() -> int:
    """Run the document-control audit."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Work root to audit")
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of paths to print per section",
    )
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"root must be an existing directory: {root}")

    deliverables, outside_documents, missing_timestamp = audit(root)
    print(f"Document-control audit root: {root}")
    print(f"Deliverables scanned: {len(deliverables)}")
    print_section("Outside documents/", root, outside_documents, args.limit)
    print_section("Missing timestamp suffix", root, missing_timestamp, args.limit)

    if outside_documents or missing_timestamp:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
