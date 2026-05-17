---
id: logging
domain: dev
enforcement: strict
applyTo: python, ml, automl, pipelines, analytics, etl, governance
depends_on:
  - coding-standards
provides:
  - logging-format
  - phase-logging
  - observability-hooks
description: >
  Unified logging, pipeline-phase tracking, structured governance metadata, and audit
  instrumentation across ML, AutoML, ETL, and analytics pipelines for telecom churn models.
version: 1.0.2
priority: critical
---

#  **Logging Governance `logging-governance.instructions.md`**


# Unified Logging & Governance Standard

This document defines the **mandatory logging and governance practices** for all
pipelines in the ML-as-code platform:

- ML training pipelines  
- AutoML search and evaluation  
- Feature engineering  
- Data engineering and analytics  
- Telecom churn prediction workflows  
- Validation, drift detection, leakage audits  
- Batch and streaming pipelines  

All pipelines must emit:

1. **Structured console logs**
2. **Phase logs** via `PhaseLogger`
3. **Governance JSON artifacts** (mandatory)

Logging must be:

- structured  
- auditable  
- reproducible  
- timestamped  
- tenant-aware  
- model-aware  
- consistent across all agents and pipelines  

---

# 1. Central Logging Configuration (MANDATORY)

All pipelines must use:

```
from data_analytics.configs.logs.logger import get_logger
```

Setup:

- Controlled through `logging.config.dictConfig`
- Includes timestamps, module, file, line number
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- No module may redefine logging

Every module must create loggers as:

```python
import logging
logger = logging.getLogger(__name__)
````

Central configuration lives in `data_analytics.configs.logs.logger` and is the
single source of truth for handlers and formatting.

---

# 2. Phase Logging (MANDATORY)

All critical pipeline segments — **across ML, AutoML, ETL, and Data Analytics** — must be wrapped with:

```python
with PhaseLogger("PHASE_NAME", logger):
    ...
