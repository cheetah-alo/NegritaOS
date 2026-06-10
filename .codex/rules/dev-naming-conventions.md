---
id: naming-guidelines
domain: dev
enforcement: strict
applyTo: python, ml, automl, tests, pipelines, config, sql
depends_on:
  - coding-standards
provides:
  - naming-guidelines
  - feature-name-rules
version: 1.0.3
priority: critical
---

# Naming Conventions

## Core Rules

- Names MUST reveal intent and form real, legible English words.
- Names MUST be >= 3 characters AND be pronounceable.
- `snake_case` for variables/functions, `UPPER_SNAKE_CASE` for constants, `PascalCase` for classes.
- All constants MUST live in `config/constants.py` or `config/<module>_constants.py`. No inline literals.
- Abbreviations banned unless in approved list: API, URL, CPU, GPU, ML, NLP, KPI, ARPU, QoS, VoIP, SMS, MMS, DF, DS, EDA, SHAP, BQ.
- Ruff rules E741, N801-N807 must pass.

## Variables

- Must reflect telecom churn domain: `customer_id`, `monthly_charge`, `tenure_months`, `churn_probability`.
- Forbidden: `cid`, `mnt`, `tmp`, `var1`, `df1`, `k`, `cfg` (use `config_settings` in larger scopes).

## Functions

- Must contain a verb: `calculate_churn_probability()`, `load_telecom_dataset()`.
- Boolean/predicate functions MUST use prefix: `is_*`, `has_*`, `should_*`, `can_*`, `was_*`, `did_*`, or `*_flag`.
- Forbidden: `validate()`, `check()`, `run()` without domain context.

## Classes

- PascalCase reflecting a modeling role: `ChurnPredictor`, `BillingPreprocessor`, `AutoMLChurnPipeline`.

## DataFrames

- Use suffix `_df` (pandas), `_tbl` (table), `_ds` (dataset loader).
- Short-lived local DataFrames may use bare `df`.

## Constants

```python
MIN_TENURE_MONTHS: Final[int] = 1
HIGH_CHURN_THRESHOLD: Final[float] = 0.75
DEFAULT_CONTRACT_TYPE: Final[str] = "Month-to-Month"
```

## Files

- Lowercase, descriptive, >= 3 characters: `churn_predictor.py`, `billing_preprocessing.py`.

## Tests

- Variables: `mock_customer`, `sample_usage_row`, `expected_churn_score`.
- Methods: `test_<behavior>_that_<expected>_when_<condition>`.

## Changelog
v1.0.3 — Compressed. Full domain examples removed; core rules retained.
