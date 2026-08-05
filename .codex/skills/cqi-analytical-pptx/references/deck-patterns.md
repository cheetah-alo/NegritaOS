# CQI Analytical Deck Patterns

## Purpose

Define reusable CQI analytical presentation patterns for stakeholder decks,
technical readouts, EDA findings, model-readiness reviews, and decision briefs.

## Required Slide Types

### Cover

- Dark navy background.
- Short title and decision question.
- Two to four numbered agenda bullets or decision pillars.
- Footer with CQI/CQISense, team, date, and slide count when known.

### Executive Summary

- White background with CQI cobalt left rail.
- Finding-first title.
- Three to five KPI cards.
- One dark decision or takeaway block.
- Do not combine incompatible populations or denominators.

### Section Divider

- Dark navy background.
- Section title and one-line purpose.
- Numbered topics, gates, or decision areas.
- Use the divider to reset the analytical level: population, source, signal,
  mechanism, decision, or appendix.

### Analytical Finding

- Kicker/context line.
- Finding-first title.
- Subtitle declaring denominator, window, grain, or interpretation boundary.
- Main visual: chart, table, heatmap, flow, or comparison.
- Bottom takeaway band with the strongest allowed conclusion.
- Footer with source, grain, window, and slide number.

### Decision

- Explicit recommendation.
- What is approved.
- What is not approved.
- Open owner questions or gates.
- Evidence status and next action.

### Appendix / Detail

- Table, query summary, rule details, or diagnostic plot.
- Visible source, grain, denominator, and interpretation limit.
- Keep it audit-friendly; do not hide caveats in small text.

## Slide Anatomy

Every analytical slide should expose:

1. finding-first title;
2. calculation or evidence context;
3. declared grain;
4. declared denominator;
5. main visual;
6. takeaway/note band;
7. footer source/window metadata;
8. speaker notes with the structured `[Evidence]` block.

## Visual System

- Use the CQI cobalt rail on white analytical slides.
- Use navy section dividers.
- Use KPI cards with declared color roles.
- Use IBM Plex Mono for metrics, SQL codes, field names, hashes, identifiers,
  and tabular numbers.
- Prefer one clear visual per slide.
- Split the slide when the content cannot fit at readable sizes.

## Evidence Discipline

- Do not use a chart title to overclaim beyond the underlying grain and
  denominator.
- Keep source rails separate unless join-safety evidence is declared.
- If a table, rate, or chart comes from a candidate bridge, label it as
  candidate/review, not approved.
- Use `note`, `limitation`, or `allowed conclusion`; avoid vague caveat text.
