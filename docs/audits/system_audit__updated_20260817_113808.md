# NegritaOS System Audit

## Purpose

Record the August 17, 2026 hardening audit for NegritaOS across build,
runtime, architecture, validation, integration, config, performance, security,
tests, and maintainability.

## Audience And Scope

Audience: NegritaOS maintainers and agents that need a reproducible health
baseline before code, registry, skill, or documentation changes.

Scope: `/Users/jackyb-cqi/repos/NegritaOS` only. Sibling repositories were
validated through canonical adapter checks but were not modified.

## Source Of Truth

- Project adapter: `.codex/project.yaml`
- Project registry: `projects/negritaos.yaml`
- Router: `core/orchestration/metaagent_router.yaml`
- Integrator: `integrator.yaml`
- Skill catalog: `skills/catalog.yaml`
- Brain runtime: `scripts/negrita_brain.py`, `src/negrita_brain/`
- Validation scripts: `scripts/validate_*`, `scripts/check_negrita_brain_coverage.py`

## System Health

overall_status: amber
confidence: 91%
evidence_status: PARTIALLY_VERIFIED

The repository passes the local validation and test gates listed below after
the fixes in this audit. Status is amber because the worktree contains
pre-existing uncommitted changes and Brain still reports preserved repo-local
memory as non-authoritative. CI has been upgraded from basic tracked-secret
patterns to `detect-secrets`; `gitleaks` remains deferred as an optional future
binary/action dependency.

## Findings By Severity

- Critical: 0
- High: 1
- Medium: 5
- Low: 2
- Info: 3

## Issues And Fixes

### High

H-001 Runtime skill sync failed on macOS Bash 3.

- Evidence: `.codex/skills/skill-sync/assets/sync.sh --dry-run` failed with
  `declare: -A: invalid option` under GNU Bash 3.2.57.
- Impact: Skill metadata synchronization could fail for local maintainers.
- Fix: Corrected repo-root detection, pointed the script at `.codex/skills`,
  and added a Bash 3 fallback to `scripts/sync_skill_catalog.py`.
- Status: fixed.

### Medium

M-001 `system_audit` did not resolve to a router mode.

- Evidence: Brain resolve returned `No router mode declared for action
  'system_audit'`.
- Impact: A cold agent could audit with incomplete mode-specific context.
- Fix: Added a `mode_map` to `projects/negritaos.yaml` for audit,
  documentation, review, planning, presentation, and research actions.
- Status: fixed.

M-002 `quick_validate.py` treated documented glob patterns as missing files.

- Evidence: full skill validation failed on `docs-alignment` for `.codex/*`,
  `rules/*`, and `skills/*`.
- Impact: Valid skills could fail validation when documenting path patterns.
- Fix: Added glob-aware validation and a regression test.
- Status: fixed.

M-003 `nate-excalidraw-diagram` referenced a stale source filename.

- Evidence: quick validation failed on
  `skills/skill_nate/excalidraw-diagram/SKILL (1).md`; the real source is
  `skills/skill_nate/excalidraw-diagram/SKILL.md`.
- Impact: Skill provenance could not be resolved.
- Fix: Updated the wrapper reference.
- Status: fixed.

M-004 Local quality and security tools were not installed or governed.

- Evidence: `command -v gitleaks`, `detect-secrets`, `pip-audit`, `flake8`,
  `pylint`, `mypy`, and `vulture` returned no tool path.
- Impact: Local PR gates cannot run the full requested security and quality
  toolchain without environment setup.
- Fix: Added `requirements/pr-quality-tools.txt`,
  `scripts/setup_pr_quality_tools.sh`, `scripts/run_pr_quality_checks.sh`,
  `scripts/run_detect_secrets_scan.py`, and CI installation.
- Status: fixed for governed setup; local installs remain per-machine and
  strict lint/type adoption is still gradual.

M-005 Brain reported stale runtime session warnings.

