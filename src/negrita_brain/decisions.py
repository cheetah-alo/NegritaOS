"""Append-only decision ledger and repository ADR projection."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Any

from .config import NEGRITAOS_ROOT, load_project, project_memory_home
from .errors import DecisionError
from .models import append_jsonl, iso_timestamp


VALID_KINDS = {"architecture", "contract", "governance", "product", "delivery"}


def _slug(value: str) -> str:
    """Return a bounded ASCII decision slug."""
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized[:60] or "decision"


def _ledger_path(context: Any, memory_base: Path | None) -> Path:
    """Return the canonical decision ledger path."""
    return project_memory_home(context, memory_base) / "decisions" / "ledger.jsonl"


def read_decision_state(ledger: Path) -> dict[str, dict[str, Any]]:
    """Project append-only decision events into current state by id."""
    state: dict[str, dict[str, Any]] = {}
    if not ledger.is_file():
        return state
    for line in ledger.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        decision_id = event.get("decision_id")
        if not isinstance(decision_id, str):
            continue
        current = state.setdefault(decision_id, {})
        current.update(event)
    return state


def _write_adr(root: Path, record: dict[str, Any]) -> str | None:
    """Create a candidate ADR for architecture and contract decisions in Git repos."""
    if record["kind"] not in {"architecture", "contract"} or not (root / ".git").exists():
        return None
    filename = f"{record['decision_id'].lower()}-{_slug(record['title'])}.md"
    relative = Path("docs") / "decisions" / filename
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return str(relative)
    target.write_text(
        "---\n"
        f"decision_id: {record['decision_id']}\n"
        "status: CANDIDATE\n"
        f"created_at: {record['occurred_at']}\n"
        "---\n\n"
        f"# {record['title']}\n\n"
        "## Context\n\n"
        f"{record['summary']}\n\n"
        "## Decision\n\n"
        "Candidate pending explicit acceptance or a commit/PR carrying this Decision ID.\n\n"
        "## Consequences\n\n"
        "To be completed when the decision is accepted.\n",
        encoding="utf-8",
    )
    return str(relative)


def _update_adr_status(
    root: Path,
    current: dict[str, Any],
    status: str,
    reference: str,
) -> None:
    """Project an append-only transition into the versioned ADR status."""
    raw_path = current.get("adr_path")
    if not isinstance(raw_path, str):
        return
    path = root / raw_path
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    transition = f"## Status Transition\n\n- Status: `{status}`\n- Reference: `{reference}`"
    if transition in text:
        return
    text = re.sub(r"^status: [A-Z_]+$", f"status: {status}", text, count=1, flags=re.MULTILINE)
    path.write_text(f"{text.rstrip()}\n\n{transition}\n", encoding="utf-8")


def propose_decision(
    work_root: Path,
    title: str,
    summary: str,
    kind: str,
    source_refs: list[str] | None = None,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Append a CANDIDATE decision and create an ADR when required."""
    normalized_kind = kind.lower()
    if normalized_kind not in VALID_KINDS:
        raise DecisionError(f"Unsupported decision kind: {kind}")
    context = load_project(work_root, negritaos_root)
    decision_id = f"NBD-{iso_timestamp()[:10].replace('-', '')}-{uuid.uuid4().hex[:8].upper()}"
    record = {
        "decision_id": decision_id,
        "event": "CANDIDATE",
        "kind": normalized_kind,
        "occurred_at": iso_timestamp(),
        "project_id": context.project_id,
        "source_refs": source_refs or [],
        "summary": summary,
        "title": title,
    }
    adr_path = _write_adr(context.work_root, record)
    if adr_path:
        record["adr_path"] = adr_path
    append_jsonl(_ledger_path(context, memory_base), record)
    return record


def accept_decision(
    work_root: Path,
    decision_id: str,
    accepted_by: str,
    acceptance_ref: str,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Append an ACCEPTED transition for an existing candidate."""
    context = load_project(work_root, negritaos_root)
    ledger = _ledger_path(context, memory_base)
    current = read_decision_state(ledger).get(decision_id)
    if current is None:
        raise DecisionError(f"Unknown decision: {decision_id}")
    if current.get("event") == "SUPERSEDED":
        raise DecisionError(f"Superseded decision cannot be accepted: {decision_id}")
    if current.get("event") == "ACCEPTED":
        _update_adr_status(
            context.work_root,
            current,
            "ACCEPTED",
            str(current.get("acceptance_ref", acceptance_ref)),
        )
        return {
            "decision_id": decision_id,
            "event": "ACCEPTED",
            "idempotent": True,
            "project_id": context.project_id,
        }
    record = {
        "acceptance_ref": acceptance_ref,
        "accepted_by": accepted_by,
        "decision_id": decision_id,
        "event": "ACCEPTED",
        "occurred_at": iso_timestamp(),
        "project_id": context.project_id,
    }
    append_jsonl(ledger, record)
    _update_adr_status(context.work_root, current, "ACCEPTED", acceptance_ref)
    return record


def supersede_decision(
    work_root: Path,
    decision_id: str,
    title: str,
    summary: str,
    kind: str,
    negritaos_root: Path = NEGRITAOS_ROOT,
    memory_base: Path | None = None,
) -> dict[str, Any]:
    """Create a replacement candidate and supersede the old decision append-only."""
    context = load_project(work_root, negritaos_root)
    ledger = _ledger_path(context, memory_base)
    current = read_decision_state(ledger).get(decision_id)
    if current is None:
        raise DecisionError(f"Unknown decision: {decision_id}")
    if current.get("event") == "SUPERSEDED":
        raise DecisionError(f"Decision is already superseded: {decision_id}")
    replacement = propose_decision(
        work_root,
        title,
        summary,
        kind,
        source_refs=[decision_id],
        negritaos_root=negritaos_root,
        memory_base=memory_base,
    )
    transition = {
        "decision_id": decision_id,
        "event": "SUPERSEDED",
        "occurred_at": iso_timestamp(),
        "project_id": context.project_id,
        "superseded_by": replacement["decision_id"],
    }
    append_jsonl(ledger, transition)
    _update_adr_status(
        context.work_root,
        current,
        "SUPERSEDED",
        replacement["decision_id"],
    )
    return {"replacement": replacement, "transition": transition}
