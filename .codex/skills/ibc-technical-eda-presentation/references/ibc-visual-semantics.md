# IBC Visual Semantics

## Source Layer Colors

| Layer | Color role | Guidance |
|---|---|---|
| `issues_on_subs` | base grain | cobalt |
| `ibc_asset_status_daily` | enrichment bridge | teal |
| `trap_events` | aggregated signals | violet |
| root/topology exploration | review/exploratory | amber |
| unmatched/residual | residual | slate |
| fanout/blocker | alert | coral |

## Preferred Diagrams

- Source-to-candidate-table flow for join discussions.
- Gate diagram for `PASS / REVIEW / HOLD / FAIL`.
- Sequence diagram for runner, YAML, BigQuery, evidence, and docs.
- Small matrix for source fields vs candidate ML table fields.

## Plot Guidance

- Use horizontal bars for ranked entities, recurring technical groups, and top
  problems.
- Use vertical bars for time buckets or compact count comparisons.
- Use heatmaps for source/category concentration and technical entity matrices.
- Use cards for bridge readiness and source-owner decision summaries.
- Use gray treatment for unknown, residual, or suppressed values.
