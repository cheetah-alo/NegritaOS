---
id: plain-language
domain: writing
enforcement: strict
depends_on:
  - ai-behavior
provides:
  - clear-technical-language
  - jargon-control
  - concise-user-facing-output
description: >
  Requires clear, plain, evidence-preserving language in user-facing
  NegritaOS output.
version: 1.0.0
applyTo: [agents, documentation, reviews, reports, plans, summaries]
priority: critical
---

# Plain Language

User-facing NegritaOS output must be clear, concise, and useful.

## Required Behavior

- Put the answer, decision, or action first.
- Use short sentences and short paragraphs.
- Prefer active voice.
- Use one idea per sentence when the content is procedural or high-risk.
- Explain unavoidable jargon the first time it appears.
- Keep commands, paths, filenames, metrics, dates, IDs, and status labels exact.
- Keep uncertainty, evidence gaps, and blockers visible.

## Precision Boundary

Plain language must not reduce technical truth.

Never remove or soften:

- security, privacy, legal, data, financial, production, or academic caveats;
- failed or missing validation;
- `UNVERIFIED`, `CONTRACT_INCOMPLETE`, `CANDIDATE_SHADOW`, or `BLOCKED_*`
  states;
- source, test, coverage, or reproducibility requirements.

## Prohibited Patterns

- Long preambles before the answer.
- Generic AI filler.
- Decorative metaphors.
- Jargon used when a precise plain term is enough.
- More than two decision options unless the user asks for a fuller tradeoff.
- Saying a task is done when the original user-visible path or required
  validation has not passed.
