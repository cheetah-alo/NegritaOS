# Final Pre-Commit Checklist for AI-Assisted Development

Before creating a commit, Claude, Codex, or any AI coding assistant must validate that the task is aligned with the Python Code Quality and Peer Review standards.

This checklist should be completed for every meaningful code change, especially changes involving Python modules, data pipelines, model logic, feature engineering, validation logic, tests, or production-facing scripts.

---

## 1. Scope and Intent

| Check                                                                               | Status |
| ----------------------------------------------------------------------------------- | ------ |
| The objective of the task is clear and matches the requested change.                |        |
| The implemented change does not introduce unrelated modifications.                  |        |
| The solution is minimal enough to solve the problem without unnecessary complexity. |        |
| Any assumption made during implementation is documented.                            |        |
| Existing behavior is preserved unless the task explicitly requires changing it.     |        |

---

## 2. Code Structure and Maintainability

| Check                                                                                               | Status |
| --------------------------------------------------------------------------------------------------- | ------ |
| Code is modular and follows a clear separation of responsibilities.                                 |        |
| Business logic is separated from IO, configuration, and execution scripts.                          |        |
| No function, method, or class is doing too many things at once.                                     |        |
| Files are preferably below 1500 lines. Files between 1500 and 1700 lines are justified if accepted. |        |
| Files above 1700 lines are refactored or explicitly justified.                                      |        |
| No duplicated logic was introduced.                                                                 |        |
| No large “god function” or “god class” was introduced.                                              |        |

---

## 3. Python Style

| Check                                                                          | Status |
| ------------------------------------------------------------------------------ | ------ |
| Lines are no longer than 120 characters unless there is a justified exception. |        |
| Code follows PEP8 conventions.                                                 |        |
| Imports are clean, organized, and unused imports are removed.                  |        |
| No commented-out obsolete code remains.                                        |        |
| No debugging `print()` statements remain.                                      |        |
| Constants use `UPPER_SNAKE_CASE`.                                              |        |
| Functions, methods, and variables use `snake_case`.                            |        |
| Classes use `PascalCase`.                                                      |        |
| Module and file names use lowercase with underscores.                          |        |

---

## 4. Naming and Domain Context

| Check                                                                                                                  | Status |
| ---------------------------------------------------------------------------------------------------------------------- | ------ |
| Names are aligned with the business or technical context of the repository.                                            |        |
| Function names clearly describe the action they perform.                                                               |        |
| Boolean functions read as true/false checks, for example `is_valid_*`, `has_*`, or `should_*`.                         |        |
| Variables avoid vague names such as `tmp`, `data`, `df1`, `res`, or `val`, unless the scope is very small and obvious. |        |
| Data Science variables clearly express their meaning, grain, and window when relevant.                                 |        |
| Target, feature, score, and metric names are explicit and not ambiguous.                                               |        |

Examples of preferred naming:

```python
target_churn_7d
customer_recall_24h
unexpected_reboot_12h_flag
prediction_score
feature_columns
validate_input_schema()
calculate_lift_at_k()
build_training_dataset()
```

---

## 5. Docstrings and Documentation

| Check                                                                                       | Status |
| ------------------------------------------------------------------------------------------- | ------ |
| Public modules, classes, functions, and methods include Google-style docstrings.            |        |
| Docstrings explain purpose, arguments, return values, and raised exceptions where relevant. |        |
| Complex business logic or data science assumptions are documented.                          |        |
| Documentation was updated if behavior, execution, configuration, or outputs changed.        |        |
| README or technical documentation remains accurate after the change.                        |        |

Example Google-style docstring:

```python
def validate_required_columns(
    df: pd.DataFrame,
    required_columns: set[str],
) -> None:
    """Validate that a DataFrame contains all required columns.

    Args:
        df: Input DataFrame to validate.
        required_columns: Set of required column names.

    Raises:
        ValueError: If one or more required columns are missing.
    """
```

---

## 6. Logging and Traceability

