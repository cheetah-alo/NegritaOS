---
name: analytical-dashboard-architecture
description: >
  Use when designing or modifying data-backed dashboards, FastAPI/Next.js
  applications, dashboard source structure, provider boundaries, API contracts,
  or dashboard quality gates.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, backend, frontend, data_analytics]
  auto_invoke:
    - "Designing or modifying analytical dashboards"
    - "Changing dashboard backend/frontend boundaries"
    - "Changing dashboard source providers or logical contracts"
---

# Analytical Dashboard Architecture

Apply the canonical guidance in
`skills/engineering/analytical_dashboard_architecture.md` before changing a
data-backed dashboard. Resolve the project profile first; do not assume that a
BigQuery path or a Next.js path exists in every repository.

## Required checks

- Identify the source of truth, provider, dialect, access mode, and physical
  object owner.
- Keep provider routing and dialect-specific queries in backend configuration
  and query/adapter layers.
- Keep logical score, segment, chip, metric, grain, and nullability semantics
  in a stable contract module.
- Keep physical source names and v09/v10 storage details out of frontend code.
- Require API tests and documentation for contract changes.
- Preserve connected page flows and browser states for visual changes.
- Use the project's declared integration branch; ELAL defaults to `dev_ml`.
- Report exact tests, counts, coverage, E2E results, and omitted artifacts.

## ELAL reference mapping

When the active project is `elal_journey_dashboard`, use the concrete paths in
`skills/engineering/analytical_dashboard_architecture.md` and the project
registry. For other projects, map responsibilities to their actual runtime
entrypoints and record the mapping rather than copying ELAL names.
