"""Canonical durable project memory managed exclusively by Negrita Brain."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from .config import NEGRITAOS_ROOT, load_project, project_memory_home
from .errors import MemoryPermissionError, SessionError
from .models import (
    append_jsonl,
    atomic_write_text,
    file_lock,
    iso_timestamp,
    now_madrid,
    read_json,
)
from .runtime import load_active_session, record_event


INDEX_START = "<!-- NEGRITA_BRAIN_MEMORY:START -->"
INDEX_END = "<!-- NEGRITA_BRAIN_MEMORY:END -->"
VALID_OBSERVATION_TYPES = {
    "architecture",
    "bugfix",
    "constraint",
    "decision",
    "discovery",
    "governance",
    "preference",
}


def _permission_error(memory_home: Path, exc: PermissionError) -> MemoryPermissionError:
    return MemoryPermissionError(
        f"Canonical memory is not writable: {memory_home}. "
        "Grant the provider access or retry with elevated permission. "
        f"Original error: {exc}"
    )


def _slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized[:64] or "session"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _jsonl_records(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def _active_contract(
    work_root: Path,
    negritaos_root: Path,
    memory_base: Path | None,
    provider: str | None,
    session_key: str | None,
) -> dict[str, Any] | None:
    try:
        _, contract, _ = load_active_session(
            work_root,
            negritaos_root,
            memory_base,
            provider,
            session_key,
        )
    except SessionError:
        return None
    return contract if contract.get("state") == "READY" else None


def _record_durable_event(
    work_root: Path,
    durable_ref: str,
    negritaos_root: Path,
    memory_base: Path | None,
    provider: str | None,
    session_key: str | None,
) -> None:
    try:
        record_event(
            work_root,
            "durable_memory_recorded",
            "OK",
            {"durable_ref": durable_ref, "provider": provider},
            negritaos_root,
            memory_base,
            provider,
            session_key,
        )
    except SessionError:
        return


def memory_status(
    work_root: Path,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    provider: str | None = None,
    session_key: str | None = None,
) -> dict[str, Any]:
    """Return project memory topology and active state without reading narratives."""
    context = load_project(work_root, negritaos_root)
    home = project_memory_home(context, memory_base)
    active = _active_contract(
        work_root, negritaos_root, memory_base, provider, session_key
    )
    runtime_sessions = home / "runtime" / "sessions"
    sessions = list(runtime_sessions.glob("*/contract.json")) if runtime_sessions.is_dir() else []
    durable_sessions = home / "sessions"
    return {
        "active_session_id": active.get("session_id") if active else None,
        "durable": {
            "decisions": str(home / "decisions" / "ledger.jsonl"),
            "index": str(home / "index.md"),
            "observations": str(home / "observations.jsonl"),
            "sessions": str(durable_sessions),
            "tasks": str(home / "tasks"),
        },
        "durable_session_count": len(list(durable_sessions.glob("*.md")))
        if durable_sessions.is_dir()
        else 0,
        "index_runtime_owned": index_is_runtime_owned(home / "index.md"),
        "memory_home": str(home),
        "owner": "negrita_brain",
        "project_id": context.project_id,
        "runtime_session_count": len(sessions),
        "schema_version": 2,
    }


def remember(
    work_root: Path,
    observation_type: str,
    title: str,
    summary: str,
    learned: str,
    tags: list[str] | None = None,
    files: list[str] | None = None,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    provider: str | None = None,
    session_key: str | None = None,
) -> dict[str, Any]:
    """Append one reusable observation to canonical project memory."""
    normalized = observation_type.strip().lower()
    if normalized not in VALID_OBSERVATION_TYPES:
        raise ValueError(f"Unsupported observation type: {observation_type}")
    context = load_project(work_root, negritaos_root)
    home = project_memory_home(context, memory_base)
    contract = _active_contract(
        work_root, negritaos_root, memory_base, provider, session_key
    )
    record = {
        "files": list(dict.fromkeys(files or [])),
        "learned": learned,
        "memory_id": f"NBM-{uuid.uuid4().hex.upper()}",
        "project": context.project_id,
        "session_id": contract.get("session_id") if contract else None,
        "summary": summary,
        "tags": list(dict.fromkeys(tags or [])),
        "timestamp": iso_timestamp(),
        "title": title,
        "type": normalized,
    }
    ledger = home / "observations.jsonl"
    try:
        append_jsonl(ledger, record)
    except PermissionError as exc:
        raise _permission_error(home, exc) from exc
    durable_ref = f"observations.jsonl#{record['memory_id']}"
    _record_durable_event(
        work_root,
        durable_ref,
        negritaos_root,
        memory_base,
        provider,
        session_key,
    )
    return {**record, "durable_ref": durable_ref}


def _render_handoff(
    project_id: str,
    memory_id: str,
    session_id: str | None,
    created_at: str,
    title: str,
    goal: str,
    discoveries: Iterable[str],
    accomplished: Iterable[str],
    next_steps: Iterable[str],
    files: Iterable[str],
    decisions: Iterable[str],
    blockers: Iterable[str],
) -> str:
    def section(name: str, values: Iterable[str]) -> str:
        items = list(values)
        body = "\n".join(f"- {value}" for value in items) if items else "_(none)_"
        return f"## {name}\n\n{body}\n"

    return (
        "---\n"
        "memory_schema_version: 2\n"
        f"memory_id: {memory_id}\n"
        f"project_id: {project_id}\n"
        f"session_id: {session_id or 'none'}\n"
        f"created_at: {created_at}\n"
        "---\n\n"
        f"# {title}\n\n"
        "## Goal\n\n"
        f"{goal}\n\n"
        f"{section('Discoveries', discoveries)}\n"
        f"{section('Accomplished', accomplished)}\n"
        f"{section('Decisions', decisions)}\n"
        f"{section('Blockers', blockers)}\n"
        f"{section('Next Steps', next_steps)}\n"
        f"{section('Relevant Files', (f'`{value}`' for value in files))}"
    )


def _managed_index_block(home: Path, project_id: str, updated_at: str) -> str:
    sessions_root = home / "sessions"
    sessions = [
        path
        for path in sorted(sessions_root.glob("*.md"), reverse=True)
        if path.name.lower() != "readme.md"
    ][:20]
    observations = _jsonl_records(home / "observations.jsonl")[-10:]
    session_rows = (
        "\n".join(f"- [{path.name}](sessions/{path.name})" for path in sessions)
        if sessions
        else "- _(none)_"
    )
    observation_rows = (
        "\n".join(
            f"- `{item.get('memory_id', 'unknown')}` | {item.get('title', 'Untitled')}"
            for item in reversed(observations)
        )
        if observations
        else "- _(none)_"
    )
    return (
        f"{INDEX_START}\n"
        "## Durable Memory\n\n"
        f"- Owner: `negrita_brain`\n"
        f"- Schema: `2`\n"
        f"- Project: `{project_id}`\n"
        f"- Updated: `{updated_at}`\n\n"
        "### Latest Handoffs\n\n"
        f"{session_rows}\n\n"
        "### Recent Observations\n\n"
        f"{observation_rows}\n"
        f"{INDEX_END}"
    )


def _merge_index(existing: str, block: str, project_id: str) -> str:
    if INDEX_START in existing and INDEX_END in existing:
        before, remainder = existing.split(INDEX_START, 1)
        _, after = remainder.split(INDEX_END, 1)
        return f"{before.rstrip()}\n\n{block}{after}"
    prefix = existing.rstrip() or f"# {project_id} Memory"
    return f"{prefix}\n\n{block}\n"


def handoff(
    work_root: Path,
    title: str,
    goal: str,
    discoveries: list[str] | None = None,
    accomplished: list[str] | None = None,
    next_steps: list[str] | None = None,
    files: list[str] | None = None,
    decisions: list[str] | None = None,
    blockers: list[str] | None = None,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
    provider: str | None = None,
    session_key: str | None = None,
) -> dict[str, Any]:
    """Create one immutable durable handoff and update the managed index block."""
    context = load_project(work_root, negritaos_root)
    home = project_memory_home(context, memory_base)
    contract = _active_contract(
        work_root, negritaos_root, memory_base, provider, session_key
    )
    current = now_madrid()
    created_at = iso_timestamp(current)
    memory_id = f"NBH-{uuid.uuid4().hex.upper()}"
    filename = f"{current.strftime('%Y-%m-%d_%H%M%S')}_{_slug(title)}.md"
    target = home / "sessions" / filename
    content = _render_handoff(
        context.project_id,
        memory_id,
        contract.get("session_id") if contract else None,
        created_at,
        title,
        goal,
        discoveries or [],
        accomplished or [],
        next_steps or [],
        files or [],
        decisions or [],
        blockers or [],
    )
    index_path = home / "index.md"
    try:
        with file_lock(home / ".memory.lock"):
            if target.exists():
                target = target.with_name(f"{target.stem}_{uuid.uuid4().hex[:8]}.md")
            atomic_write_text(target, content)
            existing = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
            block = _managed_index_block(home, context.project_id, created_at)
            atomic_write_text(index_path, _merge_index(existing, block, context.project_id))
    except PermissionError as exc:
        raise _permission_error(home, exc) from exc
    durable_ref = str(target.relative_to(home))
    _record_durable_event(
        work_root,
        durable_ref,
        negritaos_root,
        memory_base,
        provider,
        session_key,
    )
    return {
        "created_at": created_at,
        "durable_ref": durable_ref,
        "memory_id": memory_id,
        "project_id": context.project_id,
        "session_id": contract.get("session_id") if contract else None,
    }


def index_is_runtime_owned(index_path: Path) -> bool:
    """Detect the v1 runtime-generated index shape without changing it."""
    if not index_path.is_file():
        return False
    text = index_path.read_text(encoding="utf-8", errors="ignore")
    return "## Runtime Sessions" in text and INDEX_START not in text


def _runtime_session_state(session_dir: Path) -> tuple[int, str]:
    contract_path = session_dir / "contract.json"
    schema = 1
    if contract_path.is_file():
        try:
            schema = int(read_json(contract_path).get("schema_version", 1))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            schema = 1
    if (session_dir / "state.json").is_file() or (session_dir / "summary.json").is_file():
        return schema, "closed"
    return schema, "active"


def _memory_files(home: Path) -> list[Path]:
    candidates: list[Path] = []
    for relative in ("index.md", "observations.jsonl"):
        path = home / relative
        if path.is_file():
            candidates.append(path)
    for relative in ("sessions", "decisions", "tasks", "runtime/sessions"):
        root = home / relative
        if root.is_dir():
            candidates.extend(
                path
                for path in root.rglob("*")
                if path.is_file() and not path.name.endswith(".lock")
            )
    return sorted(set(candidates))


def _catalog_record(home: Path, project_id: str, path: Path) -> dict[str, Any]:
    relative = path.relative_to(home)
    parts = relative.parts
    artifact_type = "durable"
    authority = "canonical"
    state = "preserved"
    if parts and parts[0] == "runtime":
        artifact_type = "runtime_metadata"
        authority = "non_narrative"
        if len(parts) >= 3:
            schema, state = _runtime_session_state(home / parts[0] / parts[1] / parts[2])
            if schema == 1:
                artifact_type = "legacy_runtime"
                authority = "legacy_read_only"
    digest = _sha256_file(path)
    artifact_id = hashlib.sha256(
        f"{project_id}:{relative}:{digest}".encode("utf-8")
    ).hexdigest()
    stat = path.stat()
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "authority": authority,
        "canonical_reference": f"memory://projects/{project_id}/{relative}",
        "cataloged_at": iso_timestamp(),
        "file_path": str(relative),
        "mtime": iso_timestamp(datetime.fromtimestamp(stat.st_mtime).astimezone()),
        "project_id": project_id,
        "sha256": digest,
        "size": stat.st_size,
        "state": state,
    }


def migrate_memory(
    work_root: Path,
    apply: bool = False,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Catalog current memory in place without moving or rewriting any source."""
    context = load_project(work_root, negritaos_root)
    home = project_memory_home(context, memory_base)
    catalog = home / "catalog" / "legacy_memory.jsonl"
    existing = {
        str(item.get("artifact_id"))
        for item in _jsonl_records(catalog)
        if item.get("artifact_id")
    }
    records = [
        record
        for record in (_catalog_record(home, context.project_id, path) for path in _memory_files(home))
        if record["artifact_id"] not in existing
    ]
    if apply:
        try:
            with file_lock(home / ".memory.lock"):
                for record in records:
                    append_jsonl(catalog, record)
        except PermissionError as exc:
            raise _permission_error(home, exc) from exc
    return {
        "apply": apply,
        "catalog": str(catalog),
        "index_runtime_owned": index_is_runtime_owned(home / "index.md"),
        "new_records": len(records),
        "preserved_files": len(_memory_files(home)),
        "project_id": context.project_id,
        "status": "APPLIED" if apply else "DRY_RUN",
    }