| Check                                                                                                    | Status |
| -------------------------------------------------------------------------------------------------------- | ------ |
| Relevant execution steps include structured logs.                                                        |        |
| Logs include useful context such as step name, row counts, parameters, artifact paths, or metric values. |        |
| Logs are used instead of `print()` for operational traceability.                                         |        |
| Error messages are clear and actionable.                                                                 |        |
| Logs do not expose secrets, credentials, personal data, or sensitive customer data.                      |        |

Minimum expected logging areas:

```text
data loading
data filtering
feature engineering
model training
evaluation
artifact generation
error handling
```

---

## 7. Input Validation

| Check                                                                | Status |
| -------------------------------------------------------------------- | ------ |
| Required input columns are validated.                                |        |
| Data types are validated where relevant.                             |        |
| Accepted values for categorical fields are validated where relevant. |        |
| Date ranges and time windows are validated where relevant.           |        |
| Model input schema is validated before training or scoring.          |        |
| Invalid inputs fail clearly instead of silently propagating.         |        |

---

## 8. Testing

| Check                                                                                               | Status |
| --------------------------------------------------------------------------------------------------- | ------ |
| Unit tests were added or updated for the changed logic.                                             |        |
| Tests are deterministic and do not depend on network, databases, APIs, or uncontrolled local files. |        |
| Edge cases are covered.                                                                             |        |
| Existing tests still pass.                                                                          |        |
| Coverage remains aligned with the expected threshold.                                               |        |
| Any missing test is explicitly justified.                                                           |        |

Recommended command:

```bash
pytest --cov=src --cov-report=term-missing tests/
```

---

## 9. Static Analysis

Before committing, run the relevant checks.

| Check                   | Command                                                | Status |
| ----------------------- | ------------------------------------------------------ | ------ |
| Flake8 style check      | `flake8 src tests --max-line-length=120`               |        |
| Complexity check        | `flake8 src --max-complexity=10 --max-line-length=120` |        |
| Mypy type check         | `mypy src --ignore-missing-imports`                    |        |
| Vulture dead code check | `vulture src`                                          |        |
| Pylint review           | `pylint src`                                           |        |

If a check fails, the issue must be fixed or documented as an accepted exception before commit.

---

## 10. Data Science and ML-Specific Validation

Apply this section when the change affects data processing, features, model training, scoring, evaluation, or reporting.

| Check                                                                    | Status |
| ------------------------------------------------------------------------ | ------ |
| Data grain is clear and preserved.                                       |        |
| Join keys are explicit and validated.                                    |        |
| Denominators are clear for all metrics.                                  |        |
| Target logic is documented and protected against leakage.                |        |
| Train/test or temporal split logic is reproducible.                      |        |
| Feature names clearly describe their meaning and window.                 |        |
| Null handling is explicit.                                               |        |
| Metric calculations are documented and reproducible.                     |        |
| Model artifacts, reports, or outputs are saved in the expected location. |        |
| Business interpretation is documented where relevant.                    |        |

---

## 11. Security and Secrets

| Check                                                                                         | Status |
| --------------------------------------------------------------------------------------------- | ------ |
| No secrets, tokens, passwords, or credentials were committed.                                 |        |
| No sensitive customer data was added to examples, logs, tests, or documentation.              |        |
| `.env`, local credentials, generated artifacts, and temporary files are ignored where needed. |        |
| The `.gitignore` remains aligned with the project.                                            |        |

---

## 12. Commit Readiness

| Check                                                                | Status |
| -------------------------------------------------------------------- | ------ |
| All relevant checks were executed.                                   |        |
| All generated temporary files were removed or intentionally ignored. |        |
| Reports or artifacts were generated only when required.              |        |
| The diff was reviewed for unrelated changes.                         |        |
| The commit message clearly explains the change.                      |        |
| The PR description includes validation evidence when applicable.     |        |

Suggested commit format:

```text
type(scope): short description
```

Examples:

```text
refactor(validation): split schema checks into reusable functions
test(features): add unit tests for recall window logic
fix(logging): replace print statements with structured logger
docs(review): add pre-commit checklist for Python quality
```

---

# Final Rule for Claude/Codex

Before proposing a commit, Claude or Codex must answer the following:

