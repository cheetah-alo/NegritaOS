"""Small serialization helpers shared by runtime ledgers."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator
from zoneinfo import ZoneInfo

import fcntl


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
    """Write deterministic JSON atomically in the destination directory."""
    atomic_write_text(
        path,
        json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
    )


def atomic_write_text(path: Path, content: str) -> None:
    """Replace a text file atomically and flush it before publication."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(str(temporary_path), str(path))
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


@contextmanager
def file_lock(path: Path) -> Iterator[None]:
    """Hold an exclusive advisory lock for one short filesystem transaction."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def append_jsonl(path: Path, value: Any) -> None:
    """Append one canonical JSON record under an adjacent file lock."""
    with file_lock(path.with_name(f".{path.name}.lock")):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(canonical_json(value) + "\n")
            stream.flush()
            os.fsync(stream.fileno())


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object from disk."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return value
