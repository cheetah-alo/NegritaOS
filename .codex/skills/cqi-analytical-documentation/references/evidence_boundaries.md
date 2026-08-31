# Evidence Boundaries

## Separate The Layers

Every claim must identify which layer supports it:

1. `OBSERVED`: directly measured in the declared source and window.
2. `PARTIAL`: measured for only part of the required population, history, or
   contract.
3. `CANDIDATE` or `CANDIDATE_SHADOW`: evaluated but not approved as policy or
   production behavior.
4. `DATA_REQUIREMENT_OPEN`: required evidence is not materialized or governed.
5. `BLOCKED`: the question cannot be answered from available support.

Use the active project's exact status vocabulary when it differs. Never turn a
blocked state into zero, absence, or negative evidence.

## Required Distinctions

- Association is not causality.
- Backtesting is not production certification.
- Visual QA is not data validation.
- A successful render is not semantic correctness.
- A candidate recommendation is not an approved operating rule.
- A proxy is not the underlying business event.
- A sample or use case is not population-wide performance.
- Freshness is not capture-to-load latency.
- A stable aggregate can hide segment or cohort instability.

## Comparison Discipline

Every comparison names:

- baseline and candidate;
- same or different population;
- same or different window;
- same or different grain;
- calculation direction;
- desired direction;
- support and uncertainty;
- trade-off or displaced volume.

If any of these differ materially, qualify the comparison before interpreting
it.

## Recommendation Discipline

A recommendation must state:

- the evidence that supports it;
- the decision criterion;
- the residual risk;
- the fallback, when one is justified;
- the approval or validation gate still required.
