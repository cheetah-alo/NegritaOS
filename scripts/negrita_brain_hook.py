#!/usr/bin/env python3
"""Claude hook bridge for Negrita Brain session and mutation enforcement."""

from __future__ import annotations

import json
import re
import shlex
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from negrita_brain.documents import DELIVERABLE_EXTENSIONS  # noqa: E402
from negrita_brain.errors import BrainError, SessionError  # noqa: E402
from negrita_brain.runtime import (  # noqa: E402
    close_session,
    gate_action,
    load_active_session,
    record_event,
    resolve_session,
)


MUTATING_SHELL = re.compile(
    r"(^|[;&|]\s*)(rm|mv|cp|mkdir|touch|chmod|chown|ln|tee|apply_patch|sed\s+-i|"
    r"git\s+(add|commit|push|rebase|merge|reset|checkout|switch|restore|cherry-pick|revert)|"
    r"npm\s+(install|run)|pip\S*\s+install|python\S*\s+.*(?:write|build|generate))\b|>{1,2}",
    re.IGNORECASE,
)
READ_ONLY_SHELL = re.compile(
    r"(pwd|ls(?:\s+.*)?|find\s+.*|rg\s+.*|grep\s+.*|cat\s+.*|head\s+.*|tail\s+.*|"
    r"wc\s+.*|git\s+(status|diff|log|show|rev-parse)(?:\s+.*)?|"
    r"python3?\s+.*negrita_brain\.py\s+(gate|doctor)(?:\s+.*)?)",
    re.IGNORECASE,
)


def _payload() -> dict[str, Any]:
    """Read one Claude hook payload without retaining its user content."""
    try:
        value = json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _root(payload: dict[str, Any]) -> Path:
    """Resolve the hook workspace path."""
    raw = payload.get("cwd")
    return Path(raw).expanduser().resolve() if isinstance(raw, str) else Path.cwd()


def _session_key(payload: dict[str, Any]) -> str | None:
    """Return Claude's native session id without logging transcript content."""
    value = payload.get("session_id")
    return value if isinstance(value, str) and value.strip() else None


def _tool(payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Extract tool name and input without logging input values."""
    name = payload.get("tool_name")
    tool_input = payload.get("tool_input")
    return str(name or "unknown"), tool_input if isinstance(tool_input, dict) else {}


def _action_and_path(tool: str, tool_input: dict[str, Any]) -> tuple[str, Path | None]:
    """Classify a tool invocation for the gate."""
    raw_path = tool_input.get("file_path") or tool_input.get("path")
    path = Path(raw_path) if isinstance(raw_path, str) else None
    if tool in {"Edit", "Write", "MultiEdit", "NotebookEdit"}:
        return "write", path
    if tool == "Bash":
        command = str(tool_input.get("command", "")).strip()
        try:
            tokens = shlex.split(command)
        except ValueError:
            tokens = command.split()
        for token in reversed(tokens):
            candidate = token.split("=", 1)[-1].rstrip(";|&")
            if Path(candidate).suffix.lower() in DELIVERABLE_EXTENSIONS:
                path = Path(candidate)
                break
        if MUTATING_SHELL.search(command) or READ_ONLY_SHELL.fullmatch(command) is None:
            return "write", path
    return "read", path


def _hook_output(event: str, context: str | None = None, deny: str | None = None) -> None:
    """Emit supported Claude hook control JSON."""
    specific: dict[str, Any] = {"hookEventName": event}
    if context:
        specific["additionalContext"] = context
    if deny:
        specific["permissionDecision"] = "deny"
        specific["permissionDecisionReason"] = deny
    print(json.dumps({"hookSpecificOutput": specific}, sort_keys=True))


def handle(event: str, payload: dict[str, Any]) -> int:
    """Handle one hook event without persisting prompts, responses, or outputs."""
    root = _root(payload)
    session_key = _session_key(payload)
    if event == "SessionStart":
        contract = resolve_session(
            root, "claude", ["planning"], session_key=session_key
        )
        _hook_output(
            event,
            f"Negrita Brain {contract['state']}: {contract['session_id']} | profiles="
            + ",".join(contract["profiles"]),
        )
        return 0
    if event == "UserPromptSubmit":
        try:
            _, contract, _ = load_active_session(
                root, provider="claude", session_key=session_key
            )
            if contract.get("state") != "READY":
                raise SessionError("Active contract is closed")
        except BrainError:
            contract = resolve_session(
                root, "claude", ["planning"], session_key=session_key
            )
        _hook_output(
            event,
            f"Negrita Brain {contract['state']}: {contract['session_id']} | profiles="
            + ",".join(contract["profiles"]),
        )
        return 0
    if event == "PreToolUse":
        tool, tool_input = _tool(payload)
        action, path = _action_and_path(tool, tool_input)
        result = gate_action(
            root, action, path, provider="claude", session_key=session_key
        )
        if result["decision"] == "BLOCK":
            _hook_output(event, deny="; ".join(result["reasons"]))
            return 2
        if result["decision"] == "WARN":
            _hook_output(event, context="; ".join(result["reasons"]))
        return 0
    if event == "PostToolUse":
        tool, tool_input = _tool(payload)
        action, path = _action_and_path(tool, tool_input)
        record_event(
            root,
            "tool_completed",
            "OK",
            {
                "provider": "claude",
                "tool": tool,
                "action": action,
                "file_path": str(path) if path else None,
            },
            provider="claude",
            session_key=session_key,
        )
        return 0
    if event == "Stop":
        record_event(
            root,
            "provider_stop",
            "OK",
            {"provider": "claude"},
            provider="claude",
            session_key=session_key,
        )
        return 0
    if event == "SessionEnd":
        try:
            close_session(
                root,
                "Claude SessionEnd hook",
                "INCOMPLETE",
                provider="claude",
                session_key=session_key,
            )
        except SessionError:
            pass
        return 0
    return 0


def main() -> int:
    """Read the hook event argument and dispatch safely."""
    if len(sys.argv) != 2:
        return 1
    try:
        return handle(sys.argv[1], _payload())
    except (BrainError, OSError, ValueError) as exc:
        if sys.argv[1] == "PreToolUse":
            _hook_output("PreToolUse", deny=f"Negrita Brain preflight failed: {exc}")
            return 2
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
