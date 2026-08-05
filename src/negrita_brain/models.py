"""Small serialization helpers shared by runtime ledgers."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


MADRID = ZoneInfo("Europe/Madrid")


def now_madrid() -> datetime:
    """Return the current timezone-aware Europe/Madrid timestamp."""
    return datetime.now(MADRID)


def iso_timestamp(value: datetime | None = None) -> str:
    """Return a seconds-precision ISO timestamp in Europe/Madrid."""
    current = value or now_madrid()
    return current.astimezone(MADRID).isoformat(timespec="seconds")


def canonical_json(value: Any) -> str:
    """Serialize a value deterministically for hashing and storage."""
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    """Return the SHA-256 digest of canonical JSON."""
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    """Write deterministic, human-readable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def append_jsonl(path: Path, value: Any) -> None:
    """Append one canonical JSON record to a ledger."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(canonical_json(value) + "\n")


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object from disk."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return value
