"""Safe, idempotent Git trailers derived from a Negrita Brain contract."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


SUPPORTED_TRAILERS = frozenset(
    {
        "Negrita-Contract",
        "Negrita-Session",
        "Negrita-Worktree",
        "Negrita-Gates",
        "Negrita-Decision",
    }
)
_MAX_TRAILER_VALUE_LENGTH = 512


def _validated_value(key: str, value: Any) -> str:
    """Return one canonical trailer value or reject unsafe input."""
    if key not in SUPPORTED_TRAILERS:
        raise ValueError(f"Unsupported Negrita trailer: {key}")
    if not isinstance(value, str):
        raise ValueError(f"Trailer {key} must be a string")
    normalized = value.strip()
    if not normalized or len(normalized) > _MAX_TRAILER_VALUE_LENGTH:
        raise ValueError(
            f"Trailer {key} must contain 1-{_MAX_TRAILER_VALUE_LENGTH} characters"
        )
    if "\n" in normalized or "\r" in normalized:
        raise ValueError(f"Trailer {key} cannot contain line breaks")
    return normalized


def parse_trailers(message: str) -> dict[str, str]:
    """Return supported trailers found in a commit message.

    The last occurrence wins, matching Git's usual bottom-up trailer
    interpretation, while unknown trailer-like lines remain untouched.
    """
    if not isinstance(message, str):
        raise ValueError("Commit message must be a string")
    parsed: dict[str, str] = {}
    for line in message.splitlines():
        key, separator, raw_value = line.partition(":")
        if separator and key in SUPPORTED_TRAILERS:
            value = raw_value.strip()
            if value:
                parsed[key] = value
    return parsed


def append_trailers(message: str, trailers: Mapping[str, str]) -> str:
    """Append only missing supported trailers and preserve existing text."""
    if not isinstance(message, str):
        raise ValueError("Commit message must be a string")
    normalized = {
        key: _validated_value(key, value) for key, value in trailers.items()
    }
    existing = parse_trailers(message)
    missing = {
        key: value for key, value in normalized.items() if key not in existing
    }
    if not missing:
        return message
    body = message.rstrip("\r\n")
    trailer_block = "\n".join(f"{key}: {value}" for key, value in missing.items())
    return f"{body}\n\n{trailer_block}" if body else trailer_block


def _joined_values(values: Sequence[str] | None, key: str) -> str | None:
    """Return deterministic comma-separated values without duplicates."""
    if not values:
        return None
    unique: list[str] = []
    for value in values:
        normalized = _validated_value(key, value)
        if normalized not in unique:
            unique.append(normalized)
    return ", ".join(unique) if unique else None


def build_brain_trailers(
    contract: Mapping[str, Any],
    gates: Sequence[str] | None = None,
    decision_ids: Sequence[str] | None = None,
) -> dict[str, str]:
    """Build canonical trailers from an immutable active session contract."""
    session_id = contract.get("session_id")
    contract_sha256 = contract.get("contract_sha256")
    if not isinstance(session_id, str) or not session_id.strip():
        raise ValueError("Active contract must contain session_id")
    if not isinstance(contract_sha256, str) or not contract_sha256.strip():
        raise ValueError("Active contract must contain contract_sha256")

    trailers = {
        "Negrita-Contract": _validated_value("Negrita-Contract", contract_sha256),
        "Negrita-Session": _validated_value("Negrita-Session", session_id),
    }
    git_state = contract.get("git")
    if isinstance(git_state, Mapping):
        worktree_id = git_state.get("worktree_id")
        if worktree_id is not None:
            trailers["Negrita-Worktree"] = _validated_value(
                "Negrita-Worktree", worktree_id
            )
    gates_value = _joined_values(gates, "Negrita-Gates")
    if gates_value:
        trailers["Negrita-Gates"] = gates_value
    decisions_value = _joined_values(decision_ids, "Negrita-Decision")
    if decisions_value:
        trailers["Negrita-Decision"] = decisions_value
    return trailers
