# BigQuery Analysis Governance

## Purpose

Govern the source-quality preflight for analyses that read BigQuery. This
guidance is provider-specific; logical contracts must remain independent of
physical project, dataset, table, or column names.

## Required analysis-entry preflight

Before an analysis query runs, identify the source adapter and declare:

- logical analysis grain (`event`, `call`, `flight`, `member`, or another
  domain-owned unit);
- unique key or composite key and expected cardinality;
- join relationships and allowed fan-out;
- logical `event_time`;
- logical `source_capture_time`, meaning when the source system recorded or
  made the row available;
- logical `bq_loaded_at`, meaning when BigQuery received the row;
- timezone and timestamp precision;
- latency SLA, preferably a p95 threshold by source;
- analysis window, partition scope, and source coverage expectation.

`event_time` is not a substitute for `source_capture_time`. If capture time is
unavailable, record `NOT_APPLICABLE`, name the proxy if one is used, state the
limitation and owner, and never report the proxy as measured ingestion latency.

## Measurements

The preflight reports these separately:

```text
ingestion_latency = bq_loaded_at - source_capture_time
freshness = now - max(bq_loaded_at)
```

Validate null timestamps, negative latency, timezone normalization, temporal
coverage, p50/p95/max latency, and SLA status. A late or incomplete source is
not converted into a zero-filled result.

## Query and storage boundaries

- Physical BigQuery routing stays in source configuration or the adapter.
- Analysis SQL lives in files and is rendered with parameters; do not build
  production SQL with ad hoc Python strings or f-strings.
- Queries are `SELECT`-only unless a separately governed workflow explicitly
  permits another operation.
- Run manifests record source/config/query hashes, grain evidence, latency
  evidence, freshness, limits, and unresolved caveats.
- Outputs use immutable `outputs/run_<id>/` directories and must not mix runs.

## Downstream evidence refresh

Presentation and report updates default to `reuse_only`. Before running a
BigQuery query, inventory matching run manifests, CSV/Parquet/JSON outputs,
plot registries, rendered plots, and query/config hashes.

- Deck-only wording, agenda, notes, layout, readability, or styling changes do
  not execute queries.
- A named missing or stale metric may use `targeted_refresh` for only its
  dependency chain.
- `full_refresh` requires explicit user authorization, a bounded SELECT-only dry
  run, partition/window declaration, and estimated bytes/cost.
- Missing evidence is reported as a gap; it is not permission to rerun every
  query.
- Targeted and full refresh outputs use a new immutable run directory and are
  recorded separately from reused artifacts.

## Warn-first publication state

During adoption, a missing or incomplete source-quality contract may execute,
but the run must be marked `CONTRACT_INCOMPLETE` and cannot be described as
validated or production-ready. The final evidence must include the missing
field, impact, and remediation owner.

## Non-goals

This skill does not impose ELAL-specific raw-severity, proxy-label, blocked-plot,
or visual-subtitle semantics. Those belong to the opt-in `elal-eda-governance`
profile.
