# CQI Analytical PPTX Fixtures

## Purpose

This folder stores small synthetic fixtures. It may also contain a protected,
ignored local copy of the ELAL 70-slide acceptance deck so
`cqi-analytical-pptx` QA checks do not depend on a sibling repository path.

## Fixtures

| File | Purpose | SHA-256 |
|---|---|---|
| `elal_passenger_journey_eda_story_70slides_20260801_final.pptx` | Optional, ignored, read-only local ELAL deck fixture for release, notes, and readability audits. | `6e70d6411d484b98fe5d79314d100e5dcc8222cfa5c3c5dd8ac5048719639452` |
| `negative_aggregate_reconciliation.json` | Synthetic negative fixture that must fail reconciliation. | N/A |
| `podcast_manifest_dry_run.json` | Synthetic podcast dry-run manifest that must pass. | N/A |

## Policy

- Treat the ELAL deck as a fixture, not as a source of reusable business
  semantics.
- Never stage or commit the ELAL PPTX. The fixture path is intentionally
  ignored; QA that needs it is an optional local acceptance check.
- Do not modify this PPTX in-place. Replace it only with an explicitly approved
  fixture refresh and update the hash.
- Keep tests and scripts provider-neutral; ELAL-specific interpretation belongs
  in `../elal-analytical-profile.md`.
