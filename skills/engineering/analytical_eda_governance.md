# Analytical EDA Governance

## Purpose

Provide provider-neutral structure and evidence rules for new or migrated
exploratory analyses. Provider-specific behavior belongs to the selected data
source adapter profile.

## Package layout

For a new or migrated analysis, use a thin package entrypoint under
`analyses/`, reusable logic under `src/data_analytics/analyses/`, SQL files
under the package SQL directory, and configuration/manifests under `config/`.
Run artifacts belong under `outputs/run_<id>/` and must include a hash-bearing
run manifest.

Run-scoped CSV, Parquet, JSON, plot registries, rendered plots, and summary
artifacts are reusable downstream evidence. Deck and report workflows inventory
these outputs before requesting any source query refresh.

Historical packages are not silently rewritten. A `legacy/v<N>/` directory is
an audit-only quarantine: it is excluded from active manifests and normal
execution until a migration is recorded.

## Source and plot contracts

- Declare the analysis question, population, grain, denominator, time window,
  source coverage, and known limitations before interpreting plots.
- Keep the package's orchestration manifest distinct from the EDA/plot manifest.
- Validate output dimensions, restricted identifiers, enum values, and expected
  aggregate columns before persisting local artifacts.
- Separate `BLOCKED_DATA`, `BLOCKED_NO_SUPPORT`, and valid zero observations.
- Review rendered plots before using them as evidence in a deck or report.

## Scope

This profile applies to new or explicitly migrated analyses. It does not make
ELAL-specific operational-severity or subtitle rules global.

## Downstream refresh boundary

- Narrative, notes, layout, readability, agenda, and visual-emphasis changes do
  not rerun analysis queries.
- Plot restyling consumes the existing validated tabular output by default.
- A missing or stale artifact permits only a named targeted refresh unless the
  user explicitly authorizes a full refresh.
- New query results use a new immutable run directory and never overwrite the
  evidence behind an existing deck release.
