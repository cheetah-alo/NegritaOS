---
id: notebooks
domain: governance
enforcement: strict
depends_on:
  - ai-behavior
  - coding-standards
  - naming-guidelines
  - logging
  - error-handling
provides:
  - notebook-governance
description: >
  Governance rules for notebooks, including allowed usage and refactoring requirements.
version: 1.0.0
applyTo: [notebooks, jupyter, governance, eda]
priority: critical
---

# Notebook Governance Rules
## Scope
These rules apply to all Jupyter notebooks in the repository.

## Allowed
- Exploratory Data Analysis (EDA)
- Data profiling and visualization
- Feature prototyping
- Hypothesis testing
- Debugging
- `print()` and `display()` for exploratory visibility in notebook cells

## Forbidden
- Production feature engineering
- Training pipelines
- Model evaluation logic
- Data ingestion logic
- Hardcoded configuration

## Refactoring Rule
Any logic validated in a notebook must be:
1. Extracted into repository production modules such as `backend/app/`, `data_analytics/pipeline/`, or `mcp_server/` as appropriate
2. Parameterized
3. Logged
4. Covered by unit tests

## Reproducibility
- Notebooks must run top-to-bottom
- No hidden state
- No manual execution dependencies

## Interactive Exec Scripts (Notebook-Driven)
- `# %%` Python exec scripts used from the Interactive Window are allowed for EDA and reporting workflows.
- `print()` and `display()` are allowed in these interactive scripts for exploration/debugging output.
- Run selection must be deterministic: use explicit `HOT_TSR_RUN_DIR` or a fixed default run path in code; avoid auto-picking "latest run" at runtime.
- Plot outputs must be persisted as both HTML and PNG for traceability.
- Plots must render in Interactive Window when not headless.
- Any reusable transformation or aggregation logic must still be extracted to repository production modules, parameterized, logged, and covered by tests.

## Production Boundary
- Any code moved from notebooks/interactive scripts into production modules must remove `print()`/`display()` and use structured logging.
