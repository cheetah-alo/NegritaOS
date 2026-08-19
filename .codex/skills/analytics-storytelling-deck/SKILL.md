---
name: analytics-storytelling-deck
description: Use when creating analytical PPTs, executive decks, steering decks, finding decks, or storylines from data, plots, model outputs, or research evidence. Enforces finding-first storytelling, baseline/calculation alignment, broad-to-narrow analytical zoom, and readable PPT constraints.
metadata:
  scope: [presentation, deck, ppt, analytics, storytelling, findings]
  auto_invoke:
    - when creating or editing analytical presentation decks
    - when turning EDA or model findings into slides
    - when building a story from plots, tables, or metrics
---

# Analytics Storytelling Deck

Apply the canonical NegritaOS skill at `skills/executive/analytics_storytelling_deck.md`.

Core rules:

- Start with findings, then baseline/calculation alignment.
- Include an agenda immediately after the cover.
- New or materially rewritten analytical decks use 10 to 80 total slides,
  including appendices. Do not impose audience-specific or per-section caps.
- Apply `skills/executive/presentation_evidence_reuse.md`: reuse existing
  run-scoped evidence by default and never run queries for deck-only changes.
- Move broad to narrow: population → signal layer → family → subcategory → attribute → context overlays → interactions/sequences → mechanism/action.
- Use `note`, not `caveat`.
- Font: follow `rules/presentation/presentation_rules.yaml`.
- For CQI/CQISense analytical decks, load `.codex/skills/cqi-analytical-pptx/SKILL.md` after this skill.
- For new CQI/CQISense decks, use `brands/cqi/plantillas/CQI_PresentationTemplate_20260401.pptx`; for existing decks, preserve the source deck canvas and inherited template.
- Minimum sizes: body/table cells 16 pt, axes/legends/labels 12 pt, visible sources/notes/metadata 10 pt.
- If a table cannot fit at those sizes, split it or convert it to cards/bullets.
- Every analytical slide needs finding, how calculated, base/denominator, KPI window, `n`/support, note, and speaker note.
- CQI analytical slides also need the structured `[Evidence]` speaker-notes block required by `cqi-analytical-pptx`.