- Evidence: Brain resolve and alignment report preserved repo-local memory,
  open sessions, orphan memory homes, and `proj_data_analytics`
  `INDEX_RUNTIME_OWNED` preserved until explicit safe rebuild.
- Impact: Operational context is usable but not fully clean.
- Fix: Added `memory close-stale-runtime` and ran the authorized cleanup for
  18 stale NegritaOS Memory v2 runtime sessions while leaving the current
  active session open.
- Status: fixed for stale NegritaOS runtime sessions; preserved legacy memory
  warnings remain informational or project-specific.

### Low

L-001 `plotting-guidelines` lacked required frontmatter description.

- Evidence: quick validation failed on missing `description`.
- Impact: Skill discovery metadata was incomplete.
- Fix: Added a concise description.
- Status: fixed.

L-002 `academic-tfm-research` has no configured proposal corpus.

- Evidence: `validate_config_resolution.py` warns
  `tfm_proposal_corpus is not configured`.
- Impact: TFM proposal differentiation must be reported as unverified.
- Fix: none in this audit.
- Status: remaining risk.

### Info

I-001 No Python file exceeds the audit threshold.

- Evidence: largest Python files are below 1700 lines.
- Status: verified.

I-002 `.env` exists locally but is ignored and not tracked.

- Evidence: `git ls-files .env` returned no tracked path and
  `git check-ignore -v .env` matched `.gitignore`.
- Status: verified.

I-003 CI has a `detect-secrets` gate.

- Evidence: `.github/workflows/negrita-brain.yml` installs
  `requirements/pr-quality-tools.txt` and runs
  `python3 scripts/run_detect_secrets_scan.py`.
- Status: verified.

## Validation Evidence

Commands executed locally:

```text
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve --root /Users/jackyb-cqi/repos/NegritaOS --provider codex --action system_audit
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py gate --root /Users/jackyb-cqi/repos/NegritaOS --provider codex --action write --path <changed-path>
python3 scripts/validate_config_resolution.py
python3 scripts/validate_registry_paths.py --root /Users/jackyb-cqi/repos/NegritaOS
python3 scripts/validate_skill_catalog.py
python3 scripts/validate_alignment.py --only-meta
python3 scripts/validate_alignment.py
python3 -m unittest discover -s tests
python3 -m compileall -q scripts src tests
python3 scripts/check_negrita_brain_coverage.py --fail-under 80
python3 scripts/run_detect_secrets_scan.py
python3 scripts/audit_document_control.py /Users/jackyb-cqi/repos/NegritaOS
for d in .codex/skills/*; do if [ -f "$d/SKILL.md" ]; then python3 scripts/quick_validate.py "$d" || exit 1; fi; done
.codex/skills/skill-sync/assets/sync.sh --dry-run
.codex/skills/skill-sync/sync.sh --dry-run
scripts/setup_pr_quality_tools.sh
scripts/run_pr_quality_checks.sh scripts src tests
scripts/run_pr_quality_checks.sh scripts/negrita_brain.py scripts/run_detect_secrets_scan.py src/negrita_brain/runtime.py src/negrita_brain/security.py tests/test_negrita_brain_runtime.py tests/test_negrita_brain_security.py
.venv-pr-quality/bin/pip-audit
python3 scripts/negrita_brain.py memory close-stale-runtime --root /Users/jackyb-cqi/repos/NegritaOS --older-than-days 1 --dry-run
python3 scripts/negrita_brain.py memory close-stale-runtime --root /Users/jackyb-cqi/repos/NegritaOS --older-than-days 1 --apply --authorized-by human --authorization-reason "Approved stale runtime cleanup"
git diff --check
```

Observed results:

