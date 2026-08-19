---
name: plain-language-rewrite
description: >
  Restate dense, jargon-heavy, or overexplained technical content in plain
  human language while preserving facts, evidence, paths, commands, numbers,
  caveats, and decision constraints.
license: Apache-2.0
metadata:
  author: NegritaOS
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "User asks to re-explain, simplify, shorten, de-jargon, say it plainly, or answer quickly"
    - "User invokes /bro, /wait-what, /quick, sin jerga, habla humano, or explica simple"
---

# Plain Language Rewrite

Use this skill when the user asks for a clearer restatement of a previous
answer, technical note, report section, PR review, or documentation draft.

This skill changes the delivery, not the underlying facts.

## Modes

- `/bro` or `sin jerga`: rewrite the same message in plain human language.
- `/wait-what`: explain the missing context that made the message hard to use.
- `/quick`: give the action first, then short numbered steps and one next step.

Equivalent natural-language triggers are valid: `reexplica`, `mas simple`,
`habla claro`, `no jargon`, `answer fast`, or `solo lo necesario`.

## Hard Rules

- Preserve exact paths, commands, identifiers, dates, counts, branch names,
  filenames, metrics, and status labels.
- Keep evidence boundaries intact. Do not make uncertain claims sound proven.
- Keep security, data, legal, medical, financial, and production caveats when
  they materially affect the decision.
- If the original answer contained a blocker, keep the blocker visible.
- Use short sentences and active voice.
- Put the answer or action first.
- Use at most two options when the user must decide.

## Do Not

- Remove required warnings, test failures, validation gaps, or risk labels.
- Convert `UNVERIFIED`, `CONTRACT_INCOMPLETE`, `CANDIDATE_SHADOW`, or
  `BLOCKED_*` states into softer wording.
- Replace precise technical names with vague words when the exact name matters.
- Add metaphors or personality filler.
- Invent simpler facts to make the answer easier.

## Output Shape

Prefer this structure:

1. Direct answer.
2. What changed or what matters.
3. What the user needs to do next.

For a rewrite of a prior response, do not add new analysis unless the user asks
for it. If the prior response was wrong or unsafe, say so and correct it.
