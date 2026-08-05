"""Session contracts, gates, safe events, and memory closure."""

from __future__ import annotations

import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import (
    NEGRITAOS_ROOT,
    ProjectContext,
    load_project,
    load_yaml,
    project_memory_home,
    workspace_kind,
)
from .documents import DELIVERABLE_EXTENSIONS, is_compliant_deliverable, is_deliverable
from .errors import SessionError
from .models import append_jsonl, iso_timestamp, now_madrid, read_json, sha256_json, write_json
from .profiles import resolve_project_profiles


SAFE_EVENT_KEYS = {
    "action",
    "decision_ids",
    "file_path",
    "provider",
    "status",
    "tool",
}


def _git_state(root: Path) -> dict[str, Any]:
    """Return branch and HEAD without changing repository state."""
    if not (root / ".git").exists():
        return {"is_git": False, "branch": None, "head": None}

    def run(*args: str) -> str | None:
        result = subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True, check=False
        )
        return result.stdout.strip() if result.returncode == 0 else None

    return {
        "is_git": True,
        "branch": run("branch", "--show-current"),
        "head": run("rev-parse", "HEAD"),
    }


def _policy_root(context: ProjectContext) -> dict[str, Any]:
    """Return the versioned Negrita Brain policy mapping."""
    value = context.policy.get("negrita_brain")
    if not isinstance(value, dict):
        raise SessionError("negrita_brain policy root is missing")
    return value


def _session_id(project_id: str, now: datetime) -> str:
    """Create a sortable session identifier."""
    return f"NBS-{project_id}-{now.strftime('%Y%m%d_%H%M%S')}-{uuid.uuid4().hex[:8]}"


def _runtime_paths(
    context: ProjectContext,
    session_id: str,
    memory_base: Path | None,
) -> tuple[Path, Path]:
    """Return the session directory and active pointer path."""
    runtime = project_memory_home(context, memory_base) / "runtime"
    return runtime / "sessions" / session_id, runtime / "active_session.json"


