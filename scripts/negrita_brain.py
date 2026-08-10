#!/usr/bin/env python3
"""Command-line interface for the Negrita Brain governance kernel."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from negrita_brain.codex_config import configure_codex  # noqa: E402
from negrita_brain.config import NEGRITAOS_ROOT, load_project, load_yaml  # noqa: E402
from negrita_brain.decisions import (  # noqa: E402
    accept_decision,
    propose_decision,
    supersede_decision,
)
from negrita_brain.doctor import doctor_all, doctor_project  # noqa: E402
from negrita_brain.documents import catalog_legacy  # noqa: E402
from negrita_brain.errors import BrainError, MemoryPermissionError  # noqa: E402
from negrita_brain.installer import Installer  # noqa: E402
from negrita_brain.memory import (  # noqa: E402
    handoff,
    legacy_sessions,
    memory_status,
    migrate_memory,
    rebuild_index,
    remember,
)
from negrita_brain.runtime import (  # noqa: E402
    close_session,
    gate_action,
    record_event,
    resolve_session,
)


PROVIDERS = ["codex", "claude", "ci", "human"]


def _path(value: str) -> Path:
    """Parse a user path without requiring it to exist yet."""
    return Path(value).expanduser()


def _common(parser: argparse.ArgumentParser) -> None:
    """Add shared workspace and memory path arguments."""
    parser.add_argument("--root", type=_path, default=Path.cwd())
    parser.add_argument("--negritaos-root", type=_path, default=NEGRITAOS_ROOT)
    parser.add_argument("--memory-root", type=_path)


def _session(parser: argparse.ArgumentParser, provider_required: bool = False) -> None:
    """Add provider-scoped session selection arguments."""
    parser.add_argument("--provider", required=provider_required, choices=PROVIDERS)
    parser.add_argument("--session-key")


def _apply_switch(parser: argparse.ArgumentParser) -> None:
    """Add explicit dry-run/apply controls with dry-run as the default."""
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    """Build the public CLI grammar."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="Create a READY session contract")
    _common(resolve)
    _session(resolve, provider_required=True)
    resolve.add_argument("--action", action="append", dest="actions")

    gate = commands.add_parser("gate", help="Authorize, warn, or block an action")
    _common(gate)
    _session(gate)
    gate.add_argument(
        "--action", required=True, choices=["read", "write", "commit", "deliverable"]
    )
    gate.add_argument("--path", type=_path)
    gate.add_argument(
        "--authorize-legacy-recovery",
        action="store_true",
        help="Explicitly authorize the blocked Memory v1 recovery path",
    )
    gate.add_argument("--authorized-by")
    gate.add_argument("--authorization-reason")
    gate.add_argument("--recovery-scope")

    event = commands.add_parser("event", help="Append safe execution metadata")
    _common(event)
    _session(event)
    event.add_argument("--kind", required=True)
    event.add_argument("--status", required=True)
    event.add_argument("--tool")
    event.add_argument("--action")
    event.add_argument("--path", dest="file_path")
    event.add_argument("--decision-id", action="append", dest="decision_ids")
    event.add_argument("--acceptance-ref")

    decision = commands.add_parser("decision", help="Manage append-only decisions")
    decision_commands = decision.add_subparsers(dest="decision_command", required=True)
    propose = decision_commands.add_parser("propose")
    _common(propose)
    propose.add_argument("--title", required=True)
    propose.add_argument("--summary", required=True)
    propose.add_argument("--kind", required=True)
    propose.add_argument("--source-ref", action="append", dest="source_refs")
    accept = decision_commands.add_parser("accept")
    _common(accept)
    accept.add_argument("decision_id")
    accept.add_argument("--accepted-by", required=True)
    accept.add_argument("--acceptance-ref", required=True)
    supersede = decision_commands.add_parser("supersede")
    _common(supersede)
    supersede.add_argument("decision_id")
    supersede.add_argument("--title", required=True)
    supersede.add_argument("--summary", required=True)
    supersede.add_argument("--kind", required=True)

    close = commands.add_parser("close", help="Close the selected active session")
    _common(close)
    _session(close)
    close.add_argument(
        "--summary",
        help="Memory v1 compatibility only; ignored for Memory v2 sessions",
    )
    close.add_argument("--status", default="COMPLETE")
    close.add_argument("--durable-ref", action="append", dest="durable_refs")
    close.add_argument(
        "--legacy-session-id",
        help="Select one exact Memory v1 session for an authorized closure",
    )
    close.add_argument(
        "--authorize-legacy-close",
        action="store_true",
        help="Authorize the selected Memory v1 closure after backup",
    )
    close.add_argument("--authorized-by")
    close.add_argument("--authorization-reason")

    memory = commands.add_parser("memory", help="Manage canonical durable project memory")
    memory_commands = memory.add_subparsers(dest="memory_command", required=True)
    status = memory_commands.add_parser("status")
    _common(status)
    _session(status)
    observation = memory_commands.add_parser("remember")
    _common(observation)
    _session(observation)
    observation.add_argument("--type", required=True, dest="observation_type")
    observation.add_argument("--title", required=True)
    observation.add_argument("--summary", required=True)
    observation.add_argument("--learned", required=True)
    observation.add_argument("--tag", action="append", dest="tags")
    observation.add_argument("--file", action="append", dest="files")
    handoff_parser = memory_commands.add_parser("handoff")
    _common(handoff_parser)
    _session(handoff_parser)
    handoff_parser.add_argument("--title", required=True)
    handoff_parser.add_argument("--goal", required=True)
    handoff_parser.add_argument("--discovery", action="append", dest="discoveries")
    handoff_parser.add_argument("--accomplished", action="append")
    handoff_parser.add_argument("--next-step", action="append", dest="next_steps")
    handoff_parser.add_argument("--file", action="append", dest="files")
    handoff_parser.add_argument("--decision", action="append", dest="decisions")
    handoff_parser.add_argument("--blocker", action="append", dest="blockers")
    migrate = memory_commands.add_parser("migrate")
    _common(migrate)
    migrate.add_argument("--all", action="store_true")
    _apply_switch(migrate)
    legacy_sessions_parser = memory_commands.add_parser(
        "legacy-sessions", help="List Memory v1 sessions without reading narratives"
    )
    _common(legacy_sessions_parser)
    rebuild = memory_commands.add_parser("rebuild-index")
    _common(rebuild)
    _apply_switch(rebuild)

    doctor = commands.add_parser("doctor", help="Audit project runtime health")
    _common(doctor)
    doctor.add_argument("--all", action="store_true")

    legacy = commands.add_parser(
        "catalog-legacy",
        help="Catalog legacy deliverables without moving them",
    )
    _common(legacy)
    legacy.add_argument("--all", action="store_true")

    install = commands.add_parser("install", help="Install managed entrypoints and hooks")
    _common(install)
    install.add_argument("--backup-root", type=_path)
    install.add_argument("--all", action="store_true")
    install.add_argument("--dry-run", action="store_true")
    install.add_argument("--pre-commit", action="store_true")

    configure = commands.add_parser("configure", help="Configure provider integration")
    configure_commands = configure.add_subparsers(
        dest="configure_command", required=True
    )
    codex = configure_commands.add_parser("codex")
    codex_mode = codex.add_mutually_exclusive_group()
    codex_mode.add_argument("--check", action="store_true")
    codex_mode.add_argument("--apply", action="store_true")
    codex.add_argument("--config-path", type=_path)
    codex.add_argument("--memory-path", type=_path)
    codex.add_argument("--backup-root", type=_path)
    return parser


