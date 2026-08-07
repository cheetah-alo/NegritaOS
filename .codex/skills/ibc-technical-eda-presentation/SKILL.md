---
name: ibc-technical-eda-presentation
description: Use for IBC Fiber Network analytical PPTX decks, technical EDA reviews, data-quality bridge reviews, ML-readiness discussions, and stakeholder decision decks.
---

# IBC Technical EDA Presentation

## Purpose

Create IBC analytical decks that are visually aligned with CQI Product Owner
presentation standards while preserving IBC-specific evidence, terminology, and
data-quality guardrails.

This skill layers on:

1. `presentations:Presentations`
2. `analytics-storytelling-deck`
3. `evidence-first-plot-analysis` when plots, charts, dashboards, or technical
   visuals are interpreted.
4. `cqi-analytical-pptx`

Do not use ELAL-specific passenger-journey, flight, FR/PR, tier, rule-score, or
Arik semantics in IBC decks.

## Required Context

Before creating or editing an IBC analytical PPTX, load:

1. `.codex/project.yaml`
2. `/Users/jackyb-cqi/repos/NegritaOS/projects/ibc_fiber_network.yaml`
3. IBC project memory index, when available from the local memory home declared
   by the registry.
4. relevant analysis README, manifest, YAML config, and evidence outputs
5. `src/fiber_network_ml/config/tenants/ibc.yaml` when source contracts, source
   fields, joins, or table semantics are discussed

## References To Load

- For visual patterns and deck structure, read
  `.codex/skills/cqi-analytical-pptx/references/deck-patterns.md`.
- For color roles, plots, highlights, cards, and heatmaps, read
  `.codex/skills/cqi-analytical-pptx/references/cqi-plot-highlight-palette.md`.
- For notes and claim traceability, read
  `.codex/skills/cqi-analytical-pptx/references/analytical-evidence-contract.md`.
- For IBC-specific terms and gates, read the files in this skill's
  `references/` folder as needed.

## Visual Contract

Use the CQI analytical visual system:

- Poppins for titles.
- Noto Sans for body text.
- IBM Plex Mono for metrics, field names, SQL names, hashes, IDs, table names,
  and tabular numbers.
- Navy cover and divider slides.
- White analytical slides with CQI cobalt left rail.
- KPI cards at the top when useful.
- Tables, heatmaps, and bars with declared analytical color roles.
- Bottom note/takeaway band for the allowed conclusion.
- Footer with source, grain, window, and slide number.
- Plot-backed slide messages must separate observation, interpretation, and
  boundary; cross-plot readings must use `CONFIRMS`, `QUALIFIES`, or
  `CONTRADICTS`.

## IBC Vocabulary

Use these terms consistently:

- `issues_on_subs`
- `trap_events`
- `ibc_asset_status_daily`
- `serial bridge`
- `as-of snapshot`
- `row_fingerprint`
- `technical entity`
- `root + shelf + slot + port`
- `fanout`
- `context drift`
- `null profile`
- `bridge readiness`
- `ML-readiness`
- `candidate table`

## IBC Evidence States

Use these communicable states:

- `OBSERVED`
- `CANDIDATE`
- `REVIEW`
- `HOLD_JOIN_FANOUT`
- `HOLD_CONTRACT_INCOMPLETE`
- `ML_HOLD_JOIN_KEY_UNRESOLVED`
- `ML_HOLD_DUPLICATES`
- `ML_HOLD_REQUIRED_NULLS`
- `NOT_MATERIALIZED`
- `N/D`

Do not publish unsupported states such as `ML-ready` unless the required gates
pass and the source owner approval is recorded.

## IBC Color Semantics

Status colors:

- `OBSERVED`: cobalt
- `CONFIRMED`: teal
- `CANDIDATE`: violet
- `REVIEW`: amber/gold
- `HOLD_*`: coral/rose
- `UNKNOWN` or `N/D`: slate
- `NOT_MATERIALIZED`: muted gray

Analytical color roles:

- issue base grain: cobalt
- serial bridge / valid association: teal
- trap aggregate signals: violet
- topology/root exploratory: amber
- fanout/risk/blocker: coral
- residual/unmatched/unknown: slate

## IBC Join Guardrails

Never present a cross-source join as approved unless the deck states:

1. business question;
2. source tables;
3. grain of each source;
4. join key;
5. time/as-of rule;
6. duplicate handling;
7. fanout result;
8. null result;
9. coverage result;
10. residual handling;
11. privacy/export constraint;
12. owner approval status.

If any item is missing, label the join `CANDIDATE` or `REVIEW`, not approved.

## IBC ML-Readiness Guardrails

A candidate ML table must declare:

- target grain;
- candidate label, if any;
- leakage risks;
- feature timing;
- source windows;
- deduplication rule;
- null handling;
- unresolved joins;
- excluded raw identifiers;
- allowed conclusion.

Do not claim model readiness from EDA coverage alone.

## Speaker Notes Contract

Every analytical slide must include:

```text
[Talk track]
...
[/Talk track]

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

When a slide uses repository files, analysis outputs, PDFs, or external sources,
include the `[Sources]` block required by the Presentation tool.

## Required QA

Before delivery:

1. render every slide;
2. inspect every slide visually;
3. run overflow validation;
4. confirm speaker notes exist for every analytical slide;
5. confirm no raw serial, IP, address, subscription, customer identifier, or
   message content appears in visible slides unless explicitly approved;
6. confirm every claim has source, grain, window, denominator, and limitation;
7. cite the final deck exactly once as output.
