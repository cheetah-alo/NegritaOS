---
id: task-tracker
mode_hint: LP   # Localized Planning / TD when writing it up
loads:
  - rules/global/negritaos_router_rule.md
  - rules/dev-commit-hygiene.md
---

# Prepare Task Tracker

Prepare a **task tracker** for the implementation. For each task add a short
**context summary** describing **what / how / when / lessons learned**. Use that
context to inform and improve the next task.

## Location

`docs/task_tracker.md` (per-project). One tracker per branch / feature epic.

## Template

```markdown
# Task Tracker — <feature or epic name>

Project: <project_id from .codex/project.yaml>
Branch:  <git branch>
Owner:   <name>
Mode:    <NegritaOS mode: LP/AE/TD/MR/CR/EP/DQ/RT>

## Backlog (ordered)

| ID    | Title                          | Status | Depends on | Mode |
|-------|--------------------------------|--------|------------|------|
| T-001 | Define data contract for X     | done   | —          | DQ   |
| T-002 | Implement feature pipeline     | wip    | T-001      | MR   |
| T-003 | Add tests + coverage gate      | todo   | T-002      | CR   |

## Task log (append-only, newest at bottom)

### T-001 — Define data contract for X
- **What**: created `configs/contracts/x_v1.json` with primary_key, partitions, 12 columns.
- **How**: extracted from upstream BQ table schema; ran `data-validation` checks.
- **When**: 2026-06-01T14:22Z
- **Lessons learned**:
  - Upstream column `usage_mb` had silent type drift (FLOAT → STRING in 2% rows).
  - Decision: enforce `SAFE_CAST` in `clean_` CTE; record in governance JSON.
- **Next-task hint**: T-002 must call validator before any aggregation.

### T-002 — ...
```

## Rules

1. **Append-only**. Never rewrite history; supersede with a new entry referencing the old ID.
2. **Every task entry MUST have all 4 fields** (what/how/when/lessons).
3. **Next-task hint** is mandatory when the lesson affects downstream work.
4. The tracker is referenced from the PR description (see `dev-commit-hygiene.md` §5.1).
5. Lessons learned that generalize beyond this feature → promote to
   `.codex/rules/dev-learnings.md` via the `learn!` flow.

## Output contract

- Created/updated `docs/task_tracker.md`.
- Confirmed all open tasks have a `Mode` aligned with the NegritaOS router.
- Returned the diff of the tracker file only.
