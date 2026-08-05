# ELAL Analytical Deck Profile

## Purpose

Apply this profile only for ELAL passenger-journey analytical decks. It defines
structural semantics, not frozen numbers, dates, rule counts, or slide counts.

## Scope

This profile extends `cqi-analytical-pptx` and `elal-eda-governance`. It does
not import Hot Orange, churn, archetype, or unrelated telecom semantics into
ELAL decks.

## Structural Rules

- Separate call-level analysis, exact member links, candidate associations, and
  no-match populations.
- Show `Other/Unknown` explicitly when tier, rule family, segment, or category
  coverage is incomplete.
- Use the tier recorded in the event for rule by month by tier views.
- Treat full tier-history reconstruction as a separate data requirement.
- Keep v9 as four segments, including Critical.
- Explain v10 base, v10 final, buffer/guardrail, and chip as separate concepts.
- Do not mix chip and segment.
- Present overbooking through parallel reconciliations that are not additive.
- Apply S3 candidates only to events already classified as `F_NEG_08`.
- Keep production rules and shadow candidates visually and semantically
  separate.
- Treat the near-flight caller evidence as an identity-alignment surface:
  the operational event remains member-level, but a call matched through a
  phone owned by 2--4 members is `CANDIDATE_SHADOW`, not a confirmed individual
  member call. Phone ownership greater than four and missing phones are not
  member coverage. A unique, time-appropriate approved identity bridge is
  required for confirmed member reach.
- Do not change a productive `F_NEG_08` point value or predicate from an
  analytical deck. Until near-flight identity alignment is approved, report
  its reach, points and v9/v10 contribution separately as confirmed,
  candidate shared-phone and not-observable coverage. Add a visible
  alignment note stating that the production rule is unchanged and naming the
  decision needed to promote candidate coverage.
- Describe a 13-month view as monthly pattern or seasonal context, not proven
  seasonality.
- Annotate exceptional events only with official sources and without automatic
  causal attribution.

## Slide Pattern Per Rule

Each rule slide must support:

1. human rule name as the primary reading cue;
2. SQL code as secondary reference;
3. points;
4. predicate and effective condition;
5. precedence or first-match behavior;
6. monthly events;
7. monthly members stacked by tier;
8. period-level deduplicated totals;
9. visible `Other/Unknown`;
10. note distinguishing rule reach from causal effect.

Concrete numbers, rule counts, windows, candidate labels, and slide counts must
come from a delivery manifest or configuration. They are not global defaults.
