"""Idempotent entrypoint, hook, skill, and memory installation."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .config import NEGRITAOS_ROOT, load_project, load_yaml, project_memory_home
from .errors import BrainError
from .models import now_madrid
from .profiles import resolve_project_profiles


START = "<!-- NEGRITA_BRAIN:START -->"
END = "<!-- NEGRITA_BRAIN:END -->"


def managed_agents_block(negritaos_root: Path) -> str:
    """Render the provider-neutral root entrypoint contract."""
    cli = negritaos_root / "scripts" / "negrita_brain.py"
    return (
        f"{START}\n"
        "## Negrita Brain Runtime\n\n"
        "This workspace is governed by NegritaOS. Before substantive work:\n\n"
        "1. Read `.codex/project.yaml` and its `negrita_registry`.\n"
        f"2. Run `python3 {cli} resolve --root \"$PWD\" --provider codex --action <action>`.\n"
        "3. Use the resolved modes, agents, profile closure, rules, skills, "
        "artifact route, and gates.\n"
        f"4. Before writes or commits, run `python3 {cli} gate --root \"$PWD\" "
        "--action write|commit [--path PATH]`.\n"
        "5. New deliverables use "
        "`documents/<slug>__updated_YYYYMMDD_HHMMSS.<ext>` and "
        "`documents/document_manifest.jsonl`.\n"
        f"6. Close substantive work with `python3 {cli} close --root \"$PWD\" "
        "--summary \"...\"`.\n\n"
        "A `BLOCK` decision is mandatory. A `WARN` decision must be surfaced before proceeding. "
        "Never log prompts, responses, file contents, tool outputs, or secrets.\n"
        f"{END}"
    )


def managed_claude_block() -> str:
    """Render the Claude import bridge to the canonical root entrypoint."""
    return (
        f"{START}\n"
        "@AGENTS.md\n\n"
        "Claude must follow the imported Negrita Brain contract. Shared hooks in "
        "`.claude/settings.json` (canonical `.codex/settings.json`) enforce session, "
        "mutation, event, and closure checks.\n"
        f"{END}"
    )


def merge_managed_block(existing: str, block: str) -> str:
    """Insert or replace the Negrita Brain managed block without touching local text."""
    if START in existing and END in existing:
        before, remainder = existing.split(START, 1)
        _, after = remainder.split(END, 1)
        prefix = before.rstrip()
        return (prefix + "\n\n" if prefix else "") + block + after
    prefix = existing.rstrip()
    return (prefix + "\n\n" if prefix else "") + block + "\n"


def _hook_entry(command: str, matcher: str | None = None) -> dict[str, Any]:
    """Create one Claude command hook group."""
    entry: dict[str, Any] = {"hooks": [{"type": "command", "command": command}]}
    if matcher is not None:
        entry["matcher"] = matcher
    return entry


def merge_hook_settings(existing: dict[str, Any], hook_script: Path) -> dict[str, Any]:
    """Merge managed hooks while preserving unrelated shared settings and hooks."""
    result = json.loads(json.dumps(existing))
    hooks = result.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        hooks = {}
        result["hooks"] = hooks
    managed = str(hook_script)
    definitions = {
        "SessionStart": _hook_entry(f"python3 {managed} SessionStart"),
        "UserPromptSubmit": _hook_entry(f"python3 {managed} UserPromptSubmit"),
        "PreToolUse": _hook_entry(
            f"python3 {managed} PreToolUse",
            "Edit|Write|MultiEdit|NotebookEdit|Bash",
        ),
        "PostToolUse": _hook_entry(
            f"python3 {managed} PostToolUse",
            "Edit|Write|MultiEdit|NotebookEdit|Bash",
        ),
        "Stop": _hook_entry(f"python3 {managed} Stop"),
        "SessionEnd": _hook_entry(f"python3 {managed} SessionEnd"),
    }
    for event, entry in definitions.items():
        current = hooks.get(event, [])
        if not isinstance(current, list):
            current = []
        retained = [
            item
            for item in current
            if managed not in json.dumps(item, sort_keys=True)
        ]
        hooks[event] = [*retained, entry]
    return result


class Installer:
    """Install Negrita Brain while backing up every changed existing path."""

    def __init__(
        self,
        negritaos_root: Path = NEGRITAOS_ROOT,
        backup_root: Path | None = None,
        memory_base: Path | None = None,
    ) -> None:
        self.negritaos_root = negritaos_root.expanduser().resolve()
        self.backup_root = (
            backup_root.expanduser().resolve()
            if backup_root is not None
            else Path.home() / ".negritaos" / "backups"
        )
        self.memory_base = memory_base
        self.timestamp = now_madrid().strftime("%Y%m%d_%H%M%S")

    def _backup(self, root: Path, path: Path, project_id: str) -> Path | None:
        """Copy a file or move a directory/symlink into a project backup."""
        if not path.exists() and not path.is_symlink():
            return None
        relative = path.relative_to(root)
        destination = self.backup_root / project_id / self.timestamp / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if path.is_dir() and not path.is_symlink():
            shutil.copytree(path, destination, symlinks=True)
        elif path.is_symlink():
            destination.symlink_to(path.readlink(), target_is_directory=path.is_dir())
        else:
            shutil.copy2(path, destination)
        return destination

    def _write_text(
        self,
        root: Path,
        path: Path,
        content: str,
        project_id: str,
        dry_run: bool,
        actions: list[str],
    ) -> None:
        """Write changed text after backup."""
        current = path.read_text(encoding="utf-8") if path.is_file() else ""
        if current == content:
            return
        actions.append(f"write:{path}")
        if dry_run:
            return
        self._backup(root, path, project_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def install(
        self,
        work_root: Path,
        dry_run: bool = False,
        install_pre_commit: bool = False,
    ) -> dict[str, Any]:
        """Install all runtime entrypoints and canonical skill links."""
        context = load_project(work_root, self.negritaos_root)
        closure = resolve_project_profiles(context.catalog, context.project)
        root = context.work_root
        actions: list[str] = []
        agents = root / "AGENTS.md"
        claude = root / "CLAUDE.md"
        self._write_text(
            root,
            agents,
            merge_managed_block(
                agents.read_text(encoding="utf-8") if agents.is_file() else "",
                managed_agents_block(self.negritaos_root),
            ),
            context.project_id,
            dry_run,
            actions,
        )
        self._write_text(
            root,
            claude,
            merge_managed_block(
                claude.read_text(encoding="utf-8") if claude.is_file() else "",
                managed_claude_block(),
            ),
            context.project_id,
            dry_run,
            actions,
        )
        settings_path = root / ".codex" / "settings.json"
        existing_settings: dict[str, Any] = {}
        if settings_path.is_file():
            existing_value = json.loads(settings_path.read_text(encoding="utf-8"))
            if isinstance(existing_value, dict):
                existing_settings = existing_value
        merged_settings = merge_hook_settings(
            existing_settings, self.negritaos_root / "scripts" / "negrita_brain_hook.py"
        )
        settings_text = json.dumps(merged_settings, indent=2, sort_keys=True) + "\n"
        self._write_text(
            root,
            settings_path,
            settings_text,
            context.project_id,
            dry_run,
            actions,
        )
        skill_root = root / ".codex" / "skills"
        for skill_id in closure.skills:
            source = self.negritaos_root / ".codex" / "skills" / skill_id
            destination = skill_root / skill_id
            if destination.exists() and destination.resolve() == source.resolve():
                continue
            actions.append(f"link:{destination}->{source}")
            if dry_run:
                continue
            if destination.exists() or destination.is_symlink():
                self._backup(root, destination, context.project_id)
                if destination.is_dir() and not destination.is_symlink():
                    shutil.rmtree(destination)
                else:
                    destination.unlink()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(source, target_is_directory=True)
        memory_home = project_memory_home(context, self.memory_base)
        for relative in ("runtime/sessions", "decisions"):
            target = memory_home / relative
            if not target.is_dir():
                actions.append(f"mkdir:{target}")
                if not dry_run:
                    target.mkdir(parents=True, exist_ok=True)
        if install_pre_commit and (root / ".git").exists():
            hook = root / ".git" / "hooks" / "pre-commit"
            command = (
                "#!/bin/sh\n"
                f"python3 {self.negritaos_root / 'scripts' / 'negrita_brain.py'} "
                f"gate --root {root} --action commit\n"
            )
            self._write_text(
                root, hook, command, context.project_id, dry_run, actions
            )
            if not dry_run:
                hook.chmod(0o755)
        return {
            "actions": actions,
            "changed": bool(actions),
            "dry_run": dry_run,
            "project_id": context.project_id,
            "resolved_profiles": list(closure.profiles),
            "resolved_skills": list(closure.skills),
        }

    def install_all(
        self,
        dry_run: bool = False,
        install_pre_commit: bool = False,
    ) -> dict[str, Any]:
        """Install every registered project with a resolvable primary path."""
        reports: list[dict[str, Any]] = []
        for registry_path in sorted((self.negritaos_root / "projects").glob("*.yaml")):
            try:
                project = load_yaml(registry_path).get("project", {})
                primary = project.get("local_paths", {}).get("primary")
                if not isinstance(primary, str):
                    continue
                reports.append(
                    self.install(Path(primary).expanduser(), dry_run, install_pre_commit)
                )
            except (BrainError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
                reports.append(
                    {
                        "changed": False,
                        "error": str(exc),
                        "project_id": registry_path.stem,
                    }
                )
        return {
            "dry_run": dry_run,
            "failed": sum("error" in report for report in reports),
            "project_count": len(reports),
            "projects": reports,
        }
