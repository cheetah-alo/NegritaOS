# Task Tracker - NegritaOS System Audit Hardening

Project: negritaos
Branch: main
Owner: Codex
Mode: CR

## Backlog

| ID | Title | Status | Depends on | Mode |
|---|---|---|---|---|
| T-001 | Harden system audit and skill validation | done | none | CR |
| T-002 | Install and run extended local quality/security tooling | done | T-001 | CR |
| T-003 | Clean Brain memory warnings through controlled maintenance | done | T-001 | CR |
| T-004 | Prevent personal Git identities in CQI checkouts | done_local | none | CR |
| T-005 | Add direct Astra routing and cost-per-result comparison | done_local | none | CR |
| T-006 | Define NegritaOS 360 capability catalog and knowledge graph | planned | T-005 | LP/CR |

## Task Log

### T-006 - NegritaOS 360 Capability Catalog And Knowledge Graph

- **What**: add the OO contract, typed capability catalog, project coverage matrix and derived knowledge graph for projects, profiles, modes, agents, skills, rules, templates, gates and Brain usage.
- **Plan**: `docs/negritaos_360_dashboard_architecture_plan__updated_20260927_122000.md`.
- **Decision**: use immutable Python dataclasses and Protocol-based adapters; keep the graph as a derived read model, with registry files and Brain as sources of truth.
- **Scope**: planning/documentation only; dashboard read model, API and UI remain pending CAT-001 through CAT-008.

### T-005 - Astra Routing
- **What**: add globally routed Astra review while retaining explicit Luna workers and existing Sol production minimum.
- **How**: extend tier/action/signal/agent-impact mappings, add native Codex and Claude profiles, distribute canonical aliases, add routing and partial-rollout tests, and document comparable usage records.
- **When**: 2026-09-08, Europe/Madrid.
- **Lessons learned**: model rank is not task cost; comparison must include failed attempts and subagents. Agent-name selection must carry the same evidence impact as action selection. Runtime model availability and named-profile discovery are separate checks.
- **Limits**: no price benchmark or savings claim; four OneDrive adapters are OS-permission blocked. Source is versioned on `feature/cqi-git-identity-hooks`; merge to main is a separate step.
- **Outcome**: `astra-reviewer` and the Claude `astra` alias are available in 18/22 local adapters and the Codex personal profile. A real GPT-6 Astra delegated review completed; its agent-only impact finding was fixed and independently rechecked. The model policy validates 10 global agents, and canonical alignment passes 30/30.
- **Validation**: 219/219 tests passed; package coverage exceeds 80%; model/registry/catalog validation, Flake8 and diff hygiene passed. Four OneDrive adapters remain unavailable even with elevated filesystem permission.

### T-004 - CQI Git Identity Controls
- **What**: exact local corporate identity, shared identity hooks, preserved existing hooks, neutral CI bundle and drift checks.
- **How**: canonical identity profile, repo-local Git configuration, private backups and receipts, real Git commit/push regression tests and independent review.
- **When**: 2026-09-08T10:41:48+02:00, Europe/Madrid.
- **Lessons learned**: checking `git config user.email` misses environment overrides and inherited commits; worktrees may have no adapter but still share Git configuration. Local installation and remote enforcement require separate evidence.
- **Validation**: full suite 208/208, source coverage 82%, Flake8 and diff hygiene pass. The final 17 real-Git integration tests cover overrides, preserved hooks/stdin, pushes, legacy baselines, worktrees, rollback, CI receipts and shallow-history rejection. Local rollout passes on eight registered CQI repositories and two active linked worktrees. Canonical alignment passes 30/30; full alignment cannot read four OneDrive adapters even with elevated permission.
- **Review**: independent review prompted stable runtime snapshots, rollback of runtime files, sibling-worktree preflight, per-checkout CI hashes and explicit separation of trusted PR verification from advisory push audits.
- **Certification boundary**: the independent review reported no defect in the final scoped atomic-install correction; no formal SHA-bound independent PASS or remote certification is claimed.
- **Remaining**: source changes are on `feature/cqi-git-identity-hooks`; publish/merge the neutral repository CI files and verify required remote checks separately. Existing commit histories were not rewritten. Provider-account checks for gh/gcloud remain a separate workstream.

### T-001 - Harden system audit and skill validation
- **What**: reviewed and hardened the just-built NegritaOS audit changes, including mode resolution, skill validation, Nate provenance, plotting metadata, macOS `skill-sync`, and audit documentation.
- **How**: resolved Brain in `CR`, inspected the scoped diff, reproduced validator/runtime failures, applied minimal patches, added regression tests, and reran canonical validations.
- **When**: 2026-08-17T09:47:00Z
- **Lessons learned**:
  - Skill validators need to distinguish literal path references from command examples in Markdown code spans.
  - macOS Bash 3 compatibility must be tested directly when shell tools use arrays or associative-array-like state.
- **Next-task hint**: T-002 should install or provide a governed local wrapper for `gitleaks`, `detect-secrets`, `pip-audit`, `flake8`, `pylint`, `mypy`, and `vulture` before calling release quality fully verified.

### T-002 - Install and run extended local quality/security tooling
- **What**: upgraded PR quality/security from an ad hoc basic secret grep to a governed local/CI toolchain with `detect-secrets`, Flake8, Pylint, mypy, pytest coverage/McCabe, vulture, and `pip-audit`.
- **How**: added `requirements/pr-quality-tools.txt`, local setup and run scripts, a `detect-secrets` CI wrapper that reports metadata only, CI installation, and documentation in `docs/pr_quality_security_toolchain.md`.
- **When**: 2026-08-17T10:18:00Z
- **Lessons learned**:
  - CI should run a reproducible Python-native scanner before adopting external binary/action dependencies.
  - Local quality reports, venvs, coverage, and scan outputs need explicit ignore rules because PRR evidence belongs in summaries, not tracked artifacts.
  - `pip-audit` must run with network evidence; it found vulnerable `pytest 8.4.2`, fixed by requiring `pytest>=9.0.3`.
  - Full-repo lint/type enforcement needs gradual adoption; v1 keeps those checks advisory unless `PR_QUALITY_STRICT=1`.

### T-003 - Clean Brain memory warnings through controlled maintenance
- **What**: added and ran a separate authorized cleanup path for stale Memory v2 runtime sessions.
- **How**: implemented `memory close-stale-runtime` with dry-run default, explicit `--apply` authorization, age gating, and runtime-only `state.json` closure metadata; then closed 18 stale NegritaOS runtime sessions while leaving the current active session open.
- **When**: 2026-08-17T10:24:00Z
- **Lessons learned**:
  - Memory v1 legacy closures and Memory v2 stale runtime closures need separate commands and authorization semantics.
  - `doctor_status: WARN` can be operationally acceptable when only the current session and preserved legacy artifacts remain, but stale sessions should be closed by API instead of direct file edits.
