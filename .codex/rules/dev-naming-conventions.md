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
description: >
  Enforces strict naming rules across Python, SQL, ML pipelines, feature engineering,
  and configuration files for telecom churn prediction systems. Ensures minimum length,
  legible semantic units, domain alignment, and centralized constants management.
version: 1.0.2
priority: critical
---

#  **Naming Guidelines `naming-conventions.instructions.md`**



# Naming Conventions (Strict Version — Telecom Churn Domain)

This document defines **mandatory naming rules** for all churn-model code:

- ML training pipelines  
- AutoML search and evaluation  
- feature engineering pipelines  
- data prep and ETL  
- SQL pipelines and BigQuery materializations  
- test suites  
- configuration files  

Names MUST be explicit, descriptive, and aligned with **telecommunications churn semantics**  
(customers, contracts, usage, billing, devices, service events, retention behavior).

---

# 1. General Naming Principles

1. **Names MUST reveal intent.**  
   Code should be understandable without reading internal logic.

2. **Names MUST be ≥ 3 characters AND form real, legible English words.**  
   NOT enough to simply be long — they must be meaningful.

3. Follow PEP8 + Ruff naming rules:  
   - `snake_case` → variables, functions, parameters  
   - `UPPER_SNAKE_CASE` → constants  
   - `PascalCase` → classes  
   - lowercase file names  

4. **ALL constants MUST be centralized** under:

```python
config/constants.py
config/<module>_constants.py
config/domains/churn_constants.py

```

5. Telco churn domain concepts MUST be used consistently.

Examples of valid domain terms:
- customer  
- contract_type  
- monthly_charge  
- tenure_months  
- device_count  
- call_minutes  
- data_usage_gb  
- churn_probability  

---

# 2. LEGIBLE WORD RULE (MANDATORY)

A variable or constant name MUST be a **legible word**, defined as:

###  1. A real, readable, pronounceable semantic unit  
If you cannot **say it aloud**, it is not allowed.

> `cus`, `cfg`, `prm`, `tmp` →   
> `customer`, `config_data`, `parameter_value`, `temporary_flag` → 

---

###  2. Abbreviations are banned **unless universally recognized**
Allowed:  
- API, URL  
- CPU, GPU  
- ML, NLP  
- KPI  
- ARPU (telecom standard)  
- QoS, VoIP, SMS, MMS  
- DF, DS (dataframe, dataset)  
- CFG (configuration)  
- EDA, SHAP, BQ (domain tooling acronyms)  

Not allowed:  
- `cl`, `cs`, `uxg`, `tmp`, `var1`, `df1`

---

###  3. Minimum length ≥ 3 characters is required but NOT sufficient  
Names must carry **meaning**, not just length.

> `cfg` →   
> `config_settings` → 

---

###  4. Must reflect **telecom churn intent**
:
- `customer_tenure_months`
- `billing_cycle_date`
- `monthly_charge_amount`
- `internet_usage_gb`
- `churn_label`
- `churn_probability`
- `contract_type`

:
- `ten`  
- `chg`  
- `usr`  
- `df`  
- `tmp_var`  

---

# 3. CONSTANTS

## Mandatory constant rules:

- Stored only in `config/`
- Use `UPPER_SNAKE_CASE`
- Type-annotated  
- Reflect telecommunication churn concepts

###  Good:
```python
MIN_TENURE_MONTHS: Final[int] = 1
MAX_DEVICE_COUNT: Final[int] = 10
DEFAULT_CONTRACT_TYPE: Final[str] = "Month-to-Month"
HIGH_CHURN_THRESHOLD: Final[float] = 0.75
TELECOM_TAX_RATE: Final[float] = 0.21
````

###  Bad:

```python
MN: Final[int] = 1       # not descriptive
DCT: Final[int] = 10     # abbreviation
CTR: Final[str] = "MTM"  # low clarity
```

---

# 4. VARIABLES

Names MUST follow:

* snake_case
* ≥3 characters
* legible semantic units
* telecom churn semantics

 Good:

```python
customer_id
monthly_charge
internet_usage_gb
contract_length_months
churn_probability
billing_method
```

 Bad:

```python
cid
mnt
gb
clm
prob
```

---

# 5. DATAFRAME & DATASET RULES

DataFrame variables SHOULD use suffix:

* `_df` → pandas DataFrame
* `_tbl` → table-like structure
* `_ds` → dataset loader or wrapper

Exceptions (allowed when scope is limited and intent is clear):

* `df` for short-lived local DataFrames inside a function
* `cfg` for configuration payloads (prefer `*_cfg` in larger scopes)

:

```python
customer_features_df
billing_history_df
usage_statistics_tbl
train_ds
test_ds
```

:

```python
raw
data1
tbl
```

---

# 6. FUNCTION NAMES

Functions MUST:

* use `snake_case`
* contain a verb
* express domain-specific behavior
* follow legible word rule

:

```python
calculate_churn_probability()
prepare_customer_features()
load_telecom_dataset()
generate_churn_report()
encode_contract_features()
compute_usage_patterns()
transform_billing_history()
```

:

```python
calc_churn()
prep_data()
encode()
run()
```

---

# 7. CLASS NAMES

Class names MUST:

* use PascalCase
* reflect a **telecom churn modeling role**
* follow the legible word rule

:

```python
ChurnPredictor
CustomerFeatureEngineer
BillingPreprocessor
UsagePatternExtractor
AutoMLChurnPipeline
CustomerSegmentationModel
```

:

```python
CP
FE
BPP
AP
CSM
```

---

# 8. MODULE & FILE NAMES

Files MUST:

* be lowercase
* represent telecom churn context
* be descriptive
* be ≥3 characters

:

```
churn_predictor.py
customer_features.py
billing_preprocessing.py
usage_pattern_extractor.py
autogluon_churn_pipeline.py
flaml_churn_search.py
```

:

```
cp.py
bp.py
prep.py
clf.py
exp.py
```

---

# 9. CONFIG DIRECTORY RULES

All constants related to telecom churn MUST be placed in:

* `config/constants.py`
* `config/churn_constants.py`
* `config/<module>_constants.py`

These include:

* churn thresholds
* telecom product categories
* payment methods
* feature engineering rules
* dataset schema
* normalization constants

Never declare constants inline in business logic.

---

# 10. RUFF ENFORCEMENT

All naming must satisfy Ruff rules:

* **E741** — ambiguous variable names prohibited
* **N801–N807** — naming conventions
* **PLR1703** — minimum name clarity
* **PLR1702** — avoid confusing reuse
* **C901** — discourage complex functions (often caused by poor naming)

---

# 11. TEST VARIABLE NAMING

Test variables MUST also follow naming rules.

:

```python
mock_customer
fake_billing_record
sample_usage_row
expected_churn_score
```

:

```python
cu1
blg
rec
exp
res
```

---

# 12. LEARNINGS

```
## Learnings
* Always use descriptive, domain-aligned variable names ≥3 characters for telecom churn workflows. (2)
* Variable names must be real, legible semantic units—not abbreviations—so ML and feature pipelines remain readable. (2)
* All Telecom churn constants must live under config/ and follow clear domain naming conventions. (1)

## Changelog
v1.0.2 — Added approved acronyms and clarified DataFrame/config naming exceptions.
```

---

# Summary

This naming system ensures:

* clarity
* telecom churn domain alignment
* PEP8 + Ruff consistency
* enhanced readability in ML & AutoML pipelines
* no ambiguous or cryptic identifiers
* reproducibility and maintainability

A name must always express **what the value represents in the context of telco churn prediction**.
