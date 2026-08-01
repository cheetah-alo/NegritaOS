# Release QA Contract

## Purpose

Define the minimum release gate for CQI analytical decks and optional podcast
companions.

## Parametrized Release Config

Use a delivery-specific manifest. Example fields:

```yaml
deck_id: example_analytical_deck
source_deck: /absolute/path/source.pptx
output_deck: /absolute/path/output.pptx
expected_slide_count: 70
expected_note_count: 70
preserve_existing_canvas: true
preserve_existing_template: true
interpretation: RULE_REACH_NOT_CAUSAL_IMPACT
member_tier_semantics: EVENT_REGISTERED_TIER
score_snapshots_observed: 1
git_status_must_be_unchanged: true
forbidden_visible_terms:
  - BLOCKED_DATA
  - BLOCKED_AUTH
  - BLOQUEADO
  - Click to add
  - Lorem ipsum
```

This is an example shape. Values belong to the delivery, not to the global
skill.

## Release Workflow

1. Capture branch and `git status`.
2. Confirm temporary outputs are ignored or outside the repo.
3. Create a per-run temp directory.
4. Inspect every source slide and build a frame map.
5. Reconcile populations, denominators, stacks, and candidate universes.
6. Edit inherited slides only through declared frame-map elements.
7. Render all slides and a contact sheet.
8. Run release, readability, notes, reconciliation, placeholders, canvas, and
   forbidden-term audits.
9. Create an explicit backup of the previous version.
10. Publish an immutable version.
11. Update `current` only after QA passes.
12. Compare final and current hashes.
13. Confirm final `git status` matches the initial status when required.

## Podcast Companion

Podcast generation is optional and must be explicitly requested. A valid mobile
podcast companion:

- has one autonomous chapter per slide;
- explains question, population, denominator, data limitation, and conclusion
  without requiring the listener to see the screen;
- includes an introduction and closing;
- validates chapter count against deck slide count;
- produces mono MP3, 22.05 kHz, 96 kbps, compatible with iPhone and Android;
- produces TXT/JSON chapter indexes and a manifest with duration, hash, and
  format;
- preserves the prior version before updating `current`.

## Fixture Policy

Client decks may be used as read-only acceptance fixtures. Do not make test
suites permanently depend on confidential deck content. Keep small synthetic
negative fixtures for deliberate failure checks.
