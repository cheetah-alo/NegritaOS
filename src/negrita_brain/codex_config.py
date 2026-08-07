"""Conservative Codex user configuration for canonical memory access."""

from __future__ import annotations

import ast
import json
import re
import shutil
from pathlib import Path
from typing import Any

from .errors import ConfigurationError
from .models import atomic_write_text, now_madrid


SECTION = "sandbox_workspace_write"
KEY = "writable_roots"


def _section_bounds(lines: list[str]) -> tuple[int, int] | None:
    header = re.compile(rf"^\s*\[{re.escape(SECTION)}\]\s*(?:#.*)?$")
    section_header = re.compile(r"^\s*\[[^\]]+\]\s*(?:#.*)?$")
    start: int | None = None
    for index, line in enumerate(lines):
        if start is None and header.match(line):
            start = index
            continue
        if start is not None and section_header.match(line):
            return start, index
    return (start, len(lines)) if start is not None else None


def _parse_roots(raw: str) -> list[str]:
    if not raw.strip().endswith("]"):
        raise ConfigurationError(
            "Multiline sandbox_workspace_write.writable_roots is not supported; "
            "convert it to a single-line TOML array before applying"
        )
    try:
        value = ast.literal_eval(raw.strip())
    except (SyntaxError, ValueError) as exc:
        raise ConfigurationError(f"Cannot parse Codex writable_roots: {exc}") from exc
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ConfigurationError("Codex writable_roots must be an array of strings")
    return value


def _render_config(content: str, memory_root: Path) -> tuple[str, bool, list[str]]:
    lines = content.splitlines()
    root = str(memory_root.expanduser().resolve())
    bounds = _section_bounds(lines)
    if bounds is None:
        separator = [""] if lines and lines[-1].strip() else []
        rendered = [
            *lines,
            *separator,
            f"[{SECTION}]",
            f"{KEY} = {json.dumps([root])}",
        ]
        return "\n".join(rendered) + "\n", True, [root]
    start, end = bounds
    key_pattern = re.compile(rf"^(\s*){re.escape(KEY)}\s*=\s*(.+)$")
    for index in range(start + 1, end):
        match = key_pattern.match(lines[index])
        if match is None:
            continue
        roots = _parse_roots(match.group(2))
        if root in roots:
            return content if content.endswith("\n") else content + "\n", False, roots
        roots.append(root)
        lines[index] = f"{match.group(1)}{KEY} = {json.dumps(roots)}"
        return "\n".join(lines) + "\n", True, roots
    lines.insert(start + 1, f"{KEY} = {json.dumps([root])}")
    return "\n".join(lines) + "\n", True, [root]


def codex_config_status(
    config_path: Path | None = None,
    memory_root: Path | None = None,
) -> dict[str, Any]:
    """Report whether new workspace-write tasks can access canonical memory."""
    path = (config_path or Path.home() / ".codex" / "config.toml").expanduser()
    root = (memory_root or Path.home() / ".negritaos" / "memory").expanduser()
    content = path.read_text(encoding="utf-8") if path.is_file() else ""
    _, changed, roots = _render_config(content, root)
    return {
        "config_path": str(path),
        "configured": not changed,
        "memory_root": str(root.resolve()),
        "writable_roots": roots,
    }


def configure_codex(
    apply: bool = False,
    config_path: Path | None = None,
    memory_root: Path | None = None,
    backup_root: Path | None = None,
) -> dict[str, Any]:
    """Idempotently add canonical memory to Codex workspace-write roots."""
    path = (config_path or Path.home() / ".codex" / "config.toml").expanduser()
    root = (memory_root or Path.home() / ".negritaos" / "memory").expanduser()
    backups = (
        backup_root.expanduser()
        if backup_root is not None
        else Path.home() / ".negritaos" / "backups" / "codex-config"
    )
    content = path.read_text(encoding="utf-8") if path.is_file() else ""
    rendered, changed, roots = _render_config(content, root)
    backup_path: Path | None = None
    if apply and changed:
        timestamp = now_madrid().strftime("%Y%m%d_%H%M%S")
        if path.is_file():
            backup_path = backups / timestamp / "config.toml"
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup_path)
        atomic_write_text(path, rendered)
    return {
        "apply": apply,
        "backup_path": str(backup_path) if backup_path else None,
        "changed": changed,
        "config_path": str(path),
        "configured": not changed or apply,
        "memory_root": str(root.resolve()),
        "restart_required": bool(apply and changed),
        "writable_roots": roots,
    }
