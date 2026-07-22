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

## Provider notes

- BigQuery: keep project/dataset/table refs and partition/cost controls in the
  backend adapter/config layer.
- PostgreSQL: keep database/schema/relation refs, transaction behavior, and
  index-sensitive query choices in the backend adapter/config layer.
- Other providers follow the same contract and must not leak physical naming
  into public payloads.
