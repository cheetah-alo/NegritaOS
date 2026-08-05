"""Document routing checks and non-mutating legacy artifact cataloging."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Iterable

from .config import ProjectContext, project_memory_home
from .models import append_jsonl, iso_timestamp


DELIVERABLE_EXTENSIONS = {".md", ".pptx", ".ppt", ".pdf", ".docx", ".doc", ".html"}
TIMESTAMPED_NAME = re.compile(
    r"^[a-z0-9][a-z0-9_]*__updated_[0-9]{8}_[0-9]{6}"
    r"\.(md|pptx|ppt|pdf|docx|doc|html)$"
)
SOURCE_PARTS = {
    ".agents",
    ".claude",
    ".codex",
    ".cursor",
    ".git",
    ".github",
    "__pycache__",
    "brands",
    "core",
    "docs",
    "node_modules",
    "plots",
    "prompts",
    "projects",
    "repos_structure",
    "rules",
    "scripts",
    "skills",
    "src",
    "templates",
    "tests",
    "vendor",
    "zsmash",
}
SOURCE_NAMES = {
    "AGENTS.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "LICENSE.md",
    "README.md",
}


def is_deliverable(path: Path, root: Path) -> bool:
    """Return whether a file is an authored deliverable rather than source docs."""
    if path.suffix.lower() not in DELIVERABLE_EXTENSIONS or path.name in SOURCE_NAMES:
        return False
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    return not any(part in SOURCE_PARTS for part in parts[:-1])


def is_compliant_deliverable(path: Path, root: Path) -> bool:
    """Return whether a deliverable follows directory and timestamp policy."""
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return (
        bool(relative.parts)
        and relative.parts[0] == "documents"
        and TIMESTAMPED_NAME.fullmatch(path.name) is not None
    )


def iter_deliverables(root: Path) -> Iterable[Path]:
    """Yield deliverables without following directory symlinks explicitly."""
    for path in sorted(root.rglob("*")):
        if path.is_file() and is_deliverable(path, root):
            yield path


def _safe_digest(path: Path, root: Path) -> str | None:
    """Hash local files while avoiding downloads from cloud evidence workspaces."""
    if "/Library/CloudStorage/" in str(root):
        return None
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        return None
    return digest.hexdigest()


def audit_documents(root: Path) -> dict[str, list[str]]:
    """Return relative deliverable paths grouped by compliance state."""
    deliverables = list(iter_deliverables(root))
    outside = []
    missing_timestamp = []
    for path in deliverables:
        relative_path = path.relative_to(root)
        relative = str(relative_path)
        if not relative_path.parts or relative_path.parts[0] != "documents":
            outside.append(relative)
        if TIMESTAMPED_NAME.fullmatch(path.name) is None:
            missing_timestamp.append(relative)
    return {
        "deliverables": [str(path.relative_to(root)) for path in deliverables],
        "outside_documents": outside,
        "missing_timestamp": missing_timestamp,
    }


def catalog_legacy(
    context: ProjectContext,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Append changed legacy artifact metadata without moving source evidence."""
    memory_home = project_memory_home(context, memory_base)
    ledger = memory_home / "runtime" / "legacy_artifacts.jsonl"
    seen: set[tuple[str, int, int]] = set()
    if ledger.is_file():
        import json

        for line in ledger.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(line)
                seen.add((str(item["file_path"]), int(item["size"]), int(item["mtime_ns"])))
            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                continue
    added = 0
    skipped = 0
    for path in iter_deliverables(context.work_root):
        stat = path.stat()
        relative_path = path.relative_to(context.work_root)
        relative = str(relative_path)
        identity = (relative, stat.st_size, stat.st_mtime_ns)
        if identity in seen:
            skipped += 1
            continue
        append_jsonl(
            ledger,
            {
                "artifact_type": path.suffix.lower().lstrip("."),
                "cataloged_at": iso_timestamp(),
                "classification": (
                    "evidence"
                    if relative_path.parts and relative_path.parts[0] == "documents"
                    else "legacy"
                ),
                "file_path": relative,
                "mtime_ns": stat.st_mtime_ns,
                "project_id": context.project_id,
                "sha256": _safe_digest(path, context.work_root),
                "size": stat.st_size,
            },
        )
        added += 1
    return {"added": added, "skipped": skipped, "ledger": str(ledger)}
