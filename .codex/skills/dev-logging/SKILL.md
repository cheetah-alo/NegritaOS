---
name: dev-logging
description: >
  Unified logging standard for Python ML pipelines, AutoML, ETL, and analytics.
  Trigger: When instrumenting code with logging, adding PhaseLogger, or writing
  governance JSON artifacts.
license: Apache-2.0
metadata:
  author: local
  version: "1.0"
  scope: [backend, data_analytics, mcp_server]
  auto_invoke: "Adding logging or governance JSON to ML or analytics code"
allowed-tools: Read, Edit, Write, Glob, Grep
---

## Core Rules

- ALWAYS: Use `from data_analytics.configs.logs.logger import get_logger`; never redefine handlers.
- ALWAYS: Per-module logger: `logger = logging.getLogger(__name__)`.
- NEVER: Use `print()` in production code; use `logger.info/warning/error`.
- NEVER: Log secrets, raw PII, or connection strings.

## Phase Logging

Wrap every critical pipeline segment with `PhaseLogger`:

```python
with PhaseLogger("PHASE_NAME", logger):
    ...
```

**Phase names by domain:**

Data Engineering: `DATA_EXTRACTION`, `DATA_VALIDATION`, `DATA_CLEANING`, `FEATURE_GENERATION`, `SCHEMA_VALIDATION`, `DATA_EXPORT`

ML Training: `LOAD_DATA`, `TRAIN_TEST_SPLIT`, `FEATURE_ENGINEERING`, `MODEL_TRAINING`, `MODEL_VALIDATION`, `MODEL_EVALUATION`, `MODEL_EXPORT`

AutoML: `AUTO_ML_SEARCH`, `AUTO_ML_TRIAL`, `AUTO_ML_EVALUATION`

Governance: `LEAKAGE_AUDIT`, `MODEL_RISK_EVAL`, `DRIFT_DETECTION`, `GOVERNANCE_CHECKS`

Each phase must emit `[PHASE START]`, `[PHASE END] + elapsed`, and `[PHASE FAILED]` on exception.

## Mandatory Log Events

Dataset: shape, missing rate mean, duplicate rate, target rate train/test.  
Features: count generated, count removed (leakage), top SHAP scores.  
Training: model ID, parameters, metrics.  
AutoML: trial number, score, duration.  
Governance: GDPR_READY flag, leakage risk score, bias flag.

## Governance JSON (mandatory for all ML and AutoML)

Output to `audit/governance/<timestamp>_governance.json`.

Required sections: `experiment_metadata`, `model_metadata`, `data_audit`, `framework_parameters`, `hyperparameters`, `validation_strategy`, `metrics`, `segmentation`, `governance_flags`, `leakage_audit`, `risk_assessment`, `artifacts`.

Data engineering pipelines write separately to `audit/data/<timestamp>_data_audit.json`.

## Log Storage Layout

```
audit/
  logs/YYYY-MM-DD/pipeline.log
  governance/<timestamp>_governance.json
  data/<timestamp>_data_audit.json
  drift/<timestamp>_drift.json
  shap/<timestamp>_shap.json
```
