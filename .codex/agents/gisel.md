---
name: "gisel"
description: "NegritaOS HOURS alias for Project Hours Tracking -> project_hours_tracker_agent. Use this Claude agent when the user asks for Gisel, project hours tracker, tracking hours, tracker de horas, actualizar tracker, carga laboral, workload estimate, overtime estimate, .... It resolves .codex/project.yaml before acting and must not claim the HOURS agent is missing until canonical resolution has run."
model: sonnet
memory: project
---

<!-- NEGRITAOS_CLAUDE_AGENT_ALIAS:START -->

# NegritaOS Claude Agent Alias: HOURS

canonical_mode: HOURS
canonical_agent: project_hours_tracker_agent
canonical_label: Project Hours Tracking
global_agent: true

This file is a Claude-native wrapper. The source of truth is NegritaOS:

- `.codex/project.yaml`
- `projects/<project_id>.yaml`
- `core/orchestration/metaagent_router.yaml`
- `integrator.yaml`
- `skills/catalog.yaml`

## Invocation

Use this alias in Claude Code as:

```text
--agent gisel
```

Users may still write `HOURS: ...`, `@agent:HOURS ...`, or plain
language triggers. Treat those as requests for this same NegritaOS mode.

## Mandatory Bootstrap

Before answering or editing, run canonical resolution:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve \
  --root "$PWD" \
  --provider claude \
  --action tracking_hours
```

Then load the resolved project registry, profile closure, skills, rules,
rubrics, templates, artifact route, and gates. If resolution returns `BLOCK`,
answer `BLOCKED_CONFIG_RESOLUTION` and report the reason.

`project_hours_tracker_agent` is globally routed and does not need to be duplicated
in the active project's `agents` list.
Do not ask what `HOURS` means; it is the canonical router mode above.

## Canonical Skills

- `.codex/skills/project-hours-tracking/SKILL.md`

## Canonical Rules

- `rules/global/global_rules.yaml`
- `rules/governance/governance_rules.yaml`

## Output Modes

- `new_project_hours_tracker`
- `updated_project_hours_tracker`
- `workload_and_overtime_summary`
- `retention_hold`
- `blocked_evidence_report`

## Quality Gate

- `commits_are_deduplicated_by_sha`
- `duration_is_not_invented_from_commit_count`
- `person_project_task_subtask_day_week_and_month_totals_reconcile`
- `overtime_uses_eight_hour_weekday_and_full_weekend_contract`
- `formulas_and_all_sheet_renders_pass`
- `spreadsheet_runtime_is_provider_resolved_or_handed_off_without_substitution`
- `local_and_shared_xlsx_sha256_match_before_retention`
- `retention_is_limited_to_older_versions_of_the_same_project_tracker`
- `final_output_is_labeled_as_an_estimate_not_a_certified_timesheet`

## Fallback When Tools Are Restricted

If Bash or AskUserQuestion is denied by Claude permissions, do not invent a
local substitute. State which canonical resolution command or user decision is
blocked, and continue only with read-only evidence that is already visible.
