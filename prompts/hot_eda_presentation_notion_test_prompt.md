# HOT EDA Presentation + Notion Test Prompt

Use this prompt to test the NegritaOS presentation and Notion documentation workflow from two HOT Orange TSR/CSR analysis folders.

## Prompt

You are Bob operating inside NegritaOS.

Task mode: `presentation_plus_notion_test`

Use these source folders:

- `/Users/jackyb-cqi/repos/proj_data_analytics/analyses/poc_hot_orange_tsr_csr/p_hot_eda_ai_calls`
- `/Users/jackyb-cqi/repos/proj_data_analytics/analyses/poc_hot_orange_tsr_csr/p_hot_eda_ai_calls_fr_pr_focus`

Audience profile:

- Primary: `ceo_product_owner`
- Secondary appendix guardrail: `data_scientist_peer`

Required NegritaOS contracts:

- `rules/presentation/presentation_rules.yaml`
- `rules/presentation/audience_profiles.yaml`
- `rules/presentation/findings_contract.yaml`
- `rules/branding/branding_rules.yaml`
- `skills/executive/presentation_storyline.md`
- `skills/writing/notion_report.md`
- `brands/cqi/brand_style/brand_style.md`
- `templates/executive_deck_outline_template.md`
- `templates/notion_report_template.md`

Output language: English.

Theme preset: `white_background`.

Brand: CQI / CQISense. Use CQI blue `#0044ff`, clean white, dark neutral, and restrained executive styling. Do not improvise a new palette.

## Required Workflow

1. Identify the latest valid output run inside each source folder.
   - Prefer explicit timestamped output folders when present.
   - If no timestamped run exists, use the newest output files by modification time.
   - Do not modify the source folders.

2. Build a source inventory.
   - Include analysis scripts, README files, SQL files, output summaries, charts, CSV/JSON/HTML artifacts, and any existing report-like files.
   - Exclude `.DS_Store`, cache files, and non-informative artifacts.

3. Extract findings into the shared findings contract.
   Each finding must include:
   - `finding_id`
   - `message`
   - `evidence`
   - `implication`
   - `caveat`
   - `recommendation`
   - `source_path`

4. Compare the two analyses.
   - General AI calls analysis vs. FR/PR focus.
   - Identify what is consistent, what differs, what is newly surfaced by the FR/PR focus, and what remains uncertain.

5. Create an executive PPTX draft.
   Main deck target: 8-10 slides.
   Required structure:
   - Title
   - Executive Summary
   - Scope and source inventory
   - Finding 1
   - Finding 2
   - Finding 3
   - FR/PR focus implications
   - Risks and caveats
   - Recommendations and next actions
   - Appendix separator, if appendix follows

   Slide rules:
   - One complete sentence message per slide.
   - Every chart or table must have a takeaway headline.
   - Every recommendation must trace to a prior finding.
   - Speaker notes are required for every slide.
   - Methodology and raw technical detail belong in appendix unless needed for CEO/Product Owner decision-making.

6. Create a matching Notion document.
   The Notion doc must use the same findings contract and must not contradict the deck.
   Required structure:
   - TL;DR
   - Context
   - Objective
   - Source Inventory
   - Findings
   - Comparison: General vs. FR/PR Focus
   - Risks and Caveats
   - Recommendations
   - Next Actions
   - Appendix / Reproducibility Notes

7. Quality gates before final response.
   - Run `python3 scripts/validate_registry_paths.py` from `/Users/jackyb-cqi/repos/NegritaOS`.
   - Confirm all deck and Notion claims have source paths.
   - Confirm all deck text is English.
   - Confirm every slide has one message and speaker notes.
   - Confirm Notion next actions have owner or role set to `TBD - [role recommendation]`.

## Test Mode

Start with `dry_run_outline_only` unless explicitly told `full_delivery`.

In `dry_run_outline_only`:

- Do not create a PPTX.
- Do not publish to Notion.
- Produce:
  - latest-output detection result
  - source inventory
  - findings contract table
  - proposed slide outline
  - proposed Notion outline
  - quality gate checklist
  - missing inputs

In `full_delivery`:

- Create the editable PPTX under a thread-scoped output folder.
- Render previews and inspect them.
- Create or update the Notion page only after a Notion parent page/database URL is provided.
- Return final PPTX path, Notion URL, source inventory, and quality gate results.

## Missing Inputs to Ask For Only If Needed

Ask one concise question if any of these are required and unavailable:

- Notion parent page or database URL for publishing.
- Whether to use `white_background` or `black_background` if the user overrides the default.
- Whether the audience should be `ceo_product_owner`, `data_scientist_peer`, or `mixed_leadership_technical`.

Otherwise proceed with the defaults above.
