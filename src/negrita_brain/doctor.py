"""Read-only project health checks for Negrita Brain enforcement."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .codex_config import codex_config_status
from .config import (
    NEGRITAOS_ROOT,
    adapter_memory_home,
    load_project,
    project_memory_home,
)
from .decisions import read_decision_state
from .documents import audit_documents
from .errors import ConfigurationError
from .memory import index_is_runtime_owned
from .profiles import resolve_project_profiles


MANAGED_START = "<!-- NEGRITA_BRAIN:START -->"
HOOK_EVENTS = {
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "Stop",
    "SessionEnd",
}


def _issue(code: str, level: str, message: str) -> dict[str, str]:
    """Create one stable doctor issue."""
    return {"code": code, "level": level, "message": message}


def _check_entrypoints(root: Path) -> list[dict[str, str]]:
    """Check managed Codex and Claude root entrypoints."""
    issues: list[dict[str, str]] = []
    agents = root / "AGENTS.md"
    claude = root / "CLAUDE.md"
    if not agents.is_file() or MANAGED_START not in agents.read_text(
        encoding="utf-8", errors="ignore"
    ):
        issues.append(
            _issue("ENTRYPOINT_AGENTS", "ERROR", "Managed AGENTS.md block is missing")
        )
    if not claude.is_file():
        issues.append(_issue("ENTRYPOINT_CLAUDE", "ERROR", "CLAUDE.md is missing"))
    else:
        text = claude.read_text(encoding="utf-8", errors="ignore")
        if MANAGED_START not in text or "@AGENTS.md" not in text:
            issues.append(
                _issue(
                    "ENTRYPOINT_CLAUDE",
                    "ERROR",
                    "CLAUDE.md does not import managed AGENTS.md",
                )
            )
    return issues


def _check_hooks(root: Path) -> list[dict[str, str]]:
    """Check all required Claude hook events in shared settings."""
    settings = root / ".codex" / "settings.json"
    if not settings.is_file():
        return [_issue("HOOKS_MISSING", "ERROR", ".codex/settings.json is missing")]
    try:
        value = json.loads(settings.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [_issue("HOOKS_INVALID", "ERROR", f"Invalid shared settings JSON: {exc}")]
    hooks = value.get("hooks", {}) if isinstance(value, dict) else {}
    missing = sorted(HOOK_EVENTS - set(hooks)) if isinstance(hooks, dict) else sorted(HOOK_EVENTS)
    if missing:
        return [_issue("HOOKS_INCOMPLETE", "ERROR", f"Missing hooks: {', '.join(missing)}")]
    return []


def _check_materialized(
    root: Path, negritaos_root: Path, skills: tuple[str, ...]
) -> list[dict[str, str]]:
    """Check that each resolved skill is reachable in the workspace."""
    issues: list[dict[str, str]] = []
    target_root = root / ".codex" / "skills"
    for skill_id in skills:
        target = target_root / skill_id
        canonical = negritaos_root / ".codex" / "skills" / skill_id
        if not target.exists():
            issues.append(
                _issue(
                    "SKILL_MISSING", "ERROR", f"Missing materialized skill: {skill_id}"
                )
            )
        elif target.is_symlink() and target.resolve() != canonical.resolve():
            issues.append(
                _issue(
                    "SKILL_DRIFT",
                    "ERROR",
                    f"Skill points outside canonical root: {skill_id}",
                )
            )
    return issues


def _check_memory_writers(root: Path) -> list[dict[str, str]]:
    """Reject legacy instruction surfaces that can write project memory directly."""
    issues: list[dict[str, str]] = []
    agents = root / "AGENTS.md"
    protocol = root / ".codex" / "skills" / "local-memory-protocol" / "SKILL.md"
    handoff = root / ".codex" / "commands" / "session-handoff.md"
    agents_text = agents.read_text(encoding="utf-8", errors="ignore") if agents.is_file() else ""
    protocol_text = (
        protocol.read_text(encoding="utf-8", errors="ignore")
        if protocol.is_file()
        else ""
    )
    handoff_text = (
        handoff.read_text(encoding="utf-8", errors="ignore")
        if handoff.is_file()
        else ""
    )
    if (
        "memory remember|handoff" not in agents_text
        or "Negrita Brain is the only project-memory writer" not in protocol_text
        or "memory handoff" not in handoff_text
        or "write one at <memory_home>" in handoff_text
    ):
        issues.append(
            _issue(
                "MEMORY_DUPLICATE_WRITER",
                "ERROR",
                "AGENTS.md, memory-protocol, or session-handoff still permits or omits Brain-only project-memory writes",
            )
        )
    local_memory = root / ".codex" / "memory"
    if local_memory.is_dir() and any(local_memory.rglob("*")):
        issues.append(
            _issue(
                "LEGACY_LOCAL_MEMORY",
                "WARN",
                f"Repo-local memory is preserved but non-authoritative: {local_memory}",
            )
        )
    return issues


def _session_is_closed(session_dir: Path) -> bool:
    """Recognize both Memory v1 summaries and Memory v2 state files."""
    if (session_dir / "summary.json").is_file():
        return True
    state_path = session_dir / "state.json"
    if not state_path.is_file():
        return False
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return isinstance(state, dict) and str(state.get("status", "")).upper() not in {
        "",
        "READY",
        "OPEN",
    }


def doctor_project(
    work_root: Path,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Audit one project without mutating repository or memory state."""
    context = load_project(work_root, negritaos_root)
    closure = resolve_project_profiles(context.catalog, context.project)
    issues = [
        *_check_entrypoints(context.work_root),
        *_check_hooks(context.work_root),
        *_check_materialized(context.work_root, context.negritaos_root, closure.skills),
        *_check_memory_writers(context.work_root),
    ]
    if "document-control" not in closure.skills:
        issues.append(
            _issue(
                "DOCUMENT_ROUTING",
                "ERROR",
                "document-control is absent from resolved profile closure",
            )
        )
    memory_home = project_memory_home(context, memory_base)
    mirror = adapter_memory_home(context)
    registry_memory_home = project_memory_home(context)
    if mirror is not None and mirror != registry_memory_home:
        issues.append(
            _issue(
                "MEMORY_HOME_MIRROR",
                "ERROR",
                f"Adapter memory_home {mirror} differs from registry authority {registry_memory_home}",
            )
        )
    if not memory_home.is_dir():
        issues.append(_issue("MEMORY_HOME", "ERROR", f"Memory home is missing: {memory_home}"))
    else:
        sessions = memory_home / "runtime" / "sessions"
        open_sessions = []
        if sessions.is_dir():
            for contract in sessions.glob("*/contract.json"):
                if not _session_is_closed(contract.parent):
                    open_sessions.append(contract.parent.name)
        if open_sessions:
            issues.append(
                _issue(
                    "OPEN_SESSIONS",
                    "WARN",
                    f"Open sessions: {', '.join(sorted(open_sessions)[:5])}",
                )
            )
        states = read_decision_state(memory_home / "decisions" / "ledger.jsonl")
        cutoff = datetime.now().astimezone() - timedelta(days=30)
        stale = []
        for decision_id, record in states.items():
            if record.get("event") != "CANDIDATE":
                continue
            try:
                occurred = datetime.fromisoformat(str(record.get("occurred_at")))
            except ValueError:
                continue
            if occurred < cutoff:
                stale.append(decision_id)
        if stale:
            issues.append(
                _issue(
                    "STALE_DECISIONS",
                    "WARN",
                    f"Stale candidates: {', '.join(stale[:5])}",
                )
            )
        if index_is_runtime_owned(memory_home / "index.md"):
            issues.append(
                _issue(
                    "INDEX_RUNTIME_OWNED",
                    "WARN",
                    "index.md has the Memory v1 Runtime Sessions shape; preserve it and use memory rebuild-index explicitly after v1 sessions close",
                )
            )
    if memory_base is None:
        try:
            config_status = codex_config_status()
        except (ConfigurationError, OSError, ValueError) as exc:
            issues.append(
                _issue(
                    "CODEX_MEMORY_CONFIG",
                    "WARN",
                    f"Cannot validate Codex writable roots: {exc}",
                )
            )
        else:
            if not config_status["configured"]:
                issues.append(
                    _issue(
                        "CODEX_MEMORY_WRITABLE_ROOT",
                        "WARN",
                        "Codex workspace-write does not include ~/.negritaos/memory; run configure codex --apply and start a new task",
                    )
                )
    audit = audit_documents(context.work_root)
    if audit["missing_timestamp"]:
        issues.append(
            _issue(
                "LEGACY_DOCUMENTS",
                "WARN",
                "Deliverables missing the required version suffix: "
                f"{len(audit['missing_timestamp'])}",
            )
        )
    errors = sum(issue["level"] == "ERROR" for issue in issues)
    warnings = sum(issue["level"] == "WARN" for issue in issues)
    return {
        "project_id": context.project_id,
        "root": str(context.work_root),
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "issues": issues,
        "resolved_profiles": list(closure.profiles),
        "resolved_skills": list(closure.skills),
    }


