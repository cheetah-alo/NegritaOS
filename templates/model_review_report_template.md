# Model Review Report — [Model Name]

> **TL;DR:** [Verdict in 2-3 sentences: what the model does, the key finding, and the deployment recommendation]

---

## Context
- **Project:** [Project name]
- **Model type:** [Classification / Regression / Clustering]
- **Business objective:** [What decision or action this model supports]
- **Review date:** [YYYY-MM-DD]
- **Reviewer:** NegritaOS / [human reviewer if applicable]

---

## Model Configuration
- **Algorithm:** [XGBoost / LightGBM / AutoGluon / EBM / other]
- **Target variable:** [name + definition]
- **Prediction window:** [e.g., churn within 30 days]
- **Training data period:** [start — end]
- **Feature count:** [N features]
- **Training set size:** [N rows]
- **Holdout set size:** [N rows]

---

## Leakage Assessment

| Feature | Leakage Type | Severity | Status |
|---------|-------------|----------|--------|
| [feature_name] | [Temporal / Target / Pipeline] | [CRITICAL/HIGH/LOW] | [CONFIRMED/SUSPECTED/CLEAN] |

**Overall leakage verdict:** [NONE DETECTED / SUSPECTED — INVESTIGATE / CONFIRMED — BLOCK DEPLOYMENT]

---

## Class Balance
- **Positive class rate:** [X%]
- **Imbalance strategy applied:** [class weighting / oversampling / none]
- **Imbalance verdict:** [Addressed / Not addressed — risk stated]

---

## Performance Metrics

| Metric | Train | Validation | Holdout |
|--------|-------|-----------|---------|
| AUC-ROC | | | |
| AUC-PR | | | |
| Recall (at threshold X) | | | |
| Precision (at threshold X) | | | |
| F1 | | | |

**Threshold used:** [value + justification]

**Business interpretation:**
> [Translate metrics into business language. Example: "At the selected threshold, the model identifies X% of churners at a false positive rate of Y%."]

---

## Feature Importance

| Rank | Feature | Importance | Business Interpretation |
|------|---------|-----------|------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

**Explainability method:** [SHAP / built-in importance / permutation]

**Domain alignment:** [Do top features align with business knowledge? Flag mismatches.]

---

## Operational Rules (if applicable)

Rules extracted from model behavior for business process use:

| Rule | Support | Confidence | Risk |
|------|---------|-----------|------|
| IF [condition] THEN [outcome] | X% | X% | [state limits] |

---

## Risks and Limitations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| [risk 1] | HIGH/MEDIUM/LOW | [mitigation] |

---

## Operational Readiness

| Dimension | Status | Notes |
|-----------|--------|-------|
| Reproducibility | PASS / FAIL | |
| Experiment tracking | YES / NO | |
| Monitoring plan | YES / NO | |
| Retraining cadence defined | YES / NO | |

---

## Recommendations

1. [Action 1 — specific, owner-assignable]
2. [Action 2]
3. [Action 3]

---

## Next Actions

| Action | Owner | Timeline | Status |
|--------|-------|----------|--------|
| | | | Open |

---

*NegritaOS — model_review_agent | v1.0*
