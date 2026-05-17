# Create Unittest Agent

Use this subagent when you need to create, refactor, or standardize Python unit tests
for modules under `backend/app/`, `data_analytics/`, `mcp_server/`, and logic-only parts under `analyses/`.

## When to use

Typical triggers:

- New/changed function or module in `backend/app/`, `data_analytics/`, or `mcp_server/`
- Bug fix that needs regression coverage
- Refactor that risks behavior drift
- Any change in data transforms (casting, bucketing, splitting, grouping, leakage guards)
- EDA plot-input preparation or metric computations that must remain stable

## Hard constraints (strict)

- Follow `.codex/rules/tests-unittest-standards.md` (strict).
- Tests are `unittest`-first (written as `unittest.TestCase`), even if executed with `pytest`.
- No network / DB / API / file I/O in unit tests (patch/mocks instead).
- Deterministic fixtures via `setUp()`.
- Enforce `Test<ComponentName>` class names and `test_<behavior>_that_<expected>_when_<condition>` method names.

## Default outputs

- New/updated test file under `tests/`
- Deterministic fixtures
- Behavior-driven test names
- Minimal mocks with explicit patch scope

## Primary paths (this repo)

- Unit tests root: `tests/`
- Main code targets: `backend/app/**`, `data_analytics/**`, `mcp_server/**`
- Logic-only analysis targets (patch I/O): `analyses/**/run_queries.py`, `analyses/**/notebooks/*.py`
