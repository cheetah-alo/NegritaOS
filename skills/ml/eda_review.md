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

### Plot Evidence Review
- [ ] Population/filter is stated for every business-facing plot
- [ ] Denominator is stated: rows, calls, accounts, events, pairs, or model samples
- [ ] Sample size and support threshold are visible
- [ ] Overall/base reference is present when comparing rates, lifts, or differences
- [ ] Outcome windows and direction are explicit (`leads_to_*`, current event, prior window, future window)
- [ ] Category source is explicit: binary flag, primary slot, all slots, latest slot, sequence, or account aggregate
- [ ] Processed-with-no-signal is separated from not-processed/missing-extraction rows
- [ ] Dense plots are split rather than compressed into unreadable canvases
- [ ] Rendered plots or contact sheets were reviewed before using them as evidence
- [ ] Artifact lineage is traceable: source data, source function, output path, metric columns, and filter

## Anti-Patterns

- Plotting a distribution without stating what it means for modeling
- Reporting missing value percentages without deciding on treatment
- Including correlation heatmaps without identifying actionable pairs
- Treating a plot as evidence when denominator, base population, or outcome window is missing
- Treating `not processed` as equivalent to `no signal`
- Describing temporal association as causal impact without causal design
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

## Plot Readiness Verdict

When EDA includes plots for business or executive use, add:

```text
PLOT READINESS: [READY / NEEDS FIXES / NOT DEFENSIBLE]
Critical fixes:
  - [missing denominator/base/visual QA/etc.]
Slide/deck safe:
  - [plot ids or paths]
Appendix only:
  - [plot ids or paths]
Remove or rebuild:
  - [plot ids or paths]
```
