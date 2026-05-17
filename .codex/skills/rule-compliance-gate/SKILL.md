---
name: rule-compliance-gate
description: Enforce repository rules and active profile compliance before writing or modifying code. Trigger when starting any coding task, refactor, analysis execution script, notebook-to-script conversion, tests creation, or when outputs must follow strict governance (logging, error-handling, naming, SQL governance, plotting, and unittest standards).
---

# Rule Compliance Gate

Use this skill as a mandatory pre-flight checklist before creating or editing files.

## Workflow (mandatory)

1. Identify intent + scope

- What is being done: analytics run / SQL changes / plotting / refactor / tests / packaging / CI.
- List target folders you will touch (must be inside repo structure, never create files “outside”).

2. Select active profile

- If user specified a profile, use it.
- Else default:
  - Analytics execution (SQL -> DF -> plots -> report) => `analysis-run`
  - Audit/review => `review`
  - Refactor => `refactor`

3. Load active rules (from instruction-manifest + profile)

- Collect rule IDs from `uses:` and their `depends_on` closure.
- Treat `priority: critical` + `enforcement: strict` as hard requirements.

4. Pre-flight checklist (must pass before writing code)

A) Repo hygiene

- Files created ONLY in the appropriate repo folders (no ad-hoc root dumps).
- Any path referenced by a rule, skill, or prompt must exist in the repository. If it does not exist, treat it as stale guidance and fall back to the real on-disk structure.
- Outputs go to an `outputs/run_YYYYMMDD_HHMMSS/`-style folder (or repo-defined convention).
- No committed runtime artifacts: **pycache**, large CSVs, local creds, etc.

B) Logging and error handling

- Structured logging is present in production modules and tests.
- `print()` / `display()` are used only in notebooks or `# %%` interactive scripts.
- Exceptions are handled with clear error messages and context.
- Long-running steps emit phase-level logs.

C) Python quality gates

- Type hints on public functions.
- Google-style docstrings where required.
- Code formatted/linted to Ruff/PEP8 conventions (and mypy/pylint if project enforces).
- Deterministic behavior where required (seed, stable sorting, fixed configs).

D) SQL governance (if SQL involved)

- Queries are parameterized or templated; no hardcoded dates unless explicitly required.
- Partition filters and cost-awareness are applied (BQ best practices).
- Column naming and contracts respected.

E) Data validation + contracts (if dataframes involved)

- Validate required columns, dtypes, nullability, and key constraints per contract.
- Avoid silent coercions; log casts and dropped rows explicitly.

F) Plotting rules (if plots involved)

- Titles/labels/annotations in English.
- Explicit computation for each metric used in charts (no “magic”).
- Top-K limits + readable legends.

G) Testing (if modifying logic)

- Add/update `unittest` tests per `tests-unittest-standards`.
- Enforce `test_<behavior>_that_<expected>_when_<condition>` method names.
- Enforce `Test<ComponentName>` class naming and `test_<component>.py` file naming.
- Minimum: smoke test for execution scripts + unit tests for transforms.

5. Execution plan

- Produce a short plan with: files to touch, new files, removed files, tests to add, and commands to run locally/CI.

6. Only then: implement changes

- If any checklist item cannot be satisfied, stop and explain what is blocking and the safest alternative.