```text
Pre-commit quality check completed.

1. What changed?
2. Which files were modified?
3. Which checks were run?
4. Which checks passed?
5. Which checks failed or were skipped?
6. Are there any accepted exceptions?
7. Is the change aligned with the Peer Review code-quality standard?
```

A commit should not be proposed if the implementation introduces untested core logic, unexplained complexity, missing validation, unclear naming, or unrelated modifications.

---

# Integration Audit — `.codex/rules/` Coverage (audit date: 2026-06-01)

This section traces every checklist requirement above to an enforceable rule
under [`.codex/rules/`](../.codex/rules/) and flags drift, conflicts, and gaps.
Status legend: ✅ covered · ⚠️ partial/drift · ❌ gap.

## Coverage matrix

| § | Checklist topic | Backing rule(s) | Status | Notes |
|---|---|---|---|---|
| 1  | Scope and Intent | [ai-behavior.md](../.codex/rules/ai-behavior.md) §10 + [dev-coding-standards.md](../.codex/rules/dev-coding-standards.md) §4 | ✅ | "Safe Minimal Changes" already explicit. |
| 2  | Code Structure / file size | [dev-coding-standards.md](../.codex/rules/dev-coding-standards.md) §1.2, §7, §9 | ⚠️ | Three different thresholds in the same file (≤800, ~300, 800–900). Checklist demands ≤1500 with 1700 ceiling. **Conflict to resolve.** Also duplicate `## 9` header (`Sensitive Files` and `Size Files`). |
| 3  | Python Style | [dev-coding-standards.md](../.codex/rules/dev-coding-standards.md) §1.3 + [dev-naming-conventions.md](../.codex/rules/dev-naming-conventions.md) + [dev-python.md](../.codex/rules/dev-python.md) §1.2 | ✅ | 120-char line length aligned across rule + checklist. |
| 4  | Naming / boolean predicates | [dev-naming-conventions.md](../.codex/rules/dev-naming-conventions.md) §6 | ⚠️ | Strong on domain terms, weak on **boolean prefixes** (`is_`, `has_`, `should_`). Checklist requires this — rule should add it. |
| 5  | Docstrings (Google-style) | [dev-python.md](../.codex/rules/dev-python.md) §1.5 | ✅ | |
| 6  | Logging | [dev-logging.md](../.codex/rules/dev-logging.md) | ✅ | Phase logging + governance JSON well-defined. |
| 7  | Input Validation | [data-contracts.md](../.codex/rules/data-contracts.md) + [data-validation.md](../.codex/rules/data-validation.md) | ✅ | Three-layer validation (structural / domain / statistical). |
| 8  | Testing | [tests-unittest-standards.md](../.codex/rules/tests-unittest-standards.md) | ⚠️ | Rule mandates `unittest` + `coverage`; checklist shows `pytest --cov`. **Drift** — pick one canonical runner. |
| 9  | Static Analysis CLI | [dev-coding-standards.md](../.codex/rules/dev-coding-standards.md) §1.3 | ⚠️ | Rule lists `ruff / mypy / vulture / mccabe`; checklist lists `flake8 / pylint`. **Drift** — converge commands. |
| 10 | DS/ML Validation | [data-contracts.md](../.codex/rules/data-contracts.md) + [data-validation.md](../.codex/rules/data-validation.md) + [dev-python.md](../.codex/rules/dev-python.md) §3 | ✅ | Leakage, grain, denominators covered indirectly. Could be made explicit. |
| 11 | Security & Secrets | [dev-coding-standards.md](../.codex/rules/dev-coding-standards.md) §9 (one-liner) + [ml-telemetry.md](../.codex/rules/ml-telemetry.md) | ❌ | **No dedicated `dev-security.md`.** Coverage too thin for what the checklist demands (`.env`, `.gitignore`, secrets in tests/docs). |
| 12 | Commit Readiness | [.codex/skills/commit-hygiene/SKILL.md](../.codex/skills/commit-hygiene/SKILL.md) | ❌ | Exists only as a **skill**, not a rule. Not in [`.codex/instruction-manifest.yaml`](../.codex/instruction-manifest.yaml). Engineering modes won't auto-load it. |
| Final | Pre-commit answer template (7 questions) | — | ❌ | Not encoded anywhere as enforceable behavior. |
| Meta | This checklist file | — | ❌ | **Orphan doc.** Not referenced from any rule, [`AGENTS.md`](../AGENTS.md), or manifest. Engineering modes will never load it. |