def _project_reports(args: argparse.Namespace, operation: Any) -> list[dict[str, Any]]:
    """Run one memory operation for every registry with a resolvable primary path."""
    reports: list[dict[str, Any]] = []
    for registry_path in sorted((args.negritaos_root / "projects").glob("*.yaml")):
        project = load_yaml(registry_path).get("project", {})
        primary = project.get("local_paths", {}).get("primary") if isinstance(project, dict) else None
        if not isinstance(primary, str):
            continue
        try:
            reports.append(operation(Path(primary).expanduser()))
        except (BrainError, OSError, ValueError, json.JSONDecodeError) as exc:
            reports.append({"error": str(exc), "project_id": registry_path.stem})
    return reports


def execute(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    """Execute a parsed command and return its JSON result and exit code."""
    if args.command == "configure":
        result = configure_codex(
            apply=args.apply,
            config_path=args.config_path,
            memory_root=args.memory_path,
            backup_root=args.backup_root,
        )
        return result, 0
    common = {
        "negritaos_root": args.negritaos_root,
        "memory_base": args.memory_root,
    }
    if args.command == "resolve":
        return resolve_session(
            args.root,
            args.provider,
            args.actions,
            session_key=args.session_key,
            **common,
        ), 0
    if args.command == "gate":
        result = gate_action(
            args.root,
            args.action,
            args.path,
            provider=args.provider,
            session_key=args.session_key,
            authorize_legacy_recovery=args.authorize_legacy_recovery,
            authorized_by=args.authorized_by,
            authorization_reason=args.authorization_reason,
            recovery_scope=args.recovery_scope,
            **common,
        )
        return result, 2 if result["decision"] == "BLOCK" else 0
    if args.command == "event":
        metadata = {
            key: getattr(args, key)
            for key in ("provider", "tool", "action", "file_path", "decision_ids")
        }
        recorded = record_event(
            args.root,
            args.kind,
            args.status,
            metadata,
            provider=args.provider,
            session_key=args.session_key,
            **common,
        )
        accepted = []
        if args.kind in {"commit", "pull_request"} and args.decision_ids:
            acceptance_ref = args.acceptance_ref or f"{args.kind}:{args.status}"
            for decision_id in args.decision_ids:
                accepted.append(
                    accept_decision(
                        args.root,
                        decision_id,
                        args.provider or "runtime",
                        acceptance_ref,
                        **common,
                    )
                )
        return {"event": recorded, "accepted_decisions": accepted}, 0
    if args.command == "decision":
        if args.decision_command == "propose":
            return propose_decision(
                args.root, args.title, args.summary, args.kind, args.source_refs, **common
            ), 0
        if args.decision_command == "accept":
            return accept_decision(
                args.root,
                args.decision_id,
                args.accepted_by,
                args.acceptance_ref,
                **common,
            ), 0
        return supersede_decision(
            args.root, args.decision_id, args.title, args.summary, args.kind, **common
        ), 0
    if args.command == "close":
        return close_session(
            args.root,
            args.summary,
            args.status,
            provider=args.provider,
            session_key=args.session_key,
            legacy_session_id=args.legacy_session_id,
            authorize_legacy_close=args.authorize_legacy_close,
            authorized_by=args.authorized_by,
            authorization_reason=args.authorization_reason,
            durable_refs=args.durable_refs,
            **common,
        ), 0
    if args.command == "memory":
        if args.memory_command == "status":
            return memory_status(
                args.root,
                provider=args.provider,
                session_key=args.session_key,
                **common,
            ), 0
        if args.memory_command == "legacy-sessions":
            return legacy_sessions(args.root, **common), 0
        if args.memory_command == "remember":
            return remember(
                args.root,
                args.observation_type,
                args.title,
                args.summary,
                args.learned,
                args.tags,
                args.files,
                provider=args.provider,
                session_key=args.session_key,
                **common,
            ), 0
        if args.memory_command == "handoff":
            return handoff(
                args.root,
                args.title,
                args.goal,
                args.discoveries,
                args.accomplished,
                args.next_steps,
                args.files,
                args.decisions,
                args.blockers,
                provider=args.provider,
                session_key=args.session_key,
                **common,
            ), 0
        if args.memory_command == "migrate":
            if args.all:
                reports = _project_reports(
                    args,
                    lambda root: migrate_memory(root, args.apply, **common),
                )
                return {
                    "apply": args.apply,
                    "failed": sum("error" in report for report in reports),
                    "project_count": len(reports),
                    "projects": reports,
                }, 1 if any("error" in report for report in reports) else 0
            return migrate_memory(args.root, args.apply, **common), 0
        return rebuild_index(args.root, args.apply, **common), 0
    if args.command == "doctor":
        result = (
            doctor_all(args.negritaos_root, args.memory_root)
            if args.all
            else doctor_project(args.root, **common)
        )
        return result, 1 if result["status"] == "FAIL" else 0
    if args.command == "catalog-legacy":
        if args.all:
            reports = _project_reports(
                args,
                lambda root: {
                    "project_id": load_project(root, args.negritaos_root).project_id,
                    **catalog_legacy(
                        load_project(root, args.negritaos_root), args.memory_root
                    ),
                },
            )
            return {
                "project_count": len(reports),
                "projects": reports,
                "total_added": sum(report.get("added", 0) for report in reports),
            }, 0
        context = load_project(args.root, args.negritaos_root)
        return catalog_legacy(context, args.memory_root), 0
    installer = Installer(args.negritaos_root, args.backup_root, args.memory_root)
    result = (
        installer.install_all(args.dry_run, args.pre_commit)
        if args.all
        else installer.install(args.root, args.dry_run, args.pre_commit)
    )
    return result, 1 if result.get("failed") else 0


def main() -> int:
    """Run the CLI and emit one JSON object."""
    try:
        result, code = execute(build_parser().parse_args())
    except MemoryPermissionError as exc:
        print(
            json.dumps(
                {
                    "error": str(exc),
                    "error_code": exc.code,
                    "retry": "configure_codex_or_request_elevation",
                    "status": exc.status,
                },
                sort_keys=True,
            )
        )
        return 3
    except PermissionError as exc:
        print(
            json.dumps(
                {
                    "error": str(exc),
                    "error_code": "MEMORY_WRITE_PERMISSION",
                    "retry": "configure_codex_or_request_elevation",
                    "status": "PERMISSION_REQUIRED",
                },
                sort_keys=True,
            )
        )
        return 3
    except (BrainError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc), "status": "FAIL"}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
