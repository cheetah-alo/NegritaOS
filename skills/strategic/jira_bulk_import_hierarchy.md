# Jira Bulk Import Hierarchy

## Purpose

Guide NegritaOS agents when preparing Jira Cloud bulk-import CSVs for task
hierarchies, especially subtasks under existing parent tasks.

## Audience And Scope

Use this skill for Jira task preparation, CSV hierarchy validation, import-log
repair, and rescue imports. It does not perform the Jira import directly.

## Source Of Truth

- Runtime skill: `.codex/skills/jira-bulk-import-hierarchy/SKILL.md`
- Jira project key, existing issue keys, parent summaries, and user-provided
  task/subtask lists.
- Jira validation or import logs when repairing partial imports.

## Current Contract

For subtasks under existing Jira tasks, use parent marker rows with synthetic
`Issue Id` values. Child rows must set `Parent` to the synthetic parent `Issue Id`,
not the visible Jira issue key.

Required CSV header:

```csv
Issue Key,Issue Id,Issue Type,Summary,Description,Priority,Parent
```

Parent marker rows identify existing Jira tasks. Child rows create new subtasks.

## Procedure

1. Confirm target Jira project key and parent task keys.
2. Confirm whether the job is first import or rescue import.
3. Build UTF-8 BOM CSV with parent markers and child subtasks.
4. Provide Jira field mapping:
   - `Issue Key` -> `Clave de incidencia`
   - `Issue Id` -> `ID de la incidencia` or `ID de actividad`
   - `Issue Type` -> `Tipo de Incidencia`
   - `Summary` -> `Resumen`
   - `Description` -> `Descripcion`
   - `Priority` -> `Prioridad`
   - `Parent` -> `Principal`
5. Tell the user to run Jira validation before import.
6. For failed/partial imports, parse the detailed log and generate rescue-only
   CSVs plus audit files.

## Quality Gates

- Expected Jira validation count equals child issue count only.
- Parent marker rows are not created as new Jira issues.
- `Parent` maps to `Principal`, never `Parent Link`.
- Rescue CSV excludes already created issues.
- Audit evidence separates created, failed, remaining, and reference rows.

## Ownership And Update Trigger

Owner: NegritaOS Jira import operations.

Update this skill when Jira CSV import mapping changes, Jira locale labels
change, or a new hierarchy pattern is required.
