---
name: pull-request-risk-review
description: >
  Risk-based pull request review gate for CI status, blast radius, security,
  verification evidence, and Python code-quality checks.
  Trigger: Reviewing PRs, merge gates, PR risk review, auto-approve requests,
  GitHub PR checks, or pull request approval decisions.
license: Apache-2.0
metadata:
  author: NegritaOS
  version: "1.0"
  scope: [root]
  auto_invoke: "Reviewing pull requests, PR risk, merge gates, or PR approvals"
---

## When to Use

Use this skill before any deep PR review when the user asks to:
- review a pull request, branch, merge request, or PR diff;
- decide whether a PR is safe to approve, merge, or escalate;
- evaluate CI/check status, test evidence, code quality, or verification gaps;
- run a shadow auto-approval or merge-gate assessment.

Do not use this skill to approve, merge, dismiss checks, or post external
comments unless the user explicitly asks for that action and the connector
permissions are available.

## Operating Mode

V1 is `shadow/recommendation` only.

- `auto_approve_allowed` is always `false`.
- Low-risk PRs may receive `approve_candidate`, not an actual approval.
- Medium or high-risk PRs require `human_review` or `changes_required`.
- Missing critical evidence returns `insufficient_evidence` or `blocked`.

## Brain Degraded-State Strategy

PRR has two separate lanes:

- `review_only`: may inspect a PR and report findings when Brain has no READY
  contract, but must return `BLOCKED_CONFIG_RESOLUTION` as an execution
  limitation and may not mutate code or Git state.
- `fix_execution`: requires a READY Brain contract. If the blocker is legacy
  Memory v1, hand off to `git_tree_governance_agent`/`GT` for explicit recovery;
  do not bypass the gate from PRR.

After recovery, resolve a new READY session and rerun PRR before applying the
requested fixes. A PR review must never become the mechanism that silently
repairs or closes Brain sessions.

## Required Inputs

Collect and cite the evidence actually inspected:

- PR metadata: title, description, author, base branch, head branch, repository.
- Full diff and changed file list, not only the PR summary.
- Lines changed and file categories: source, tests, docs, config, CI/CD, infra,
  secrets, data contracts, SQL, migrations, generated artifacts.
- Required checks and status: complete, passed, failed, pending, skipped.
- Test evidence and exact commands when available.
- Comments or review threads that change acceptance risk.
- CODEOWNERS or project-declared ownership rules when present.

If required checks are unavailable or still pending, do not infer success.

## Risk Model

Score each dimension from `0` to `10`, where `0` is no material risk and `10`
is severe or unresolved risk.

| Dimension | Review Focus |
|---|---|
| `blast_radius` | Number of users, services, data products, workflows, or repositories affected. |
| `reversibility` | Ability to roll back safely without data loss, migration damage, or manual recovery. |
| `data_security` | Secrets, auth, permissions, PII, data export, logging, and dependency trust. |
| `operational_impact` | CI/CD, jobs, runtime reliability, cost, latency, monitoring, and on-call burden. |
| `verification_gap` | Missing tests, failed checks, missing reproduction, weak coverage, or unrun quality gates. |
| `change_surface` | Diff size, cross-module coupling, generated code, config spread, and ownership complexity. |

Report:

- `risk_total_60 = sum(dimensions)`
- `risk_score_100 = round(risk_total_60 / 60 * 100)`
- `risk_level`: `low`, `medium`, `high`, `blocked`, or `insufficient_evidence`

Default thresholds:

| Total | Level | Recommended Action |
|---:|---|---|
| 0-15 | low | `approve_candidate` in shadow mode |
| 16-30 | medium | `human_review` |
| 31-45 | high | `changes_required` or `human_review` |
| 46-60 | blocked | `blocked` |

Hard stops override numeric thresholds.

## Hard Stops

Return `blocked` or `insufficient_evidence` when any of these apply:

- required CI/checks are failed, missing, or still pending;
- secrets, tokens, credentials, or sensitive local artifacts appear in the diff;
- auth, permissions, billing, deployment, CI/CD, or security boundaries change
  without explicit review evidence;
- destructive migrations or data-loss paths lack rollback evidence;
- production data contracts, schemas, SQL, or source adapters change without
  contract tests or dry-run evidence;
- generated coverage/tmp/output/local artifacts are committed;
- the diff cannot be inspected fully.

## Python Code Quality Checks

Use the project venv when available. Do not install packages globally.

```bash
source <venv>/bin/activate
pip install flake8 flake8-docstrings pep8-naming pylint mypy vulture pytest pytest-mccabe
flake8 --version
pylint --version
```

Canonical commands:

```bash
flake8 <path_to_folder> --max-line-length=120
flake8 <path_to_folder> --max-complexity=10
pylint <path_to_folder> --output-format=colorized
pylint <path_to_folder> --disable=all --enable=R0913,R0914,R0915,R0916 --output-format=colorized
mypy <path_to_folder> --ignore-missing-imports
pytest --mccabe tests/
pytest --cov=src tests/
vulture <path_to_folder>
```

Notes:

- `C901` indicates cyclomatic complexity from Flake8/McCabe.
- `R0913`, `R0914`, `R0915`, and `R0916` are Pylint design-risk signals.
- Pylint `C0116` is `missing-function-docstring`; type hinting is primarily
  validated by `mypy`.
- Persisted reports must be ignored or run-scoped evidence; do not commit
  `flake8_output.txt`, `pylint_output.txt`, coverage, tmp, or local outputs.

## Output Contract

Return a structured review:

```yaml
pull_request:
  repository: <repo>
  number: <number-or-null>
  title: <title>
  base: <base>
  head: <head>
checks:
  required_complete: true|false
  required_passed: true|false
  failed_or_missing: []
risk_dimensions:
  blast_radius: {score: 0, evidence: []}
  reversibility: {score: 0, evidence: []}
  data_security: {score: 0, evidence: []}
  operational_impact: {score: 0, evidence: []}
  verification_gap: {score: 0, evidence: []}
  change_surface: {score: 0, evidence: []}
quality_checks:
  flake8: {command: <exact-command-or-null>, status: pass|fail|not_run, summary: <summary>}
  pylint: {command: <exact-command-or-null>, status: pass|fail|not_run, summary: <summary>}
  mypy: {command: <exact-command-or-null>, status: pass|fail|not_run, summary: <summary>}
  mccabe: {command: <exact-command-or-null>, status: pass|fail|not_run, threshold: 10}
  coverage: {command: <exact-command-or-null>, status: pass|fail|not_run, summary: <summary>}
  vulture: {command: <exact-command-or-null>, status: pass|fail|not_run, summary: <summary>}
hard_escalation_reasons: []
risk_total_60: 0
risk_score_100: 0
risk_level: low|medium|high|blocked|insufficient_evidence
recommended_action: approve_candidate|human_review|changes_required|blocked|insufficient_evidence
auto_approve_allowed: false
uncertainties: []
audit:
  policy_version: pull-request-risk-review@1.0
  review_mode: shadow
```

## Review Discipline

- Findings first, ordered by severity.
- Distinguish observed evidence from assumptions.
- Missing evidence is a risk signal, not a pass.
- Never claim checks, tests, coverage, or code-quality tools ran unless their
  exact command and result are known.
