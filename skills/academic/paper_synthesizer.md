# Skill: Paper Synthesizer

**Type:** Domain — Academic
**Applicable agents:** paper_review_agent, ai_trend_radar_agent

## Purpose
Extracts structured, operationally relevant information from academic and industry papers.
Produces a condensed synthesis that highlights: what was done, what was found, what the
limitations are, and why it matters to the user's domains.

## Synthesis Protocol

### Step 1: Paper Metadata
- Title, authors, year, venue
- Type: empirical study / theoretical / survey / industry report
- Availability: open access / paywalled / preprint

### Step 2: Core Structure Extraction
- Research question or problem addressed
- Dataset(s): name, size, domain, timeframe
- Method: algorithm, architecture, or framework used
- Evaluation: metrics and benchmarks
- Key result: headline finding (quantified if possible)

### Step 3: Limitations and Caveats
- What the paper cannot claim
- Generalizability issues (domain, data size, temporal scope)
- Reproducibility: is code available?
- Conflicts of interest (industry-funded research)

### Step 4: Relevance Assessment
Rate relevance to the following user domains:
- Telecom ML / Operations
- AI Governance / MLOps
- Blockchain / Decentralized AI
- TFM topic opportunity

Use: `HIGH / MEDIUM / LOW / NOT APPLICABLE`

### Step 5: TFM Opportunity Flag
If the paper has TFM potential:
- State the angle: replication + extension / application to new domain / critique
- Feasibility: dataset availability, method complexity, 6-month scope fit

## Output Template

```
PAPER SYNTHESIS
───────────────
Title: [...]
Authors: [...] | Year: [...] | Venue: [...]
Type: [empirical / survey / theoretical / industry]

Problem: [one sentence]
Dataset: [name, size, domain]
Method: [algorithm / approach]
Key Result: [quantified finding]

Limitations:
  - [limitation 1]
  - [limitation 2]

Relevance:
  - Telecom ML: [HIGH/MEDIUM/LOW]
  - AI Governance: [HIGH/MEDIUM/LOW]
  - Blockchain AI: [HIGH/MEDIUM/LOW]
  - TFM Opportunity: [YES/NO] — [angle if YES]

Operational Takeaway: [one sentence — what a practitioner should do with this]
```

## Strict Rules
- Never invent citations
- Never invent results that are not in the paper
- If the abstract is the only available text, state: "SYNTHESIS BASED ON ABSTRACT ONLY — verify full paper"
