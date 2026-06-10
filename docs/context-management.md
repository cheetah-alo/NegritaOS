# Context Management

This document defines the architecture for managing agent context in this repository.

---

## 1. What belongs where

### Rules (`.codex/rules/`)

**Always loaded** for every task via `instruction-manifest.yaml`.

Rules must:
- Be short (target under 80 lines after compression).
- Contain only mandatory, universally applicable constraints.
- Use bullet points, not prose explanations or code examples.
- Reference skills for detailed implementation guidance.

Rules that belong here:
- `ai-behavior.md` — agent tone, escalation, code quality expectations.
- `dev-coding-standards.md` — style, file size, complexity gates.
- `dev-security.md` — secrets, PII, gitignore requirements.
- `data-contracts.md` — schema governance core rules.
- `negritaos-router.md` — router stub, points to canonical router.

Rules that do NOT belong as globals (migrate to skills):
- Anything task-specific (SQL governance, plotting, notebooks).
- Anything with long examples or code templates.
- Anything that is advisory (`enforcement: advisory`).

---

### Skills (`.codex/skills/`)

**Loaded on demand** when the task matches the skill's trigger.

Skills must:
- Have a clear `description` and `Trigger:` in their metadata.
- Be self-contained: include all context needed to perform the task.
- Be brief when used as a reference stub, or comprehensive when used as the primary reference.

Skills that exist for each migrated rule:

| Migrated rule | Target skill |
|---------------|-------------|
| `dev-logging.md` | `dev-logging/SKILL.md` (created) |
| `dev-naming-conventions.md` | `python-core/SKILL.md` |
| `dev-error-handling.md` | `python-core/SKILL.md` |
| `dev-python.md` | `python-core/SKILL.md` |
| `dev-object-orientation.md` | `python-core/SKILL.md` |
| `tests-unittest-standards.md` | `create-unittest/SKILL.md` |
| `dev-commit-hygiene.md` | `commit-hygiene/SKILL.md` |
| `data-sql-governance.md` | `data-analytics/SKILL.md` |
| `data-validation.md` | `data-contracts/SKILL.md` |
| `plotting-guidelines.md` | `eda-reports/SKILL.md` |
| `notebooks.md` | `eda-reports/SKILL.md` |

---

### Commands (`.codex/commands/`)

**Explicit workflows** triggered by the user or by the router for a specific operational task.

Commands must:
- Describe a repeatable, end-to-end procedure.
- List the steps explicitly (not just principles).
- Reference skills that need to be loaded for the command to execute correctly.

Commands inventory:

| Command | Purpose |
|---------|---------|
| `code-review-harden.md` | Full code review and hardening workflow |
| `confidence-gate.md` | Output quality confidence assessment |
| `load-context.md` | Context loading and profile activation |
| `system-audit.md` | System-wide health audit |
| `task-tracker.md` | Task planning and status tracking |
| `commit-push-pr.md` | Commit, push, and PR creation workflow |
| `run-quality-checks.md` | Local quality gate (lint, tests, coverage) |

---

### Templates (`templates/`)

Reusable output formats for structured deliverables (PRs, reports, Notion docs, slide outlines).

---

### Docs (`docs/`)

Long-form reference documents used occasionally, not loaded automatically.

| File | Purpose |
|------|---------|
| `context-management.md` | This file — architecture guide |
| `context-management-audit.md` | Audit report with file-by-file classification |
| `daily_usage_manual.md` | User-facing daily usage guide |
| `testing.md` | Testing strategy and tooling |

---

## 2. How to keep `/context` under control

1. Run the `system-audit` command periodically to review always-loaded rule file sizes.
2. Any rule file over 150 lines should be reviewed for compression.
3. Any rule with `enforcement: advisory` should be a skill, not a global rule.
4. Any rule whose `applyTo` could be narrowed (e.g., SQL-only, EDA-only) should be migrated.
5. When adding new rules: default to a skill first; promote to a global rule only if it applies to all tasks.

---

## 3. Routing table

The NegritaOS router (`integrator.yaml` + `negritaos-mode-router` skill) maps user intent to skills.

| User intent | Skills to activate |
|-------------|-------------------|
| Review code | `code-review-harden` (command), `python-core`, `pr-review-deep` |
| Review SQL | `data-analytics`, `data-contracts` |
| ML analysis / EDA | `eda-reports`, `data-contracts`, `data-loading` |
| Write documentation | `docs-alignment` |
| Commit / PR | `commit-hygiene`, `pr-review-deep` |
| Architecture change | `architecture-guardrails`, `project-structure` |
| Run quality checks | `run-quality-checks` (command) |
| Data pipeline work | `data-analytics`, `data-loading`, `data-contracts` |
| Logging instrumentation | `dev-logging` |
| Unit tests | `create-unittest`, `pytest` |
