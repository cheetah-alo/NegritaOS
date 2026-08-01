# Skill: Analytics Storytelling Deck

**Type:** Domain — Executive / Analytics  
**Applicable agents:** presentation_agent

## Purpose
Turns validated analytical findings into a decision-ready deck. The deck must
start with the answer, then show how the answer was calculated, and only then
zoom into evidence layers.

For CQI/CQISense analytical PowerPoint delivery, this is the narrative layer.
Apply `.codex/skills/cqi-analytical-pptx/SKILL.md` after this skill for brand,
template, evidence-notes, release QA, and optional podcast contracts.

## Required Story Order

Use this order unless the user explicitly provides a different deck structure:

1. Executive findings first.
2. Baseline and calculation alignment.
3. Data decomposition by population, channel, processing state, or segment.
4. Broad signal layer.
5. Family layer.
6. Subcategory layer.
7. Attribute layer.
8. Context overlays such as reason, satisfaction, duration, resolution, or journey position.
9. Interactions or sequences.
10. Archetypes, mechanisms, or operational interpretation.
11. Recommended action, productization, dashboard, or next decision.

## Slide Contract

Every analytical slide must include:

- Finding headline: a complete sentence, not a chart label.
- Base population and denominator.
- Metric window and direction when relevant.
- Nominal support (`n`) or support threshold.
- Overall or baseline reference when rates/lifts are compared.
- Note: what not to overclaim, missing context, or validation need.
- Speaker note: how to explain the calculation and takeaway.

## Readability Contract

- Font: use `rules/presentation/presentation_rules.yaml`.
- For CQI/CQISense analytical decks, load
  `.codex/skills/cqi-analytical-pptx/SKILL.md`.
- For new CQI/CQISense decks, use
  `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx`.
- For existing decks, preserve the source deck canvas, masters, layouts,
  cobalt rail, cover, and inherited footers.
- Body and table cells: minimum 16 pt.
- Axes, legends, and labels: minimum 12 pt.
- Visible sources, notes, and metadata: minimum 10 pt.
- Footer text may be smaller if it does not carry the main finding.
- If a table cannot fit at these sizes, split it or convert it to cards/bullets.
- Do not use dense tables as executive slides when cards or KPI strips are clearer.

## Analytical Role Mapping

Do not preserve domain labels blindly. Map every dataset to analytical roles:

- population
- unit of analysis
- baseline
- signal layer
- family
- subcategory
- attribute
- context overlay
- interaction or sequence
- outcome
- validation metric

If the unit changes, the interpretation changes. Call-level, account-level,
event-level, and sequence-level rates must not be described as equivalent.

## Output Skeleton

For each slide:

```text
Slide N:
  Finding:
  Evidence object:
  How calculated:
  Base / denominator:
  Main KPI(s):
  Note:
  Speaker note:
  Transition:
```

For CQI analytical slides, the speaker note must also include the structured
`[Evidence]` block defined by `cqi-analytical-pptx`.
