---
name: dashboard-architecture
description: >
  Enforces maintainable modular dashboard architecture.
  Trigger: creating or modifying dashboards, dashboard HTML, BI-style pages,
  chart-heavy report UIs, or dashboard generation scripts.
license: Apache-2.0
metadata:
  author: local
  version: "1.0"
  scope: [root, frontend]
  auto_invoke:
    - "Creating or modifying dashboards"
    - "Creating static dashboard HTML or chart-heavy report UI"
    - "Changing dashboard generation scripts or dashboard templates"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Dashboard Architecture

## Core Rule

Dashboard source code must be maintainable, modular, documented, and testable.
A single huge `.html` file with inline CSS, JavaScript, data, and thousands of
lines is not an acceptable final implementation for Codex, Claude, or any
NegritaOS adapter.

## Non-Negotiables

- ALWAYS split dashboard source by responsibility: data loading, normalization,
  state, filters, layout, visual components, chart adapters, styles, and export
  or build code.
- ALWAYS keep the source of truth in modules/templates under the work root
  (`src/`, `dashboard/`, `components/`, `lib/`, `styles/`, `templates/`, or the
  repo's established equivalent).
- ALWAYS document the dashboard entrypoint, build/run command, data sources,
  expected schema, and validation steps in a README or runbook.
- NEVER create or accept a final dashboard implemented as one monolithic source
  `.html` file with inline CSS/JS/data and thousands of lines.
- NEVER let a generated HTML artifact become the editable source of truth.
- NEVER mix business KPI formulas into UI rendering when a backend, SQL, or
  data-contract layer is the canonical authority.

## Static Dashboard Exception

A static dashboard may produce one bundled `.html` file only when all of these
conditions are true:

- The bundled HTML is generated output under `dist/`, `build/`, `outputs/`, or
  another repo-approved artifact directory.
- The tracked source remains modular and documented.
- The generation command is documented and reproducible.
- The artifact is clearly marked as generated and is not edited by hand.

## Required Shape

Use the repo's established stack first. If no pattern exists, prefer this
baseline:

```text
dashboard/
├── README.md
├── src/
│   ├── data/
│   ├── components/
│   ├── charts/
│   ├── state/
│   ├── styles/
│   └── main.*
├── tests/
└── build or dist/
```

For analysis repos, `analyses/<analysis_id>/<dashboard_name>/` can replace the
top-level `dashboard/` folder, but the same modular split applies.

## Review Checklist

- Source files are cohesive and below repo file-size gates.
- Data contracts and required fields are explicit.
- UI components do not own data cleansing, enrichment, or business rules.
- Charts have isolated configuration and readable labels.
- Filters/state are testable without rendering the whole dashboard.
- README/runbook explains how to rebuild the dashboard from source.
- Generated HTML, screenshots, and exported documents are separated from source.

## If Asked For One HTML File

If the user asks for a dashboard as a single HTML file:

1. Treat it as a prototype or generated artifact request, not a final source
   architecture.
2. Create modular source first when modifying a repo.
3. Generate the single HTML only from that modular source if needed.
4. State clearly that hand-editing the generated HTML is not allowed.
