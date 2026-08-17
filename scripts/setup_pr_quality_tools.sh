#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${PR_QUALITY_VENV:-"$ROOT/.venv-pr-quality"}"

python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r "$ROOT/requirements/pr-quality-tools.txt"

echo "PR quality/security tools installed in $VENV"
echo "Activate with: source $VENV/bin/activate"
"$VENV/bin/flake8" --version
"$VENV/bin/pylint" --version
"$VENV/bin/mypy" --version
"$VENV/bin/detect-secrets" --version
