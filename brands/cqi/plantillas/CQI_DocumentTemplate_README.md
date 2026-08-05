# CQI Word Document Template

Canonical template:

`brands/cqi/plantillas/CQI_DocumentTemplate_20260720.docx`

Regenerator:

`scripts/build_cqi_docx_template.py`

## Style Line

- Use the CQISense Design System as visual source of truth:
  `brands/cqi/brand_style/CQISense_Design_System/`.
- Use A4 portrait as the default formal report page.
- Header uses the CQI logo only once, on the right. Do not repeat a text logo
  on the left; use the left header only for the document control name.
- Footer uses small text with document name and short edit date:
  `[Document name] · [DD/MM/YY]`.
- Body copy uses Arial, 12 pt, 1.5 line spacing.
- Paragraph spacing uses 12 pt after normal paragraphs.
- Headings use Arial Bold and must stay organized, readable, and not oversized:
  - Heading 1: 15 pt maximum, 12 pt before, 6 pt after.
  - Heading 2: 14 pt, 10 pt before, 6 pt after.
  - Heading 3: 13 pt, 8 pt before, 6 pt after.
- Table captions use compact spacing: 8.5 pt, 1.15 line spacing, 6 pt after.
- Tables must not leave cut rows in the document:
  - prevent row splitting across pages;
  - repeat header rows on multi-row tables;
  - use explicit column widths;
  - keep table width within the document margins;
  - keep captions visually paired with their tables;
  - move, resize, split, or convert tables when the layout still cuts awkwardly.
- Follow APA numbering for tables and figures:
  - `Table 1` / `Figure 1` in bold on its own line;
  - title in italic title case directly below the number;
  - table or figure placed directly below the title;
  - optional `Note.` below the table or figure for source, scope, sample size,
    calculation boundary, or caveat.
- Every figure and table must be numbered, referenced in the text, and explained.
- Use CQI token colors only: cobalt, navy, pink, teal, green, and cool grays.
- Metrics and codes use Arial Bold in CQI semantic colors unless a project
  explicitly needs a monospaced technical table.

## Required Review

Before a CQI Word document is considered ready:

1. Render the `.docx` to page images.
2. Inspect every page for clipped text, cut tables, orphaned captions, oversized
   headings, and inconsistent spacing.
3. Fix and re-render until the document is clean.
