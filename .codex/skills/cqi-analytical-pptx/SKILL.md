---
name: cqi-analytical-pptx
description: Create, edit, audit, release, and optionally publish mobile podcast companions for CQI/CQISense analytical PowerPoint decks. Trigger when working on CQI PPTX decks, analytical slide releases, deck QA, speaker notes evidence blocks, inherited CQI templates, ELAL analytical deck profiles, or deck-to-podcast outputs.
---

# CQI Analytical PPTX

Use this skill after `analytics-storytelling-deck` and before any CQI/CQISense
analytical deck is created, edited, audited, released, or accompanied by a
mobile podcast.

Layering:

```text
Presentations / Artifact Tool
-> analytics-storytelling-deck
-> evidence-first-plot-analysis when charts, plots, or visual evidence are used
-> cqi-analytical-pptx
-> optional project profile, for example elal-analytical-deck
```

## When To Use

- Creating a new CQI/CQISense analytical `.pptx`.
- Editing or extending an existing CQI/CQISense deck.
- Auditing slide count, notes, placeholders, canvas, readability, terms, or
  release manifests before publication.
- Producing a stakeholder-ready analytical deck from plots, EDA, model output,
  rules, or operational evidence.
- Creating an optional mobile podcast companion for a deck.

## Source Of Truth

- Visual system: `brands/cqi/brand_style/CQISense_Design_System/`.
- New deck template: `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx`.
- Existing deck edits: the source deck owns the canvas, masters, layouts, rails,
  cover, and inherited footers.
- Narrative layer: `skills/executive/analytics_storytelling_deck.md`.
- Presentation rules: `rules/presentation/presentation_rules.yaml`.

The extracted `CQISense_Design_System/` folder is the editable visual authority.
The zip bundle is a distribution artifact, not the primary source.

## Critical Contracts

1. Preserve the user's requested language or the dominant language of the source
   deck. Do not force English. Keep SQL, field names, IDs, and codes unchanged.
2. Use Poppins for titles, Noto Sans for body text, and IBM Plex Mono for
   metrics, codes, and tabular numbers.
3. Minimum readable sizes: main text and cells 16 pt; axes, legends, and labels
   12 pt; visible sources, notes, and metadata 10 pt. Never auto-shrink below
   those thresholds.
4. If content does not fit, shorten, split the slide, or change the visual
   pattern. Do not hide overflow or place opaque overlays on undeclared content.
5. Always validate `expected_slide_count` before release.
6. Use communicable evidence states: `OBSERVED`, `CANDIDATE_SHADOW`,
   `DATA_REQUIREMENT_OPEN`, `NOT_MATERIALIZED`, and `N/D`.
7. Do not publish `BLOCKED_DATA`, `BLOCKED_AUTH`, `BLOQUEADO`, placeholders, or
   lorem ipsum in visible slide text or notes.
8. Every non-neutral plot, table, card, chip, or highlight color must have a
   declared role: status, category, emphasis, magnitude, comparison, or alert.
   Load `references/cqi-plot-highlight-palette.md` before creating or editing
   analytical charts, heatmaps, KPI cards, tables, or highlighted findings.
9. For new CQI/CQISense decks, use the deck patterns in
   `references/deck-patterns.md` unless a user-provided template owns the
   structure.
10. Plot-backed slide messages must apply `evidence-first-plot-analysis`:
    explain how to read the plot, separate observation from interpretation,
    state the evidence boundary, and classify cross-plot relationships when
    multiple visuals are used.

## Analytical Evidence Block

Every analytical slide must include this speaker-notes block:

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
Plot relationship:
[/Evidence]
```

When external sources are used, keep the `[Sources]` block required by the
Presentation tool as well.

## Required Workflow

1. Capture branch and `git status` before work.
2. Confirm outputs and intermediates are ignored or outside the repo.
3. Use a per-run temporary directory.
4. Inspect every slide in the source deck.
5. Build a complete frame map before editing.
6. Reconcile populations, denominators, stacks, and candidate universes before
   designing.
7. Duplicate inherited slides and edit declared elements only.
8. Render slides and inspect all slides plus a contact sheet.
9. Run release, readability, notes, terms, placeholders, canvas, overflow, and
   template-fidelity audits.
10. Back up the prior version, publish an immutable version, update `current`
    only after QA passes, and compare hashes.
11. Confirm final `git status` matches the initial status when release config
    requires it.

## Project Profiles

- Generic CQI analytical decks use this skill directly.
- ELAL passenger-journey decks must also apply
  `references/elal-analytical-profile.md`.
- Do not import Hot Orange, churn, archetype, or other domain semantics into
  ELAL decks. Reuse controls, not meaning.

## References

- `references/analytical-evidence-contract.md`
- `references/cqi-visual-contract.md`
- `references/cqi-plot-highlight-palette.md`
- `references/deck-patterns.md`
- `references/elal-analytical-profile.md`
- `references/release-qa-contract.md`

## Scripts

Use scripts in `scripts/` as read-only QA gates unless an explicit release flow
asks otherwise:

```bash
node .codex/skills/cqi-analytical-pptx/scripts/audit_pptx_release.mjs --deck <deck.pptx> --expected-slide-count <n>
node .codex/skills/cqi-analytical-pptx/scripts/audit_pptx_readability.mjs --deck <deck.pptx>
node .codex/skills/cqi-analytical-pptx/scripts/audit_pptx_notes.mjs --deck <deck.pptx>
node .codex/skills/cqi-analytical-pptx/scripts/validate_aggregate_reconciliation.mjs --spec <checks.json>
node .codex/skills/cqi-analytical-pptx/scripts/build_mobile_podcast.mjs --manifest <manifest.json> --dry-run
```
