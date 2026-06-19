---
id: commit-hygiene
domain: dev
enforcement: strict
applyTo: [git, commits, pull-requests, ci]
depends_on:
  - coding-standards
  - tests-unittest-standards
  - security
  - logging
provides:
  - commit-checklist
  - pr-checklist
  - coverage-reporting
  - precommit-answer-template
description: >
  Mandatory commit-readiness and PR-readiness checklists for the ML-as-code
  churn platform. Every commit must declare its test coverage and pass status.
  Every PR must aggregate coverage across its commits. Loaded only for
  engineering modes MR / CR / DQ as defined by the NegritaOS router.
version: 1.0.0
priority: critical
---

# Commit & PR Hygiene Standard

Two checklists are mandatory:

1. A **per-commit checklist** (every commit, including WIP commits in a PR).
2. A **per-PR checklist** (run once before requesting review and again
   before merge), which **aggregates** the coverage of every commit on the
   branch.

Both checklists are enforced for engineering modes (MR / CR / DQ). AI
agents MUST run them and report the result before proposing a commit or a
PR.

---

## 1. Branch Hygiene Before Work

Before any mutating work, agents MUST inspect and report the git tree:

```bash
git status --short --branch
git log --oneline origin/main..HEAD
```

If the remote base is not `origin/main`, use the appropriate upstream or
merge base for the repository. The report MUST include the current branch,
uncommitted changes, untracked files, pending commits, and the branch
decision: continue current branch, create a new branch, or open a PR before
continuing.

If the current branch has more than 5 unmerged commits over its base, agents
MUST recommend opening a PR and continuing new work on a fresh branch. Long
branches must not accumulate unrelated work.

---

## 2. Commit Message Format

```
type(scope): short imperative description

<optional body explaining WHY, not WHAT>

<optional trailer block: see \u00a75>
```

Allowed `type` values:

| Type        | When to use                                              |
| ----------- | -------------------------------------------------------- |
| `feat`      | New behavior visible to a user, contract, or API.        |
| `fix`       | Bug fix. MUST be paired with a regression test.          |
| `refactor`  | Internal change with no behavior delta.                  |
| `test`      | Adding or updating tests only.                           |
| `docs`      | Documentation / rules / READMEs only.                    |
| `chore`     | Tooling, deps, CI, formatting only.                      |
| `data`      | Dataset contract / schema / SQL governance changes.      |
| `ml`        | Model, feature engineering, or AutoML pipeline changes.  |

`scope` is the area touched (`validation`, `features`, `pipeline`,
`logging`, `router`, etc.).

Commits MUST be atomic: one concern per commit. If you need the word
"and" in the subject, split the commit.

---

## 3. Per-Commit Checklist (MANDATORY)

Run this for **every** commit. Paste the result into the commit body
trailer (see \u00a75) so reviewers can audit history without re-running.

| # | Check                                                                 | Pass / Fail / N/A |
| - | --------------------------------------------------------------------- | ----------------- |
| 1 | Diff contains only changes relevant to the stated scope.              |                   |
| 2 | All files touched comply with \u00a71.2 file-size policy (\u22641500 preferred). |                   |
| 3 | New / changed public symbols have Google-style docstrings.            |                   |
| 4 | Naming follows `dev-naming-conventions.md` (incl. \u00a76.1 predicates).    |                   |
| 5 | No `print()` in production code; structured logging used.             |                   |
| 6 | No secrets, PII, or credentials introduced (see `dev-security.md`).   |                   |
| 7 | `python -m unittest discover -s tests` -> **100% pass**.              |                   |
| 8 | `pytest --cov` run; coverage delta vs `main` is reported (\u00a74).        |                   |
| 9 | Static analysis (ruff + mypy + vulture) clean on changed files.       |                   |

A commit MUST NOT be created if any item is failing without an explicit
justification recorded in \u00a75 trailer.

---

## 4. Coverage Reporting per Commit (MANDATORY)

Every commit MUST report:

- **Pass rate**: `<passed>/<total>` tests passing under `unittest`.
  MUST be `100%`.
