# Analytical Evidence Contract

## Purpose

Define the analytical evidence that every CQI analytical slide must expose in
speaker notes so deck claims remain traceable after the deck is copied,
reviewed, exported, or converted to a podcast.

## Required Notes Block

Every analytical slide must include exactly one structured evidence block:

```text
[Evidence]
Source:
Window:
Grain:
Population:
Denominator:
Association:
Deduplication:
Evidence status:
Limitation:
Allowed conclusion:
[/Evidence]
```

If a slide uses external sources, keep a separate `[Sources]` block required by
the Presentation artifact workflow.

## Field Meaning

| Field | Required meaning |
|---|---|
| Source | Path, query, run manifest, table contract, or evidence artifact. |
| Window | Observation period or snapshot timestamp. |
| Grain | Unit of analysis: call, member, event, flight, rule-event, account, etc. |
| Population | Parent population that constrains the slide. |
| Denominator | Exact denominator used for rates, shares, lifts, or percentages. |
| Association | Link type, for example exact match, candidate match, no match, or not applicable. |
| Deduplication | How duplicate records or multi-event entities were handled. |
| Evidence status | One of the approved communicable states. |
| Limitation | What the audience must not overclaim. |
| Allowed conclusion | The strongest defensible conclusion. |

## Approved Evidence States

- `OBSERVED`: directly observed in the declared source and window.
- `CANDIDATE_SHADOW`: candidate or shadow logic, not production behavior.
- `DATA_REQUIREMENT_OPEN`: source or window needed for a stronger conclusion is
  not available yet.
- `NOT_MATERIALIZED`: planned or designed artifact has not been built.
- `N/D`: not applicable or not determined; explain which one in `Limitation`.

Do not publish `BLOCKED_DATA`, `BLOCKED_AUTH`, or `BLOQUEADO` as stakeholder
deck vocabulary.

## Prohibited Equivalences

- calls = members;
- unmatched calls = uncovered members;
- candidate phone association = exact member link;
- tier recorded in an event = full member tier history;
- one snapshot = time series;
- cohorts grouped by latest event = monthly migration of the same member;
- rule reach = causal effect on satisfaction, churn, or resolution;
- overbooking proxy = confirmed denied boarding;
- shadow signal = production rule.

## Reconciliation Gates

Fail publication when:

- a subset exceeds its parent population;
- mutually exclusive categories do not sum to the total;
- a monthly stack by tier does not sum to the monthly total;
- an entity appears in more than one exclusive tier in the same cut;
- unmatched calls are converted into estimated members;
- alternative definitions are summed despite different contracts;
- identifiers or person-level rows are exported;
- a candidate rule creates events outside its base universe;
- slide count changes outside the approved release configuration.
