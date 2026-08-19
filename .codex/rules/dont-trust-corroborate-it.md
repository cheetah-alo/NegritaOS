---
id: dont-trust-corroborate-it
domain: evidence-governance
enforcement: strict
priority: critical
depends_on:
  - ai-behavior
provides:
  - evidence-corroboration
  - source-backed-technical-claims
description: >
  Adapter-discoverable rule requiring factual, data, technical, analytical,
  and documentation claims to be corroborated with trustworthy evidence before
  they are presented as true.
version: 1.0.0
applyTo: [repo, agents, prompts, claude, codex, copilot]
---

# Don't Trust. Corroborate It.

Use this rule whenever an agent states something about data, technical behavior,
repository state, external concepts, standards, model results, plots, or
deliverable quality.

## Contract

- Treat LLM output as a hypothesis until corroborated.
- For repository facts, cite inspected files, commands, diffs, tests, or
  manifests.
- For data claims, cite the query, source contract, row counts, grain,
  denominator, filters, freshness, and validation status.
- For technical concepts, prefer official documentation, primary sources, or
  current local package/tool output.
- For documents, PPTX, DOCX, PDF, and plots, inspect the actual artifact or
  rendered output before declaring quality, formatting, or readiness.
- If evidence is missing, mark the claim `UNVERIFIED`,
  `CONTRACT_INCOMPLETE`, `HYPOTHESIS`, or `BLOCKED_EVIDENCE` as appropriate.

## Anti-Patterns

- Do not present memory, prior chat, or model recall as current truth without
  validation.
- Do not infer data correctness from a successful script run alone.
- Do not claim CI, coverage, browser, BigQuery, publication, or rendering passed
  unless the exact check was executed or its current result was inspected.
- Do not turn a plausible explanation into a fact when the source has not been
  checked.

The global evidence policy also lives in
[rules/global/global_rules.yaml](../../rules/global/global_rules.yaml).
