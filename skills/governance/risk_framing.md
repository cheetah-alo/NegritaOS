# Skill: Risk Framing

**Type:** Domain — Governance
**Applicable agents:** team_lead_ds_agent, decision_support_agent, data_quality_sentinel_agent

## Purpose
Ensures that risks in any output are expressed in a structured, actionable format.
A risk that is not quantified, owned, and mitigated is just anxiety in writing.

## Risk Entry Format

```
Risk: [Short label]
Description: [What could go wrong and in what conditions]
Severity: [HIGH / MEDIUM / LOW]
Likelihood: [HIGH / MEDIUM / LOW]
Business Impact: [Quantified or bounded estimate if possible]
Owner: [Role or person responsible for monitoring / mitigating]
Mitigation: [Specific action to reduce probability or impact]
Residual Risk: [What remains after mitigation]
Status: [OPEN / MITIGATED / ACCEPTED / MONITORING]
```

## Severity x Likelihood Matrix

| | HIGH Likelihood | MEDIUM Likelihood | LOW Likelihood |
|---|---|---|---|
| HIGH Severity | CRITICAL — act immediately | HIGH — plan mitigation | MEDIUM — monitor |
| MEDIUM Severity | HIGH — plan mitigation | MEDIUM — document | LOW — log |
| LOW Severity | MEDIUM — document | LOW — log | NEGLIGIBLE |

## Risk Categories for NegritaOS Domains

### ML Risks
- Data leakage (severity: CRITICAL)
- Model drift without monitoring
- Biased training data producing discriminatory outputs
- Overclaimed operational rules
- Reproducibility failure

### Data Quality Risks
- KPI computation on corrupted source
- Schema changes propagated silently to production models
- Imputation masking structural data absence

### Delivery Risks
- Dependency on a single team member
- Scope creep without stakeholder acknowledgment
- Timeline not accounting for data access delays

### Governance Risks
- Model deployed without auditability documentation
- Regulatory non-compliance (GDPR, AI Act) in model design
- Experiment not tracked — cannot reproduce or audit

## Anti-Patterns in Risk Framing

- "There may be risks related to data quality" — too vague
- Risk listed without owner — unactionable
- "Risk: low" without mitigation — not useful
- Risk identified but no residual risk assessed — incomplete
