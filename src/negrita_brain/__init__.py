"""Executable governance and canonical memory kernel for NegritaOS projects."""

from .memory import handoff, memory_status, migrate_memory, rebuild_index, remember
from .git_traceability import snapshot_git
from .git_trailers import append_trailers, build_brain_trailers, parse_trailers
from .runtime import close_session, gate_action, record_event, resolve_session

__all__ = [
    "close_session",
    "append_trailers",
    "build_brain_trailers",
    "gate_action",
    "handoff",
    "memory_status",
    "migrate_memory",
    "rebuild_index",
    "record_event",
    "parse_trailers",
    "remember",
    "resolve_session",
    "snapshot_git",
]
__version__ = "2.0.0"
