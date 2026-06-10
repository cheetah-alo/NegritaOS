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
version: 1.1.0
priority: critical
see_also: skills/dev-logging/SKILL.md
---

# Logging Rules

For full governance JSON spec and PhaseLogger details see `dev-logging` skill.

## Central configuration

- Import: `from data_analytics.configs.logs.logger import get_logger`
- Per-module: `logger = logging.getLogger(__name__)`
- Never redefine handlers or call `logging.basicConfig` in modules.
- Never use `print()` in production code.

## Phase logging

Wrap every critical segment: `with PhaseLogger("PHASE_NAME", logger): ...`

Phases by domain:
- Data engineering: `DATA_EXTRACTION`, `DATA_VALIDATION`, `DATA_CLEANING`, `FEATURE_GENERATION`, `SCHEMA_VALIDATION`, `DATA_EXPORT`
- ML: `LOAD_DATA`, `TRAIN_TEST_SPLIT`, `FEATURE_ENGINEERING`, `MODEL_TRAINING`, `MODEL_VALIDATION`, `MODEL_EVALUATION`, `MODEL_EXPORT`
- AutoML: `AUTO_ML_SEARCH`, `AUTO_ML_TRIAL`, `AUTO_ML_EVALUATION`
- Governance: `LEAKAGE_AUDIT`, `MODEL_RISK_EVAL`, `DRIFT_DETECTION`, `GOVERNANCE_CHECKS`

## Mandatory events

- Dataset: shape, missing rate mean, duplicate rate, target rate train/test.
- Features: count generated, count removed (leakage), top SHAP scores.
- Training: model ID, parameters, metrics.
- AutoML: trial number, score, duration.
- Governance: GDPR_READY flag, leakage risk score, bias flag.

## Governance JSON

- Output: `audit/governance/<timestamp>_governance.json`
- Required sections: `experiment_metadata`, `model_metadata`, `data_audit`, `framework_parameters`, `hyperparameters`, `validation_strategy`, `metrics`, `segmentation`, `governance_flags`, `leakage_audit`, `risk_assessment`, `artifacts`.
- Data engineering writes separately to `audit/data/<timestamp>_data_audit.json`.

## Log storage layout

```
audit/logs/YYYY-MM-DD/pipeline.log
audit/governance/<timestamp>_governance.json
audit/data/<timestamp>_data_audit.json
audit/drift/<timestamp>_drift.json
audit/shap/<timestamp>_shap.json
```

## Changelog
v1.0.3 → v1.1.0: Compressed. Full spec moved to `skills/dev-logging/SKILL.md`.
