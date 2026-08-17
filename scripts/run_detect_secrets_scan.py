#!/usr/bin/env python3
"""Run detect-secrets and fail when tracked content contains findings."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from negrita_brain.security import (  # noqa: E402
    detect_secrets_finding_keys,
    detect_secrets_findings,
)


DEFAULT_EXCLUDE_FILES = [
    r"^\.git/",
    r"^\.secrets\.baseline$",
    r"^\.venv/",
    r"^\.venv-pr-quality/",
    r"^__pycache__/",
    r"^\.pytest_cache/",
    r"^\.mypy_cache/",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--baseline", type=Path, default=ROOT / ".secrets.baseline")
    parser.add_argument("--exclude-files", action="append", default=[])
    return parser


def _tool(name: str) -> str | None:
    """Find a tool on PATH or in the active Python environment."""
    executable = shutil.which(name)
    venv_executable = Path(sys.prefix) / "bin" / name
    if not executable and venv_executable.is_file():
        executable = str(venv_executable)
    repo_venv_executable = ROOT / ".venv-pr-quality" / "bin" / name
    if not executable and repo_venv_executable.is_file():
        executable = str(repo_venv_executable)
    return executable


def main() -> int:
    """Execute detect-secrets and report redacted finding metadata."""
    args = build_parser().parse_args()
    exclude_files = [*DEFAULT_EXCLUDE_FILES, *args.exclude_files]
    baseline = args.baseline if args.baseline.is_absolute() else args.root / args.baseline
    executable = _tool("detect-secrets")
    if not executable:
        print(
            "detect-secrets is not installed. Run scripts/setup_pr_quality_tools.sh.",
            file=sys.stderr,
        )
        return 2
    command = [executable, "scan", "--force-use-all-plugins"]
    baseline_keys: set[tuple[object, ...]] = set()
    if baseline.is_file():
        try:
            baseline_report = json.loads(baseline.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Invalid detect-secrets baseline: {exc}", file=sys.stderr)
            return 2
        baseline_keys = detect_secrets_finding_keys(baseline_report)
    for pattern in exclude_files:
        command.extend(["--exclude-files", pattern])
    result = subprocess.run(
        command,
        cwd=args.root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return result.returncode
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"Invalid detect-secrets JSON output: {exc}", file=sys.stderr)
        return 2
    if baseline_keys:
        current_keys = detect_secrets_finding_keys(report)
        if current_keys <= baseline_keys:
            print("detect-secrets: no unbaselined findings")
            return 0
        allowed = {
            key
            for key in current_keys
            if key not in baseline_keys
        }
        raw_results = report.get("results", {})
        if not isinstance(raw_results, dict):
            raw_results = {}
        report = {
            **report,
            "results": {
                filename: [
                    entry
                    for entry in entries
                    if (
                        str(entry.get("filename") or filename),
                        entry.get("line_number"),
                        str(entry.get("type") or "Unknown"),
                        str(entry.get("hashed_secret") or ""),
                    )
                    in allowed
                ]
                for filename, entries in raw_results.items()
                if isinstance(entries, list)
            },
        }
    findings = detect_secrets_findings(report)
    if findings:
        print("detect-secrets found potential secret material:")
        for finding in findings:
            print(
                f"- {finding['filename']}:{finding['line_number']} "
                f"{finding['type']} verified={finding['is_verified']}"
            )
        return 1
    print("detect-secrets: no findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
