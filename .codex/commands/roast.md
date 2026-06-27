---
id: roast
mode_hint: LP
loads:
  - skills/transversal/roast.md
---

# Roast

Runs the NegritaOS roast council for an idea, product direction, analytical
proposal, business model, or implementation plan.

## When to use

- The user says `/roast`.
- The user asks to pressure-test, stress-test, red-team, or get a brutal second
  opinion on an idea.
- The user asks to convene the council before investing time or money.

## Procedure

1. Load `skills/transversal/roast.md`.
2. Use the user's command arguments as the idea brief when present.
3. If the brief is incomplete, ask only the short context questions required by
   the skill.
4. Run the five-perspective council and Judge synthesis exactly as specified by
   the skill.

## Output contract

Return the roast verdict in the skill's required format:

- `GO`, `RESHAPE`, or `KILL`
- confidence
- one-line call
- why
- biggest risk
- biggest upside
- money read
- cheapest 48-hour test
- council scores

Do not write files or memory unless the user separately asks to preserve the
decision.
