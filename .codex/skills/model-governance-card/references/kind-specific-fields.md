# Kind-Specific Fields

## ML Predictive

Require target definition, prediction horizon, feature cutoff, algorithm,
feature count, hyperparameter/config reference, split strategy, entity/time
isolation, imbalance treatment, baseline, threshold selection, calibration,
leakage assessment, train/validation/holdout metrics, explainability method,
runtime interface, monitoring, retraining, and rollback.

For overlapping temporal windows, explicitly test whether the same entity or
event can cross train/validation/test boundaries.

## Analytical Rule

Require input grain, rule catalog/version, source evidence, eligibility gates,
conditions, score/band output, thresholds, rule precedence, overlap/conflict
resolution, null/missing/default behavior, caps/floors, boosters, state or
persistence behavior, decay/reset, sensitivity variants, backtest design,
support/outcome association, operational action, monitoring, change approval,
and rollback.

Do not use predictive vocabulary unless an outcome backtest supports it. A
descriptive or operational score remains descriptive/operational.

## Hybrid

Populate both sections and document the interface between them:

- which component runs first;
- whether rules modify inputs, model score, threshold, eligibility, segment,
  or final action;
- precedence and conflict resolution;
- independent and combined validation;
- rollback behavior when either component is disabled.
