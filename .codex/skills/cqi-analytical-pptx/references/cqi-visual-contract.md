# CQI Visual Contract

## Purpose

Define the CQI/CQISense visual constraints for analytical PowerPoint decks
without duplicating the design system.

## Source Of Truth

| Purpose | Canonical path |
|---|---|
| Editable visual system | `brands/cqi/brand_style/CQISense_Design_System/` |
| New deck template | `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx` |
| Brand routing guide | `brands/cqi/brand_style/brand_style.md` |
| Presentation rules | `rules/presentation/presentation_rules.yaml` |

The extracted design-system folder is the visual authority. A zip archive is
only a distribution bundle derived from that folder.

## Typography

- Titles: Poppins.
- Body text: Noto Sans.
- Metrics, codes, and tabular numbers: IBM Plex Mono.

Do not use Spectral, Public Sans, or Malgun Gothic as normative CQI
presentation fonts.

## Readability Thresholds

- Main text and table cells: at least 16 pt.
- Axes, legends, and labels: at least 12 pt.
- Visible sources, notes, and metadata: at least 10 pt.

Auto-shrink below these thresholds is prohibited. If a slide cannot fit, shorten
the copy, split the slide, or change the visual pattern.

## Canvas And Template Rules

- New CQI decks start from `CQI_PresentationTemplate_20260401.pptx`.
- Existing CQI decks keep their own canvas, masters, layouts, cobalt rail,
  cover, and inherited footers.
- Do not force a universal 26.67 by 15 inch canvas onto an existing deck with a
  different 16:9 size.
- Use relative coordinates or coordinates derived from the actual slide canvas.
- Do not place opaque overlays on inherited content unless that edit is declared
  in the frame map.

## Language

Preserve the requested language or the dominant language of the source deck. Do
not force English. Keep SQL, field names, IDs, source paths, rule IDs, and
technical codes unchanged.

## Length

An explicitly approved slide count wins. Guidance such as 10, 15, or 25 slides
applies to executive bodies, not to dossiers, appendices, or audited analytical
packs. Validate `expected_slide_count` before publication.
