# Skill: ML Model Findings

**Type:** Domain — ML  
**Applicable agents:** model_review_agent, presentation_agent

## Purpose
Converts model outputs into findings without overstating performance. Use for
classification, regression, survival, clustering, explainability, and operational
rule extraction.

## Required Finding Contract

Each model finding must include:

- target definition and prediction window
- train/validation/test split
- baseline or random/reference comparator
- metric and threshold when relevant
- support or class balance
- leakage assessment
- explainability evidence when used
- note
- operational implication

## Rules

- Never report AUC, accuracy, recall, precision, lift, or SHAP without business meaning.
- Default threshold metrics are not final unless threshold tuning is documented.
- Random temporal splits are a risk for sequential/customer behavior data unless justified.
- Model explanations are evidence about model behavior, not guaranteed causal drivers.
- Recommendations must be proportional to validation strength.

## Output Pattern

```text
Finding:
Model evidence:
Baseline/reference:
Metric interpretation:
Leakage/readiness note:
Operational implication:
Recommendation:
Source:
```
