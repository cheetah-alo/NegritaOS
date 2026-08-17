# PR Quality And Security Toolchain

## Purpose

This page defines the local and CI toolchain for pull-request quality/security
evidence in NegritaOS.

## CI Secret-Scan Decision

NegritaOS CI uses `detect-secrets` instead of the previous basic `git grep`
pattern scan.

Rationale:

- It is Python-native and fits the current `actions/setup-python` workflow.
- It can run locally from the same project venv as Flake8, Pylint, mypy, pytest,
  vulture, and `pip-audit`.
- The wrapper reports only finding metadata, never secret values.
- Existing false positives are captured in `.secrets.baseline`; CI fails only
  on unbaselined findings.
- `gitleaks` remains a valid future hardening option, but it introduces an
  additional external binary/action dependency and is not required for v1.

## Local Install

Do not install PR tooling globally. Use the isolated venv:

```bash
scripts/setup_pr_quality_tools.sh
source .venv-pr-quality/bin/activate
```

Version checks:

```bash
flake8 --version
pylint --version
mypy --version
detect-secrets --version
pip-audit --version
```

## Canonical Commands

Run the local suite when preparing or fixing a PR:

```bash
scripts/run_pr_quality_checks.sh
```

Target a narrower path when the PR is intentionally scoped:

```bash
scripts/run_pr_quality_checks.sh scripts src tests
```

The runner has two severities in v1:

- Required: unittest, Negrita Brain coverage, and `detect-secrets`.
- Advisory by default: Flake8, McCabe, Pylint, mypy, pytest coverage, vulture,
  and `pip-audit`.

Make advisory failures fail the command when the project is ready for strict
enforcement:

```bash
PR_QUALITY_STRICT=1 scripts/run_pr_quality_checks.sh scripts src tests
```

Individual commands:

```bash
flake8 <path_to_folder> --max-line-length=120
flake8 <path_to_folder> --max-complexity=10
pylint <path_to_folder> --output-format=colorized
pylint <path_to_folder> --disable=all --enable=R0913,R0914,R0915,R0916 --output-format=colorized
mypy <path_to_folder> --ignore-missing-imports
pytest --mccabe tests/
pytest --cov=src tests/
vulture <path_to_folder>
python3 scripts/run_detect_secrets_scan.py
pip-audit
```

## Artifact Policy

Do not commit local reports, coverage, caches, venvs, or scratch outputs.
Summarize results in the PR review or task handoff. If a report must be
preserved, store it in a run-scoped ignored evidence location.

## Failure Semantics

- Missing toolchain: `scripts/run_pr_quality_checks.sh` exits `2` and prints the
  setup command.
- Secret findings: `scripts/run_detect_secrets_scan.py` exits `1` and reports
  file, line, type, and verification flag only.
- Quality failures: keep the failing command and summary in the PRR output.
  Advisory failures increase `verification_gap` but do not fail v1 unless
  `PR_QUALITY_STRICT=1`.
- A green suite is not sufficient if the original user-visible reproduction
  path still fails.
