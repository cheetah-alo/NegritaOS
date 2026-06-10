You are working inside the `NegritaOS` repository.

Your task is to audit and improve how project context is managed for Claude/Codex agents.

## Current state snapshot (as of 2026-06-01)

**Actual rule file inventory — `.claude/rules/` (21 files, 4177 lines total)**

| File | Lines | Status |
|------|-------|--------|
| `dev-logging.md` | 446 | Loaded globally — oversized |
| `dev-naming-conventions.md` | 443 | Loaded globally — oversized |
| `tests-unittest-standards.md` | 388 | Loaded globally — oversized |
| `dev-error-handling.md` | 381 | Loaded globally — oversized |
| `dev-python.md` | 357 | Loaded globally — oversized |
| `dev-object-orientation.md` | 312 | Loaded globally |
| `plotting-guidelines.md` | 308 | Advisory — should be a skill |
| `dev-learnings.md` | 297 | Meta — should stay global but be trimmed |
| `dev-commit-hygiene.md` | 229 | Should be a skill + command |
| `dev-security.md` | 206 | Loaded globally |
| `data-contracts.md` | 185 | Loaded globally |
| `dev-coding-standards.md` | 167 | Loaded globally |
| `ai-behavior.md` | 153 | Core — should stay |
| `data-sql-governance.md` | 118 | Should be a skill |
| `data-validation.md` | 75 | Should be a skill |
| `notebooks.md` | 60 | Should be a skill |
| `negritaos-router.md` | 32 | Stub — keep |
| `pipelines.md` | 5 | Too thin — merge or expand |
| `ml-telemetry.md` | 5 | Too thin — merge or expand |
| `dev-tree-widgets.md` | 5 | Too thin — merge or expand |
| `dev-observables.md` | 5 | Too thin — merge or expand |
| `data-contracts-lite.md` | 0 | **EMPTY FILE — must be filled or removed** |

**Existing `.claude/commands/` (5 files)**

* `code-review-harden.md`
* `confidence-gate.md`
* `load-context.md`
* `system-audit.md`
* `task-tracker.md`

**Existing `.claude/skills/` (30+ skills already built)**
Notable: `commit-hygiene`, `python-core`, `data-contracts`, `data-analytics`, `data-loading`, `eda-reports`, `pr-review-deep`, `rule-compliance-gate`, `sdd-flow`, `negritaos-mode-router`, and more.

**Observed context characteristics**

* Memory files carry the dominant load because every rule file is loaded globally.
* Skills consume minimal tokens because they are on-demand.
* The current issue is not critical yet, but memory files are carrying too much permanent context.
* The goal is to make the agent more modular, maintainable, deterministic, and context-efficient.

## Objective

Redesign the context architecture so that only essential global rules are always loaded, while specialized knowledge is moved into skills, commands, or task-specific documents.

The final result should reduce always-loaded context, avoid duplicated rules, improve routing between tasks, and make the repository easier to scale as more agents are added.

## What you need to do

### 1. Audit current context sources

Review the current structure:

* `.claude/rules/`  (NOT `.codex/rules/` — this repo uses `.claude/` exclusively)
* `.claude/commands/`
* `.claude/skills/`
* `.claude/memory/` and project memory files
* `integrator.yaml` and `.claude/instruction-manifest.yaml` for load order

Identify:

* which rules are truly global and should always be loaded;
* which rules are task-specific and should become skills;
* which rules are duplicated across files;
* which files are too verbose;
* which files contain examples that should be moved out of global memory;
* which files are obsolete, stale, or overlapping.

Do not delete anything immediately. First produce an audit report.

## Classification framework

Classify each file into one of these categories:

| Category   | Meaning                                   | Recommended destination                                |
| ---------- | ----------------------------------------- | ------------------------------------------------------ |
| Core Rule  | Must always apply to all tasks            | `.claude/rules/` (trim to bullets, keep always-loaded) |
| Skill      | Needed only for a specific type of work   | `.claude/skills/<skill-name>/SKILL.md`                 |
| Command    | A repeatable operational workflow         | `.claude/commands/<command>.md`                        |
| Template   | Reusable output format                    | `templates/`                                           |
| Reference  | Long-form documentation used occasionally | `docs/` or `knowledge/`                                |
| Deprecated | No longer needed or superseded            | mark as deprecated, do not remove without confirmation |

## Target architecture

All paths are under `.claude/` — this repo does not use `.codex/`.

Propose and, if safe, implement this delta on top of what already exists:

```text
.claude/
  rules/
    # KEEP (trim to bullet-point form):
    ai-behavior.md          (core — always loaded)
    dev-coding-standards.md (core — trim examples)
    dev-security.md         (core — always loaded)
    negritaos-router.md     (core stub — keep)
    data-contracts.md       (core — trim, delegate details to skill)

    # MIGRATE to skills (remove from always-loaded):
    dev-logging.md          -> skills/dev-logging/SKILL.md
    dev-naming-conventions.md -> merge into skills/python-core/
    tests-unittest-standards.md -> skill create-unittest (already exists)
    dev-error-handling.md   -> skills/python-core/ + keep short core rule
    dev-python.md           -> skills/python-core/ (already exists)
    plotting-guidelines.md  -> skills/eda-reports/ (already exists)
    dev-commit-hygiene.md   -> skills/commit-hygiene/ (already exists)
    data-sql-governance.md  -> skills/data-analytics/ (already exists)
    data-validation.md      -> skills/data-contracts/ (already exists)
    notebooks.md            -> skills/eda-reports/ (already exists)
    dev-object-orientation.md -> skills/python-core/ (already exists)

    # RESOLVE:
    data-contracts-lite.md  EMPTY — fill with 5-bullet summary or delete
    pipelines.md            3 bullets only — merge into core or expand
    ml-telemetry.md         3 bullets only — merge into core or expand
    dev-tree-widgets.md     3 bullets only — merge into core or expand
    dev-observables.md      3 bullets only — merge into core or expand

  commands/
    # EXISTING (do not recreate):
    code-review-harden.md
    confidence-gate.md
    load-context.md
    system-audit.md         (covers audit-context purpose)
    task-tracker.md

    # ADD (gaps vs plan):
    commit-push-pr.md       (not yet created)
    run-quality-checks.md   (not yet created)

  skills/
    # ALREADY EXISTS — do not recreate:
    commit-hygiene/
    python-core/
    data-contracts/
    data-analytics/
    data-loading/
    eda-reports/
    pr-review-deep/
    rule-compliance-gate/
    create-unittest/
    negritaos-mode-router/
    # and ~20 more

    # GAPS — create if needed:
    dev-logging/            (no equivalent skill exists yet)
    academic-evaluator/     (check skills/academic/ first)

templates/                  (already exists at repo root)
docs/                       (already exists — add context-management-audit.md here)
```

## Design principles

Apply these principles:

1. Keep global rules short and mandatory.
2. Move task-specific details into skills.
3. Move long examples into templates or docs.
4. Avoid loading large documents by default.
5. Avoid duplicated instructions across rules and skills.
6. Prefer explicit routing over implicit behavior.
7. Every rule should have a clear purpose.
8. Every skill should have a clear activation trigger.
9. Every command should describe a repeatable workflow.
10. The system should be easy to audit with `/context`.

## Expected deliverables

Produce the following:

### A. Context audit report

Create or update:

```text
docs/context-management-audit.md
```

Include:

* current files reviewed;
* estimated role of each file;
* recommended action;
* duplicate or overlapping areas;
* largest context consumers;
* quick wins;
* risks;
* proposed migration plan.

Use this table:

| File | Current role | Problem | Recommendation | Priority |
| ---- | ------------ | ------- | -------------- | -------- |

### B. Proposed context architecture

Create or update:

```text
docs/context-management.md
```

Explain:

* what belongs in rules;
* what belongs in skills;
* what belongs in commands;
* what belongs in templates;
* what belongs in docs;
* how to keep `/context` under control.

### C. Rule compression

Review existing `.claude/rules/*.md` files.

For each large rule file, propose a compressed version with:

* mandatory rules only;
* no duplicated examples;
* no long explanations unless necessary;
* clear bullet points;
* maximum useful density.

Do not remove important governance requirements.

### D. Skill migration plan

For task-specific content, propose the corresponding skill.

For example:

* `dev-error-handling.md` may become part core rule, part `python-engineering`, part `backend-service`.
* `dev-naming-conventions.md` may become part `core-code-quality`, part `python-engineering`, part `api-design`.
* `dev-commit-hygiene.md` may become part `commit-hygiene` skill and `.claude/commands/commit-push-pr.md`.

### E. Router improvement

Review or update `.claude/skills/negritaos-mode-router/SKILL.md` (already exists) and `integrator.yaml` (already exists at repo root). Do not create a new router — the router is already implemented.

Verify the routing table aligns with actual skill names (use `.claude/skills/` directory as the source of truth):

| User intent | Activate (actual skill folder names) |
|---|---|
| Review code | `code-review-harden` (command), `python-core`, `pr-review-deep` |
| Review SQL | `data-analytics`, `data-contracts` |
| Build ML analysis | `eda-reports`, `data-contracts`, `data-loading` |
| Write Notion/docs | `docs-alignment` |
| Build executive presentation | check `brands/` skills under `.claude/skills/` |
| Academic TFM review | check `skills/academic/` under `skills/` |
| Commit / PR | `commit-hygiene`, `pr-review-deep` |
| Architecture change | `architecture-guardrails`, `project-structure` |

Note: `notion-docs`, `presentation-executive`, `security-review`, and `python-engineering` do not exist as named skills. Use the closest existing equivalent or create them.

### F. Verification command

Do NOT create `audit-context.md` — `.claude/commands/system-audit.md` already exists and covers this purpose. Review and update it instead.

The command should:

1. Run `/context`.
2. Identify the largest context consumers.
3. List always-loaded memory files.
4. Recommend files to compress, migrate, or deactivate.
5. Check whether rules, skills, and commands are clearly separated.
6. Produce a short summary with:

   * current context usage;
   * memory files token usage;
   * skills token usage;
   * recommended action.

## Implementation rules

Before modifying files:

1. Inspect the existing repo structure.
2. Do not overwrite files blindly.
3. Preserve existing useful content.
4. Prefer moving or summarizing over deleting.
5. If a change is risky, create a proposal instead of editing.
6. Keep diffs small and reviewable.
7. Document every structural decision.
8. Do not introduce emojis in repo files.
9. Use clear professional English.
10. Keep files maintainable and readable.

## Final response format

At the end, provide:

1. Summary of what was found.
2. Files changed.
3. Files proposed for migration.
4. Estimated context savings.
5. Risks or unresolved decisions.
6. Next recommended command to run.

Do not just explain. Perform the audit and make safe improvements where possible.