def doctor_all(
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Audit every registered primary path and report orphan memory homes."""
    from .config import load_yaml

    reports: list[dict[str, Any]] = []
    registered: set[str] = set()
    for registry_path in sorted((negritaos_root / "projects").glob("*.yaml")):
        try:
            project = load_yaml(registry_path).get("project", {})
            project_id = project.get("id")
            primary = project.get("local_paths", {}).get("primary")
            if not isinstance(project_id, str) or not isinstance(primary, str):
                continue
            registered.add(project_id)
            reports.append(doctor_project(Path(primary).expanduser(), negritaos_root, memory_base))
        except Exception as exc:
            reports.append(
                {
                    "project_id": registry_path.stem,
                    "root": None,
                    "status": "FAIL",
                    "issues": [_issue("DOCTOR_ERROR", "ERROR", str(exc))],
                }
            )
    base = (
        memory_base.expanduser().resolve()
        if memory_base is not None
        else Path.home() / ".negritaos" / "memory" / "projects"
    )
    orphans = []
    if base.is_dir():
        orphans = sorted(
            path.name
            for path in base.iterdir()
            if path.is_dir() and path.name not in registered
        )
    return {
        "status": "FAIL" if any(item["status"] == "FAIL" for item in reports) else "PASS",
        "projects": reports,
        "orphan_memory_homes": orphans,
        "preserved_orphans": [name for name in orphans if name == "negritoos"],
        "duplicate_candidates": [],
    }
