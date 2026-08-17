# Task Tracker - NegritaOS System Audit Hardening

Project: negritaos
Branch: main
Owner: Codex
Mode: CR

## Backlog

| ID | Title | Status | Depends on | Mode |
|---|---|---|---|---|
| T-001 | Harden system audit and skill validation | done | none | CR |
| T-002 | Install and run extended local quality/security tooling | done | T-001 | CR |
| T-003 | Clean Brain memory warnings through controlled maintenance | done | T-001 | CR |

## Task Log

### T-001 - Harden system audit and skill validation
- **What**: reviewed and hardened the just-built NegritaOS audit changes, including mode resolution, skill validation, Nate provenance, plotting metadata, macOS `skill-sync`, and audit documentation.
- **How**: resolved Brain in `CR`, inspected the scoped diff, reproduced validator/runtime failures, applied minimal patches, added regression tests, and reran canonical validations.
- **When**: 2026-08-17T09:47:00Z
- **Lessons learned**:
  - Skill validators need to distinguish literal path references from command examples in Markdown code spans.
  - macOS Bash 3 compatibility must be tested directly when shell tools use arrays or associative-array-like state.
- **Next-task hint**: T-002 should install or provide a governed local wrapper for `gitleaks`, `detect-secrets`, `pip-audit`, `flake8`, `pylint`, `mypy`, and `vulture` before calling release quality fully verified.

### T-002 - Install and run extended local quality/security tooling
- **What**: upgraded PR quality/security from an ad hoc basic secret grep to a governed local/CI toolchain with `detect-secrets`, Flake8, Pylint, mypy, pytest coverage/McCabe, vulture, and `pip-audit`.
- **How**: added `requirements/pr-quality-tools.txt`, local setup and run scripts, a `detect-secrets` CI wrapper that reports metadata only, CI installation, and documentation in `docs/pr_quality_security_toolchain.md`.
- **When**: 2026-08-17T10:18:00Z
- **Lessons learned**:
  - CI should run a reproducible Python-native scanner before adopting external binary/action dependencies.
  - Local quality reports, venvs, coverage, and scan outputs need explicit ignore rules because PRR evidence belongs in summaries, not tracked artifacts.
  - `pip-audit` must run with network evidence; it found vulnerable `pytest 8.4.2`, fixed by requiring `pytest>=9.0.3`.
  - Full-repo lint/type enforcement needs gradual adoption; v1 keeps those checks advisory unless `PR_QUALITY_STRICT=1`.

### T-003 - Clean Brain memory warnings through controlled maintenance
- **What**: added and ran a separate authorized cleanup path for stale Memory v2 runtime sessions.
- **How**: implemented `memory close-stale-runtime` with dry-run default, explicit `--apply` authorization, age gating, and runtime-only `state.json` closure metadata; then closed 18 stale NegritaOS runtime sessions while leaving the current active session open.
- **When**: 2026-08-17T10:24:00Z
- **Lessons learned**:
  - Memory v1 legacy closures and Memory v2 stale runtime closures need separate commands and authorization semantics.
  - `doctor_status: WARN` can be operationally acceptable when only the current session and preserved legacy artifacts remain, but stale sessions should be closed by API instead of direct file edits.
