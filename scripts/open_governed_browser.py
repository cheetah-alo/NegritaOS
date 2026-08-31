#!/usr/bin/env python3
"""Resolve and optionally open the governed Brave profile for a project."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from negrita_brain.browser_routing import (  # noqa: E402
    BrowserRoutingError,
    build_brave_command,
    load_browser_routing_config,
    resolve_browser_route,
    verify_local_brave_profiles,
)
from negrita_brain.config import load_project  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="NegritaOS-managed project root. Defaults to the current directory.",
    )
    parser.add_argument("--purpose", help="Browser purpose, for example bigquery, github, jira, or documentation.")
    parser.add_argument("--url", help="Target URL. Queries and fragments are never printed.")
    parser.add_argument(
        "--profile",
        help="Explicit canonical profile alias. Explicit selection overrides automatic routing.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Open Brave after resolving the profile.")
    mode.add_argument("--dry-run", action="store_true", help="Resolve only. This is the default.")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        context = load_project(args.root.expanduser().resolve(), ROOT)
        config = load_browser_routing_config(ROOT)
        route = resolve_browser_route(
            context.project,
            config,
            purpose=args.purpose,
            url=args.url,
            explicit_profile=args.profile,
        )
        profile_errors = verify_local_brave_profiles(config)
        if profile_errors:
            raise BrowserRoutingError(profile_errors[0])
        command = build_brave_command(route, config, args.url)
        executable = Path(command[0])
        if not executable.is_file():
            raise BrowserRoutingError(f"Brave executable is missing: {executable}")
        if args.apply:
            subprocess.Popen(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        result = {
            "status": "OPENED" if args.apply else "DRY_RUN",
            "decision": "ALLOW",
            **route.as_dict(),
            "command_preview": [
                command[0],
                f"--profile-directory={route.profile_directory}",
                *config.get("browser", {}).get("launch_arguments", []),
                *([f"<URL host={route.target_host}>"] if args.url else []),
            ],
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (BrowserRoutingError, OSError, ValueError) as exc:
        print(
            json.dumps(
                {
                    "status": "BLOCKED_BROWSER_PROFILE_RESOLUTION",
                    "decision": "BLOCK",
                    "error": str(exc),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