def _open_v1_sessions(home: Path) -> list[str]:
    sessions = home / "runtime" / "sessions"
    if not sessions.is_dir():
        return []
    result = []
    for contract in sessions.glob("*/contract.json"):
        schema, state = _runtime_session_state(contract.parent)
        if schema == 1 and state == "active":
            result.append(contract.parent.name)
    return sorted(result)


def legacy_sessions(
    work_root: Path,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """List Memory v1 sessions without exposing narrative content."""
    context = load_project(work_root, negritaos_root)
    home = project_memory_home(context, memory_base)
    sessions_root = home / "runtime" / "sessions"
    rows: list[dict[str, Any]] = []
    if sessions_root.is_dir():
        for session_dir in sorted(sessions_root.iterdir()):
            contract_path = session_dir / "contract.json"
            if not contract_path.is_file():
                continue
            try:
                contract = read_json(contract_path)
                schema = int(contract.get("schema_version", 1))
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                continue
            if schema != 1:
                continue
            _, state = _runtime_session_state(session_dir)
            rows.append(
                {
                    "has_events": (session_dir / "events.jsonl").is_file(),
                    "has_summary": (session_dir / "summary.json").is_file(),
                    "session_id": session_dir.name,
                    "state": state,
                }
            )
    return {
        "project_id": context.project_id,
        "sessions": rows,
        "status": "READY",
    }


def _rebuilt_index(home: Path, project_id: str) -> str:
    block = _managed_index_block(home, project_id, iso_timestamp())
    return f"# {project_id} Memory\n\n{block}\n"


def rebuild_index(
    work_root: Path,
    apply: bool = False,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Preview or explicitly replace an index after all v1 sessions are closed."""
    context = load_project(work_root, negritaos_root)
    home = project_memory_home(context, memory_base)
    open_v1 = _open_v1_sessions(home)
    if open_v1:
        raise SessionError(
            "Cannot rebuild index while Memory v1 sessions are active: "
            + ", ".join(open_v1[:5])
        )
    index_path = home / "index.md"
    proposed = _rebuilt_index(home, context.project_id)
    backup_path: Path | None = None
    changed = not index_path.is_file() or index_path.read_text(encoding="utf-8") != proposed
    if apply and changed:
        current = now_madrid().strftime("%Y%m%d_%H%M%S")
        backup_path = home / "legacy_import" / "index" / f"{current}__index.md"
        try:
            with file_lock(home / ".memory.lock"):
                if index_path.is_file():
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(index_path, backup_path)
                atomic_write_text(index_path, proposed)
        except PermissionError as exc:
            raise _permission_error(home, exc) from exc
    return {
        "apply": apply,
        "backup_path": str(backup_path) if backup_path else None,
        "changed": changed,
        "index_path": str(index_path),
        "preview": proposed if not apply else None,
        "project_id": context.project_id,
        "status": "APPLIED" if apply else "DRY_RUN",
    }
