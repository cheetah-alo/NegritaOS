# Pull Request Risk Review

This native engineering skill defines NegritaOS governance for PR risk review.
It complements `pr-review-deep`: run the risk gate first, then perform deep
technical review when the risk score, changed surface, or user request requires
it.

## Activation

Use for:

- pull request, merge request, branch, or diff review;
- merge-gate or auto-approval evaluation;
- GitHub PR checks, CI status, PR comments, or approval readiness;
- Python, SQL, BigQuery, dashboard, ML, pipeline, or documentation PRs where
  production risk needs to be made explicit.

## Required Review Evidence

The reviewer must inspect:

- PR title, description, repository, base/head, author, and comments;
- full diff, changed file list, file categories, and lines changed;
- required check status and exact test/validation commands;
- generated artifacts, coverage/tmp/output files, secrets, auth, config,
  deployment, CI/CD, schema, SQL, migration, and data-contract changes;
- CODEOWNERS or project ownership rules when present.

If a required input is unavailable, return `insufficient_evidence` and list the
missing item. Do not substitute assumptions for check results.

## Risk Scoring

Score six dimensions from `0` to `10`:

- `blast_radius`
- `reversibility`
- `data_security`
- `operational_impact`
- `verification_gap`
- `change_surface`

Report `risk_total_60`, `risk_score_100`, `risk_level`, hard-stop reasons, and
the recommended action. Hard stops override thresholds.

## Quality Tooling Gate

When reviewing Python-bearing PRs, the reviewer should request or run, when
safe and available, these checks from the project venv:

```bash
source <venv>/bin/activate
pip install flake8 flake8-docstrings pep8-naming pylint mypy vulture pytest pytest-mccabe
flake8 --version
pylint --version
flake8 <path_to_folder> --max-line-length=120
flake8 <path_to_folder> --max-complexity=10
pylint <path_to_folder> --output-format=colorized
pylint <path_to_folder> --disable=all --enable=R0913,R0914,R0915,R0916 --output-format=colorized
mypy <path_to_folder> --ignore-missing-imports
pytest --mccabe tests/
pytest --cov=src tests/
vulture <path_to_folder>
```

Persisted outputs are evidence artifacts only. They must not be committed unless
the repository explicitly declares a tracked report location.

## V1 Policy

- Mode: `shadow/recommendation`.
- Actual approval, merge, check dismissal, or external PR comment requires an
  explicit user request and available connector permissions.
- `auto_approve_allowed` remains `false`.
- Low risk returns `approve_candidate`, not a merge action.

## Brain Degraded-State Strategy

Keep PR review and fix execution as separate lanes:

- `review_only` can run with a missing READY Brain contract and must report
  `BLOCKED_CONFIG_RESOLUTION` as a limitation without mutating code or Git.
- `fix_execution` requires a READY contract. Legacy Memory v1 blockers route to
  `git_tree_governance_agent` (`GT`) for explicit, backed-up session recovery.
- After recovery, resolve a new READY session and rerun PRR before applying the
  fixes. PRR must not silently close or repair Brain sessions itself.
