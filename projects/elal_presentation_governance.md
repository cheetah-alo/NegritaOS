# ELAL presentation governance

Status: active canonical NegritaOS governance contract as of 2026-08-04.

## Purpose

Every ELAL PPTX must make discussion order, evidence state, and decision gates
easy to audit. This contract applies to creation, editing, review, and release;
it also applies to one-slide replacements. It does not authorize a change to an
ELAL productive rule, score, V9/V10 state, chip, dashboard, or source table.

## Mandatory reference

Use [the Product Owner reference deck](/Users/jackyb-cqi/repos/proj_data_analytics/analyses/poc_elal_passenger_journey/documents/elal_passenger_journey_product_owner_summary_44slides_20260804_final_no_text_frames.pptx)
as the mandatory visual and speaker-notes reference. The filename is not an
identity check: the inspected artifact has 46 slides and 46 notes, with SHA-256
`b5bbf5eb7b940b7681bcf227cd0bf38e0c953d258d87cd7686a27682d4252c28`.

Its form is intentional: 16:9 `2048 x 1152`; a cobalt left rail; dark-navy
cover and `ACTO` divider slides; light evidence slides with a fixed footer;
Poppins for the hierarchy, Noto Sans for body copy, and IBM Plex Mono for
labels and numeric context. Work from its masters, layouts, and duplicated
slides rather than recreating its style from memory.

The reference has 46 notes, but six have incomplete marker pairs (slides 7, 9,
25, 26, 28, and 46). The deck itself is not to be corrected, saved, reordered,
or overwritten in this work. New or changed slides improve on this baseline by
having complete notes as specified below.

## Safe source rule

PPTX artifacts in a user-selected local or external output folder are client
artifacts and may be open; do not move them into the repository unless asked.
Before editing, obtain the exact, closed source path from Jacky, verify it, and
work from a duplicate. A similar filename, a `final` suffix, or a file visible
in a directory does not identify an editable source. Organization means a
semantic register; it does not mean moving, renaming, or deleting PPTX files.

## Required discussion order

Use this sequence in a decision deck. A focused deck may omit a section only
when its scope is explicitly stated in the cover and notes.

1. **Coverage and grain.** State sources, time window, population,
   denominator, identity/association quality, and what is unavailable.
2. **Observed signals.** Separate flights/events from reason/subreason and
   FR/PR conversation evidence; do not combine source rails into an additive
   population.
3. **Current production policy.** Describe what is actually productive and
   what remains unchanged.
4. **Candidate rule or audit finding.** State the literal review point, tested
   logic, measured effect, and evidence status.
5. **Decision gate.** Name the owner, contract/operational evidence still
   required, capacity implication, and whether the result is observed,
   candidate, shadow, approved, or insufficient.

## Speaker notes are release evidence

Every output slide needs one note with complete `[Talk track]` and `[Evidence]`
blocks. Evidence must declare source, window, grain, population/denominator,
deduplication or association method, evidence status, limitation, and allowed
conclusion. Preserve notes when an inherited slide remains materially valid;
rewrite them when a claim, figure, or conclusion changes.

The output must have the same number of notes as slides. Check marker pairs and
render every slide before delivery; a claim on the canvas without its bounded
evidence note is not release-ready.

## Rule and data constraints to preserve in every deck

- The active EDA call rail is `CALLS.calls_fric_prom_w_metadata`.
  `CALLS.ia_calls` is deprecated for this EDA. Do not create a broad additive
  union or `FULL OUTER JOIN` of the two rails.
- `Seat Overbooking` is observed as a call subreason; the operational cause
  `denied_boarding_overbooking` is not certified in the active call rail.
  Transcript `resolved`/`acknowledged` is not a completed-flight outcome.
- A future call rule must have identity, deduplication, precedence, points,
  enumerated contract, operational truth, and owner approval. A candidate may
  replace existing `F_NEG_08`; it must not add every FR/PR call as a score event.
- Tier changes treatment and priority, not pressure score. The severe chip
  keeps context and does not change color directly.
- A V9/V10 comparison on one snapshot is a reclassification crosswalk, not a
  temporal transition. The 31-May snapshot cannot prove recovery or flapping.

## Organization and selection

[`elal_presentation_artifact_register.yaml`](elal_presentation_artifact_register.yaml) is the current semantic index for
the 41 local PPTX artifacts. Select a supporting deck by its discussion theme,
then verify its evidence and lifecycle status. The register does not declare a
candidate as current, replace a user selection, or supersede the mandatory
Product Owner reference deck.

## Release checklist

- The mandatory skill and this contract were read.
- The exact reference and editable source were verified; an open source was not
  modified.
- Reference layouts, forms, fonts, footer, dark `ACTO` dividers, and visual
  hierarchy were preserved through slide duplication.
- All slides rendered cleanly with no overflow, clipping, overlap, missing
  fonts, or empty placeholders.
- Slide count equals note count; every changed slide has complete paired note
  blocks and an evidence status.
- Every rule statement is bounded to the current productive, observed,
  candidate, shadow, approved, or insufficient state.
- Every rule or audit claim cites the applicable record in
  `projects/elal_rule_traceability.yaml` in its speaker-note evidence; the
  baseline ID is `BASELINE-2026-08-04-ELAL-RULES` unless a later record applies.
