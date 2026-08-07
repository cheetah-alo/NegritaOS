---
name: evidence-first-plot-analysis
description: >
  Use when interpreting, comparing, reviewing, or writing about plots,
  charts, visualizations, dashboards, EDA figures, model diagnostic plots,
  or plot-backed claims in Markdown, DOCX, PDF, PPTX, reports, or decks.
license: Apache-2.0
metadata:
  author: NegritaOS
  version: "1.0"
  scope: [root, analytics, plots, reports, decks, model-review]
  auto_invoke:
    - when interpreting plots or charts
    - when converting plots into analytical findings
    - when writing DOCX, PDF, Markdown, or PPTX reports that include plots
    - when comparing multiple plots or chart-backed claims
---

# Evidence-First Plot Analysis

Apply the canonical NegritaOS skill at
`skills/ml/evidence_first_plot_analysis.md`.

## Required Reading Sequence

For every plot-backed claim, answer these in order:

1. What am I looking at?
2. How do I read it?
3. When, where, and at what grain?
4. What do we observe?
5. What matters most?
6. How should it be interpreted?
7. What is the evidence boundary?
8. How does it relate to other plots?
9. What is the final takeaway?

## Core Rule

Say what the visual evidence is strong enough to say, and state what it cannot
establish. Do not turn visual correlation, ranking, separation, or co-movement
into causality unless the underlying design supports that claim.

## Output Contract

Every plot interpretation must include:

- `how_to_read_it`: plot type, X axis, Y axis, units, scale, marks, color,
  denominator, filters, and population.
- `time_space_grain`: snapshot or time series, period, window, geography or
  operational scope, and analytical grain.
- `observation`: facts visible in the plot only.
- `interpretation`: evidence-supported meaning.
- `boundary`: what the plot does not prove.
- `cross_plot_relationship`: `CONFIRMS`, `QUALIFIES`, or `CONTRADICTS` when
  comparing plots.
- `takeaway`: what it tells us, what it does not tell us, and what to inspect
  next when useful.

## Style Contract

Use professional analytical language with clarity, curiosity, and explicit
uncertainty. The Brene Brown influence is translated into evidence humility:
be clear about meaning, be brave about limitations, and avoid artificial
emotional language.