```

Full phase list:

###  Data Engineering & Analytics

* DATA_EXTRACTION
* DATA_VALIDATION
* DATA_CLEANING
* FEATURE_GENERATION
* FEATURE_AGGREGATION
* SCHEMA_VALIDATION
* DATA_EXPORT

###  ML / Feature Engineering

* LOAD_DATA
* TRAIN_TEST_SPLIT
* FEATURE_ENGINEERING
* FEATURE_SELECTION
* LABEL_ENGINEERING

###  ML Training

* MODEL_TRAINING
* MODEL_VALIDATION
* MODEL_EVALUATION
* MODEL_EXPORT

###  AutoML

* AUTO_ML_SEARCH
* AUTO_ML_TRIAL
* AUTO_ML_EVALUATION

###  Governance

* LEAKAGE_AUDIT
* MODEL_RISK_EVAL
* DRIFT_DETECTION
* GOVERNANCE_CHECKS

Every phase logs:

* `[PHASE START]`
* `[PHASE END] + elapsed time`
* `[PHASE FAILED]` on exceptions

---

# 3. Structured Logging Requirements

Every log entry must contain:

* timestamp
* log level
* logger name
* file + line number
* message

### **Mandatory logging events**

#### Dataset-level

```
logger.info("Dataset shape: %s", df.shape)
logger.info("Missing rate mean: %.4f", missing_mean)
logger.info("Duplicate rate: %.4f", duplicate_rate)
logger.info("Target rate train/test: %s", rate_dict)
```

#### Feature engineering

```
logger.info("Generated %d new variables", len(new_features))
logger.debug("Feature list: %s", feature_names)
logger.info("Removed %d features due to leakage risk", risky_count)
```

#### Feature audit

```
logger.info("Total input variables: %d", n_features)
logger.info("Feature SHAP top scores: %s", shap_summary)
```

#### ML training

```
logger.info("Training started for model: %s", model_id)
logger.info("Parameters: %s", params)
logger.debug("Training metrics: %s", metrics_dict)
```

#### AutoML

```
logger.info("Trial #%d — Score: %.4f (Duration: %.2fs)", trial_id, score, duration)
```

#### Governance

```
logger.info("GDPR_READY: %s", gdpr_flag)
logger.info("Leakage risk score: %.2f", leakage_risk)
logger.info("Bias detected: %s", bias_flag)
```

---

# 4. Governance JSON (MANDATORY FOR ALL ML & AUTOML)

Every ML pipeline **must** output a JSON in:

```
audit/governance/<timestamp>_governance.json
```

This JSON MUST contain the following sections:

## 4.1 Experiment Metadata

```
experiment_name
client
created_at
```

## 4.2 Model Metadata

```
model_id
version
registry_group
framework
python_version
library_version
training_start
training_end
execution_duration
environment {
    mlflow_run_id
    git_commit_hash
    docker_image
    platform
}
```

## 4.3 Data Audit

```
primary_table
source_system
query_hash
rows_raw
rows_train
rows_test
train_range
test_range
missing_rate_mean
duplicate_rate
target_rate_train
target_rate_test
```

## 4.4 Framework Parameters (for ML & AutoML)

All model or AutoML parameters must be stored.

## 4.5 Hyperparameters

ML-specific hyperparameters.

## 4.6 Validation Strategy

```
validation_strategy
validation_method
metric_primary
metric_secondary
test_window_days
model_drift_expected
```

## 4.7 Metrics

Includes:

* AUC train/test
* uplift metrics
* precision, recall (top decile & mean)
* cumulative metrics
* SHAP
* number of features
* training/test record counts

## 4.8 Segmentation (Telecom-specific)

```
segment_scope
groups_available
segment_thresholds
```

## 4.9 Governance Flags

```
gdpr_ready
iso_ready
temporal_valid
leakage_checked
```

## 4.10 Leakage Audit

```
temporal_overlap_days
risky_feature_flags
feature_risk_detected
leakage_risk_score
manifest_features
```

## 4.11 Risk Assessment

```
bias_detected
fairness_checked
explainability_score
model_risk_level
intended_use
limitations
ethical_impact
```

## 4.12 Artifacts

* predictions
* models
* plots
* feature importance
* drift reports
* AutoML artifacts

This structure is **required** for consistency.

---

# 5. Feature Engineering Logging Requirements

Every pipeline must track:

* number of raw features
* number of engineered features
* number of selected features
* list of new variables
* transformations applied
* removed or risky features
* SHAP importance
* segment-based metrics (Telecom churn)

These MUST appear in both logs and the governance JSON.

---

# 6. Data Engineering / Analytics Logging Requirements

Data engineering pipelines must log:

* source system
* query hash
* extraction timestamp
* row counts
* column counts
* missing/duplicate rates
* schema mismatch
* datatype inference
* distribution drift
* unexpected category levels
* anomalies in telecom usage (e.g., call minutes spikes)

These pipelines must also write:

```
audit/data/<timestamp>_data_audit.json
```

with:

* schema summary
* column stats
* distribution metrics

---

# 7. AutoML Logging Requirements

AutoML must log:

* search space
* number of trials
* trial start/end
* trial hyperparameters
* validation performance
* best model updates
* early stopping events
* interruptions/errors

AutoML datasets must follow the same governance JSON structure.

---

# 8. Log Storage

All logs must follow directory structure:

```
audit/
  logs/YYYY-MM-DD/pipeline.log
  governance/<timestamp>_governance.json
  data/<timestamp>_data_audit.json
  drift/<timestamp>_drift.json
  shap/<timestamp>_shap.json
```

---

# 9. Learnings

```
## Learnings
* Governance JSONs must capture complete experiment, data, feature, and model metadata. (4)
* All ML, AutoML, and Data pipelines must log phases using PhaseLogger for traceability. (3)
* Feature engineering steps must be explicitly logged and included in governance artifacts. (2)
* Data engineering must log schema, distribution, anomalies, and missing/duplicate stats. (2)
```

---

# SUMMARY

This unified logging and governance standard ensures:

* consistency
* observability
* auditability
* transparency
* compliance (GDPR, ISO)
* reproducibility
* structured logs across ML, AutoML, analytics, and ETL pipelines

Every pipeline must produce **logs + governance JSON + audit artifacts** with a predictable structure that supports governance, lineage, and model accountability.

## Changelog
v1.0.2 — Pointed central logging to `data_analytics.configs.logs.logger` and clarified dictConfig usage.
