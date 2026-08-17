#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${PR_QUALITY_VENV:-"$ROOT/.venv-pr-quality"}"
export PYTHONPATH="$ROOT:$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
export PYLINT_HOME="${PYLINT_HOME:-"${TMPDIR:-/tmp}/negritaos-pylint-cache"}"
export PYLINTHOME="${PYLINTHOME:-$PYLINT_HOME}"
TARGETS=("$@")
if [ "${#TARGETS[@]}" -eq 0 ]; then
  TARGETS=("scripts" "src" "tests")
fi

if [ -x "$VENV/bin/python" ]; then
  PYTHON="$VENV/bin/python"
else
  PYTHON="python3"
fi

required=(flake8 pylint mypy vulture detect-secrets pip-audit pytest)
missing=()
for tool in "${required[@]}"; do
  if [ -x "$VENV/bin/$tool" ]; then
    continue
  fi
  if ! command -v "$tool" >/dev/null 2>&1; then
    missing+=("$tool")
  fi
done
if [ "${#missing[@]}" -gt 0 ]; then
  echo "Missing PR quality/security tools: ${missing[*]}" >&2
  echo "Run: scripts/setup_pr_quality_tools.sh" >&2
  exit 2
fi

run_tool() {
  local name="$1"
  shift
  if [ -x "$VENV/bin/$name" ]; then
    "$VENV/bin/$name" "$@"
  else
    "$name" "$@"
  fi
}

required_failures=()
advisory_failures=()

run_required() {
  local label="$1"
  shift
  echo "[required] $label"
  if ! "$@"; then
    required_failures+=("$label")
  fi
}

run_advisory() {
  local label="$1"
  shift
  echo "[advisory] $label"
  if ! "$@"; then
    advisory_failures+=("$label")
  fi
}

run_required "unittest" "$PYTHON" -m unittest discover -s tests -p 'test_*.py'
run_required "brain coverage" "$PYTHON" scripts/check_negrita_brain_coverage.py --fail-under 80
run_required "detect-secrets" "$PYTHON" scripts/run_detect_secrets_scan.py

run_advisory "flake8 style/docstrings" run_tool flake8 "${TARGETS[@]}" --max-line-length=120
run_advisory "flake8 mccabe complexity" run_tool flake8 "${TARGETS[@]}" --max-complexity=10
run_advisory "pylint full" run_tool pylint "${TARGETS[@]}" --output-format=colorized
run_advisory "pylint design subset" run_tool pylint "${TARGETS[@]}" --disable=all --enable=R0913,R0914,R0915,R0916 --output-format=colorized
run_advisory "mypy" run_tool mypy "${TARGETS[@]}" --ignore-missing-imports
run_advisory "pytest mccabe" run_tool pytest --mccabe tests/
run_advisory "pytest coverage" run_tool pytest --cov=src tests/
run_advisory "vulture" run_tool vulture "${TARGETS[@]}"
run_advisory "pip-audit" run_tool pip-audit

if [ "${#required_failures[@]}" -gt 0 ]; then
  echo "Required PR quality/security checks failed: ${required_failures[*]}" >&2
  exit 1
fi

if [ "${#advisory_failures[@]}" -gt 0 ]; then
  echo "Advisory PR quality/security checks reported issues: ${advisory_failures[*]}" >&2
  if [ "${PR_QUALITY_STRICT:-0}" = "1" ]; then
    exit 1
  fi
fi

echo "PR quality/security required checks passed"
