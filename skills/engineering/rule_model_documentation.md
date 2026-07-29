# Rule Model Documentation

Use this native skill when documenting deterministic rule-based models, rules
engines, operational scoring layers, boosters, persistence/sticky logic,
sensitivity analyses, and validation reports.

## Core Positioning

A rule-based model document must classify the system before explaining it:

- **Descriptive-operational**: rules convert observable behavior into
  interpretable operational segments or actions.
- **Predictive**: only if formal target labels, backtests, lift/precision/recall,
  calibration, and stability evidence support predictive claims.
- **Hybrid**: only if the relationship between ML baseline and rule uplift is
  explicit and tested.

Never describe a rules layer as a standalone churn model when it only augments a
daily ML model with near-real-time behavioral signals.

## Required Document Architecture

| Section | Required Content |
|---|---|
| Context and objective | Operational question, audience, business decision, methodological status |
| Data foundation | Source, window, grain, key, denominator, eligibility gates, exclusions, outcome label |
| Rule framework | Rule ID, definition, logical condition, score/band, evidence, action, limitation |
| Pipeline process | Stage name, script/procedure, input, output, grain, DML/write behavior, idempotency |
| Scoring | Base rules, boosters, effective score, bands, segment rank direction, cap/ceiling logic |
| State lifecycle | Persistence, sticky behavior, decay, reset, TTL/delete behavior, re-entry behavior |
| Sensitivity comparison | Candidate variants, baseline anchor, changed mechanism, unchanged upstream logic |
| Validation | Lift, overcount, drift, stability, re-engagement, use cases, decision matrix |

## Rule Explanation Contract

Each rule must be written with this shape:

```text
Rule <ID>: <Name>
Definition: <plain-language trigger>
Eligibility: <population, segment, duration, window, source gates>
Logical condition: <auditable condition or pseudocode>
Evidence: <table/plot/metric and denominator>
Score/band: <points, band, segment movement>
Operational interpretation: <why this matters>
Action: <what the operation should do or monitor>
Limitation: <where the rule can be noisy or provisional>
```

## Scoring And Booster Rules

- Keep `rule_score`, `booster_score`, and `effective_score` separate.
- State whether boosters are autonomous or require an active base rule.
- State whether meta-rules count base rules and which flags are included.
- State mutually exclusive rule hierarchy when it exists.
- Explain score-to-band thresholds and segment rank direction.
- Show worked examples that add components line by line.

## Plot And Table Narration

Every plot explanation must answer:

1. What mechanism is being tested?
2. What are the axes, denominator, window, and baseline?
3. What behavior is desired?
4. What behavior is risky or undesired?
5. What decision follows?

Preferred phrasing pattern:

```text
The plot below should be read as <plot role>. It tests whether <mechanism>
behaves as expected under <population/window>. The important comparison is not
only <metric A>, but also <trade-off metric B>. This means <decision>.
```

For tables, do not rely on numbers alone. Explain:

- baseline or anchor distribution;
- direction of improvement;
- displaced volume;
- hidden distortion risk;
- primary and fallback recommendation.

## Validation Expectations

A rule-model validation report should include:

- baseline comparison, usually ML Base or current production;
- target window and population definition;
- overcount or overflow checks for operational segments;
- Q-stage or pipeline drift checks when downstream layers correct upstream
  assignments;
- lifecycle validation for persistence, decay, reset, and re-entry;
- use cases that verify aggregate conclusions at account or journey level;
- weighted decision matrix with primary candidate, fallback candidate, and
  benchmark/worst case.

## Guardrails

- Do not make causal claims from operational association alone.
- Do not hide source grain, denominator, or eligibility gates.
- Do not present overflow control as successful if it collapses another segment.
- Do not leave diagrams, plots, or heatmaps without interpretation.
- Do not merge lifecycle behavior into scoring; persistence/decay/reset are
  separate mechanisms.
- Do not reuse HOTMobile-specific thresholds, segment names, or Hebrew/Spanish
  labels as universal defaults; treat them as project-specific evidence.
