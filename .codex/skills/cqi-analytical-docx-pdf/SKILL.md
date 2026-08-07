---
name: cqi-analytical-docx-pdf
description: Use when creating, updating, auditing, or exporting CQI/CQISense analytical Word/PDF deliverables, technical reports, decision memos, EDA reports, model-readiness reports, or client-facing DOCX/PDF artifacts. Applies the CQI Word template, APA table/figure rules, document-control, visual QA, and render-to-PNG verification.
---

# CQI Analytical DOCX/PDF

## Purpose

Create CQI/CQISense formal DOCX and PDF deliverables that follow the CQI Word
visual system, NegritaOS analytical content contract, and render-and-inspect QA.

This skill fills the DOCX/PDF gap that is not covered by `cqi-analytical-pptx`.

## Required Layering

Use these in order when the task is a formal report, memo, or PDF/DOCX
deliverable:

1. `documents:documents` for DOCX creation/editing and render verification.
2. `pdf:pdf` when PDF reading, rendering, or inspection is required.
3. `docs-alignment` for documentation structure and provenance.
4. `document-control` for deliverable versioning unless the user explicitly
   provides a project evidence-output folder.
5. `evidence-first-plot-analysis` when the report includes plots, charts,
   dashboard screenshots, EDA figures, or model diagnostics.
6. This skill for CQI visual and analytical report formatting.

## Source Of Truth

| Purpose | Canonical path |
|---|---|
| CQI brand routing | `/Users/jackyb-cqi/repos/NegritaOS/brands/cqi/brand_style/brand_style.md` |
| Current Word template | `/Users/jackyb-cqi/repos/NegritaOS/brands/cqi/plantillas/CQI_DocumentTemplate_20260720.docx` |
| Word template guide | `/Users/jackyb-cqi/repos/NegritaOS/brands/cqi/plantillas/CQI_DocumentTemplate_README.md` |
| Design system | `/Users/jackyb-cqi/repos/NegritaOS/brands/cqi/brand_style/CQISense_Design_System/` |
| Content contract | `/Users/jackyb-cqi/repos/NegritaOS/integrator.yaml` `default_output_contract` |

For formal CQI DOCX reports, start from `CQI_DocumentTemplate_20260720.docx`.
Do not build from a blank `Document()` unless the user requests a lightweight
non-branded draft.

## Required DOCX Structure

Use the NegritaOS `analytical_report` contract unless the user provides a
stricter outline:

1. Document control.
2. Index or reading guide.
3. TLDR.
4. Context.
5. Objective.
6. Methodology.
7. Evidence.
8. Findings.
9. Interpretation.
10. Risks and notes.
11. Recommendations.
12. Next actions.
13. Appendix / traceability.

Small memos can compress sections, but must still show scope, evidence,
limitations, owner questions, and next actions.

## Visual Contract

- Page: A4 portrait by default for formal reports.
- Template: preserve CQI cover, header, footer, document-control table, and
  template styles.
- Header: CQI logo once on the right; left header is document-control name only.
- Footer: `[Document name] · [DD/MM/YY]`.
- Body: Arial 12 pt, 1.5 line spacing.
- Headings: Arial Bold, controlled sizes from the Word template guide.
- Tables: `Light Grid Accent 1` unless the source template defines a stricter
  style.
- Colors: CQI token colors only: cobalt, navy, pink, teal, green, coral/risk,
  and cool grays.
- Do not invent alternate palettes, fonts, logos, covers, or table styles.

## APA Table And Figure Rules

Every table and figure must be numbered and explained:

```text
Table N
Italic Title Case Table Title
<table>
Note. Source, scope, sample size, calculation boundary, or caveat when needed.
```

```text
Figure N
Italic Title Case Figure Title
<figure>
Interpretation (contrato NegritaOS)
- Que muestra. ...
- Como leerla. ...
- Por que importa. ...
- Takeaway operativo. ...
```

For plots, include the four `plot_interpretation` fields from
`default_output_contract`: `what_it_shows`, `how_to_read_it`, `why_it_matters`,
and `operational_takeaway`.

## Placement And Versioning

Default to `document-control`: timestamped deliverables under the active work
root's `documents/` folder with a manifest.

If the user provides an evidence-output folder, preserve that folder convention
and create versioned filenames there without overwriting prior artifacts. Report
that this is an explicit project-output convention.

## Required QA

Before delivery:

1. Render DOCX to PDF.
2. Render PDF pages to PNG.
3. Inspect every page visually.
4. Check clipped text, cut tables, orphan captions, oversized headings,
   inconsistent spacing, and unreadable figures.
5. Check content gates: evidence vs inference, source paths, scope, limitations,
   and next actions.
6. Confirm no sensitive raw identifiers are exposed unless explicitly approved.
7. Cite final PDF exactly once as output in the final response.

## Failure Mode

If the CQI Word template is unavailable, stop and report the missing path. Do
not silently fall back to a blank document for a formal CQI deliverable.
