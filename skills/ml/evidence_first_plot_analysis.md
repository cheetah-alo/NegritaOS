# Evidence-First Plot Analysis

## Purpose

Provide a transversal contract for reading, comparing, and writing about plots
without overclaiming what the visual evidence can support.

## Audience And Scope

Use this for EDA, dashboards, model review, technical reports, Markdown notes,
DOCX/PDF deliverables, and PPTX decks whenever plots, charts, figures, or
visualizations are interpreted.

This skill does not govern how to generate plots. It governs how to read them,
connect them to evidence, and write about them.

## Source Of Truth

The activable wrapper is
`.codex/skills/evidence-first-plot-analysis/SKILL.md`. Agent routing is
declared in `integrator.yaml`, `core/orchestration/metaagent_router.yaml`, and
the relevant standalone agent manifests.

## Interpretation Contract

Every plot analysis must answer:

1. What am I looking at?
   - plot type;
   - question answered;
   - X axis;
   - Y axis;
   - units;
   - scale;
   - marks, color, shape, size, or facets;
   - denominator and base population;
   - filters and exclusions.

2. When and where?
   - snapshot vs time series;
   - total period;
   - retrospective or forecast window;
   - cohort comparability;
   - geography, operational unit, account, member, route, node, OLT/PON, or
     other relevant space;
   - analytical grain.

3. What do we observe?
   - visible pattern;
   - separation;
   - concentration;
   - slope change;
   - saturation;
   - anomaly;
   - outlier;
   - absence of difference;
   - inversion of an expected hypothesis.

4. How do we interpret it?
   - give the evidence-supported meaning;
   - connect it to domain vocabulary;
   - distinguish ranking, association, temporal ordering, and causality;
   - explain why the pattern matters rather than narrating every bar or point.

5. What is the boundary?
   - what the plot cannot establish;
   - unsupported causal claims;
   - missing denominators;
   - insufficient support;
   - non-comparable cohorts;
   - proxy labels;
   - snapshot limitations;
   - aggregation or fan-out risks.

6. How does it relate to other plots?
   - `CONFIRMS`: another plot supports the same reading;
   - `QUALIFIES`: another plot narrows or changes the reading;
   - `CONTRADICTS`: another plot challenges the reading.

## Required Output Shape

Use this shape in reports and decks. Compress it for slide notes, but do not
drop the evidence boundary.

```text
How to read it:
Observation:
Interpretation:
Boundary:
Cross-plot relationship:
Takeaway:
- What it tells us:
- What it does not tell us:
- What to inspect next:
```

## Writing Rules

- Do not explain generic chart mechanics unless the plot construction is
  ambiguous.
- Do not narrate every visible value.
- Do not use "significant", "important", or "interesting" without explaining
  why it changes the analytical reading.
- Do not write "this proves" unless the design actually supports proof.
- Do not make recommendations unless the plot and surrounding evidence support
  them.
- Do not hide uncertainty. State it as part of the analytical value.

## Quality Gates

- The denominator is explicit or the limitation is stated.
- The grain is explicit.
- Time and scope are explicit.
- Observations are separated from interpretation.
- Evidence boundaries are explicit.
- Cross-plot relationships use `CONFIRMS`, `QUALIFIES`, or `CONTRADICTS` when
  more than one plot is involved.
- The final takeaway includes what the plot tells us and what it does not tell
  us.

## Ownership And Update Trigger

Owner: NegritaOS analytical governance.

Update this skill when plot-backed reporting standards change, when new
deliverable formats are added, or when project-specific plot semantics become
general enough to reuse across projects.
