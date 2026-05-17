# Skill: Notion Report Writer

**Type:** Domain — Writing
**Applicable agents:** technical_writer_agent

## Purpose
Produces Notion-ready technical reports with consistent structure, appropriate formatting,
and operational clarity. The output must be paste-ready into Notion with minimal reformatting.

## Relationship to Presentations

When the document is generated from the same analytical material as a presentation,
use `rules/presentation/findings_contract.yaml` as the shared source of truth.

- The presentation is the decision-ready narrative.
- The Notion document is the auditable, source-traceable record.
- Findings, risks, recommendations, and next actions must not contradict the deck.
- If the target audience is `ceo_product_owner`, keep the Notion TL;DR executive-first and move methodology into a later section.
- If the target audience is `data_scientist_peer`, include assumptions, validation detail, and reproducibility notes.

## Document Structure

```
# [Document Title]

> **TL;DR:** [1-3 sentence callout — verdict + action]

---

## Context
[Why this document exists. What triggered it. What the scope is.]

## Objective
[What specific question or task this document addresses.]

## [Analysis / Findings / Review — section name varies by document type]
[Main content. Use H3 for subsections. No more than 2 nesting levels.]

Each finding should follow:
- **Finding:** [claim]
- **Evidence:** [metric/chart/table/source path]
- **Implication:** [why it matters]
- **Caveat:** [limitation or uncertainty]
- **Recommendation:** [action if any]

## Risks and Caveats
[What could be wrong with the findings. What assumptions were made.]

## Recommendations
[Specific, owner-assignable actions derived from findings.]

## Next Actions

| Action | Owner | Timeline | Status |
|--------|-------|----------|--------|
| [action 1] | [role] | [date/sprint] | Open |
| [action 2] | [role] | [date/sprint] | Open |

---

*Document version: [x.x] | Author: NegritaOS | Date: [YYYY-MM-DD]*
```

## Formatting Rules for Notion

- Use `>` for callout blocks (TL;DR, warnings, hypotheses)
- Use `---` as section dividers
- Use tables instead of long bullet lists where applicable
- Code blocks: use triple backtick with language specifier
- Inline `code` for: field names, table names, metric names, function names
- No nested bullets beyond 2 levels
- Each H2 section must have content — no empty headers

## Content Rules

- TL;DR must be the first thing in the document, in a callout block
- Every section must connect to the document objective
- Orphan sections (sections with no connection to the objective) are a quality gate failure
- Next Actions table must have an Owner column — if unknown, write "TBD — [role recommendation]"

## Anti-Patterns

- Using headers as labels without content under them
- Bullets that end with a colon and no continuation
- Mixing executive summary narrative with raw data tables
- Findings section that is just a list of metrics without interpretation
