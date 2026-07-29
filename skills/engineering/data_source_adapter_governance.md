# Data Source Adapter Governance

## Purpose

Keep BigQuery, PostgreSQL, files, and future providers behind explicit backend
adapters while preserving one logical contract for APIs, dashboards, and
analytics consumers.

## Contract

Each project declares:

- `provider`: `bigquery`, `postgresql`, `files`, `api`, or another named source;
- `dialect`: provider SQL/API dialect;
- `source_of_truth`: governed remote, local, API, or mixed;
- `access`: `read_only` or `read_write`;
- physical object references in backend configuration only.

## Rules

1. Configuration owns provider selection, environment overrides, credentials
   references, and physical object routing.
2. Query or repository adapters own provider-specific SQL, pagination, filters,
   casting, and cost/transaction safeguards.
3. Domain contracts own logical names, nullability, units, grain, and version
   semantics.
4. Routes validate parameters and call domain/query services; they do not build
   provider SQL or select physical tables.
5. Frontends consume logical API fields only. They never know datasets, schemas,
   table suffixes, relation names, or provider dialects.
6. Provider changes require adapter tests and contract tests proving payload
   compatibility.
7. Documentation names the source, grain, refresh behavior, access mode,
   rollback/operational limits, and validation commands.

## Analysis source-quality preflight

When the selected provider is BigQuery and the request starts a new or migrated
analysis, the analysis must declare and verify a source-quality contract before
interpreting results. The contract uses logical fields and maps them to
provider-specific columns inside the adapter or source manifest.

Required declarations:

- logical grain and unique/composite key;
- expected cardinality and join relationships;
- `event_time`;
- `source_capture_time`, when the upstream system recorded the row;
- `bq_loaded_at`, when BigQuery received the row;
- timezone, precision, analysis window, and source coverage;
- p95 latency SLA by source where one is available.

Measure ingestion latency as `bq_loaded_at - source_capture_time`. Measure
freshness separately as `now - max(bq_loaded_at)`. Event time must never
silently stand in for source capture time. If capture time is unavailable,
record `NOT_APPLICABLE`, identify the proxy and limitation, and keep the result
provisional.

The run evidence must include row count, distinct-key count, duplicate rate,
join-cardinality checks, timestamp null/invalid counts, latency percentiles,
freshness, SLA status, query/config hashes, and unresolved limitations. During
the Warn-first adoption phase, incomplete evidence produces
`CONTRACT_INCOMPLETE`; it does not produce a validated or production-ready
claim.

## Provider notes

- BigQuery: keep project/dataset/table refs and partition/cost controls in the
  backend adapter/config layer.
- PostgreSQL: keep database/schema/relation refs, transaction behavior, and
  index-sensitive query choices in the backend adapter/config layer.
- Other providers follow the same contract and must not leak physical naming
  into public payloads.
