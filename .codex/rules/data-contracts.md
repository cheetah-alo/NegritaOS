---
id: data-contracts
domain: data-governance
enforcement: strict
depends_on:
  - naming-guidelines
  - data-validation
  - logging
provides:
  - dataset-contract-rules
  - schema-governance
  - versioning-standards
description: >
  Defines how dataset contracts are authored, versioned, validated, and enforced
  across SQL, Python, and AutoML pipelines for telecom churn modeling.
version: 1.1.0
applyTo: [data, contracts, schema, pipelines, sql, python]
priority: critical
---

#  **Normalized File: `data-contracts.instructions.md`**


# Data Contracts for Telecom Churn Models

Dataset contracts define the **canonical schema** of every dataset consumed or produced
by churn models—regardless of whether features are built in SQL, Python, or AutoML.

Contracts ensure **traceability, governance, interoperability**, and **schema evolution safety**
across tenants and pipelines.

Contracts live under:

- `configs/contracts/*.json` (e.g., `calls_hourly_v1.json`)
- optional tenant overrides: `configs/tenants/<tenant>/`

They must describe:

- `name` — dataset identifier  
- `version` — semantic version (`MAJOR.MINOR.PATCH`)  
- `primary_key` — unique column set  
- `partitions` — partitioning metadata  
- `required` — mandatory columns  
- `properties` — JSON Schema–compatible column definitions  
- `rules` — expectations/validations  
- `deprecations` — removed or discouraged fields  

---

## 1. Contract Authoring Rules

1. Every dataset consumed by ML or analytics **must** have a JSON contract file.
2. Contracts must follow **JSON Schema draft-2020–12 style**.
3. Column names in contracts define the **single source of truth** for:
   - BigQuery SQL transformations  
   - Python feature engineering  
   - AutoML feature inputs  
4. Each `properties.<column>` entry must include at minimum:
   - `type` (`string`, `integer`, `number`, `boolean`)
   - optional constraints: `minimum`, `maximum`, `enum`, `format`
   - a business-level `description`

**Example:**

```json
"xgb_propensity": {
  "type": "number",
  "minimum": 0.0,
  "maximum": 1.0,
  "description": "Propensity score from the baseline XGBoost churn model."
}
````

---

## 2. Versioning Rules

Semantic versioning applies:

### **MAJOR**

Breaking changes:

* removing columns
* renaming columns
* changing column type or meaning

### **MINOR**

Non-breaking enhancements:

* adding optional columns
* adding new rules
* extending metadata

### **PATCH**

Documentation or constraint refinements:

* clarifying descriptions
* tightening numeric bounds where historical data remains valid

Model governance must record:

* exact contract version
* model version compatible with this schema
* any schema deviation detected

---

## 3. Usage in Code

### Python

A contract loader (e.g., `DatasetContract` in `data/domain/contract.py`) must:

* load JSON contracts
* validate required fields
* expose schema metadata to pipelines

Validation utilities must:

* check all required columns exist
* optionally validate column types
* check rules if enabled (`data-validation.instructions.md`)

### BigQuery / SQL

Pipelines must enforce schema compliance:

* explicit type casts
* ensure partition columns exist
* guarantee the primary key is unique

### AutoML

AutoML data ingestion must respect:

* required columns
* types
* target definitions

---

## 4. Strict vs. Flexible Schema Enforcement

### Strict (non-negotiable)

* primary key definitions
* required columns
* data types for required columns

### Flexible (allowed)

* extra columns may be present in source tables
* new columns may be introduced under `MINOR` version increments
* rules may be gradually tightened

---

## 5. Governance Integration

Each model training run must persist to governance metadata:

* dataset contract name + version
* list of features actually used
* any contract deviations (missing/dropped columns, type mismatches)

These are stored under:

```
governance_json["data_audit"]
```

Deviations must also trigger **logging warnings or errors** depending on severity.

---

## 6. Learnings

## Learnings
* Validate dataset schema against the contract before any feature engineering to detect drift early. (1)
* Use semantic versioning to clearly track breaking vs. non-breaking schema changes. (1)


