---
id: data-validation
domain: data-governance
enforcement: strict
applyTo: [python, sql, bigquery, data-validation]
depends_on:
  - data-contracts
  - error-handling
  - logging
  - naming-guidelines
provides:
  - dataset-validation-rules
  - domain-validation-rules
  - statistical-quality-rules
description: >
  Defines structural, domain, and statistical validation rules used across SQL,
  Python, and hybrid pipelines for telecom churn modeling. Ensures datasets
  comply with schema contracts, domain logic, and governance expectations
  before entering feature engineering or model training flows.
version: 1.1.0
priority: critical
---

#  **Data Validation `data-validation.instructions.md`**



# Data Validation for Pipelines

Data validation ensures every dataset consumed by churn pipelines is:

- **structurally correct** (matches the dataset contract),
- **domain-consistent** (enums, ranges, semantics),
- **statistically healthy** (no silent data degradation),
- **aligned with governance requirements**.

Validation is mandatory **before**:

- feature engineering,
- model training,
- scoring / batch inference,
- AutoML ingestion.

Validation operates in **three layers**:

1. **Structural validation**  
2. **Domain validation**  
3. **Statistical / quality validation**

---

## 1. Structural Validation

Performed in modules such as:

- `data/domain/validation.py`
- `data/domain/contract.py`

### Structural validation rules

- Use `validate_required_columns(found_cols, required)` before any downstream processing.
- When required columns are missing:
  - Log at **ERROR** level with code: `ERR_MISSING_REQUIRED_COLUMNS`.
  - Raise a domain-specific exception: `MissingColumnError`.
  - Include context: dataset name, missing set, contract version.
- Structural validation must occur **before**:
  - SQL materializations,
  - Python feature logic,
  - AutoML ingestion,
  - training and scoring scripts.

### Outputs to governance

Record structural validation status in:

