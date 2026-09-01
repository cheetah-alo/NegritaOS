#!/usr/bin/env python3
"""Enforce aggregate Coverage.py statement coverage for src/negrita_brain."""

from __future__ import annotations

import argparse
import io
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "src" / "negrita_brain"
sys.path.insert(0, str(ROOT))


def measure() -> tuple[int, int, unittest.result.TestResult, list[tuple[str, int, int]]]:
    """Run the full test suite and return package line-coverage evidence."""
    from coverage import Coverage  # type: ignore[import-not-found]

    coverage = Coverage(data_file=None)
    coverage.start()
    try:
        loader = unittest.TestLoader()
        suite = loader.discover(str(ROOT / "tests"), pattern="test_*.py")
        runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
        result = runner.run(suite)
    finally:
        coverage.stop()
    covered = 0
    executable = 0
    details: list[tuple[str, int, int]] = []
    for path in PACKAGE.glob("*.py"):
        _, statements, _, missing, _ = coverage.analysis2(str(path))
        file_covered = len(statements) - len(missing)
        executable += len(statements)
        covered += file_covered
        details.append((path.name, file_covered, len(statements)))
    return covered, executable, result, details


def _rerun_with_quality_venv() -> int | None:
    """Use the governed quality venv when system Python lacks Coverage.py."""
    candidate = ROOT / ".venv-pr-quality" / "bin" / "python"
    quality_prefix = candidate.parent.parent
    if not candidate.is_file() or Path(sys.prefix).resolve() == quality_prefix.resolve():
        return None
    completed = subprocess.run(
        [str(candidate), str(Path(__file__).resolve()), *sys.argv[1:]],
        cwd=ROOT,
        check=False,
    )
    return completed.returncode


def main() -> int:
    """Run the focused suite and enforce the requested threshold."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fail-under", type=float, default=80.0)
    parser.add_argument("--details", action="store_true")
    args = parser.parse_args()
    try:
        covered, executable, result, details = measure()
    except ModuleNotFoundError as exc:
        if exc.name != "coverage":
            raise
        rerun = _rerun_with_quality_venv()
        if rerun is not None:
            return rerun
        print(
            "Coverage.py is required. Run scripts/setup_pr_quality_tools.sh.",
            file=sys.stderr,
        )
        return 2
    percent = (covered / executable * 100) if executable else 100.0
    print(
        f"Negrita Brain line coverage: {covered}/{executable} "
        f"({percent:.2f}%), required >= {args.fail_under:.2f}%"
    )
    if args.details:
        for name, file_covered, file_executable in sorted(details):
            percent_file = (
                file_covered / file_executable * 100 if file_executable else 100.0
            )
            print(f"- {name}: {file_covered}/{file_executable} ({percent_file:.2f}%)")
    if not result.wasSuccessful():
        print("NegritaOS tests failed while measuring Negrita Brain coverage.")
        return 1
    if percent < args.fail_under:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
