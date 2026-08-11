# Presentation and Notion Workflow

This workflow defines how NegritaOS turns analytical outputs into an English
executive presentation and a matching Notion document.

## Shared Source of Truth

Use `rules/presentation/findings_contract.yaml` before writing slides or Notion
sections. Each finding must include:

- message
- evidence
- implication
- note
- recommendation
- source path

## Audience Profiles

Use `rules/presentation/audience_profiles.yaml` to select the communication mode.

| Chat phrase | Audience profile | Output behavior |
|-------------|------------------|-----------------|
| CEO / Product Owner | `ceo_product_owner` | Short, decision-oriented, business and product impact first |
| Data Scientist peer | `data_scientist_peer` | Evidence-first, methodology visible, validation and notes explicit |
| Mixed audience | `mixed_leadership_technical` | Executive main story with technical appendix |

## Brand and Theme

Use `rules/presentation/presentation_rules.yaml` for presentation behavior.

- Default deck language: English.
- Default visual preset: `white_background`.
- Supported presets: `white_background`, `black_background`.
- CQI brand reference: `brands/cqi/brand_style/brand_style.md`.
- CQI brand archive: `brands/cqi/brand_style/CQISense_Design_System.zip`.
- CQI PPTX skill wrapper: `brands/cqi/brand_style/pptx_skill_cqi.md`.
- CQI PPTX reference: `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx`.
- Deprecated PPTX name: `Template_CQISense.pptx` must not be used.

## Output Pairing

The deck and Notion document should agree:

- Presentation: decision-ready narrative.
- Notion: auditable record with source paths and implementation detail.
- The TL;DR, findings, risks, recommendations, and next actions must not contradict each other.

## Document Control

Load `.codex/skills/document-control/SKILL.md` before creating or updating
deliverable decks, PDFs, Word docs, HTML deliverables, or Notion/Confluence
markdown.

- The user selects the exact output path before a deck or matching document is created.
- `documents/` is a compatible repository-local default, not a mandatory folder.
- PPTX, PDF, and DOCX artifacts outside the repository are external by default and are not added to Git.
- Filenames use `<slug>__updated_YYYYMMDD_HHMMSS.<ext>` with Europe/Madrid time unless the user defines another versioning convention.
- Updates create new timestamped versions; previous versions are not overwritten.
- For tracked repository artifacts, append each version to the applicable manifest. For external binaries, record the path, hash, and Git policy in Brain memory or an external sidecar manifest.
- Existing scattered deliverables should be audited before migration; do not
  bulk-move historical files without an explicit migration request.
- The active Negrita Brain session contract must resolve `document-delivery`.
  For analytical CQI decks, the inherited chain is
  `analytical-deck-delivery` -> `cqi-analytical-pptx` -> project-specific
  ELAL/IBC profile.

## Validation

Run this before relying on the registry:

```bash
python3 scripts/validate_registry_paths.py
python3 scripts/audit_document_control.py /path/to/work-root
```

The command fails if a system file references a missing skill, rule, rubric, template, doc, or agent path.
