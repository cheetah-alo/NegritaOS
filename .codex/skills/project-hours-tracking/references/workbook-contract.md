# Workbook Contract

## Required Sheets

Every tracker contains these sheets:

1. `Tracking Hours`
2. `Commits`
3. `Analytics`
4. `Diagrama de Gantt`
5. `Meeting Load Allocation`
6. `Update Summary`
7. `Evidence Daily`
8. `Method`

Add `Duration Calibration` when a confirmed manual adjustment exists. Preserve
additional useful sheets from an existing tracker unless the user asks to
remove them.

## Minimum Fields

### Tracking Hours

`Date`, `ISO Week`, `Month`, `Person`, `Project`, `Task`, `Subtask`,
`Evidence IDs`, `Start`, `End`, `Base Hours`, `Calibration Hours`, `Total
Hours`, `Day Type`, `Estimated Overtime`, `Confidence`, `Notes`.

`Total Hours` and `Estimated Overtime` must be formulas. Keep the eight-hour
weekday capacity in a labeled assumption cell and reference that cell instead
of hardcoding `8` throughout the workbook.

### Commits

`SHA`, `Author`, `Email`, `Authored At`, `Committed At`, `Local Date`, `ISO
Week`, `Month`, `Subject`, `Changed Paths`, `Insertions`, `Deletions`, `Merge`,
`Evidence Class`, `Included`, `Exclusion Reason`.

### Analytics

Provide filterable summaries by person, project, task, subtask, day, ISO week,
and month. Include total estimated hours, weekday overtime, weekend overtime,
and total overtime. All aggregates must reconcile to `Tracking Hours`.

### Diagrama de Gantt

Include project, task, subtask, owner, start date, end date, duration, estimated
hours, and status. Dates and numeric values must remain typed values.

### Meeting Load Allocation

Include date, person, project, meeting, evidence source, confirmed duration,
allocation ratio, allocated hours, and notes. The allocated total must not
exceed the confirmed meeting duration.

### Update Summary

Record generated timestamp, timezone, previous version, coverage start/end,
latest included commit, new and total commit counts, new and total hours,
estimated overtime, source paths, SHA-256 values, retention actions, and the
non-certified-timesheet caveat.

### Evidence Daily

Include person/date, evidence count, first and last event, session count,
estimated hours, overtime, confidence, and evidence IDs.

### Method

Document source boundaries, extraction commands, identity mapping, session
break threshold, overlap handling, classification rules, overtime formulas,
calibration rules, exclusions, limitations, and update procedure.

## Formula And Visual QA

- Use formulas for derived values and quoted cross-sheet references such as
  `='Tracking Hours'!A1`.
- Keep dates, hours, counts, and percentages typed, not text-formatted.
- Scan every formula-bearing range for errors and circular references.
- Reconcile totals at workbook, person, day, week, month, task, and project
  levels.
- Render all sheets and check frozen headers, filters, legibility, clipping,
  number formats, conditional formatting, and chart/Gantt readability.
- Open the exported file with the spreadsheet runtime and run `unzip -t` as an
  independent XLSX-container check.