## Conflicts that MUST be resolved

1. **File-size policy** ([dev-coding-standards.md](../.codex/rules/dev-coding-standards.md)):
   - §1.2 says **≤800 lines**.
   - §7 says **split files >~300 lines**.
   - §9 (Size Files) says **800–900 max**.
   - Checklist §2 says **≤1500, justify ≤1700, refactor >1700**.
   → Choose one canonical threshold, delete the rest, fix the duplicate `## 9` header.

2. **Test runner**:
   - [tests-unittest-standards.md](../.codex/rules/tests-unittest-standards.md) → `python -m unittest discover` + `coverage`.
   - Checklist §8 → `pytest --cov=src`.
   → Either declare `unittest` canonical and `pytest` optional (the [pytest skill](../.codex/skills/pytest/SKILL.md) already says this), or update the checklist to match.

3. **Static analysis toolchain**:
   - Rule → `ruff / mypy / vulture / mccabe / pylint`.
   - Checklist → `flake8 / mypy / vulture / pylint`.
   → Single source of truth; one matrix.

## Gaps to close (concrete actions)

| Action | Target file | What to add |
|---|---|---|
| A1 | [dev-naming-conventions.md](../.codex/rules/dev-naming-conventions.md) §6 | Subsection "Predicate / boolean functions" mandating `is_*`, `has_*`, `should_*`, `can_*` prefixes. |
| A2 | [dev-coding-standards.md](../.codex/rules/dev-coding-standards.md) | Replace §1.2 + §7 + duplicate §9 with a single "Module Boundaries" section stating the chosen threshold. |
| A3 | New rule `.codex/rules/dev-security.md` | Secrets/PII/`.env`/`.gitignore`/credential-scanning rules. Add to manifest with `depends_on: [coding-standards, logging]`, enforcement `strict`. |
| A4 | New rule `.codex/rules/dev-commit-hygiene.md` (or promote skill) | Encode commit-message format, atomic-commit rule, the 7-question pre-commit answer template. Add to manifest. |
| A5 | [dev-coding-standards.md](../.codex/rules/dev-coding-standards.md) §1.3 | Replace ad-hoc tool list with a single CLI matrix that matches checklist §9. |
| A6 | [tests-unittest-standards.md](../.codex/rules/tests-unittest-standards.md) §9 | Add an explicit "Optional pytest runner" subsection or update the checklist. |
| A7 | This file (`zsmash/check_qc_code_june1.md`) | Move to `.codex/rules/dev-precommit-checklist.md` and register in the manifest so engineering modes (MR/CR/DQ) load it automatically. |
| A8 | [AGENTS.md](../AGENTS.md) | Reference the precommit checklist + commit-hygiene rule from the "Engineering modes" block. |

## Federation impact

Per [negritaos_router_rule.md](../rules/global/negritaos_router_rule.md), only the **engineering modes** (MR / CR / DQ) load `.codex/rules/dev-*.md`. So all new rules above MUST follow the `dev-*.md` naming convention to be picked up automatically — and the orphan checklist must be renamed to `dev-precommit-checklist.md` and registered in [`.codex/instruction-manifest.yaml`](../.codex/instruction-manifest.yaml) for the agent loader to honor it.

## Suggested execution order

1. A2 (resolve file-size conflict — bug fix, low risk).
2. A1 (boolean prefix — small append).
3. A5 + A6 (toolchain + test runner alignment — small edits).
4. A3 (new `dev-security.md`).
5. A4 (new `dev-commit-hygiene.md`).
6. A7 (relocate this checklist, add to manifest).
7. A8 (update `AGENTS.md`).
8. Re-run `python3 scripts/validate_alignment.py` to confirm no regressions.

---

