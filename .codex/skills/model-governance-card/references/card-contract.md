# Model Governance Card Contract

## Identification

Require stable `card_id`, model `id`, name, version, kind, lifecycle status,
business objective, supported decision, scope, created/updated timestamps,
evidence cutoff, and supersession link.

## Ownership

Name the business owner, technical owner, validation owner, deployment owner,
and monitoring owner. Generic team labels are acceptable only when no person
has been assigned; mark that gap `PENDING` rather than implying accountability.

## Evidence

Record repository revision, run IDs, configuration/query hashes, artifact
references, review references, and independent validation evidence. Evidence
references must be resolvable within the authorized environment and must not
expose internal orchestration paths in client-facing output.

## Data Foundation

Declare source-of-truth objects, transformations, grain, entity keys,
prediction/scoring timestamp, target/outcome timestamp, temporal window,
eligibility, exclusions, latency/freshness status, and populations at source,
eligible, train/backtest, validation, test, and scored stages.

Population figures must reconcile or include a named reconciliation gap. Do not
place two incompatible volumes in the card without explaining their filters or
stages.

## Validation

Each metric row requires:

- metric name and definition;
- dataset/split or backtest variant;
- population/support;
- threshold or `NOT_APPLICABLE` reason;
- value and unit;
- comparison baseline;
- evidence reference;
- interpretation and limitation;
- status.

Separate model performance from operational effectiveness. Correlation,
feature importance, SHAP, rule support, and outcome association do not prove
causal impact.

## Monitoring

Every monitored indicator requires baseline, control limit, direction,
cadence, owner, source, response action, and evidence/status. A threshold copied
from a prior model is `OBSERVED` until justified for the current model.

## Governance

Track lifecycle stage, approver, decision date, evidence, open conditions,
deployment revision, rollback procedure, retraining/change policy, and
retirement/supersession plan. A status label never replaces evidence.
