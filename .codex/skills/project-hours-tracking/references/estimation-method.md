# Evidence-Based Duration Estimation

## Evidence Priority

Use evidence in this order and retain its provenance:

1. user-confirmed duration or meeting records;
2. existing tracker calibrations with a named source and author;
3. Git commits and changed-file evidence;
4. dated test, review, document, deck, plot, release, or run artifacts;
5. Negrita Brain/Codex session metadata when available and deduplicated.

Do not use filesystem modification time as sole proof of work. Do not treat an
artifact's existence as proof of its full creation duration.

## Git Extraction

- Use `git log --all` for a first build and the last included boundary for an
  update.
- Deduplicate by full commit SHA across branches and tags.
- Record author name, author email, authored timestamp, commit timestamp,
  subject, changed paths, insertions, deletions, and merge status.
- Apply `.mailmap` when present. Preserve separate identities when no reliable
  mapping exists.
- Keep merge commits in the evidence table but do not assign duplicate effort
  already represented by their contained commits.

## Time Windows

Commits alone cannot establish exact start and end times. Build conservative
daily evidence windows and record the method used:

- group attributable events by person and local day;
- split sessions when the inactivity gap exceeds the declared threshold;
- use 90 minutes only as a default session-break threshold, not as credited
  work time;
- do not add unsupported time before the first or after the last event;
- isolated events without supporting duration evidence may establish activity
  but must not be expanded into a multi-hour interval;
- merge overlapping evidence intervals before summing hours.

If the evidence cannot support a defensible duration, record
`INSUFFICIENT_DURATION_EVIDENCE` and exclude it from the hour total rather than
inventing a value.

## Classification

Classify work from paths, commit subjects, and corroborating artifacts. Keep
project, task, and subtask distinct. Recommended task families include code,
SQL/data, tests/QA, plots, plot analysis, documentation, presentation build,
results analysis, review, deployment, and project coordination.

Classification confidence must be `high`, `medium`, or `low`. Low-confidence
classification remains visible and must not be silently reassigned.

## Manual Calibration

Manual calibration is allowed only when the user confirms the duration or an
authoritative record supports it. Record original estimate, adjustment,
resulting duration, reason, source, confirmer, and timestamp. Never use a
calibration from one project as factual duration evidence for another.

## Update Boundary

For an update, read the prior `Update Summary`, `Commits`, and `Method` sheets.
Use the latest included commit SHA and timestamp together. Re-scan a small
overlap window to detect late-arriving or rebased evidence, then deduplicate by
SHA so totals remain stable.