def resolve_session(
    work_root: Path,
    provider: str,
    actions: list[str] | None = None,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Resolve, hash, and persist an immutable executable session contract."""
    context = load_project(work_root, negritaos_root)
    policy = _policy_root(context)
    closure = resolve_project_profiles(context.catalog, context.project)
    requested_actions = actions or ["planning"]
    mode_map = context.project.get("mode_map", {})
    default_mode_map = policy.get("default_mode_map", {})
    warnings: list[str] = []
    modes: list[str] = []
    for action in requested_actions:
        mode = mode_map.get(action) if isinstance(mode_map, dict) else None
        if not isinstance(mode, str) and isinstance(default_mode_map, dict):
            mode = default_mode_map.get(action)
        if isinstance(mode, str):
            if mode not in modes:
                modes.append(mode)
        else:
            warnings.append(f"No router mode declared for action {action!r}")
    current = now or now_madrid()
    session_id = _session_id(context.project_id, current)
    kind = workspace_kind(context)
    from .doctor import doctor_project

    health = doctor_project(context.work_root, context.negritaos_root, memory_base)
    state = "BLOCKED" if health["status"] == "FAIL" else "READY"
    warnings.extend(
        issue["message"]
        for issue in health["issues"]
        if issue["level"] == "WARN"
    )
    quality = policy.get("quality_gates", {}).get(kind, [])
    route = policy.get("artifact_route", {})
    router = load_yaml(
        context.negritaos_root / "core" / "orchestration" / "metaagent_router.yaml"
    )
    router_modes = router.get("metaagent_router", {}).get("modes", {})
    agent_by_mode = (
        {
            value.get("id"): value.get("agent")
            for value in router_modes.values()
            if isinstance(value, dict)
        }
        if isinstance(router_modes, dict)
        else {}
    )
    available_agents = list(context.project.get("agents", []))
    selected_agents: list[str] = []
    for mode in modes:
        agent = agent_by_mode.get(mode)
        if (
            isinstance(agent, str)
            and agent in available_agents
            and agent not in selected_agents
        ):
            selected_agents.append(agent)
    contract: dict[str, Any] = {
        "schema_version": 1,
        "session_id": session_id,
        "created_at": iso_timestamp(current),
        "project": {
            "id": context.project_id,
            "name": context.project.get("name"),
            "root": str(context.work_root),
            "registry": str(context.registry_path),
            "workspace_kind": kind,
        },
        "provider": provider,
        "git": _git_state(context.work_root),
        "actions": requested_actions,
        "modes": modes,
        "agents": selected_agents or available_agents,
        "available_agents": available_agents,
        "profiles": list(closure.profiles),
        "rules": [
            "rules/global/negritaos_router_rule.md",
            "core/orchestration/negrita_brain_policy.yaml",
        ],
        "skills": list(closure.skills),
        "artifact_route": {
            "directory": str(context.work_root / str(route.get("directory", "documents"))),
            "manifest": str(
                context.work_root
                / str(route.get("manifest", "documents/document_manifest.jsonl"))
            ),
            "filename_pattern": route.get("filename_pattern"),
            "timezone": route.get("timezone", "Europe/Madrid"),
        },
        "quality_gates": {
            "doctor_status": health["status"],
            "required": list(quality),
            "status": "READY" if state == "READY" else "BLOCKED",
        },
        "warnings": warnings,
        "state": state,
    }
    contract["contract_sha256"] = sha256_json(contract)
    session_dir, active_pointer = _runtime_paths(context, session_id, memory_base)
    write_json(session_dir / "contract.json", contract)
    write_json(
        active_pointer,
        {
            "contract_path": str(session_dir / "contract.json"),
            "project_id": context.project_id,
            "session_id": session_id,
            "state": state,
            "updated_at": iso_timestamp(current),
        },
    )
    append_jsonl(
        session_dir / "events.jsonl",
        {
            "event_id": f"NBE-{uuid.uuid4().hex}",
            "event_kind": "session_resolved",
            "occurred_at": iso_timestamp(current),
            "provider": provider,
            "session_id": session_id,
            "status": state,
        },
    )
    return contract


def load_active_session(
    work_root: Path,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> tuple[ProjectContext, dict[str, Any], Path]:
    """Load and verify the active session contract for a workspace."""
    context = load_project(work_root, negritaos_root)
    runtime = project_memory_home(context, memory_base) / "runtime"
    pointer_path = runtime / "active_session.json"
    if not pointer_path.is_file():
        raise SessionError(f"No active Negrita Brain session for {context.project_id}")
    pointer = read_json(pointer_path)
    contract_path = Path(str(pointer.get("contract_path", ""))).expanduser()
    if not contract_path.is_file():
        raise SessionError(f"Active contract is missing: {contract_path}")
    contract = read_json(contract_path)
    expected = contract.pop("contract_sha256", None)
    actual = sha256_json(contract)
    contract["contract_sha256"] = expected
    if expected != actual:
        raise SessionError(f"Session contract hash mismatch: {contract_path}")
    if pointer.get("state") != "READY":
        contract["state"] = str(pointer.get("state", "CLOSED"))
    return context, contract, contract_path.parent


def gate_action(
    work_root: Path,
    action: str,
    file_path: Path | None = None,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Authorize, warn, or block an action under the active contract."""
    normalized = action.lower()
    try:
        context, contract, _ = load_active_session(
            work_root, negritaos_root, memory_base
        )
        kind = str(contract["project"]["workspace_kind"])
        ready = contract.get("state") == "READY"
    except (SessionError, KeyError):
        context = load_project(work_root, negritaos_root)
        kind = workspace_kind(context)
        contract = None
        ready = False
    policy = _policy_root(context)
    rules = policy.get("enforcement", {}).get(kind, {})
    reasons: list[str] = []
    decision = "ALLOW"
    if normalized != "read" and not ready:
        policy_key = (
            "commit_without_ready_contract"
            if normalized == "commit"
            else "mutation_without_ready_contract"
        )
        decision = str(rules.get(policy_key, "warn")).upper()
        reasons.append("Mutation requires an active READY session contract")
    if file_path is not None and file_path.suffix.lower() in DELIVERABLE_EXTENSIONS:
        candidate = file_path if file_path.is_absolute() else context.work_root / file_path
        if is_deliverable(candidate, context.work_root) and not is_compliant_deliverable(
            candidate, context.work_root
        ):
            route_decision = str(rules.get("noncompliant_deliverable", "warn")).upper()
            if route_decision == "BLOCK" or decision == "ALLOW":
                decision = route_decision
            reasons.append(
                "New deliverables must use documents/<slug>__updated_YYYYMMDD_HHMMSS.<ext>"
            )
    return {
        "action": normalized,
        "decision": decision,
        "project_id": context.project_id,
        "reasons": reasons,
        "session_id": contract.get("session_id") if contract else None,
        "workspace_kind": kind,
    }


def record_event(
    work_root: Path,
    event_kind: str,
    status: str,
    metadata: dict[str, Any] | None = None,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Append safe execution metadata and discard unapproved keys."""
    _, contract, session_dir = load_active_session(
        work_root, negritaos_root, memory_base
    )
    safe = {
        key: value
        for key, value in (metadata or {}).items()
        if key in SAFE_EVENT_KEYS and value is not None
    }
    event = {
        "event_id": f"NBE-{uuid.uuid4().hex}",
        "event_kind": event_kind,
        "occurred_at": iso_timestamp(),
        "session_id": contract["session_id"],
        "status": status,
        **safe,
    }
    append_jsonl(session_dir / "events.jsonl", event)
    return event


def _update_memory_index(memory_home: Path, project_id: str) -> None:
    """Regenerate a bounded runtime session index from immutable summaries."""
    sessions_root = memory_home / "runtime" / "sessions"
    rows: list[str] = []
    for summary_path in sorted(sessions_root.glob("*/summary.json"), reverse=True)[:50]:
        summary = read_json(summary_path)
        rows.append(
            f"- `{summary.get('session_id')}` | {summary.get('status')} | "
            f"{summary.get('closed_at')} | {summary.get('summary')}"
        )
    content = (
        f"# {project_id} Memory\n\n"
        "## Runtime Sessions\n\n"
        + ("\n".join(rows) if rows else "No closed runtime sessions.")
        + "\n"
    )
    (memory_home / "index.md").parent.mkdir(parents=True, exist_ok=True)
    (memory_home / "index.md").write_text(content, encoding="utf-8")


def close_session(
    work_root: Path,
    summary: str,
    status: str = "COMPLETE",
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Close the active session, append an event, and refresh project memory."""
    context, contract, session_dir = load_active_session(
        work_root, negritaos_root, memory_base
    )
    if contract.get("state") == "CLOSED":
        raise SessionError(f"Session is already closed: {contract['session_id']}")
    closed = {
        "closed_at": iso_timestamp(),
        "contract_sha256": contract["contract_sha256"],
        "project_id": context.project_id,
        "session_id": contract["session_id"],
        "status": status.upper(),
        "summary": summary,
    }
    write_json(session_dir / "summary.json", closed)
    append_jsonl(
        session_dir / "events.jsonl",
        {
            "event_id": f"NBE-{uuid.uuid4().hex}",
            "event_kind": "session_closed",
            "occurred_at": closed["closed_at"],
            "session_id": contract["session_id"],
            "status": closed["status"],
        },
    )
    _, pointer_path = _runtime_paths(context, contract["session_id"], memory_base)
    write_json(
        pointer_path,
        {
            "contract_path": str(session_dir / "contract.json"),
            "project_id": context.project_id,
            "session_id": contract["session_id"],
            "state": "CLOSED",
            "updated_at": closed["closed_at"],
        },
    )
    _update_memory_index(project_memory_home(context, memory_base), context.project_id)
    return closed
