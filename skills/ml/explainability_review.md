# Skill: Explainability Review

**Type:** Domain — ML
**Applicable agents:** model_review_agent, hot_operations_agent

## Purpose
Reviews model explainability outputs for business meaning, technical validity, and overclaiming risk.

## Checks
- Explainability method is named.
- Global and local explanations are not mixed without warning.
- Feature effects are tied to operational interpretation.
- Proxy, leakage, and missingness risks are called out.
- Recommendations do not exceed what the explanation supports.

## Output
For each explainability finding: claim, evidence, operational meaning, caveat, and recommended follow-up.
