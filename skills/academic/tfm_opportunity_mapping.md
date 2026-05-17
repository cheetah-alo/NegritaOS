# Skill: TFM Opportunity Mapping

**Type:** Domain — Academic
**Applicable agents:** ai_trend_radar_agent, paper_review_agent, research_radar_agent

## Purpose
Converts research signals — papers, tools, gaps, trends — into viable TFM topic candidates.
A viable TFM topic is: scoped, feasible in 6 months, academically novel, practically relevant,
and addressable with publicly available data.

## TFM Viability Criteria

| Criterion | Requirement |
|---|---|
| Scope | Completable by one student in 4–6 months |
| Novelty | Not a direct replication of an existing thesis with same dataset and method |
| Data | Public dataset available OR access plan is realistic |
| Method | Does not require compute resources beyond student access (GPU optional, not required) |
| Relevance | Connected to an applied domain: Telecom, Finance, Healthcare, Logistics |
| Measurability | Success can be defined with a metric |

## Topic Card Format

```
TFM TOPIC CANDIDATE
───────────────────
Title Candidate: [Draft title — domain + problem + method]

Problem Statement:
  [2-3 sentences: what gap or need does this address?]

Proposed Approach:
  [Method or framework to be applied]

Dataset Candidates:
  - [dataset name] — [source] — [public/restricted]

Success Metrics:
  - [metric 1]
  - [metric 2]

Novelty Claim:
  [What makes this different from existing work?]

Risks:
  - [risk 1]: [mitigation]
  - [risk 2]: [mitigation]

Viability Score: [HIGH / MEDIUM / LOW]
Viability Notes: [brief justification]

Related Papers:
  - [paper 1]
  - [paper 2]
```

## Prioritization Rules

Prefer topics that:
- Apply established methods to underexplored domains (higher success probability)
- Have reproducible baselines in the literature
- Connect to active industry problems (Telecom churn, fraud, network operations)
- Can be extended in multiple directions (publishable potential)

Avoid topics that:
- Require novel algorithm design (scope too large for TFM)
- Depend on restricted datasets with no access plan
- Are direct replications with no differentiation
- Have been exhaustively covered in recent TFM databases