- **Coverage**: total line coverage % from `pytest --cov` over the
  production paths (`backend/app/`, `data_analytics/`, `mcp_server/`, or
  whatever the project's `local-overrides.md` declares).
- **Coverage delta**: percentage-point change vs the merge base.
  A commit that decreases coverage MUST justify it.

Command:

```bash
pytest --cov=backend/app --cov=data_analytics --cov=mcp_server \
       --cov-report=term-missing --cov-report=xml tests/
```

Minimum total coverage thresholds (from `tests-unittest-standards.md` \u00a710):

| Stage      | Floor |
| ---------- | ----- |
| Prototype  | 40%   |
| MVP        | 60%   |
| Production | 80%   |

---

## 5. Commit Message Trailer (MANDATORY)

Append the following block to every commit body:

```
Tests: 142/142 passing (unittest)
Coverage: 83.4% (Δ +0.6 pp vs main)
Checks:
  scope-clean: pass
  file-size: pass
  docstrings: pass
  naming: pass
  no-print: pass
  no-secrets: pass
  unittest: pass
  coverage-delta: pass
  static-analysis: pass
Notes: <free text, e.g. accepted exceptions>
```

CI MUST parse this block and reject commits where it is missing or where
any required field is absent.

---

## 6. Per-PR Checklist (MANDATORY, aggregated)

Run this once before requesting review and once more before merging. It
**aggregates** every commit on the branch.

| # | Check                                                                                    | Pass / Fail |
| - | ---------------------------------------------------------------------------------------- | ----------- |
| 1 | Branch hygiene was reported before mutating work (\u00a71).                                |             |
| 2 | Branch has 5 or fewer unmerged commits, or PR/new-branch plan is recorded.                |             |
| 3 | Every commit on the branch carries a valid trailer (\u00a75).                              |             |
| 4 | All commits combined: `unittest` passes `100%` on the merged state.                      |             |
| 5 | Aggregated coverage on the merged state \u2265 the stage floor (\u00a74). Report the number.     |             |
| 6 | Coverage delta across the whole PR vs `main` is reported and justified if negative.      |             |
| 7 | No new file exceeds 1700 lines; any file in 1500-1700 has a justification in the PR body.|             |
| 8 | No secret-scan hits; `.gitignore` still satisfies `dev-security.md` \u00a73.1.                |             |
| 9 | Dataset contract changes (if any) are versioned per `data-contracts.md` \u00a72.              |             |
| 10 | Public docs / README / AGENTS.md updated when behavior or workflow changed.             |             |
| 11 | The 7-question pre-commit answer (\u00a77) is included in the PR description.               |             |

A PR MUST NOT be marked "ready for review" until items 1\u20139 are green.

### 6.1 PR description coverage section (mandatory)

The PR description MUST contain a block like:

```
## Coverage summary (aggregated across N commits)

- Tests: 287/287 passing (unittest, merged state)
- Coverage: 84.1% (Δ +1.3 pp vs main)
- Per-package:
    backend/app       : 86.0%
    data_analytics    : 81.7%
    mcp_server        : 78.4%   <-- below 80% production floor; see notes
- Coverage report artifact: ci/artifacts/coverage.xml
```

---

## 7. Pre-Commit Answer Template (MANDATORY)

Before proposing a commit OR a PR, the AI agent MUST answer these seven
questions explicitly. The answer goes in the PR description; for
individual commits, a short version goes in the trailer Notes field.

```
1. What changed?
2. Which files were modified?
3. Which checks were run? (commands)
4. Which checks passed?
5. Which checks failed or were skipped? (with reason)
6. Are there any accepted exceptions?
7. Is the change aligned with the Peer Review code-quality standard?
```

A commit MUST NOT be proposed if the change introduces untested core
logic, unexplained complexity, missing validation, unclear naming, or
modifications unrelated to the stated scope.

---

## 8. CI Enforcement

CI MUST enforce, on every PR:

| Gate                                | Tool                                   | On failure |
| ----------------------------------- | -------------------------------------- | ---------- |
| Commit-message format (\u00a72)         | `commitlint` or equivalent             | Block      |
| Commit trailer presence (\u00a75)       | repo script (e.g. `scripts/validate_commit_trailers.py`) | Block |
| `unittest` pass rate                | `python -m unittest discover`          | Block      |
| Coverage floor (\u00a74)                 | `pytest --cov` + threshold check       | Block      |
| Static analysis (ruff, mypy, vulture)| pre-commit or CI step                 | Block      |
| Secret scan                         | `gitleaks` / `detect-secrets`          | Block      |
| File-size policy                    | repo script                            | Warn @1500, block @1700 |

---

## 9. Learnings

```
## Learnings
* Per-commit coverage trailers turn `git log` into a quality audit trail with zero extra effort. (1)
* Aggregating coverage at the PR level catches regressions hidden by individually-passing commits. (1)
* The 7-question template forces the agent to admit what was skipped, which is where bugs hide. (1)
```
