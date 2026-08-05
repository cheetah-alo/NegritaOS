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

from negrita_brain.config import NEGRITAOS_ROOT, load_project, load_yaml  # noqa: E402
from negrita_brain.decisions import (  # noqa: E402
    accept_decision,
    propose_decision,
    supersede_decision,
)
from negrita_brain.doctor import doctor_all, doctor_project  # noqa: E402
from negrita_brain.documents import catalog_legacy  # noqa: E402
from negrita_brain.errors import BrainError  # noqa: E402
from negrita_brain.installer import Installer  # noqa: E402
from negrita_brain.runtime import (  # noqa: E402
    close_session,
    gate_action,
    record_event,
    resolve_session,
)


def _path(value: str) -> Path:
    """Parse a user path without requiring it to exist yet."""
    return Path(value).expanduser()


def _common(parser: argparse.ArgumentParser) -> None:
    """Add shared workspace and memory path arguments."""
    parser.add_argument("--root", type=_path, default=Path.cwd())
    parser.add_argument("--negritaos-root", type=_path, default=NEGRITAOS_ROOT)
    parser.add_argument("--memory-root", type=_path)


def build_parser() -> argparse.ArgumentParser:
    """Build the public CLI grammar."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="Create a READY session contract")
    _common(resolve)
    resolve.add_argument("--provider", required=True, choices=["codex", "claude", "ci", "human"])
    resolve.add_argument("--action", action="append", dest="actions")

    gate = commands.add_parser("gate", help="Authorize, warn, or block an action")
    _common(gate)
    gate.add_argument("--action", required=True, choices=["read", "write", "commit", "deliverable"])
    gate.add_argument("--path", type=_path)

    event = commands.add_parser("event", help="Append safe execution metadata")
    _common(event)
    event.add_argument("--kind", required=True)
    event.add_argument("--status", required=True)
    event.add_argument("--provider")
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

    close = commands.add_parser("close", help="Close the active session")
    _common(close)
    close.add_argument("--summary", required=True)
    close.add_argument("--status", default="COMPLETE")

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
    return parser


def execute(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    """Execute a parsed command and return its JSON result and exit code."""
    common = {
        "negritaos_root": args.negritaos_root,
        "memory_base": args.memory_root,
    }
    if args.command == "resolve":
        return resolve_session(args.root, args.provider, args.actions, **common), 0
    if args.command == "gate":
        result = gate_action(args.root, args.action, args.path, **common)
        return result, 2 if result["decision"] == "BLOCK" else 0
    if args.command == "event":
        metadata = {
            key: getattr(args, key)
            for key in ("provider", "tool", "action", "file_path", "decision_ids")
        }
        recorded = record_event(args.root, args.kind, args.status, metadata, **common)
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
        return close_session(args.root, args.summary, args.status, **common), 0
    if args.command == "doctor":
        result = (
            doctor_all(args.negritaos_root, args.memory_root)
            if args.all
            else doctor_project(args.root, **common)
        )
        return result, 1 if result["status"] == "FAIL" else 0
    if args.command == "catalog-legacy":
        if args.all:
            reports = []
            for registry_path in sorted((args.negritaos_root / "projects").glob("*.yaml")):
                project = load_yaml(registry_path).get("project", {})
                primary = project.get("local_paths", {}).get("primary")
                if not isinstance(primary, str):
                    continue
                context = load_project(Path(primary).expanduser(), args.negritaos_root)
                reports.append(
                    {
                        "project_id": context.project_id,
                        **catalog_legacy(context, args.memory_root),
                    }
                )
            return {
                "project_count": len(reports),
                "projects": reports,
                "total_added": sum(report["added"] for report in reports),
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
    except (BrainError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc), "status": "FAIL"}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
