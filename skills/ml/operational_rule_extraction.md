# Skill: Operational Rule Extraction

**Type:** Domain — ML / Operations
**Applicable agents:** model_review_agent

## Purpose
Converts analytical findings into operational rules without overstating model certainty.

## Rule Format
```
Rule:
  trigger: [observable condition]
  action: [recommended operational response]
  owner: [role or TBD]
  evidence: [source finding or chart]
  caveat: [limit or validation need]
```

## Rules
- Do not convert correlations into hard policy without validation.
- Keep thresholds traceable to data.
- Mark uncertain rules as candidates.
