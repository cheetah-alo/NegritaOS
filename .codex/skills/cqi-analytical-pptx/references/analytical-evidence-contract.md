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

## Cross-source join safety gate

A cross-source join is not a canonical dataset by default. Do not create,
label as canonical, or use a combined population for reporting, scoring, or
model inputs merely because two tables expose a similarly named key.

This gate applies to `INNER`, `LEFT`, `FULL OUTER`, `UNION`, `UNION ALL`, key
coalescing, and additive denominators. Before implementation, the analyst must
record and validate all of the following:

1. the business question that requires the combination;
2. source owner and certified physical lineage/DDL for both sources;
3. grain and unique key of each source;
4. common analysis window and timestamp semantics;
5. join key, normalization and expected cardinality;
6. duplicate, fanout, overlap and parent/subset reconciliation results;
7. interpretation of missing fields and absent signals; and
8. explicit approval from the responsible Data Engineering owner.

If any item is unknown, keep source rails separate. Do not add row counts, do
not publish a combined denominator or coverage percentage, and do not convert
shared identifiers into confirmed individual entities. A combined artifact is
`CANDIDATE_SHADOW` until the evidence contract and reconciliation tests pass.

## Reconciliation Gates

Fail publication when:

- a subset exceeds its parent population;
- mutually exclusive categories do not sum to the total;
- a monthly stack by tier does not sum to the monthly total;
- an entity appears in more than one exclusive tier in the same cut;
- unmatched calls are converted into estimated members;
- alternative definitions are summed despite different contracts;
- a cross-source join or combined denominator lacks the approved join-safety
  evidence contract;
- identifiers or person-level rows are exported;
- a candidate rule creates events outside its base universe;
- slide count changes outside the approved release configuration.
