# Skill: EDA Analytics Findings

**Type:** Domain — Analytics / EDA  
**Applicable agents:** model_review_agent, presentation_agent, technical_writer_agent

## Purpose
Converts EDA outputs, plots, tables, cohorts, funnels, and segment summaries
into findings that can be defended in a report or deck.

## Required Finding Contract

Each EDA finding must include:

- finding_id
- message
- evidence
- implication
- note
- recommendation
- source_path
- denominator
- base_population
- support_threshold
- outcome_window when relevant
- baseline_reference when comparing rates/lifts

## Rules

- State the unit of analysis: rows, calls, accounts, events, pairs, sessions, or devices.
- State whether a metric is current, prior-window, future-window, or sequence-based.
- Separate processed-with-no-signal from not-processed or missing-extraction rows.
- For plots, apply the plotting-guidelines skill before promoting the chart to a finding.
- Do not describe temporal association as causal impact without a causal design.
- If support is low, mark the finding as directional or move it to appendix.

## Output Pattern

```text
Finding:
Evidence:
Base / denominator:
Window / direction:
Implication:
Note:
Recommendation:
Source:
```
