---
id: code-review-harden
mode_hint: CR   # Code Review
loads:
  - rules/global/negritaos_router_rule.md
  - rules/dev-coding-standards.md
  - rules/dev-naming-conventions.md
  - rules/dev-error-handling.md
  - rules/dev-logging.md
  - rules/dev-security.md
  - rules/tests-unittest-standards.md
  - rules/dev-commit-hygiene.md
---

# Code Review & Hardening (just-built code)

Review the code you (or the agent) just built. Identify potential **bugs, edge
cases, weak assumptions, and missing validations**. Make it **robust and
production-ready**. Then update the task tracker.

## Scope

Only the files changed in the current branch / staging area:

```bash
git diff --name-only
git diff --stat
```

## Review checklist

### 1. Correctness
- [ ] Happy path covered by an explicit unit test.
- [ ] At least one negative test (invalid input / missing column / empty df).
- [ ] Boolean predicates use `is_*`/`has_*`/`should_*`/`can_*` (naming §6.1).
- [ ] No silent `except:` or bare `pass` (error-handling rule).

### 2. Edge cases (ML/data context)
- [ ] Empty DataFrame.
- [ ] All-NaN column.
- [ ] Single-row group.
- [ ] Time-window boundary (open vs closed).
- [ ] Duplicate primary keys.
- [ ] Future timestamps / negative usage.

### 3. Weak assumptions
- [ ] Magic numbers extracted to `config/` constants (naming §3).
- [ ] No `print()` / `display()` outside notebooks (notebooks rule).
- [ ] Logging via `get_logger(__name__)`, not `logging.basicConfig`.
- [ ] Dataset access goes through a contract validator (data-contracts rule).

### 4. Validation
- [ ] Inputs validated at the system boundary.
- [ ] Schema check runs BEFORE feature engineering.
- [ ] Error raised includes `ERR_*` code + context (customer_id, window, feature).

### 5. Tests
- [ ] Tests named `test_<behavior>_that_<expected>_when_<condition>`.
- [ ] Pass under BOTH `python -m unittest discover` and `pytest --cov`.
- [ ] Coverage of changed files ≥80% (production) or ≥60% (MVP).

### 6. Security
- [ ] No secrets, tokens, real customer IDs, or emails in code/fixtures/logs.
- [ ] `.env.example` updated if a new env var was added.

## Hardening actions

For each unchecked box → propose the minimal diff and apply it.

## Task tracker update

Append a row to `docs/task_tracker.md` (create if missing):

```markdown
| Task ID | What was done | How it was done | When (UTC) | Lessons learned |
|---------|----------------|------------------|------------|------------------|
| T-<id>  | <summary>      | <approach>       | <iso8601>  | <1-2 bullets>    |
```

## Output contract

1. Findings table (Severity / File / Line / Issue / Fix).
2. Diffs applied.
3. Re-run of `pytest --cov` with delta vs main.
4. Tracker row added.
