"""Session contracts, provider-scoped gates, safe events, and closure."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Mapping

from .config import (
    NEGRITAOS_ROOT,
    ProjectContext,
    load_project,
    load_yaml,
    project_memory_home,
    workspace_kind,
)
from .documents import DELIVERABLE_EXTENSIONS, is_compliant_deliverable, is_deliverable
from .errors import MemoryPermissionError, SessionError
from .models import (
    append_jsonl,
    file_lock,
    iso_timestamp,
    now_madrid,
    read_json,
    sha256_json,
    write_json,
)
from .profiles import resolve_project_profiles


SAFE_EVENT_KEYS = {
    "action",
    "decision_ids",
    "durable_ref",
    "file_path",
    "provider",
    "status",
    "tool",
}
VALID_PROVIDERS = {"codex", "claude", "ci", "human"}
LEGACY_RECOVERY_SCOPE = "legacy-memory-v1"
RECOVERY_BRANCH_PREFIXES = ("fix/", "chore/brain-")


@dataclass(frozen=True)
class SessionIdentity:
    """Provider-specific identity used to isolate active session pointers."""

    provider: str
    key: str
    source: str

    @property
    def key_hash(self) -> str:
        """Return a non-reversible path-safe key for the native session id."""
        value = f"{self.provider}:{self.key}".encode("utf-8")
        return hashlib.sha256(value).hexdigest()


@dataclass(frozen=True)
class _SessionHandle:
    """Internal verified session plus the pointer that selected it."""

    context: ProjectContext
    contract: dict[str, Any]
    session_dir: Path
    pointer_path: Path
    legacy: bool
    update_pointer: bool = True


def resolve_session_identity(
    provider: str | None = None,
    session_key: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> SessionIdentity:
    """Resolve explicit, provider-native, or compatibility session identity."""
    environment = environ if environ is not None else os.environ
    normalized_provider = (provider or "").strip().lower()
    if not normalized_provider:
        normalized_provider = "codex"
    if normalized_provider not in VALID_PROVIDERS:
        raise SessionError(f"Unsupported session provider: {normalized_provider}")
    if isinstance(session_key, str) and session_key.strip():
        return SessionIdentity(normalized_provider, session_key.strip(), "explicit")
    if normalized_provider == "codex" and environment.get("CODEX_THREAD_ID"):
        return SessionIdentity(
            normalized_provider,
            str(environment["CODEX_THREAD_ID"]),
            "CODEX_THREAD_ID",
        )
    return SessionIdentity(
        normalized_provider,
        f"{normalized_provider}-default",
        "provider_default",
    )


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


def _memory_policy(context: ProjectContext) -> dict[str, Any]:
    """Return Memory v2 policy defaults without inventing project overrides."""
    value = _policy_root(context).get("memory", {})
    return value if isinstance(value, dict) else {}


def _agent_codex_skill_ids(context: ProjectContext, agent_ids: list[str]) -> list[str]:
    """Return catalog skill ids referenced by selected agents' codex_skills."""
    if not agent_ids:
        return []
    catalog_paths = {
        entry.get("path"): entry.get("id")
        for entry in context.catalog.get("skills", [])
        if isinstance(entry, dict)
        and isinstance(entry.get("path"), str)
        and isinstance(entry.get("id"), str)
    }
    integrator = load_yaml(context.negritaos_root / "integrator.yaml").get(
        "negrita_os", {}
    )
    agents = integrator.get("agents", {}) if isinstance(integrator, dict) else {}
    if not isinstance(agents, dict):
        return []
    skill_ids: list[str] = []
    for agent_id in agent_ids:
        agent = agents.get(agent_id)
        if not isinstance(agent, dict):
            continue
        codex_skills = agent.get("codex_skills", [])
        if not isinstance(codex_skills, list):
            continue
        for raw_path in codex_skills:
            skill_id = catalog_paths.get(raw_path)
            if isinstance(skill_id, str) and skill_id not in skill_ids:
                skill_ids.append(skill_id)
    return skill_ids


def _session_id(project_id: str, now: datetime) -> str:
    """Create a sortable session identifier."""
    return f"NBS-{project_id}-{now.strftime('%Y%m%d_%H%M%S')}-{uuid.uuid4().hex[:8]}"


