# Analytical Dashboard Architecture

## Purpose

Use this skill before designing or changing a data-backed dashboard. It defines
stable ownership boundaries without coupling the dashboard to BigQuery,
PostgreSQL, or a particular frontend framework.

## Vocabulary

- **Data source**: the governed system that supplies data.
- **Source adapter**: provider-specific connection, routing, and query code.
- **Physical storage object**: table, relation, dataset, schema, view, or file.
- **Provider dialect**: SQL or API syntax used by a source adapter.
- **Logical data contract**: stable payload fields exposed to consumers.
- **Source of truth**: the governed data layer for the project, not the UI.

## Non-negotiable boundaries

| Responsibility | Owner | Must not own |
|---|---|---|
| Provider, environment, and physical object references | backend config | UI state or rendered markup |
| Dialect-specific SQL and domain queries | backend query/adapter layer | route parsing or React components |
| Score, segment, chip, and metric semantics | logical contract module | physical table names |
| Routes and parameter validation | FastAPI route boundary | SQL construction and source routing |
| Pages, filters, and state orchestration | frontend app/page layer | source names or business SQL |
| Reusable controls and visual components | frontend component layer | data loading policy |
| API helpers, URL builders, formatting | frontend library layer | provider credentials or SQL |
| Runbooks, inventories, contracts, changelog | `docs/` | undocumented tribal knowledge |
| Regression, contract, integration, and browser checks | backend/frontend tests | manual-only signoff |

## FastAPI + Next.js profile

For the ELAL dashboard, use these concrete owners:

- `backend/app/config.py` owns provider selection, environment overrides, and
  physical table or relation references.
- `backend/app/queries/**` owns SQL and domain query logic.
- `backend/app/queries/attention_schema.py` owns the stable score, segment, and
  chip contract.
- `backend/app/main.py` owns routes and parameter validation.
- `frontend/src/app/**` owns pages, filters, and state orchestration.
- `frontend/src/components/**` owns reusable UI.
- `frontend/src/lib/**` owns API helpers, URL builders, and formatting.
- `docs/**` owns API contracts, table/source inventory, changelog, and runbooks.
- `tests/**` and frontend tests are release gates.

If a project uses another framework, map the same responsibilities to its
actual entrypoints and record that mapping in the project registry.

## Provider flexibility

- The frontend never references physical tables, datasets, schemas, `_p`
  tables, provider credentials, or v09/v10 storage columns.
- BigQuery and PostgreSQL routing stays in backend configuration and source
  adapters. Swapping providers must not change the logical API payload.
- Provider-specific optimizations remain behind the adapter boundary and are
  documented as implementation details.
- A project must declare provider, dialect, source-of-truth mode, and access
  mode. Read-only projects must enforce parameterized reads and no write path.

## Delivery gates

- API changes include success, validation-error, and regression tests plus docs.
- Visual changes preserve connected page flows, loading states, empty states,
  error states, and URL/filter behavior.
- PRs target the declared integration branch. `dev_ml` is the ELAL default;
  any other base requires an explicit project override.
- PR evidence reports exact commands, test counts, coverage, and E2E results.
- Never commit coverage, tmp, output, screenshots, local credentials, or other
  generated artifacts unless the project explicitly promotes them.

## Required architecture output

Return the repository purpose, workflow map, boundary table, dependency
direction, source-of-truth policy, provider profile, test layers, documentation
surfaces, quality score, blockers, first three implementation steps, and exact
validation commands.
