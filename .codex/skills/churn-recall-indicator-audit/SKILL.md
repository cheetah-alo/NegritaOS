---
name: churn-recall-indicator-audit
description: >
  Churn, recall, recontact, journey-pressure, DiscReq, retention, and account
  KPI audit workflow for SQL and analytics reports. Use when reviewing or
  creating queries, dashboards, PPT/Notion summaries, or EDA outputs that
  calculate recall_24h, churn_30d, discreq_30d, account journey pressure, or
  related call-center indicators.
metadata:
  scope: [root, data_analytics, analyses, z_smash]
  auto_invoke: "Reviewing or creating churn, recall, DiscReq, retention, recontact, or account journey pressure metrics"
---

# Churn & Recall Indicator Audit

Use this skill before changing, approving, or presenting any query/report that contains churn, recall, recontact, DiscReq, retention, or account journey pressure indicators.

## Core Rule

Never accept a metric label like `recall_24h`, `churn_30d`, or `discreq_30d` without documenting its base, grain, time window, event direction, numerator, denominator, and boundary behavior.

## Required Workflow

1. Locate the source query/table and downstream consumer.
2. Identify whether the metric is stored, recomputed, or filtered after computation.
3. Classify the metric grain:
   - call-level rolling
   - account-level
   - account-month
   - non-overlapping account episode
   - agent/event attribution
4. Write the denominator explicitly.
5. Write the numerator explicitly.
6. Check whether future events are restricted by:
   - same account
   - same destination/VDN
   - same call_type
   - same reason/subreason
   - incoming only
   - answered/attended only
   - first future event only
7. Check invalid identifiers:
   - null/blank account
   - sentinel accounts such as `2222` or `-1`
   - duplicated call ids or source ids
8. Check time-window semantics:
   - inclusive/exclusive date filters
   - lookahead buffer beyond the report end date
   - timezone and timestamp type
   - whether the future event can cross a month boundary
9. Compare at least two definitions when the metric is being reconciled:
   - dashboard-like strict definition
   - broad journey-pressure definition
   - account-level or episode-level alternative if requested
10. Produce the standard report below.

## Recall Checks

For any `recall_24h` or recontact flag, answer these questions:

- Is the source grain a call, interaction, segment, account, or account-month?
- Is recall rolling by source call, or non-overlapping by account episode?
- Does one source call count at most the first future call?
- Is the future event required to be incoming?
- Is the future event required to be answered/attended?
- Is the future event required to be same destination/VDN?
- If VDN is unavailable, is same `call_type` being used as a proxy?
- Are future RET/outgoing events included?
- Is the flag computed before or after filtering the output table?
- Is a lookahead buffer available for the final 24h of the reporting window?

### Standard Recall Definitions

Use these names unless the user explicitly requests otherwise:

| Metric name | Meaning |
| --- | --- |
| `Dashboard Recall 24h` | First future answered call from same account and same destination/VDN within 24h |
| `ia_calls Same-Type Recall Proxy <=24h` | First future incoming call from same account and same `call_type` within 24h |
| `Account Contact Pressure <=24h` | Next account call within 24h, not restricted to same destination/type |
| `Account Recontact Episodes <=24h` | Non-overlapping account-level recontact episodes |

When explaining dashboard-style recall, be precise:

- A source call can only contribute one recall flag.
- If several future calls qualify, use the first future qualifying call.
- A chain can still produce multiple flags because each future call can become a new source call.

## Churn / DiscReq Checks

For `churn_30d`, `discreq_30d`, or retention-related indicators:

- Define the event source table.
- Define the event timestamp/date used.
- Confirm whether the event must occur after the call timestamp.
- Confirm the horizon: 7d, 15d, 30d, calendar month, or contract period.
- Confirm whether the metric is first future event, any future event, or nearest future event.
- Check whether the event is account-level, contract-level, subscription-level, or ticket-level.
- Check account id normalization and joins.
- Check whether calls after the churn/disconnection request are excluded.
- Check if there is right-censoring near the report end date.

## Required Standard Report

Every completed analysis should include:

```markdown
## Metric Audit Summary

### Source
- Query/table:
- Output/report using it:
- Window:

### Base And Grain
- Source grain:
- Metric grain:
- Denominator:
- Invalid-id handling:
- Dedup rule:

### Numerator
- Event:
- Future-event filters:
- Time horizon:
- First future only:
- Direction/answered constraints:
- Same destination/type/reason constraints:

### Boundary Conditions
- Timezone:
- Window end lookahead:
- Month crossing:
- Right-censoring risk:

### Results
| Definition | N | Metric N | Metric % | Notes |
| --- | ---: | ---: | ---: | --- |

### Reconciliation
- Closest dashboard-like definition:
- Broad journey-pressure definition:
- Main driver of variance:
- Decision: keep / rename / recompute / split metrics

### Recommendation
- Approved metric label:
- Where it can be used:
- Where it should not be compared:
```

## Presentation Guidance

- Do not call broad account pressure simply `Recall 24h`.
- Use `Recall 24h` only when the denominator and numerator match the dashboard-style definition.
- Use `Account Contact Pressure <=24h` for journey wear, repeated contacts, operational pressure, and friction escalation.
- Use side-by-side tables when reconciling dashboard vs AI or enriched tables.
- Include a one-line caveat whenever the table is filtered after the recall flag was already computed.

## SQL Review Pattern

When reading SQL, search for:

- `LEAD(` and `LAG(`
- `TIMESTAMP_DIFF`
- `DATE_DIFF`
- `ROW_NUMBER`
- `QUALIFY`
- `PARTITION BY account_id`
- `PARTITION BY call_id`
- `direction`
- `call_type`
- `main_vdn`, `interaction_main_vdn`, `destination`
- `atention_flag`, `answered`, `attended`
- `churn`, `discreq`, `retention`, `disconnect`

The metric definition usually lives where the window function and final `CASE WHEN` flag are created, not where the final report filters rows.
