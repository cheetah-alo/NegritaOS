---
name: cqi-analytical-documentation
description: >
  Create or review evidence-bound analytical narrative for EDA documentation,
  plot explanations, rule analyses, executive reports, stakeholder questions,
  DOCX/PDF/Markdown outputs, and analytical presentations. Use when the work
  must explain what the evidence shows, how to read it, what it means, what it
  cannot prove, and which decision it supports.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, documentation, analytics, plots, presentation, model-review]
  auto_invoke:
    - "Writing analytical documentation or an executive analytical report"
    - "Explaining plots, EDA results, rules, scoring, or validation findings"
    - "Answering stakeholder or Arik questions from analytical evidence"
    - "Creating speaker notes for plot-backed presentation slides"
---

# CQI Analytical Documentation

Use this skill for the analytical narrative. It does not replace the visual
template, the data contract, or the domain profile.

Combine it with:

- `evidence-first-plot-analysis` for plot interpretation;
- `rule-model-documentation` for deterministic rule systems;
- `cqi-analytical-docx-pdf` for Word/PDF production and QA;
- `analytics-storytelling-deck` and `cqi-analytical-pptx` for presentations;
- the active project profile for domain-specific semantics.

## Required Narrative

Every analytical section, finding, stakeholder answer, or plot discussion must
follow this order:

```text
Question
-> Executive answer
-> Evidence
-> How to read the plot or table
-> Observation
-> Interpretation
-> Evidence boundary
-> Operational implication or next analysis
```

Do not start with implementation detail when the audience first needs the
answer. Do not end at a metric or a caption. The narrative must explain why the
result matters and how far the evidence supports the conclusion.

## Plot Contract

For every plot, declare:

1. the question it answers;
2. population, grain, window, filters, denominator, and comparison baseline;
3. how to read axes, units, scales, marks, colors, groups, and direction;
4. the material pattern with `n`, percentages, rates, deltas, or support;
5. the evidence-supported interpretation;
6. what the plot cannot establish;
7. the operational decision, risk, or next check it enables.

Load [plot_discussion.md](references/plot_discussion.md) whenever a deliverable
contains a chart, table, heatmap, funnel, flow, or diagram.

## Presentation Notes Contract

The visible slide carries the concise message. The speaker notes carry the
complete discourse guide. Every new or materially changed slide must contain
this block:

```text
[Talk track]
Question:
Executive answer:
How to read:
What stands out:
Interpretation:
Evidence boundary:
Operational implication:
Transition:
[/Talk track]
```

For a slide without a plot, table, diagram, or other visual evidence, use
`How to read: N/A - no visual` and keep the remaining fields substantive. For
plot-backed slides, the talk track must point the speaker to the relevant
visual feature and quantified pattern.

For CQI/CQISense decks, keep the separate `[Evidence]` block required by
`cqi-analytical-pptx`. The talk track explains the story; the evidence block
records provenance and allowed conclusions. Neither replaces the other.

The talk track must be fluent, natural, presentation-ready prose in the output
language. Do not write stage directions, jargon-heavy fragments, or text that
merely repeats the slide.

## Stakeholder Questions

When the request is organized around stakeholder or Arik questions, load
[arik_questions.md](references/arik_questions.md). Answer each question as a
self-contained decision record. Do not bury the evidence status at the end.

## Project Boundaries

This skill is provider-neutral and project-neutral. It must not import HOT,
ELAL, IBC, BigQuery, churn, telecom, or aviation semantics unless the active
project profile supplies them.

For ELAL work, load the active ELAL governance skills and the ELAL section in
[arik_questions.md](references/arik_questions.md). Keep customer-facing and
internal/auditable routes distinct.

## Required References

- Load [voice_and_tone.md](references/voice_and_tone.md) for any full report,
  document, or deck narrative.
- Load [plot_discussion.md](references/plot_discussion.md) for visual evidence.
- Load [arik_questions.md](references/arik_questions.md) only for stakeholder
  question packs or ELAL/Arik review.
- Load [evidence_boundaries.md](references/evidence_boundaries.md) whenever a
  claim, status, comparison, or recommendation is written.
- Use [anti_patterns.md](references/anti_patterns.md) as the final narrative QA
  gate.

## Calibration Boundary

The HOTMobile PDFs named in `references/voice_and_tone.md` are read-only style
calibration. They are not factual authority for another project. Do not copy
their claims, thresholds, tables, wording, colors, layouts, grammar defects,
or unresolved placeholders.
