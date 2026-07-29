# HOTMobile Rule Documentation Style Model

Purpose: summarize the local HOTMobile rule-system PDF set used to calibrate
the tone and structure of `rule-model-documentation`. This reference is a style
guide, not a source of truth for future projects.

Source folder inspected page-by-page:

`/Users/jackyb-cqi/Library/CloudStorage/OneDrive-Personal/CQI Documents/Projects/Hotmobile/Rules_Final_Doc/DocFinalReglas`

PDFs reviewed:

- `CDS-4. Rule System base on Data Performance for Churn Risk Enhance-290726-104507.pdf` (4 pages)
- `CDS-I. Data Foundation and Preparation-290726-104526.pdf` (6 pages)
- `CDS-II. Operational Rules Framework-290726-104524.pdf` (12 pages)
- `CDS-III. Rule Process End to End-290726-104603.pdf` (17 pages)
- `CDS-III.1 Rule Scoring-290726-104551.pdf` (9 pages)
- `CDS-III.2 Rule Scoring Sensitivities-290726-104601.pdf` (11 pages)
- `CDS-IV. Solution Comparison & Validation Process-290726-104611.pdf` (27 pages)

## Tone

- Formal, technical, and operational.
- Explains why a mechanism matters before presenting it as a decision.
- Uses cautious methodological language: descriptive-operational unless
  predictive backtesting is proven.
- Converts each metric into a business interpretation.
- Keeps traceability visible: source, grain, period, rule ID, pipeline stage,
  output table, and downstream consumer.

## Narrative Pattern

1. Start with the operational question.
2. Declare the analytical scope and methodological status.
3. Explain the data foundation before rules.
4. Move from static evidence to sequential journey behavior.
5. Convert observed patterns into deterministic rules.
6. Describe pipeline stages and state lifecycle.
7. Compare sensitivity variants against a baseline anchor.
8. End with a decision matrix and primary/fallback recommendation.

## Plot Explanation Pattern

For every plot:

- introduce what the plot is intended to test;
- name the x-axis, y-axis, denominator, and comparison baseline;
- state how the reader should interpret the chart;
- identify desired and undesired behavior;
- connect the visual evidence to a rule, lifecycle mechanism, or candidate
  decision.

## Table Pattern

- Use tables to expose contracts, eligibility gates, scoring rules, solution
  differences, lifecycle phases, and weighted decisions.
- Include comparison anchors such as ML Base, current production, or baseline
  solution.
- Mark best/worst behavior in the narrative even when the table already shows
  the values.
- Explain displaced volume and hidden distortion; do not call a solution better
  merely because one metric improves.
