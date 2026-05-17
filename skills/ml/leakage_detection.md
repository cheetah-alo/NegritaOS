# Skill: Leakage Detection

**Type:** Domain — ML
**Applicable agents:** model_review_agent, eda_reviewer_agent

## Purpose
Systematically identifies and classifies target leakage and data leakage risks in
ML pipelines. Leakage is a silent model failure: metrics appear good in validation
but the model fails in production because it trained on unavailable information.

## Leakage Types

### Type 1: Target Leakage
Feature derived from or causally following the target event.
- Example: `churn_flag_30d` as a feature when target is `churn_flag_30d`
- Example: `final_invoice_amount` in a churn model where churn causes billing changes

### Type 2: Temporal Leakage
Feature computed at a point in time that is after the prediction timestamp.
- Example: Using monthly aggregates that include the prediction month in the training set
- Example: Rolling 7-day average that includes days after the event date

### Type 3: Pipeline Leakage
Preprocessing step sees test data before training — e.g., scaling fitted on full dataset,
or imputation strategy computed on train+test.

### Type 4: Label Leakage
Label encoding or target encoding that incorporates test set statistics.

## Detection Protocol

```
For each feature in the dataset:

1. TIMESTAMP CHECK
   When is this feature computed relative to the target event?
   [BEFORE target] → safe
   [SAME TIME as target] → conditional — investigate causality
   [AFTER target] → LEAKAGE CONFIRMED

2. DERIVATION CHECK
   Is this feature derived from the target variable or its consequences?
   [YES] → LEAKAGE CONFIRMED

3. STATISTICAL SIGNAL CHECK
   Does this feature have > 0.9 correlation with target or near-zero model importance?
   [HIGH CORRELATION] → investigate for leakage
   [NEAR-ZERO IMPORTANCE] → low signal, consider dropping but not leakage per se

4. PIPELINE CHECK
   Is any preprocessing step (scaler, imputer, encoder) fit on full dataset?
   [YES] → PIPELINE LEAKAGE — refit on training fold only
```

## Output Format

```
LEAKAGE ASSESSMENT
─────────────────
Confirmed Leakage:
  - feature_name: [type] — [reason] — BLOCK DEPLOYMENT

Suspected Leakage:
  - feature_name: [type] — [reason] — INVESTIGATE BEFORE DEPLOYMENT

Clean:
  - [N] features reviewed, no leakage detected

Pipeline:
  - [preprocessing step]: [status]
```
