# Skill: EDA Review

**Type:** Domain — ML
**Applicable agents:** eda_reviewer_agent, model_review_agent

## Purpose
Evaluates the completeness and operational quality of exploratory data analysis.
An EDA is not complete if it only produces plots. Every observation must connect
to a decision about modeling, feature engineering, or data quality.

## EDA Completeness Checklist

### Dataset Overview
- [ ] Row count and column count stated
- [ ] Date range of data (if temporal)
- [ ] Source system and extraction date noted
- [ ] Schema version or dataset version referenced

### Target Variable
- [ ] Distribution plotted and described
- [ ] Class balance stated with exact ratios
- [ ] Temporal trend of target reviewed (if applicable)
- [ ] Business definition of target confirmed

### Missing Values
- [ ] Missing value rates per column reported
- [ ] Pattern analysis: is missingness random or systematic?
- [ ] Business interpretation of missingness stated
- [ ] Imputation strategy decided and justified

### Distributions and Outliers
- [ ] Continuous features: distribution type noted (normal, skewed, bimodal)
- [ ] Outliers: method of detection stated; operational decision on treatment
- [ ] Categorical features: cardinality reviewed; rare categories flagged

### Correlations
- [ ] Target-feature correlation reviewed
- [ ] High inter-feature correlation flagged (multicollinearity risk)
- [ ] Spurious correlations distinguished from meaningful ones

### Leakage Screening
- [ ] Feature timestamps reviewed relative to target event
- [ ] Post-event derived features identified and flagged
- [ ] Suspiciously high correlations with target investigated

### Data Quality Flags
- [ ] Inconsistent categories (spelling variants, encoding issues)
- [ ] Implausible values (negative ages, future dates in past-dated fields)
- [ ] Schema changes over time (if longitudinal)

## Anti-Patterns

- Plotting a distribution without stating what it means for modeling
- Reporting missing value percentages without deciding on treatment
- Including correlation heatmaps without identifying actionable pairs
- EDA that ends without a data readiness verdict

## Data Readiness Verdict

Every EDA review must conclude with:
```
DATA READINESS: [READY / CONDITIONAL / NOT READY]
Conditions (if applicable):
  - [condition 1]
  - [condition 2]
Blocking issues (if NOT READY):
  - [issue 1]
```
