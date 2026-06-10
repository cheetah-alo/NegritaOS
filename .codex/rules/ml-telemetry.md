# ML Telemetry Rules

- ML workflows must log dataset scope, model version, metric names, and artifact paths on every run.
- Metrics must be tied to a run identifier (MLflow run ID or equivalent); never log metrics without a run context.
- Do not log secrets, raw personal data, or credentials in any telemetry event.
- Log training start/end timestamps and wall-clock duration for every training run.
- Feature importance and SHAP summaries must be logged as artifacts, not as raw log lines.
- AutoML trials must log trial number, hyperparameters, score, and duration per trial.
- Drift detection results must be logged to `audit/drift/<timestamp>_drift.json`.
