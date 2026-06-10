---
id: commit-push-pr
mode_hint: MR
loads:
  - .codex/skills/commit-hygiene/SKILL.md
  - .codex/skills/pr-review-deep/SKILL.md
  - .codex/rules/dev-security.md
---

# Commit, Push, and Open PR

Repeatable workflow for committing staged changes, pushing to remote, and opening a pull request.

## Prerequisites

- All tests pass: `python -m unittest discover -s tests`
- No secrets in diff: `gitleaks detect --source . --verbose`
- Static analysis clean on changed files: `ruff check <files> && mypy <files>`

## Procedure

### Step 1 — Verify staged changes

```bash
git diff --cached --stat
git diff --cached
```

Check:
- Diff matches the intended scope.
- No unrelated changes bundled in.
- No `print()`, debug artifacts, secrets, or PII.

### Step 2 — Run pre-commit quality gate

```bash
python -m unittest discover -s tests
pytest --cov=backend/app --cov=data_analytics --cov=mcp_server \
       --cov-report=term-missing tests/ 2>&1 | tail -20
ruff check .
mypy .
```

Record: pass rate, coverage %, coverage delta vs main.

### Step 3 — Build commit message

Format: `type(scope): short imperative description`

Allowed types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `data`, `ml`

Append mandatory trailer:
```
Tests: <N>/<N> passing (unittest)
Coverage: <NN.N>% (Δ <+/-N.N> pp vs main)
Checks:
  scope-clean: pass
  no-secrets: pass
  unittest: pass
  static-analysis: pass
Notes: <justification for any skipped check>
```

### Step 4 — Commit

```bash
git commit -m "type(scope): description

<optional body>

Tests: N/N passing (unittest)
Coverage: NN.N% (Δ +N.N pp vs main)
Checks:
  scope-clean: pass
  no-secrets: pass
  unittest: pass
  static-analysis: pass"
```

### Step 5 — Push

```bash
git push origin <branch>
```

### Step 6 — Open PR

Open PR via `gh pr create` or the UI.

PR description must include:
- What changed and why.
- Coverage summary block (see `dev-commit-hygiene` rule).
- Pre-commit 7-question answer.
- Links to relevant issues or contracts.

## Checklist

- [ ] Tests pass 100%
- [ ] Coverage at or above stage floor (prototype: 40%, MVP: 60%, production: 80%)
- [ ] No secrets or PII in diff
- [ ] Commit message trailer present
- [ ] PR description complete
