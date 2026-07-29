---
name: jira-bulk-import-hierarchy
description: >
  Create, validate, repair, and document Jira Cloud bulk-import CSVs for Epic,
  Task, and Subtask hierarchies. Trigger: importing Jira issues from CSV,
  creating subtasks under existing tasks, fixing invalid Parent selection
  errors, parsing Jira import logs, or preparing import-ready rescue CSV files.
license: Apache-2.0
metadata:
  author: CQI
  version: "1.0.0"
  scope: [root]
  auto_invoke:
    - "Create, validate, repair, or document Jira Cloud bulk-import CSVs"
    - "Prepare Jira issue hierarchies or rescue imports"
---

# Jira Bulk Import Hierarchy

## Purpose

Prepare Jira Cloud CSV imports without breaking hierarchy or duplicating issues.
Use this skill for first imports, rescue imports after partial failure, and
audit-ready evidence files for Jira task preparation.

## Audience And Scope

Use this for Jira Cloud CSV preparation, validation guidance, import-log parsing,
and rescue CSV generation. This skill does not import directly into Jira and
does not replace Jira administrator approval.

## Source Of Truth

- User-provided target Jira project key and issue hierarchy.
- Existing Jira parent task keys and summaries.
- Jira CSV validation/import logs when repairing a failed import.
- Local generated CSV files under the project or tenant working folder.

## Core Rule

For subtasks under existing Jira tasks, do not rely only on visible parent keys
in the child rows. Use parent marker rows plus synthetic `Issue Id` values.

```csv
Issue Key,Issue Id,Issue Type,Summary,Description,Priority,Parent
EXTCQI-38,10038,,DS-04 Build and Run Data Quality Checks,,,
,20001,Subtask,DS-04.1 Check critical nulls.,,Medium,10038
```

The subtask `Parent` must point to the synthetic `Issue Id` of the parent marker
row.

## Required Inputs

Ask for or discover:

- Target Jira project key, for example `EXTCQI`.
- Existing parent task keys, for example `EXTCQI-38`.
- Parent task summaries.
- Subtask summaries and optional descriptions.
- Whether this is a first import or a rescue import after partial failure.
- Jira validation/import log if there was a previous failure.

## CSV Output Contract

Use UTF-8 with BOM (`utf-8-sig`) and comma delimiter.

For subtask imports under existing tasks, generate this header:

```csv
Issue Key,Issue Id,Issue Type,Summary,Description,Priority,Parent
```

Parent marker rows:

- `Issue Key`: existing Jira issue key.
- `Issue Id`: synthetic stable numeric ID, usually derived from key number,
  for example `EXTCQI-38 -> 10038`.
- `Issue Type`: blank.
- `Summary`: existing parent task summary.
- `Description`, `Priority`, `Parent`: blank.

Child rows:

- `Issue Key`: blank.
- `Issue Id`: synthetic child ID, for example `20001`.
- `Issue Type`: `Subtask`.
- `Summary`: subtask title.
- `Description`: optional.
- `Priority`: usually `Medium`.
- `Parent`: synthetic parent `Issue Id`, not the visible Jira key.

## Jira Field Mapping

Tell the user to map:

- `Issue Key` -> `Clave de incidencia`
- `Issue Id` -> `ID de la incidencia` or `ID de actividad`
- `Issue Type` -> `Tipo de Incidencia`
- `Summary` -> `Resumen`
- `Description` -> `Descripcion`
- `Priority` -> `Prioridad`
- `Parent` -> `Principal`

Do not map `Parent` to `Parent Link`.
Do not map `Parent` to `Id de Incidencia`.
Do not map `Parent` to any `Link ...` field.

## Value Mapping

On Jira value mapping:

- `Subtask` -> `Subtask` or `Subtarea`, depending on Jira locale.
- `Medium` -> `Medium`.
- Leave blank values unmapped.

## Validation Gate

Always instruct the user to click `Validar` before importing.

Expected count must equal the number of child subtasks only.

Example:

- CSV has 8 parent marker rows and 66 child subtasks.
- Expected validation: `66 incidencia(s) se crearan correctamente`.

Stop if Jira says it will create parent marker rows too.
Stop if Jira says some subtasks have invalid parent selection.
Stop if Jira count is lower or higher than expected and request the detailed
import log.

## Rescue Import Workflow

When an import partially succeeds:

1. Parse the Jira detailed log.
2. Extract created issues from lines like:
   `Issue created successfully with Key [EXTCQI-47]`.
3. Extract failed issues from lines like:
   `doesn't have a valid Parent selection`.
4. Do not reimport the full original CSV.
5. Generate a rescue CSV with failed subtasks only.
6. Generate audit files:
   - `jira_subtasks_created_from_log.csv`
   - `jira_subtasks_failed_from_log.csv`
   - `jira_subtasks_remaining_import_ready.csv`
   - `jira_subtasks_all_reference_do_not_reimport.csv`
   - `jira_subtasks_parent_key_map_check.csv`

## Safety Rules

- Never import directly after a failed validation.
- Never reuse an old Jira configuration file unless the mapping is verified.
- Never use exported Jira CSV headers as-is without normalization.
- Never reimport rows already created.
- Use Python `csv` or a structured parser; do not parse CSV with shell splitting
  because summaries may contain commas.

## Recommended Storage

Store local evidence under:

```text
team-lead-qaqc/tenants/<tenant>/jira_imports/
```

If the user needs the file in OneDrive or Downloads, copy it there only after
approval when sandbox rules require it.

## User-Facing Closeout

Always report:

- Which file to import.
- Which files are evidence only.
- Expected validation count.
- Exact Jira field mapping.
- Whether any issues were already created and must not be duplicated.

## Validation

Before closeout, verify:

- The import CSV has UTF-8 BOM and the required header.
- Every child `Parent` references a parent marker `Issue Id`.
- Validation count equals child issue count.
- Rescue CSV excludes already created issues.