def _session_dir(
    context: ProjectContext,
    session_id: str,
    memory_base: Path | None,
) -> Path:
    """Return the immutable runtime directory for one session."""
    return project_memory_home(context, memory_base) / "runtime" / "sessions" / session_id


def _active_pointer(
    context: ProjectContext,
    identity: SessionIdentity,
    memory_base: Path | None,
) -> Path:
    """Return the Memory v2 provider/session active pointer."""
    runtime = project_memory_home(context, memory_base) / "runtime"
    return runtime / "active" / identity.provider / f"{identity.key_hash}.json"


def _legacy_pointer(context: ProjectContext, memory_base: Path | None) -> Path:
    """Return the Memory v1 workspace-global pointer."""
    return project_memory_home(context, memory_base) / "runtime" / "active_session.json"


def _verified_contract(session_dir: Path) -> dict[str, Any]:
    """Load one session contract and verify its immutable hash."""
    contract_path = session_dir / "contract.json"
    if not contract_path.is_file():
        raise SessionError(f"Session contract is missing: {contract_path}")
    contract = read_json(contract_path)
    expected = contract.pop("contract_sha256", None)
    actual = sha256_json(contract)
    contract["contract_sha256"] = expected
    if expected != actual:
        raise SessionError(f"Session contract hash mismatch: {contract_path}")
    return contract


def _load_legacy_handle(
    work_root: Path,
    negritaos_root: Path,
    memory_base: Path | None,
    session_id: str,
) -> _SessionHandle:
    """Select one Memory v1 session by its exact persisted id."""
    if not session_id or Path(session_id).name != session_id:
        raise SessionError("legacy-session-id must be one session directory name")
    context = load_project(work_root, negritaos_root)
    session_dir = _session_dir(context, session_id, memory_base)
    contract = _verified_contract(session_dir)
    if int(contract.get("schema_version", 1)) != 1:
        raise SessionError(f"Session is not a Memory v1 session: {session_id}")
    if (session_dir / "summary.json").is_file() or (session_dir / "state.json").is_file():
        raise SessionError(f"Session is already closed: {session_id}")
    pointer_path = _legacy_pointer(context, memory_base)
    update_pointer = False
    if pointer_path.is_file():
        pointer = read_json(pointer_path)
        update_pointer = pointer.get("session_id") == session_id
    return _SessionHandle(
        context,
        contract,
        session_dir,
        pointer_path,
        True,
        update_pointer=update_pointer,
    )


def _runtime_session_is_closed(session_dir: Path) -> bool:
    """Return whether a runtime session already has a closure marker."""
    if (session_dir / "summary.json").is_file():
        return True
    state_path = session_dir / "state.json"
    if not state_path.is_file():
        return False
    try:
        state = read_json(state_path)
    except (OSError, ValueError):
        return False
    return isinstance(state, dict) and str(state.get("status", "")).upper() not in {
        "",
        "READY",
        "OPEN",
    }


