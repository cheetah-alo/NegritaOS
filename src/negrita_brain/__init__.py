"""Executable governance kernel for NegritaOS projects."""

from .runtime import close_session, gate_action, record_event, resolve_session

__all__ = ["close_session", "gate_action", "record_event", "resolve_session"]
__version__ = "1.0.0"