- Brain resolve for `system_audit`: READY, mode `CR`.
- Brain resolve for `technical_documentation`: READY, mode `TD`.
- Configuration resolution: OK with the existing TFM corpus warning.
- Registry paths: OK.
- Skill catalog: OK, 68 skills and 26 profiles.
- Meta alignment: 23/23.
- Full alignment: 405/405.
- Unit tests: 100 tests, OK.
- Brain coverage: 1868/2327 lines, 80.28%, required 80.00%.
- Compileall: OK.
- Document-control audit: 0 scanned deliverables outside policy.
- All visible `.codex/skills/*/SKILL.md` quick validations: OK.
- Bash 3 skill-sync dry-run wrappers: OK, already synchronized.
- `detect-secrets`: no findings after local toolchain install.
- PR quality runner: required checks passed. Advisory checks reported existing
  C901/Pylint/mypy/pytest-mccabe debt and are not fail-closed in v1.
- `pip-audit`: no known vulnerabilities after raising `pytest` to a fixed
  version.
- Stale NegritaOS runtime cleanup: closed 18 old Memory v2 sessions. Doctor now
  reports only the current active session as open, plus preserved legacy memory
  and document warnings.
- YAML parse via Ruby/Psych: OK.
- `git diff --check`: OK.

## Remaining Risks

- R-001 Medium: dirty worktree contains many pre-existing uncommitted changes.
  Any commit must stage explicit paths only.
- R-002 Low: `gitleaks` is not enabled in CI v1. `detect-secrets` is the active
  scanner; add `gitleaks` only after approving the external binary/action path.
- R-003 Low: TFM research corpus remains unconfigured. Academic proposal
  differentiation must stay `UNVERIFIED` until the corpus is declared.
- R-004 Low: CI runs meta alignment, not full sibling alignment, because hosted
  CI cannot assume local sibling paths.

## Next Steps

1. Monitor the first GitHub Actions run after the `detect-secrets` gate lands.
2. Add `gitleaks` only if the team accepts the extra binary/action dependency.
3. Keep commits path-scoped because this checkout includes unrelated dirty work.

## Task Log

| When (CEST) | What | How | Lessons learned |
|---|---|---|---|
| 2026-08-17 11:30 | Loaded governed context | Read `.codex/project.yaml`, resolved Brain for `system_audit`, inspected Git status | The audit action itself must have an explicit mode map. |
| 2026-08-17 11:31 | Ran baseline validations | Executed config, registry, catalog, meta alignment, full alignment, tests, coverage, compile, document-control audit | Core gates were passing, but broader skill validation was not yet covered. |
| 2026-08-17 11:33 | Hardened router config | Added `mode_map` entries to `projects/negritaos.yaml` | A READY state can still carry useful WARN signals worth fixing. |
| 2026-08-17 11:34 | Hardened skill validation | Made `quick_validate.py` glob-aware and added `tests/test_quick_validate.py` | Documentation patterns need validation semantics different from literal file links. |
| 2026-08-17 11:35 | Fixed stale skill provenance | Updated `nate-excalidraw-diagram` source reference | Catalog correctness is not enough if the activable wrapper still points to an old file. |
| 2026-08-17 11:36 | Fixed skill metadata | Added `description` to `plotting-guidelines` | Visible skills must meet the same frontmatter contract even when legacy. |
| 2026-08-17 11:37 | Hardened skill-sync runtime | Fixed root detection, `.codex/skills` discovery, and Bash 3 fallback | macOS default Bash cannot run associative-array scripts; Python fallback keeps the workflow portable. |
| 2026-08-17 11:38 | Recorded audit | Wrote this report under `docs/audits/` | Keep audit evidence beside the system source, with commands and residual risks explicit. |
| 2026-08-17 12:18 | Added PR quality/security toolchain | Added local setup/run scripts, Python requirements, a `detect-secrets` wrapper, CI install, and documentation | Prefer reproducible Python-native gates before adding external CI actions. |
| 2026-08-17 12:24 | Cleaned stale Brain runtime sessions | Added and ran `memory close-stale-runtime` with explicit authorization | Runtime v2 stale sessions need a separate maintenance path from v1 legacy closures. |
