.claude/commands/commit-push-pr.md
# Commit, Push, and PR

Use this command when the implementation is complete and ready for final review, commit, push, and PR preparation.

## Objective

Validate the current changes against the Python Code Quality and Peer Review standards, then prepare a clean commit, push the branch, and generate a PR-ready summary.

Do not commit blindly.

---

## 1. Inspect Changes

Run:

```bash
git status --short
git diff --stat
git diff
```

Verify:

* The diff matches the requested task.
* No unrelated files are included.
* No secrets, credentials, cache files, local files, or temporary artifacts are included.
* No debug `print()` statements or obsolete commented-out code remain.

Stop before committing if the diff is risky, unrelated, or unclear.

---

## 2. Python Quality Checklist

Before committing, verify:

* Line length is max 120 characters unless justified.
* Python files are preferably below 1500 lines.
* Files between 1500 and 1700 lines are allowed only with justification.
* Files above 1700 lines should be refactored or explicitly justified.
* Code follows PEP8.
* Imports are clean and unused imports are removed.
* Functions, methods, and variables use `snake_case`.
* Classes use `PascalCase`.
* Constants use `UPPER_SNAKE_CASE`.
* Module/file names use lowercase with underscores.
* Naming is aligned with the business and technical context.
* Public modules, classes, functions, and methods use Google-style docstrings.
* Code uses logging instead of `print()` for operational traceability.
* Inputs are validated when data, model, or business logic is affected.
* Unit tests are added or updated for changed core logic.
* No unrelated refactor or scope creep was introduced.

---

## 3. Data Science / ML Checklist

Apply when the change affects data, features, models, scoring, metrics, or reports.

Verify:

* Data grain is clear.
* Join keys are explicit.
* Denominators are documented.
* Target logic is documented and checked for leakage risk.
* Train/test or temporal split logic is reproducible.
* Feature names include clear meaning and window where relevant.
* Null handling is explicit.
* Metric formulas are reproducible.
* Business interpretation is documented when relevant.

---

## 4. Run Checks

Prefer `uv` when available:

```bash
uv run flake8 src tests --max-line-length=120
uv run flake8 src --max-complexity=10 --max-line-length=120
uv run mypy src --ignore-missing-imports
uv run vulture src
uv run pytest --cov=src --cov-report=term-missing tests/
```

Otherwise run:

```bash
flake8 src tests --max-line-length=120
flake8 src --max-complexity=10 --max-line-length=120
mypy src --ignore-missing-imports
vulture src
pytest --cov=src --cov-report=term-missing tests/
```

If a tool is unavailable, do not install dependencies automatically. Report it as skipped with the reason.

---

## 5. Stage and Commit

Stage only intended files.

```bash
git status --short
git add <file_1> <file_2>
git diff --cached --stat
git diff --cached
```

Use Conventional Commit format:

```text
type(scope): short description
```

Examples:

```text
fix(logging): replace print statements with structured logger
test(features): add tests for recall window logic
docs(review): add python pre-commit checklist
```

Commit:

```bash
git commit -m "<type(scope): short description>"
```

---

## 6. Push

```bash
git branch --show-current
git push -u origin "$(git branch --show-current)"
```

Do not force push unless explicitly instructed.

---

## 7. PR Summary

Generate this PR-ready output:

```markdown
## Summary
- What changed and why.

## Changes
- Key files or modules modified.

## Validation
- Flake8: Passed / Failed / Skipped
- Complexity: Passed / Failed / Skipped
- Mypy: Passed / Failed / Skipped
- Vulture: Passed / Failed / Skipped
- Pytest: Passed / Failed / Skipped
- Coverage: value if available

## Peer Review Alignment
- Code Quality: Optimized / Adequate / Marginal / Unregulated
- Technical Documentation: Optimized / Adequate / Marginal / Unregulated
- Unit Testing: Optimized / Adequate / Marginal / Unregulated
- Metrics and KPIs: Optimized / Adequate / Marginal / Unregulated

## Risk / Impact
- Technical, data, model, or operational risk.

## Rollback
- How to revert if needed.
```

---

## Stop Conditions

Stop before committing if:

* Secrets or credentials are detected.
* Unrelated files are included.
* Core logic changed without tests or justification.
* Static checks fail without explanation.
* Naming, validation, or logging is clearly misaligned.
* The branch state is ambiguous.
* The task scope is unclear.
