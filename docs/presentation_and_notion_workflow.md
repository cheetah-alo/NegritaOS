# Presentation and Notion Workflow

This workflow defines how NegritaOS turns analytical outputs into an English
executive presentation and a matching Notion document.

## Shared Source of Truth

Use `rules/presentation/findings_contract.yaml` before writing slides or Notion
sections. Each finding must include:

- message
- evidence
- implication
- caveat
- recommendation
- source path

## Audience Profiles

Use `rules/presentation/audience_profiles.yaml` to select the communication mode.

| Chat phrase | Audience profile | Output behavior |
|-------------|------------------|-----------------|
| CEO / Product Owner | `ceo_product_owner` | Short, decision-oriented, business and product impact first |
| Data Scientist peer | `data_scientist_peer` | Evidence-first, methodology visible, validation and caveats explicit |
| Mixed audience | `mixed_leadership_technical` | Executive main story with technical appendix |

## Brand and Theme

Use `rules/presentation/presentation_rules.yaml` for presentation behavior.

- Default deck language: English.
- Default visual preset: `white_background`.
- Supported presets: `white_background`, `black_background`.
- CQI brand reference: `brands/cqi/brand_style/brand_style.md`.
- CQI PPTX reference: `brands/cqi/plantillas/Template_CQISense.pptx`.

## Output Pairing

The deck and Notion document should agree:

- Presentation: decision-ready narrative.
- Notion: auditable record with source paths and implementation detail.
- The TL;DR, findings, risks, recommendations, and next actions must not contradict each other.

## Validation

Run this before relying on the registry:

```bash
python3 scripts/validate_registry_paths.py
```

The command fails if a system file references a missing skill, rule, rubric, template, doc, or agent path.
