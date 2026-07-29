---
name: rule-model-documentation
description: >
  Create CQI-style documents for deterministic rule-based models, rules engines,
  scoring layers, boosters, persistence/sticky logic, sensitivity analysis,
  validation, plots, and decision recommendations. Trigger: documenting or
  explaining operational rule systems, rule scoring, rule-model backtests, or
  rule-vs-model solution comparisons.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, data_analytics, model-review, documentation]
  auto_invoke:
    - "Creating documentation for rule-based models or rules engines"
    - "Explaining rule scoring, boosters, persistence, sticky logic, or decay"
    - "Writing rule-model validation, sensitivity, or solution comparison reports"
    - "Explaining plots or tables for deterministic operational rules"
---

## When to Use

Use this skill when creating or reviewing stakeholder-facing documents for:

- deterministic rules engines, rule-based models, or operational scoring layers;
- rule flags, boosters, bands, segment shifts, persistence, sticky state, or decay logic;
- BigQuery/SQL rule pipelines with Q-stage or procedure-based processing;
- sensitivity analyses comparing multiple rule/scoring variants;
- validation reports that explain plots, tables, lifecycle funnels, and decision matrices.

Pair this skill with `document-control` when producing a deliverable file and
with `data-contracts`/`bigquery-analysis-governance` when source quality, grain,
or BigQuery evidence is part of the document.

## Critical Patterns

Apply the native NegritaOS guide at
`skills/engineering/rule_model_documentation.md`.

Always preserve these constraints:

1. Position the rules layer correctly: descriptive-operational unless formal
   outcome backtesting supports predictive claims.
2. Start from data foundation: window, source, grain, denominator, eligibility
   gates, joins, churn/outcome label, and exclusions.
3. Document every rule as evidence -> condition -> score/band -> operational
   meaning -> limitation.
4. Separate base rules from boosters and show how they combine into the final
   score or segment movement.
5. Explain persistence, sticky logic, decay, reset, and state tables as lifecycle
   behavior, not as incidental implementation detail.
6. Every plot needs a lead-in, axis/metric explanation, reading instruction,
   business interpretation, and decision consequence.
7. Every solution comparison needs a baseline anchor, direction of improvement,
   trade-off, and explicit recommendation.
8. Never leave a table or chart as decoration. Convert it into a traceable
   operating decision.

## Document Skeleton

```markdown
# <Rule System / Rule Model Name>

## Context And Objective
State the operational question and whether the system is descriptive,
operational, predictive, or hybrid.

## Data Foundation And Boundaries
Declare source, window, grain, eligibility gates, exclusions, denominator, and
outcome label.

## Operational Rules Framework
Explain each rule with definition, evidence, condition, score/band, and action.

## Pipeline And State Design
Describe stages, inputs, outputs, grain, DML/write behavior, idempotency,
persistence, sticky windows, and reset logic.

## Scoring And Sensitivity
Separate rule score, booster score, effective score, bands, segment shifts, and
candidate variants.

## Validation And Results
Compare against baseline, quantify lift/drift/overcount/stability, explain
plots, and test lifecycle behavior.

## Decision Matrix And Recommendation
Rank candidates with weighted criteria, identify primary/fallback choices, and
state residual risks.
```

## Commands

```bash
pdfinfo "/path/to/reference.pdf"
pdftotext -layout -f 1 -l 1 "/path/to/reference.pdf" -
python3 scripts/validate_config_resolution.py
python3 scripts/validate_registry_paths.py --root /Users/jackyb-cqi/repos/NegritaOS
python3 scripts/validate_skill_catalog.py
```

## Resources

- Reference style model:
  `references/hotmobile-rules-doc-style.md`
