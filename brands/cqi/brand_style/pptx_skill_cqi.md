---
name: pptx-cqi
description: >
  Use this CQI presentation wrapper whenever creating, editing, reviewing, or
  extracting content from a CQI/CQISense .pptx deck. It routes agents to the
  current CQI presentation template and the CQISense design-system archive.
---

# CQI PPTX Skill

## Purpose

This file is the agent entrypoint for CQI/CQISense presentation work. It keeps
Codex, Claude, and other NegritaOS adapters aligned to the current brand package
without duplicating the full design system.

## Source Of Truth

| Purpose | Canonical path |
|---|---|
| Current CQI PPT template | `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx` |
| Full brand/design system archive | `brands/cqi/brand_style/CQISense_Design_System.zip` |
| Brand routing guide | `brands/cqi/brand_style/brand_style.md` |
| Deprecated PPT template | `Template_CQISense.pptx` |

Do not use the deprecated PPT template. If a deck references it, migrate the
deck workflow to `CQI_PresentationTemplate_20260401.pptx`.

## When To Use

Use this wrapper when the user mentions:

- CQI, CQISense, Hot Orange, executive deck, slide deck, PPT, or presentation.
- Creating or editing `.pptx` files.
- Extracting or summarizing a CQI presentation.
- Building a deck from analysis outputs, plots, or model findings.

## Mandatory Workflow

1. Load brand context from:

   `brands/cqi/brand_style/brand_style.md`

2. Inspect the design-system archive:

   ```bash
   unzip -l brands/cqi/brand_style/CQISense_Design_System.zip
   unzip -p brands/cqi/brand_style/CQISense_Design_System.zip SKILL.md
   unzip -p brands/cqi/brand_style/CQISense_Design_System.zip readme.md
   ```

3. Use the current PPT template:

   `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx`

4. Apply presentation rules from:

   `rules/presentation/presentation_rules.yaml`

5. If creating a stakeholder deliverable, apply:

   `.codex/skills/document-control/SKILL.md`

## Current Visual Contract

The archive is canonical. The current high-level contract is:

- Primary brand: CQI cobalt `#1A43F5`.
- Accent: pink `#FF8093`.
- Display font: Poppins.
- Body font: Noto Sans.
- Numeric/data font: IBM Plex Mono with tabular numbers.
- Reading rule: brand/UI = cobalt; Repair = teal; Risk = pink; Operational =
  green; Hot Orange/heat = priority flag only, not a surface.
- Slide writing: one idea per slide, conclusion first, minimal body text,
  evidence visible, no hype.

If any of the above conflicts with a newer `CQISense_Design_System.zip`, the
newer zip wins.

## Deck Quality Gates

- The deck uses `CQI_PresentationTemplate_20260401.pptx` as template.
- Colors, fonts, logos, spacing, and slide style come from the zip/template.
- Every slide has one main message.
- Every analytical claim has evidence or is marked as hypothesis.
- Metrics use consistent source paths, sample sizes, and calculation notes.
- No lorem ipsum, placeholders, hidden TODOs, or stale client names remain.
- Exported PPT/PDF deliverables follow `document-control` naming and manifest
  rules when they are final stakeholder artifacts.

## Ownership And Update Trigger

Owner: NegritaOS CQI brand governance.

Update this wrapper when the CQI PPT template or the CQISense design-system zip
changes.
