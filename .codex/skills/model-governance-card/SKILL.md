---
name: model-governance-card
description: >
  Create or update a standardized evidence-bound governance card for machine
  learning, analytical rule, or hybrid models. Use when a model is created,
  materially changed, validated, deployed, monitored, retrained, superseded,
  or reviewed for operational readiness.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, ml, rule-model, governance, documentation]
  auto_invoke:
    - "Creating or materially changing an ML model"
    - "Creating or materially changing an analytical rule model"
    - "Documenting model validation, deployment, monitoring, or retraining"
    - "Creating a model card or production governance ficha"
---

# Model Governance Card

Use this skill through **Vera**, the canonical
`model_governance_card_agent`. The card tracks what the model is, what evidence
supports it, what remains unresolved, and which lifecycle decisions are
currently allowed.

The supplied Hotmobile PDF is calibration only. Read
[reference-calibration.md](references/reference-calibration.md) for the
structure retained from it and the unsupported patterns that must not be
copied as truth.

## Canonical Outputs

Create or update both when the project permits:

1. A machine-readable YAML card based on
   `templates/model_governance_card_template.yaml`.
2. A human-readable Markdown view with the same facts and evidence statuses.

DOCX or PDF is an optional rendered delivery, not the source of truth. Route
binary delivery through the active project artifact policy. For CQI projects,
do not expose internal orchestration names, internal agent IDs, or paths to the
governance meta-repository in the client-facing card.

Validate the YAML before release:

```bash
python3 scripts/validate_model_governance_card.py --card <card.yaml>
```

## Model Kinds

Set exactly one `model.kind`:

- `ml_predictive`: trained statistical or machine-learning model;
- `analytical_rule`: deterministic rules, score, bands, boosters, or state
  transitions;
- `hybrid`: trained model combined with governed deterministic rules.

Read [kind-specific-fields.md](references/kind-specific-fields.md) and populate
only the applicable sections. `NOT_APPLICABLE` must include a reason; it is not
a synonym for missing evidence.

## Required Evidence Order

Build the card from evidence, not from a narrative draft:

1. model/rule configuration and version;
2. source contract, grain, time window, keys, eligibility, and exclusions;
3. training/scoring run IDs, commit SHA, query/config hashes, and artifacts;
4. validation design, baseline, metrics, sensitivity/ablation, and limitations;
5. explainability or rule-level traceability;
6. deployment, monitoring, rollback/retraining, owners, and decisions.

Every quantitative result records population, dataset/split, threshold when
relevant, value, evidence reference, and status.

## Status Contract

Use only:

- `OBSERVED`: present in source evidence but not independently validated;
- `VERIFIED`: supported by a named, reproducible evidence reference;
- `PENDING`: planned work with owner or next action;
- `NOT_APPLICABLE`: intentionally outside scope with reason;
- `BLOCKED`: required evidence or approval is missing.

Lifecycle status is separate:

`DRAFT`, `CONTRACT_INCOMPLETE`, `VALIDATION_HOLD`, `VALIDATED`,
`PRODUCTION_CANDIDATE`, `DEPLOYED`, `RETIRED`.

Do not convert a parent model's production status into a derived model's
status. A derived model is `DEPLOYED` only when its own version, deployment,
validation, monitoring, and rollback evidence are verified.

## Mandatory Card Sections

Use [card-contract.md](references/card-contract.md) for exact fields:

1. Identification and business objective
2. Ownership and decision scope
3. Data lineage, grain, temporal coverage, and population reconciliation
4. Data quality and source constraints
5. Target/label policy or analytical rule outcome semantics
6. Model/rule design and configuration
7. Experimentation, sensitivity, and variant decision
8. Validation metrics and interpretation
9. Explainability or rule traceability
10. Operational evaluation and action policy
11. Monitoring, drift, stability, and response actions
12. Governance, deployment, rollback/retraining, and decision history

## Hard Stops

The card cannot claim `VALIDATED`, `PRODUCTION_CANDIDATE`, or `DEPLOYED` when:

- target/outcome, grain, prediction/scoring time, or eligibility is unresolved;
- train/validation/test or backtest boundaries are missing;
- leakage or temporal contamination is unresolved;
- population counts do not reconcile;
- metrics have no dataset, threshold, support, or evidence reference;
- a rule model lacks precedence, overlap/conflict, missing-value, or state
  semantics;
- monitoring thresholds have no baseline, owner, cadence, or response action;
- placeholders such as `TBD`, `[add value]`, or "working on strategy" remain;
- validation or deployment status is represented only by an icon or assertion.

## Update Triggers

Create a new card version after changes to data source, grain, target/outcome,
features, rules, thresholds, precedence, state behavior, split/backtest,
training/configuration, selected variant, deployment, monitoring, rollback,
retraining, or responsible owner.

Preserve prior versions and record `supersedes`, change summary, evidence
cutoff, and decision status. Do not silently rewrite the history of a model.

## Final Report

Report:

- model ID, kind, version, and lifecycle status;
- card paths and SHA-256;
- evidence cutoff and source revision;
- verified sections and blocked sections;
- allowed claim and prohibited claim;
- owners and next actions;
- whether a DOCX/PDF rendering was produced and where it was routed.
