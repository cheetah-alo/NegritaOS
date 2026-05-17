---
name: eda-reports
description: >
  EDA and reporting workflows for this repository: notebook-driven exploration,
  analytics helpers, chart generation, and deterministic output artifacts.
  Use when modifying analytics/reporting code, chart generation, notebook-backed
  workflows, or output folder conventions.
---

# EDA Reports

## Operating model

EDA in this repo is a deterministic analytics workflow:

inputs or stored state -> DataFrames / tabular processing -> explicit metrics -> charts / summaries -> persisted outputs.

This skill provides workflow and entry points. Naming, logging, testing, and notebook boundaries are enforced by rules and other skills.

## Scope

- Load or prepare analysis inputs for inspection and reporting.
- Compute explicit metrics for charts and summaries.
- Generate charts or report artifacts from deterministic helpers.
- Persist outputs in the repository-defined output locations.

## Primary modules (this repo)

### Entry points

- Interactive analytics scripts: `data_analytics/notebook/*.py`
- Notebooks: `data_analytics/notebook/*.ipynb`
- Pipeline entry point: `data_analytics/pipeline/main.py`

### Core library

- Analytics helpers: `backend/app/analytics/charts.py`
- KPI and finance services when used for reporting: `backend/app/services/frontend_kpis.py`, `backend/app/services/financial_kpis.py`, `backend/app/services/cashflow_kpis.py`

### Outputs

- `data_analytics/output/`
- `output/`

## Workflow

1. Resolve the input source and run context explicitly.
2. Load data without hiding business transforms inside the loading step.
3. Validate only the assumptions required by the report or chart.
4. Compute metrics in named, testable functions.
5. Render charts or summaries through reusable helpers.
6. Persist outputs and logs in deterministic locations.
7. Add or update `unittest` coverage for reusable logic.

## Guardrails

- Do not leave reusable reporting logic only in notebooks.
- Keep chart builders traceable and deterministic.
- Prefer reusable analytics helpers over repeated notebook cell logic.
- `print()` and `display()` are acceptable only in notebooks or `# %%` interactive scripts.
