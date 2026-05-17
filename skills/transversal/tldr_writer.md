# Skill: TL;DR Writer

**Type:** Transversal
**Applicable agents:** All (mandatory for outputs > 300 words)

## Purpose
Produces a concise, decision-oriented summary that stands alone at the top of any
substantial output. The TL;DR must be readable by a non-technical stakeholder and must
communicate: what was done, what was found, and what action is required.

## TL;DR Structure

```
TL;DR

[1-2 sentences: What was reviewed / analyzed / produced]
[1-2 sentences: The key finding or verdict]
[1 sentence: The recommended action or decision required]
```

## Length Constraint

- Minimum: 3 sentences
- Maximum: 6 sentences / ~120 words
- No bullet points inside TL;DR
- No jargon without brief inline definition

## Quality Tests

A good TL;DR passes these tests:
1. Can a non-technical manager read it and understand what to do next?
2. Does it contain the word "this" as a placeholder for something not defined? (fail if yes)
3. Does it reference a finding that does not appear in the body? (fail if yes)
4. Is it a copy-paste of the introduction? (fail if yes — TL;DR summarizes conclusions, not setup)

## Examples

**Bad TL;DR:**
> "This document provides an analysis of the churn model and discusses various aspects including feature importance, model performance, and some recommendations."

Problems: no verdict, no action, generic, describes the document not the findings.

**Good TL;DR:**
> "This report reviews the XGBoost churn model trained on Q1 2025 customer data.
> The model achieves 0.82 AUC-ROC on holdout but shows signs of temporal leakage in the
> `days_since_last_contact` feature, which was derived post-churn event.
> The leakage must be resolved before this model is deployed to production."

## Placement
Always at the top of the document, before any section headers.
Formatted as a highlighted callout block in Notion/Confluence outputs.
