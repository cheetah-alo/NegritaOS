# Skill: Executive Summary Writer

**Type:** Domain — Executive
**Applicable agents:** presentation_agent, technical_writer_agent, decision_support_agent

## Purpose
Compresses technical analysis into a concise, decision-oriented summary for
senior, non-technical, or time-constrained audiences. The executive summary
does not explain methodology — it communicates the verdict and what to do about it.

## Structure

```
EXECUTIVE SUMMARY

Situation:
[1-2 sentences: business context and what triggered this analysis]

Finding:
[1-3 bullet points: the most important results, expressed in business terms]
  - Avoid: "AUC of 0.82"
  - Use: "The model correctly identifies 7 in 10 customers at churn risk within the next 30 days"

Implication:
[1-2 sentences: what does this finding mean for a decision or plan?]

Recommended Action:
[1-3 bullet points: specific, owner-assignable actions]
  - Each action: [What] + [Who] + [By When if known]

Risk of Inaction:
[Optional — 1 sentence: what happens if nothing is done?]
```

## Length Constraints
- Maximum: 1 page or ~400 words
- No tables, no charts, no code blocks
- Acronyms must be defined on first use
- All monetary or percentage claims must include the measurement basis

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|---|---|
| "Results were promising" | No specificity. Tells reader nothing actionable |
| Long methodology description | Executives need verdict, not derivation |
| "We recommend further study" | Not actionable without a specific next step |
| Passive voice throughout | Obscures ownership and accountability |
| Jargon without definition | Creates distance, not credibility |

## Audience Calibration

| Audience | Jargon Level | Detail Level | Focus |
|---|---|---|---|
| C-Suite / Board | None | Minimal | Business impact + decision |
| VP / Director | Low | Moderate | KPI + recommendation |
| Senior Manager | Medium | Moderate | Findings + actions |
| Technical Lead | High | Full | Methods + evidence |
