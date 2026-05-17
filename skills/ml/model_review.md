# Skill: ML Model Review

**Type:** Domain — ML
**Applicable agents:** model_review_agent, eda_reviewer_agent

## Purpose
Provides a systematic protocol for reviewing ML model outputs, configurations,
and experimental setups. Prioritizes leakage detection, metric interpretation,
explainability, and operational readiness over raw performance reporting.

## Review Protocol

### Step 1: Target Definition
- Is the target variable clearly defined?
- Is the prediction window explicit? (e.g., predict churn within 30 days)
- Is the target binary, multiclass, or regression? Is this appropriate for the problem?

### Step 2: Data Split Strategy
- Is the split temporal or random?
- For time-series or sequential data: random split is a defect unless justified
- Is the holdout truly unseen, or was it used for hyperparameter tuning?
- Check: stratification for imbalanced targets

### Step 3: Leakage Detection (Priority: CRITICAL)
- Review each feature:
  - Is it available at prediction time? Or is it derived from post-event data?
  - Is there a temporal gap between feature computation and target event?
- Red flags: perfect accuracy, unnaturally high AUC, features with near-zero importance
- Output: `LEAKAGE_RISK: [feature_name] — [reason] — [severity: confirmed/suspected]`

### Step 4: Class Imbalance Assessment
- Report class distribution
- If imbalance > 10:1, accuracy is not a valid primary metric
- Check: was imbalance addressed in training? (class weighting, oversampling, threshold tuning)
- Required metrics for imbalanced: Recall, Precision, F1, AUC-ROC, AUC-PR

### Step 5: Metric Interpretation
- Do not report metrics in isolation. Each metric requires a business context sentence.
- Example: "Recall of 0.71 means 29% of churners are missed — at an estimated €X per missed customer."
- Flag if threshold was not tuned. Default 0.5 is rarely optimal.

### Step 6: Explainability Review
- Are global feature importances provided?
- Do SHAP values or similar exist for individual prediction explanation?
- Flag: importances that do not align with domain knowledge require investigation
- State explainability limits explicitly

### Step 7: Operational Readiness
- Can the model be retrained with versioned configs?
- Is there a monitoring plan post-deployment?
- What is the expected model decay timeframe?
- Are operational rules extractable from the model?

## Output Format for Model Review

```
MODEL REVIEW SUMMARY
├── Target Definition: [PASS/FAIL/NOTE]
├── Split Strategy: [PASS/FAIL/NOTE]
├── Leakage Risk: [NONE/SUSPECTED/CONFIRMED] — [details]
├── Imbalance Handling: [PASS/FAIL/NOT APPLICABLE]
├── Metric Interpretation: [findings]
├── Explainability: [available/not available] — [limits]
├── Operational Readiness: [READY/NOT READY/CONDITIONAL]
└── Recommended Next Steps: [numbered list]
```
