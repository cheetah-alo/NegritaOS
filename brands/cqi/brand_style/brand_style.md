# CQI Brand Style

## Purpose

This file is the lightweight agent entrypoint for CQI/CQISense brand usage.
The full editable visual source of truth is the extracted design-system folder:

`brands/cqi/brand_style/CQISense_Design_System/`

Use this Markdown file to route Codex, Claude, and other NegritaOS adapters to
the current brand assets. The zip bundle is a distribution artifact derived
from the folder; do not treat older inline brand notes as canonical.

## Audience And Scope

Use these rules for:

- CQI and CQISense client-facing presentations.
- CQI-branded documents, Notion/Confluence pages, PDFs, and proposals.
- CQISense dashboards, demos, prototypes, and product UI.
- Hot Orange / CQISense analytical decks and stakeholder deliverables.

This file does not duplicate the zip. If a visual detail is missing here, inspect
the zip instead of improvising.

## Source Of Truth

| Purpose | Canonical path |
|---|---|
| Editable visual design system | `brands/cqi/brand_style/CQISense_Design_System/` |
| Distribution bundle | `brands/cqi/brand_style/CQISense_Design_System.zip` |
| Agent skill inside design system | `brands/cqi/brand_style/CQISense_Design_System/SKILL.md` |
| Brand overview inside design system | `brands/cqi/brand_style/CQISense_Design_System/readme.md` |
| CSS entrypoint inside design system | `brands/cqi/brand_style/CQISense_Design_System/styles.css` |
| Token source inside design system | `brands/cqi/brand_style/CQISense_Design_System/tokens/` |
| Component source inside design system | `brands/cqi/brand_style/CQISense_Design_System/components/` |
| Official logo assets inside design system | `brands/cqi/brand_style/CQISense_Design_System/assets/` |
| Current CQI PPT template | `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx` |
| Current CQI Word template | `brands/cqi/plantillas/CQI_DocumentTemplate_20260720.docx` |
| CQI Word template guide | `brands/cqi/plantillas/CQI_DocumentTemplate_README.md` |
| CQI PPT agent wrapper | `brands/cqi/brand_style/pptx_skill_cqi.md` |

Deprecated PPT file name:

`Template_CQISense.pptx`

Do not reference or recreate the deprecated PPT template.

## Current Brand Contract

The current brand is defined by the extracted design-system folder. The most
important tokens observed in that folder are:

| Role | Token / value | Source |
|---|---|---|
| Primary brand | `--brand`, `--blue-500`, `#1A43F5` | `tokens/colors.css` |
| Brand hover | `--brand-hover`, `--blue-600`, `#0037D5` | `tokens/colors.css` |
| Dark surface | `--surface-inverse`, `--blue-900`, `#001450` | `tokens/colors.css` |
| Main text | `--text-strong`, `--gray-800`, `#232324` | `tokens/colors.css` |
| Page surface | `--surface-page`, `--gray-50`, `#F7F7F7` | `tokens/colors.css` |
| Card surface | `--surface-card`, `#FFFFFF` | `tokens/colors.css` |
| Accent | `--accent`, `--pink-300`, `#FF8093` | `tokens/colors.css` |
| Repair | `--repair`, teal | `tokens/domain.css` |
| Risk | `--risk`, pink | `tokens/domain.css` |
| Operational | `--operational`, green | `tokens/domain.css` |
| Display font | `--font-display`, Poppins | `tokens/typography.css` |
| Body font | `--font-sans`, Noto Sans | `tokens/typography.css` |
| Numeric font | `--font-mono`, IBM Plex Mono | `tokens/typography.css` |

If these values conflict with the extracted design-system folder, the extracted
folder wins.

## How Agents Must Use The Design System

Before generating or modifying CQI visual work:

1. Inspect the extracted design system:

   ```bash
   find brands/cqi/brand_style/CQISense_Design_System -maxdepth 2 -type f
   ```

2. Read the skill and overview:

   ```bash
   sed -n '1,220p' brands/cqi/brand_style/CQISense_Design_System/SKILL.md
   sed -n '1,220p' brands/cqi/brand_style/CQISense_Design_System/readme.md
   ```

3. For UI, HTML, and dashboards, use the embedded CSS/tokens:

   ```bash
   sed -n '1,220p' brands/cqi/brand_style/CQISense_Design_System/styles.css
   sed -n '1,220p' brands/cqi/brand_style/CQISense_Design_System/tokens/colors.css
   sed -n '1,220p' brands/cqi/brand_style/CQISense_Design_System/tokens/domain.css
   ```

4. For presentations, use:

   `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx`

## Quality Gates

- Use the extracted design-system folder as visual authority for colors,
  typography, tokens, components, logos, spacing, and presentation style.
- Use the current PPT template for any new CQI/CQISense deck.
- Use the current Word template for any CQI/CQISense formal report, proposal,
  decision memo, or client-facing `.docx`.
- Do not use `Template_CQISense.pptx`.
- Do not invent alternate palettes, fonts, logos, or slide styles.
- Keep deliverables under the active work root's `documents/` folder when
  `document-control` applies.
- For dashboards, also apply `dashboard-architecture`; generated HTML is an
  artifact, not the editable source of truth.

## Ownership And Update Trigger

Owner: NegritaOS CQI brand governance.

Update this file whenever `CQISense_Design_System/`, its distribution zip, or
the canonical CQI PPT template changes.
