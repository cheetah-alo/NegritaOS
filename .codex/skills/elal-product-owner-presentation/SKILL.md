---
name: elal-product-owner-presentation
description: Required for ELAL PPTX creation, editing, review, audit, or release. Uses the Product Owner reference deck and verifies speaker notes, evidence, and rule governance.
---

# ELAL Product Owner Presentation

## Overview

Use this skill for every ELAL PowerPoint task in the external
`proj_data_analytics/analyses/poc_elal_passenger_journey` project, including a one-slide replacement, a
rule-review deck, an Arik-audit deck, a Product Owner brief, or a release
check. It makes the designated Product Owner deck the mandatory visual and
speaker-notes reference and keeps ELAL rule claims evidence-bound.

## Non-bypass gate

Before creating, editing, reviewing, or releasing an ELAL PPTX, read:

1. The external project's `.codex/project.yaml` and the canonical
   `projects/proj_data_analytics.yaml` registry in NegritaOS.
2. `projects/elal_presentation_governance.md`.
3. `projects/elal_presentation_artifact_register.yaml`.
4. `projects/elal_rule_traceability.yaml` for
   every rule, audit, score, source, outcome, or treatment claim.
5. The relevant current handoff and rule/data contracts.
6. The system `presentations` skill and its template-following instructions.

The authoritative reference is exactly:

`/Users/jackyb-cqi/repos/proj_data_analytics/analyses/poc_elal_passenger_journey/documents/elal_passenger_journey_product_owner_summary_44slides_20260804_final_no_text_frames.pptx`

Its filename says `44slides`, but the inspected artifact contains **46 slides and
46 notes**. Identify it by this path and the SHA-256 recorded in
`projects/proj_data_analytics.yaml`, never by its filename's slide count.

If the file is unavailable, the hash does not match, the exact closed source has
not been confirmed by Jacky, or the file is open in PowerPoint, stop. Ask for
the exact closed source path. Do not substitute a similar-looking deck and do
not create a detached design.

## Mandatory source and editing workflow

1. Inspect the reference deck, all of its slides, its layouts, and its notes.
   Use the existing masters/layouts and build a frame map before making changes.
2. For an edit, duplicate the user-confirmed closed PPTX first. Never save into
   the reference deck, an open PPTX, or a legacy deck in place.
3. Duplicate reference slides and edit inherited elements in place. Preserve the
   16:9 `2048 x 1152` canvas, cobalt left rail, light content footer, dark
   section/`ACTO` dividers, and the Poppins / Noto Sans / IBM Plex Mono hierarchy.
   Do not rebuild an approximation from blank slides.
4. Use the semantic register to select supporting decks by discussion theme; it
   is an index, not permission to declare a candidate, a filename containing
   `final`, or an earlier V10 deck as the active policy.
5. Render every produced slide and inspect the full deck before release. Check
   overflow, overlaps, clipping, font substitution, layout drift, and empty
   placeholders.

## Speaker-notes contract

Every delivered slide must have exactly one speaker-note entry containing both
complete, paired blocks:

```text
[Talk track]
What the presenter should say, including decision wording and caveats.
[/Talk track]
[Evidence]
Source: ...
Window: ...
Grain: ...
Population and denominator: ...
Deduplication / association: ...
Evidence status: OBSERVED | CANDIDATE | SHADOW | APPROVED
Limitation: ...
Allowed conclusion: ...
[/Evidence]
```

The reference deck has notes on all 46 slides, but its marker pairs are not
fully closed on slides 7, 9, 25, 26, 28, and 46. Preserve that source as-is;
do not copy this defect. New or changed slides must meet the complete-pair
contract above. A release fails if note count differs from slide count or if a
required block is absent or unpaired.

## ELAL decision and evidence guardrails

1. Use the discussion order: evidence coverage and grain; observed signals;
   current productive rules; candidate rules and measured impact; owner decision
   and next gate.
2. Keep `CALLS.calls_fric_prom_w_metadata` as the active EDA call rail.
   `CALLS.ia_calls` is deprecated for this EDA. Never create a broad additive
   union or `FULL OUTER JOIN` between call rails.
3. A transcript `resolved`/`acknowledged` signal is not a verified operational
   outcome. `Seat Overbooking` is shadow-only until its operational taxonomy,
   identity, deduplication, precedence, points, and owner approvals are governed.
4. Tier changes treatment, priority, outreach, escalation, or SLA; it does not
   change the underlying pressure score without explicit ELAL policy approval.
   The severe chip remains context and does not change color directly.
5. Label same-date V9/V10 comparisons as reclassification crosswalks, not
   temporal transitions. The available 31-May snapshot does not prove recovery,
   flapping, or prior-day movement.
6. Do not turn a backtest, candidate, or Arik agreement into production policy,
   accuracy, or an approved rule. State the required gate in the slide and its
   notes.

## Release evidence

Record the exact source PPTX path and hash, source and output slide counts,
source and output note counts, render/overflow result, and which discussion
topic from the artifact register was used. For a rule or audit claim, record
the applicable traceability ledger change ID in the `[Evidence]` note (use
`BASELINE-2026-08-04-ELAL-RULES` only when no later change applies) and state
the controlled rule status. Do not move, rename, delete, or overwrite client
PPTX artifacts as part of organization work.
