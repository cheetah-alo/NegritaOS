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

Use the project's adapter/registry first. Repository-specific analysis paths, run folders, and output conventions override the generic paths listed below.

## Scope

- Load or prepare analysis inputs for inspection and reporting.
- Compute explicit metrics for charts and summaries.
- Generate charts or report artifacts from deterministic helpers.
- Persist outputs in the repository-defined output locations.
- Build plot manifests or registries that make generated evidence auditable.
- Convert plot sets into business findings only after visual and semantic QA.

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

## Agile EDA Plot Workflow

Use this loop for plot-heavy analyses:

1. Inventory: list generated plots, source functions, and source data files.
2. Triage: classify each plot as keep, fix, split, replace, or remove.
3. Evidence contract: define base population, denominator, support threshold, KPI windows, and category semantics.
4. Visual contract: enforce readable labels, stable palettes, no overlaps, and no more than two subplots per output.
5. Generate: create new suffixed outputs instead of overwriting legacy artifacts unless the user asked for replacement.
6. Inspect: visually review rendered outputs or contact sheets before using them in a deck/report.
7. Report: summarize common fixes, regenerated artifacts, remaining concerns, and commands/tests run.

## Minimum Plot Evidence Contract

Every business-facing plot or plot family should answer:

- What population is included and excluded?
- What is the denominator?
- What is `n` and what support threshold was used?
- What does each KPI mean and in which time window?
- Is the grouping based on flags, slots, all extracted signals, sequences, or account-level aggregation?
- Are missing/not-processed rows separated from processed rows with no detected signal?
- What overall/base reference should the audience compare against?

## Guardrails

- Do not leave reusable reporting logic only in notebooks.
- Keep chart builders traceable and deterministic.
- Prefer reusable analytics helpers over repeated notebook cell logic.
- `print()` and `display()` are acceptable only in notebooks or `# %%` interactive scripts.
- Do not manually patch generated PNG/HTML artifacts; fix the source plot function.
- Do not promote a plot into a finding if its data semantics are ambiguous.
- Do not compress many analytical questions into one dense figure; split by business question.
- Do not treat temporal association metrics as causal without a causal design.
