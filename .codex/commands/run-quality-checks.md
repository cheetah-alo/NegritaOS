---
id: run-quality-checks
mode_hint: MR
loads:
  - .codex/skills/create-unittest/SKILL.md
  - .codex/skills/pytest/SKILL.md
---

# Run Quality Checks

Runs the full local quality gate before committing or opening a PR.

## When to use

- Before any commit on production code.
- Before marking a PR ready for review.
- After resolving merge conflicts.
- When a CI run fails and you need to reproduce locally.

## Procedure

### 1. Unit tests

```bash
python -m unittest discover -s tests
```

Expected: 100% pass. Any failure blocks the commit.

### 2. Coverage

```bash
pytest --cov=backend/app --cov=data_analytics --cov=mcp_server \
       --cov-report=term-missing --cov-report=xml tests/
```

Thresholds:
- Prototype: 40%
- MVP: 60%
- Production: 80%

Report delta vs `main`:
```bash
git stash && pytest --cov=backend/app ... --cov-report=xml -q && cp coverage.xml /tmp/base.xml
git stash pop && pytest --cov=backend/app ... --cov-report=xml -q
python -c "import xml.etree.ElementTree as ET; base=float(ET.parse('/tmp/base.xml').getroot().get('line-rate'))*100; cur=float(ET.parse('coverage.xml').getroot().get('line-rate'))*100; print(f'Base: {base:.1f}%  Current: {cur:.1f}%  Delta: {cur-base:+.1f} pp')"
```

### 3. Static analysis

```bash
ruff check .
mypy . --ignore-missing-imports
vulture . --min-confidence 80
```

All must be clean on files changed in the current branch.

### 4. Secret scan

```bash
gitleaks detect --source . --verbose
```

Block on any finding. Rotate any exposed secret before proceeding.

### 5. File size check

```bash
find . -name "*.py" -not -path "./.venv/*" | xargs wc -l | sort -rn | awk '$1 > 1500 {print $1, $2}'
```

Files between 1500 and 1700 lines: add justification.  
Files above 1700 lines: must be refactored before merging.

## Output format

Report results as:

```
Quality Gate Summary
====================
unittest : N/N passing
coverage : NN.N% (Δ +N.N pp vs main)
ruff     : clean / N issues
mypy     : clean / N errors
vulture  : clean / N unused
gitleaks : clean / BLOCKED
file-size: N files over 1500 lines
```

Status: PASS / FAIL
