# EDA Reports Agent

Use this subagent for EDA execution, interactive analytics workflows, chart generation, deterministic output handling, plot evidence contracts, and visual QA before reporting.

## Primary paths (this repo)

### Entry points
- `data_analytics/notebook/*.py`
- `data_analytics/notebook/*.ipynb`
- `data_analytics/pipeline/main.py`

### Core library
- `backend/app/analytics/charts.py`
- `backend/app/services/frontend_kpis.py`
- `backend/app/services/financial_kpis.py`
- `backend/app/services/cashflow_kpis.py`

### Outputs
- `data_analytics/output/**`
- `output/**`

## Required review focus
- Confirm population, denominator, KPI windows, support threshold, and category semantics.
- Maintain plot artifact lineage through a manifest, registry, or report table.
- Review rendered plots/contact sheets before using plots in decks or executive summaries.
- Flag `not processed` versus `processed no signal` as separate evidence states when extraction layers exist.
