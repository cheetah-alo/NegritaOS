#!/usr/bin/env python3
"""Enforce aggregate stdlib trace coverage for src/negrita_brain."""

from __future__ import annotations

import argparse
import io
import sys
import trace
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "src" / "negrita_brain"
sys.path.insert(0, str(ROOT))


def measure() -> tuple[int, int, unittest.result.TestResult, list[tuple[str, int, int]]]:
    """Run focused tests and return covered lines, executable lines, and result."""
    tracer = trace.Trace(
        count=True,
        trace=False,
        ignoredirs=[str(Path(sys.prefix).resolve())],
    )
    def run_tests() -> unittest.result.TestResult:
        loader = unittest.TestLoader()
        suite = loader.discover(
            str(ROOT / "tests"), pattern="test_negrita_brain_*.py"
        )
        runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
        return runner.run(suite)

    result = tracer.runfunc(run_tests)
    counts = tracer.results().counts
    covered = 0
    executable = 0
    details: list[tuple[str, int, int]] = []
    for path in PACKAGE.glob("*.py"):
        lines = set(trace._find_executable_linenos(str(path)))  # noqa: SLF001
        file_covered = sum((str(path), line) in counts for line in lines)
        executable += len(lines)
        covered += file_covered
        details.append((path.name, file_covered, len(lines)))
    return covered, executable, result, details


def main() -> int:
    """Run the focused suite and enforce the requested threshold."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fail-under", type=float, default=80.0)
    parser.add_argument("--details", action="store_true")
    args = parser.parse_args()
    covered, executable, result, details = measure()
    percent = (covered / executable * 100) if executable else 100.0
    print(
        f"Negrita Brain line coverage: {covered}/{executable} "
        f"({percent:.2f}%), required >= {args.fail_under:.2f}%"
    )
    if args.details:
        for name, file_covered, file_executable in sorted(details):
            percent_file = file_covered / file_executable * 100 if file_executable else 100.0
            print(f"- {name}: {file_covered}/{file_executable} ({percent_file:.2f}%)")
    if not result.wasSuccessful():
        print("Focused Negrita Brain tests failed.")
        return 1
    if percent < args.fail_under:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
