# CQI Brand Style

## Purpose

This file is the lightweight agent entrypoint for CQI/CQISense brand usage.
The full visual source of truth is the bundled design-system archive:

`brands/cqi/brand_style/CQISense_Design_System.zip`

Use this Markdown file to route Codex, Claude, and other NegritaOS adapters to
the current brand assets. Do not treat older inline brand notes as canonical.

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
| Full brand/design system archive | `brands/cqi/brand_style/CQISense_Design_System.zip` |
| Agent skill inside archive | `SKILL.md` |
| Brand overview inside archive | `readme.md` |
| CSS entrypoint inside archive | `styles.css` |
| Token source inside archive | `tokens/` |
| Component source inside archive | `components/` |
| Official logo assets inside archive | `assets/` |
| Current CQI PPT template | `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx` |
| CQI PPT agent wrapper | `brands/cqi/brand_style/pptx_skill_cqi.md` |

Deprecated PPT file name:

`Template_CQISense.pptx`

Do not reference or recreate the deprecated PPT template.

## Current Brand Contract

The current brand is defined by the archive contents. The most important tokens
observed in the current archive are:

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

If these values conflict with a newer zip, the newer zip wins.

## How Agents Must Use The Zip

Before generating or modifying CQI visual work:

1. Inspect the archive index:

   ```bash
   unzip -l brands/cqi/brand_style/CQISense_Design_System.zip
   ```

2. Read the embedded skill and overview:

   ```bash
   unzip -p brands/cqi/brand_style/CQISense_Design_System.zip SKILL.md
   unzip -p brands/cqi/brand_style/CQISense_Design_System.zip readme.md
   ```

3. For UI, HTML, and dashboards, use the embedded CSS/tokens:

   ```bash
   unzip -p brands/cqi/brand_style/CQISense_Design_System.zip styles.css
   unzip -p brands/cqi/brand_style/CQISense_Design_System.zip tokens/colors.css
   unzip -p brands/cqi/brand_style/CQISense_Design_System.zip tokens/domain.css
   ```

4. For presentations, use:

   `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx`

## Quality Gates

- Use the zip as visual authority for colors, typography, tokens, components,
  logos, spacing, and presentation style.
- Use the current PPT template for any new CQI/CQISense deck.
- Do not use `Template_CQISense.pptx`.
- Do not invent alternate palettes, fonts, logos, or slide styles.
- Keep deliverables under the active work root's `documents/` folder when
  `document-control` applies.
- For dashboards, also apply `dashboard-architecture`; generated HTML is an
  artifact, not the editable source of truth.

## Ownership And Update Trigger

Owner: NegritaOS CQI brand governance.

Update this file whenever `CQISense_Design_System.zip` or the canonical CQI PPT
template changes.
