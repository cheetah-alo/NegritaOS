# Skill: Research Paper Findings

**Type:** Domain — Academic / Research  
**Applicable agents:** paper_review_agent, presentation_agent, ai_trend_radar_agent

## Purpose
Converts research papers into findings that separate what the paper shows,
what it does not show, and how it can be used in applied work.

## Required Finding Contract

Each paper finding must include:

- paper/source
- research question
- methodology
- evidence strength
- main result
- limitation or validation note
- relevance to user domain
- implementation or research implication

## Rules

- Never invent citations, datasets, metrics, or results.
- If only abstract text is available, label the synthesis as abstract-only.
- Separate paper claims from your interpretation.
- Generalizability, reproducibility, and conflict-of-interest risks must be visible as notes.
- A paper can inspire a proposal without being production-ready evidence.

## Output Pattern

```text
Finding:
Paper evidence:
Method:
Evidence strength:
Note:
Relevance:
Potential use:
Source:
```
