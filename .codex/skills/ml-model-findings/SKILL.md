---
name: ml-model-findings
description: Use when converting ML model outputs, metrics, thresholds, lift, explainability, leakage checks, or operational model reviews into defensible findings.
metadata:
  scope: [ml, model-review, metrics, explainability, findings]
  auto_invoke:
    - when summarizing model performance findings
    - when interpreting model metrics or thresholds
    - when converting explainability outputs into recommendations
---

# ML Model Findings

Apply the canonical NegritaOS skill at `skills/ml/ml_model_findings.md`.

Each model finding must state target/window, split, baseline/reference, metric
meaning, threshold if relevant, support/class balance, leakage/readiness note,
operational implication, and recommendation.
