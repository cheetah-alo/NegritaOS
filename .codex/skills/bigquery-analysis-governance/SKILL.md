---
name: bigquery-analysis-governance
description: >
  Govern BigQuery analysis preflight for logical grain, key/cardinality checks,
  source-capture-to-load latency, freshness, SELECT-only SQL, cost controls,
  and run-scoped evidence. Use at the start of new or migrated BigQuery
  analyses, source-quality reviews, or BigQuery EDA execution.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, data_analytics]
  auto_invoke: true
---

# BigQuery Analysis Governance

Read and apply the canonical guidance in
`skills/engineering/bigquery_analysis_governance.md`.

## Required first response state

Before planning or running a new or migrated BigQuery analysis, report:

- source adapter and physical object owner;
- logical grain, key, expected cardinality, and join relationships;
- event, source-capture, and BigQuery-load timestamp mappings;
- latency definition and SLA;
- freshness definition and analysis window;
- source-quality contract path and preflight status.

If the canonical project-to-registry-to-profile resolution fails, stop with
`BLOCKED_CONFIG_RESOLUTION`. If the source contract is incomplete during the
Warn-first phase, continue only as a provisional run with
`CONTRACT_INCOMPLETE`.

## Evidence requirements

Run-scoped evidence must distinguish:

- `ingestion_latency = bq_loaded_at - source_capture_time`;
- `freshness = now - max(bq_loaded_at)`;
- missing capture timestamp (`NOT_APPLICABLE` with a documented limitation);
- invalid, negative, null, or SLA-breaching observations.

Never silently replace source-capture time with event time and never turn
unsupported coverage into zero-valued evidence.

If the BigQuery analysis uses Jinja-rendered SQL, also load `jinja-bigquery`
before editing or reviewing the template. Validate the rendered GoogleSQL, not
only the template source.

For downstream PPTX or report work, inventory existing run manifests,
CSV/Parquet/JSON outputs, plot registries, plots, and hashes first. Use
`reuse_only` by default, `targeted_refresh` for a named gap, and `full_refresh`
only with explicit user authorization plus SELECT-only cost preflight. Deck-only
changes never execute BigQuery queries.