def _created_at(contract: Mapping[str, Any]) -> datetime | None:
    """Parse a runtime contract timestamp when available."""
    raw_value = contract.get("created_at")
    if not isinstance(raw_value, str) or not raw_value:
        return None
    try:
        parsed = datetime.fromisoformat(raw_value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.astimezone()
    return parsed


def close_stale_runtime_sessions(
    work_root: Path,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    older_than_days: int = 1,
    session_ids: list[str] | None = None,
    apply_changes: bool = False,
    authorized_by: str | None = None,
    authorization_reason: str | None = None,
    status: str = "STALE_CLOSED",
    now: datetime | None = None,
) -> dict[str, Any]:
    """Close old Memory v2 runtime sessions through an explicit maintenance action."""
    if older_than_days < 0:
        raise SessionError("older_than_days must be >= 0")
    if apply_changes and (not authorized_by or not authorization_reason):
        raise SessionError(
            "Closing stale runtime sessions requires authorized_by and authorization_reason"
        )
    context = load_project(work_root, negritaos_root)
    memory_home = project_memory_home(context, memory_base)
    runtime = memory_home / "runtime"
    sessions_root = runtime / "sessions"
    selected = set(session_ids or [])
    if any(Path(session_id).name != session_id for session_id in selected):
        raise SessionError("session-id must be one session directory name")
    current = now or now_madrid()
    cutoff = current - timedelta(days=older_than_days)
    planned: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    closed: list[dict[str, Any]] = []
    if not sessions_root.is_dir():
        return {
            "apply": apply_changes,
            "closed": closed,
            "planned": planned,
            "project_id": context.project_id,
            "skipped": skipped,
            "status": "READY",
        }
    for contract_path in sorted(sessions_root.glob("*/contract.json")):
        session_dir = contract_path.parent
        session_id = session_dir.name
        if selected and session_id not in selected:
            continue
        contract = _verified_contract(session_dir)
        if int(contract.get("schema_version", 1)) != 2:
            skipped.append({"session_id": session_id, "reason": "not_memory_v2"})
            continue
        if _runtime_session_is_closed(session_dir):
            skipped.append({"session_id": session_id, "reason": "already_closed"})
            continue
        created_at = _created_at(contract)
        if created_at is None:
            skipped.append({"session_id": session_id, "reason": "missing_created_at"})
            continue
        if created_at > cutoff:
            skipped.append({"session_id": session_id, "reason": "too_recent"})
            continue
        planned_item = {
            "actions": contract.get("actions", []),
            "created_at": contract.get("created_at"),
            "provider": contract.get("provider"),
            "session_id": session_id,
        }
        planned.append(planned_item)
        if not apply_changes:
            continue
        closed_at = iso_timestamp()
        closed_state: dict[str, Any] = {
            "authorization": {
                "authorized_by": authorized_by,
                "mode": "explicit_stale_runtime_close",
                "reason": authorization_reason,
            },
            "closed_at": closed_at,
            "contract_sha256": contract["contract_sha256"],
            "project_id": context.project_id,
            "schema_version": 2,
            "session_id": session_id,
            "status": status.upper(),
        }
        identity = contract.get("session_identity", {})
        provider = contract.get("provider")
        key_hash = identity.get("key_hash") if isinstance(identity, dict) else None
        pointer_path: Path | None = None
        if isinstance(provider, str) and isinstance(key_hash, str):
            pointer_path = runtime / "active" / provider / f"{key_hash}.json"
        with file_lock(runtime / ".project.lock"):
            write_json(session_dir / "state.json", closed_state)
            if pointer_path and pointer_path.is_file():
                pointer = read_json(pointer_path)
                if pointer.get("session_id") == session_id:
                    pointer.update(
                        {
                            "schema_version": 2,
                            "session_id": session_id,
                            "state": "CLOSED",
                            "updated_at": closed_at,
                        }
                    )
                    write_json(pointer_path, pointer)
        append_jsonl(
            session_dir / "events.jsonl",
            {
                "event_id": f"NBE-{uuid.uuid4().hex}",
                "event_kind": "stale_runtime_session_closed",
                "occurred_at": closed_at,
                "session_id": session_id,
                "status": status.upper(),
            },
        )
        closed.append(closed_state)
    return {
        "apply": apply_changes,
        "closed": closed,
        "closed_count": len(closed),
        "older_than_days": older_than_days,
        "planned": planned,
        "planned_count": len(planned),
        "project_id": context.project_id,
        "skipped": skipped,
        "status": "READY",
    }


def _permission_error(memory_home: Path, exc: PermissionError) -> MemoryPermissionError:
    """Classify sandbox denial separately from configuration resolution."""
    return MemoryPermissionError(
        f"Canonical memory is not writable: {memory_home}. "
        "Grant the provider access or retry with elevated permission. "
        f"Original error: {exc}"
    )


def resolve_session(
    work_root: Path,
    provider: str,
    actions: list[str] | None = None,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    now: datetime | None = None,
    session_key: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Resolve and persist an immutable Memory v2 session contract."""
    context = load_project(work_root, negritaos_root)
    identity = resolve_session_identity(provider, session_key, environ)
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
    if identity.source == "provider_default":
        warnings.append(
            "Provider-native session id unavailable; concurrent sessions must pass --session-key"
        )
    current = now or now_madrid()
    session_id = _session_id(context.project_id, current)
    kind = workspace_kind(context)
    from .doctor import doctor_project

    health = doctor_project(context.work_root, context.negritaos_root, memory_base)
    state = "BLOCKED" if health["status"] == "FAIL" else "READY"
    warnings.extend(
        issue["message"] for issue in health["issues"] if issue["level"] == "WARN"
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
    memory_home = project_memory_home(context, memory_base)
    memory_policy = _memory_policy(context)
    agent_skill_ids = _agent_codex_skill_ids(context, selected_agents)
    resolved_skill_ids = list(closure.skills)
    for skill_id in agent_skill_ids:
        if skill_id not in resolved_skill_ids:
            resolved_skill_ids.append(skill_id)
    contract: dict[str, Any] = {
        "schema_version": 2,
        "session_id": session_id,
        "created_at": iso_timestamp(current),
        "project": {
            "id": context.project_id,
            "name": context.project.get("name"),
            "root": str(context.work_root),
            "registry": str(context.registry_path),
            "workspace_kind": kind,
        },
        "provider": identity.provider,
        "session_identity": {
            "key_hash": identity.key_hash,
            "source": identity.source,
        },
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
        "skills": resolved_skill_ids,
        "agent_skills": agent_skill_ids,
        "artifact_route": {
            "selection": route.get("selection", "canonical_default"),
            "directory": str(context.work_root / str(route.get("directory", "documents"))),
            "manifest": str(
                context.work_root
                / str(route.get("manifest", "documents/document_manifest.jsonl"))
            ),
            "manifest_mode": route.get("manifest_mode", "required"),
            "require_explicit_path_for": list(
                route.get("require_explicit_path_for", [])
            ),
            "default_git_policy": dict(route.get("default_git_policy", {})),
            "filename_pattern": route.get("filename_pattern"),
            "timezone": route.get("timezone", "Europe/Madrid"),
        },
        "memory": {
            "home": str(memory_home),
            "owner": memory_policy.get("owner", "negrita_brain"),
            "persistence": memory_policy.get("persistence", "relevant"),
            "schema_version": memory_policy.get("schema_version", 2),
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
    session_dir = _session_dir(context, session_id, memory_base)
    active_pointer = _active_pointer(context, identity, memory_base)
    pointer = {
        "contract_path": str(session_dir / "contract.json"),
        "key_hash": identity.key_hash,
        "project_id": context.project_id,
        "provider": identity.provider,
        "schema_version": 2,
        "session_id": session_id,
        "state": state,
        "updated_at": iso_timestamp(current),
    }
    try:
        with file_lock(memory_home / "runtime" / ".project.lock"):
            write_json(session_dir / "contract.json", contract)
            write_json(active_pointer, pointer)
        append_jsonl(
            session_dir / "events.jsonl",
            {
                "event_id": f"NBE-{uuid.uuid4().hex}",
                "event_kind": "session_resolved",
                "occurred_at": iso_timestamp(current),
                "provider": identity.provider,
                "session_id": session_id,
                "status": state,
            },
        )
    except PermissionError as exc:
        raise _permission_error(memory_home, exc) from exc
    return contract


def _load_active_handle(
    work_root: Path,
    negritaos_root: Path,
    memory_base: Path | None,
    provider: str | None,
    session_key: str | None,
    environ: Mapping[str, str] | None,
) -> _SessionHandle:
    """Load a v2 pointer, using the v1 pointer only without explicit selection."""
    context = load_project(work_root, negritaos_root)
    identity = resolve_session_identity(provider, session_key, environ)
    pointer_path = _active_pointer(context, identity, memory_base)
    legacy = False
    if not pointer_path.is_file():
        if session_key:
            raise SessionError(
                "No Memory v2 pointer for session-key; use --legacy-session-id "
                "to select a Memory v1 session explicitly"
            )
        pointer_path = _legacy_pointer(context, memory_base)
        legacy = True
    if not pointer_path.is_file():
        raise SessionError(f"No active Negrita Brain session for {context.project_id}")
    pointer = read_json(pointer_path)
    contract_path = Path(str(pointer.get("contract_path", ""))).expanduser()
    if not contract_path.is_file():
        raise SessionError(f"Active contract is missing: {contract_path}")
    contract = _verified_contract(contract_path.parent)
    if pointer.get("state") != "READY":
        contract["state"] = str(pointer.get("state", "CLOSED"))
    return _SessionHandle(context, contract, contract_path.parent, pointer_path, legacy)


def load_active_session(
    work_root: Path,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    provider: str | None = None,
    session_key: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> tuple[ProjectContext, dict[str, Any], Path]:
    """Load and verify the active session selected for this provider task."""
    handle = _load_active_handle(
        work_root, negritaos_root, memory_base, provider, session_key, environ
    )
    return handle.context, handle.contract, handle.session_dir


def gate_action(
    work_root: Path,
    action: str,
    file_path: Path | None = None,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    provider: str | None = None,
    session_key: str | None = None,
    authorize_legacy_recovery: bool = False,
    authorized_by: str | None = None,
    authorization_reason: str | None = None,
    recovery_scope: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Authorize, warn, or block an action under the selected contract."""
    normalized = action.lower()
    try:
        context, contract, _ = load_active_session(
            work_root,
            negritaos_root,
            memory_base,
            provider,
            session_key,
            environ,
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
    authorization: dict[str, str] | None = None
    if normalized != "read" and not ready:
        if authorize_legacy_recovery:
            branch = _git_state(context.work_root).get("branch")
            if recovery_scope != LEGACY_RECOVERY_SCOPE:
                raise SessionError(
                    f"Legacy recovery requires recovery_scope={LEGACY_RECOVERY_SCOPE}"
                )
            if not isinstance(branch, str) or not branch.startswith(RECOVERY_BRANCH_PREFIXES):
                raise SessionError(
                    "Legacy recovery authorization requires a fix/ or chore/brain- branch"
                )
            if not authorized_by or not authorization_reason:
                raise SessionError(
                    "Legacy recovery authorization requires authorized_by and reason"
                )
            decision = "ALLOW"
            authorization = {
                "authorized_by": authorized_by,
                "reason": authorization_reason,
                "mode": "explicit_legacy_recovery_override",
                "scope": recovery_scope,
                "branch": branch,
            }
            reasons.append(
                "Human authorization recorded for the legacy-memory recovery path"
            )
        else:
            policy_key = (
                "commit_without_ready_contract"
                if normalized == "commit"
                else "mutation_without_ready_contract"
            )
            decision = str(rules.get(policy_key, "warn")).upper()
            reasons.append("Mutation requires an active READY session contract")
    route = policy.get("artifact_route", {})
    user_selected_route = route.get("selection") == "user_selected"
    required_extensions = {
        str(value).lower().lstrip(".")
        for value in route.get("require_explicit_path_for", [])
    }
    if normalized == "deliverable" and file_path is None:
        if "*" in required_extensions or required_extensions:
            route_decision = str(rules.get("noncompliant_deliverable", "warn")).upper()
            if route_decision == "BLOCK" or decision == "ALLOW":
                decision = route_decision
            reasons.append(
                "Deliverable path must be provided under the canonical team-lead-qaqc/documents route"
            )
    if file_path is not None and file_path.suffix.lower() in DELIVERABLE_EXTENSIONS:
        candidate = file_path if file_path.is_absolute() else context.work_root / file_path
        if user_selected_route:
            compliant = is_compliant_deliverable(
                candidate,
                context.work_root,
                user_selected_route=True,
                canonical_directory=str(route.get("directory", "documents")),
            )
            if not compliant:
                route_decision = str(rules.get("noncompliant_deliverable", "warn")).upper()
                if route_decision == "BLOCK" or decision == "ALLOW":
                    decision = route_decision
                reasons.append(
                    "Deliverable names must use <slug>__updated_YYYYMMDD_HHMMSS.<ext>"
                )
            elif not candidate.resolve().is_relative_to(context.work_root.resolve()):
                reasons.append(
                    "External deliverable route explicitly selected; artifact is not tracked by default"
                )
        elif (
            route.get("selection") == "canonical_default"
            and not candidate.resolve().is_relative_to(context.work_root.resolve())
        ):
            route_decision = str(rules.get("noncompliant_deliverable", "warn")).upper()
            if route_decision == "BLOCK" or decision == "ALLOW":
                decision = route_decision
            reasons.append(
                "Deliverables must remain inside the repository canonical team-lead-qaqc/documents route"
            )
        elif is_deliverable(candidate, context.work_root) and not is_compliant_deliverable(
            candidate,
            context.work_root,
            canonical_directory=str(route.get("directory", "documents")),
        ):
            route_decision = str(rules.get("noncompliant_deliverable", "warn")).upper()
            if route_decision == "BLOCK" or decision == "ALLOW":
                decision = route_decision
            reasons.append(
                "Deliverable names must use <slug>__updated_YYYYMMDD_HHMMSS.<ext>"
            )
    return {
        "action": normalized,
        "decision": decision,
        "project_id": context.project_id,
        "reasons": reasons,
        "session_id": contract.get("session_id") if contract else None,
        "workspace_kind": kind,
        "authorization": authorization,
    }


def record_event(
    work_root: Path,
    event_kind: str,
    status: str,
    metadata: dict[str, Any] | None = None,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    provider: str | None = None,
    session_key: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Append safe execution metadata and discard unapproved keys."""
    context, contract, session_dir = load_active_session(
        work_root,
        negritaos_root,
        memory_base,
        provider,
        session_key,
        environ,
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
    try:
        append_jsonl(session_dir / "events.jsonl", event)
    except PermissionError as exc:
        raise _permission_error(project_memory_home(context, memory_base), exc) from exc
    return event


def close_session(
    work_root: Path,
    summary: str | None = None,
    status: str = "COMPLETE",
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    provider: str | None = None,
    session_key: str | None = None,
    legacy_session_id: str | None = None,
    authorize_legacy_close: bool = False,
    authorized_by: str | None = None,
    authorization_reason: str | None = None,
    durable_refs: list[str] | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Close one selected session without rewriting durable project memory."""
    if legacy_session_id and session_key:
        raise SessionError("Choose session-key or legacy-session-id, not both")
    if authorize_legacy_close and not legacy_session_id:
        raise SessionError("authorize_legacy_close requires legacy_session_id")
    if legacy_session_id:
        if not authorize_legacy_close:
            raise SessionError(
                "Explicit authorization is required to close a Memory v1 session"
            )
        if not authorized_by or not authorization_reason:
            raise SessionError(
                "Legacy session closure requires authorized_by and authorization_reason"
            )
        handle = _load_legacy_handle(
            work_root, negritaos_root, memory_base, legacy_session_id
        )
    else:
        handle = _load_active_handle(
            work_root, negritaos_root, memory_base, provider, session_key, environ
        )
    context = handle.context
    contract = handle.contract
    if not legacy_session_id and contract.get("state") != "READY":
        raise SessionError(f"Session is already closed: {contract['session_id']}")
    closed_at = iso_timestamp()
    refs = list(dict.fromkeys(durable_refs or []))
    closed: dict[str, Any] = {
        "closed_at": closed_at,
        "contract_sha256": contract["contract_sha256"],
        "durable_refs": refs,
        "project_id": context.project_id,
        "schema_version": 1 if handle.legacy else 2,
        "session_id": contract["session_id"],
        "status": status.upper(),
    }
    backup_path: Path | None = None
    if legacy_session_id:
        memory_home = project_memory_home(context, memory_base)
        backup_path = (
            memory_home
            / "legacy_import"
            / "authorized_closures"
            / closed_at.replace(":", "").replace("+", "_")
            / legacy_session_id
        )
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(handle.session_dir, backup_path)
        legacy_pointer = _legacy_pointer(context, memory_base)
        if legacy_pointer.is_file():
            shutil.copy2(legacy_pointer, backup_path.parent / legacy_pointer.name)
        closed["authorization"] = {
            "authorized_by": authorized_by,
            "reason": authorization_reason,
            "mode": "explicit_legacy_session_close",
        }
        closed["backup_path"] = str(backup_path)
    if summary and handle.legacy:
        closed["summary"] = summary
    state_path = handle.session_dir / ("summary.json" if handle.legacy else "state.json")
    pointer = {
        "contract_path": str(handle.session_dir / "contract.json"),
        "project_id": context.project_id,
        "schema_version": 1 if handle.legacy else 2,
        "session_id": contract["session_id"],
        "state": "CLOSED",
        "updated_at": closed_at,
    }
    if not handle.legacy:
        pointer["provider"] = contract.get("provider")
        identity = contract.get("session_identity", {})
        if isinstance(identity, dict):
            pointer["key_hash"] = identity.get("key_hash")
    memory_home = project_memory_home(context, memory_base)
    try:
        with file_lock(memory_home / "runtime" / ".project.lock"):
            write_json(state_path, closed)
            if handle.update_pointer:
                write_json(handle.pointer_path, pointer)
        append_jsonl(
            handle.session_dir / "events.jsonl",
            {
                "event_id": f"NBE-{uuid.uuid4().hex}",
                "event_kind": "session_closed",
                "occurred_at": closed_at,
                "session_id": contract["session_id"],
                "status": closed["status"],
            },
        )
    except PermissionError as exc:
        raise _permission_error(memory_home, exc) from exc
    return closed
