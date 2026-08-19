# Presentation Evidence Reuse

## Purpose

Prevent analytical deck creation and repair from rerunning expensive source
queries when governed analysis artifacts already exist. Presentation work
consumes analysis evidence; it does not silently recreate the analysis.

## Refresh Modes

| Mode | Use | Query policy |
|---|---|---|
| `reuse_only` | Titles, agenda, notes, layout, readability, interpretation, plot emphasis, or deck assembly | No analytical queries |
| `targeted_refresh` | A named metric, period, plot input, or contract artifact is missing, stale, or invalid | Run only the dependency needed for that gap |
| `full_refresh` | The user explicitly requests a complete analytical refresh or a declared dependency change invalidates the full run | Requires explicit authorization and cost preflight |

`reuse_only` is the default. Missing evidence does not authorize
`full_refresh`.

## Evidence Priority

Before any query execution, inventory and validate evidence in this order:

1. `run_manifest`, `analysis_manifest`, technique manifests, and source-quality
   contracts;
2. run-scoped CSV, Parquet, JSON, XLSX, or other governed tabular extracts;
3. plot registry entries and existing rendered plots;
4. query, config, source, and output hashes;
5. a targeted query for one named evidence gap.

An artifact is reusable when its source, window, grain, denominator, query or
config hash, status, and limitations match the slide claim. A stale or
unverifiable artifact must be marked, not silently refreshed.

## Hard Rules

- Never execute queries to change wording, titles, agenda, speaker notes,
  layout, fonts, colors, card placement, highlights, or takeaway bands.
- Restyling or rebuilding a plot uses its existing validated tabular output by
  default.
- Do not rerun unrelated techniques because one slide lacks one metric.
- Do not rerun a query merely to reconfirm an unchanged value when a matching
  manifest and hash-bearing output exist.
- A targeted refresh declares the exact missing artifact, dependency, SQL,
  partition/window, expected output, and dry-run estimate before execution.
- A full refresh requires explicit user authorization, SELECT-only and bounded
  BigQuery preflight where applicable, and a reported estimated cost/bytes.
- Preserve prior immutable runs. New query output belongs to a new run-scoped
  directory and never overwrites evidence used by an existing release.

## Delivery Record

The deck delivery manifest records:

```yaml
evidence_refresh:
  mode: reuse_only
  reused_artifacts: []
  stale_or_missing_artifacts: []
  targeted_queries: []
  full_refresh_authorized: false
  authorization_reference: null
```

Report reused artifacts and executed queries separately. A deck can be
released from validated existing evidence without any query execution.
