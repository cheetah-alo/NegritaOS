---
name: frontend-web
description: >
  Generic frontend patterns for component layout, state, and UI structure.
  Trigger: When building UI components, pages, or shared UI utilities.
license: Apache-2.0
metadata:
  author: generic
  version: "1.0"
  scope: [root, frontend]
  auto_invoke: "Creating/modifying frontend UI components"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Core Rules

- ALWAYS: Keep components small and composable.
- ALWAYS: Co-locate feature-only code; share only if used in 2+ places.
- NEVER: Mix data fetching with presentation if it bloats components.
- NEVER: Ship a dashboard as one monolithic source `.html` file with inline
  CSS, JavaScript, data, and thousands of lines.

## Dashboard Rules

- ALWAYS invoke `dashboard-architecture` before creating or modifying
  dashboards, static dashboard HTML, BI-style pages, chart-heavy report UIs, or
  dashboard generation scripts.
- Dashboard source must separate data loading, normalization, state, filters,
  layout, visual components, chart adapters, styles, and build/export code.
- A bundled static HTML dashboard is allowed only as generated output under
  `dist/`, `build/`, `outputs/`, or the repo-approved artifact directory. It
  must not be the editable source of truth.
- Codex, Claude, and other NegritaOS adapters must not accept a single huge
  dashboard HTML file as the final maintainable implementation.
- Each dashboard must document its entrypoint, build/run command, data sources,
  expected schema, and validation steps.

## Suggested Structure

```
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── lib/
│   └── styles/
```

## State

- Prefer local state first; lift only when needed.
- Use a store only for cross-feature state.
