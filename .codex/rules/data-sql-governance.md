---
id: data-sql-governance
domain: data-engineering
enforcement: strict
applyTo: [sql, bigquery, pipelines]
depends_on:
  - data-contracts
  - naming-guidelines
  - logging
provides:
  - sql-governance-rules
  - bigquery-style-guide
description: >
  Governance, style, and reproducibility standards for BigQuery SQL pipelines
  used in telecom churn modeling. Ensures deterministic transformations,
  contract alignment, and maintainable feature-engineering workflows.
version: 1.0.0
priority: critical
---

#  **Data SQL Gov `data-sql-governance.instructions.md`**



# SQL Governance for BigQuery Pipelines

SQL is a first-class citizen in the ML-as-code platform.  
These rules ensure that SQL transformations remain **deterministic, governed, auditable, and aligned with dataset contracts**.

---

## 1. Style and Structure

### 1.1 CTE Layering Standard

Every pipeline must use layered CTEs with explicit prefixes:

- `raw_` — ingestion of upstream tables or API extracts  
- `clean_` — deduplication, normalization, tagging, rule fixes  
- `feat_` or `agg_` — windowed aggregations and feature engineering  
- `final_` — strictly ordered output aligned with the dataset contract  

### 1.2 Naming & Readability

- Use explicit aliases with `AS`.
- Never use `SELECT *` in any `final_` CTE or materialized output.
- Column names **must match the dataset contract** exactly.
- Prefer long, descriptive aliases over cryptic ones.

### 1.3 SQL Style

- Capitalize reserved keywords (`SELECT`, `FROM`, `JOIN`, `WHERE`).
- One expression per line.
- Joins must always specify the join key explicitly.

---

## 2. Determinism and Reproducibility

- Time filters **must** come from tenant configuration or pipeline configuration.
- Never use nondeterministic functions such as `RAND()` or `GENERATE_UUID()` unless documented and intentional.
- Use `SAFE_` operations to prevent silent failures:
  - `SAFE_DIVIDE`
  - `SAFE_CAST`
  - `SAFE_OFFSET`

### 2.1 Avoiding Hidden Errors
- Avoid implicit type coercions.
- Fail fast when schema mismatches occur.
- Derivations must be stable across re-runs.

---

## 3. Validation & Assertions (SQL-Level Data Quality)

Pipelines should include optional validation CTEs or separate monitoring queries for:

- **Row count expectations**  
  (e.g., number of records must fall within expected ranges)
- **Date range checks**  
  (no future timestamps, no invalid gaps)
- **Uniqueness checks**  
  on primary keys defined in the contract
- **Null checks**  
  for required columns

Validation failures must propagate to:

- logging  
- alerting systems  
- model governance metadata (data audit block)

---

## 4. Performance Rules

- Always partition and cluster tables based on contract definitions.
- Avoid unbounded scans (`_TABLE_SUFFIX`, missing filters).
- Avoid unnecessary `CROSS JOIN`s.
- Use incremental build patterns where possible:
  - `INSERT INTO`
  - windowed recomputation
  - partition-based overwrite

### 4.1 Cost Awareness

- Prefer aggregated sources over raw logs where possible.
- Document large scans in code comments.
- Use BigQuery `EXPLAIN` to validate performance before deploying.

---

## 5. Learnings

```markdown
## Learnings
* Use layered CTE stages (`raw_`, `clean_`, `agg_`, `final_`) to keep SQL pipelines understandable, maintainable, and testable. (1)
* Explicitly match final SELECT columns to contract definitions to prevent schema drift and ensure reproducibility. (1)
