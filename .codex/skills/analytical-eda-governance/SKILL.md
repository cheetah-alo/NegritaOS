---
name: analytical-eda-governance
description: >
  Govern new or migrated exploratory analyses with thin entrypoints, reusable
  logic boundaries, SQL/config manifests, immutable hashed runs, aggregate
  contracts, blocked-state semantics, and visual evidence review.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, data_analytics]
  auto_invoke: true
---

# Analytical EDA Governance

Read and apply `skills/engineering/analytical_eda_governance.md` after resolving
the active project profile. Apply it to new or migrated analyses only; do not
rewrite historical packages merely to satisfy the layout.

## First checks

1. Resolve project registry, `skill_profiles`, `mode_map`, agent, and active
   rules.
2. Identify the analysis package, source contract, orchestration manifest, and
   plot/config manifest.
3. Confirm grain, denominator, source coverage, output status vocabulary, and
   run directory before interpreting results.

Use provider-specific source skills, such as
`bigquery-analysis-governance`, when the selected source requires them.
