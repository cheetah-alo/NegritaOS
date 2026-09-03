# Project Hours Tracking

Create or update a versioned XLSX workload tracker from corroborated project
evidence. The canonical executable procedure is
`.codex/skills/project-hours-tracking/SKILL.md`.

Mandatory boundaries:

- commits and artifacts prove activity, not exact continuous duration;
- deduplicate commits by SHA and evidence intervals before estimating hours;
- do not normalize people without `.mailmap` or confirmed identity evidence;
- weekday overtime is `max(0, daily hours - 8)` and all weekend hours are
  overtime;
- preserve required workbook sheets, formulas, source evidence, confidence,
  limitations, and the non-certified-timesheet caveat;
- validate and hash-match local/shared copies before any retention deletion;
- delete only older canonical tracker filenames for the exact same project
  slug and never follow symlinks;
- do not add XLSX files to Git without explicit authorization.
