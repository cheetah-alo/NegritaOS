---
id: confidence-gate
mode_hint: LP   # Localized Planning
loads:
  - rules/global/negritaos_router_rule.md
  - .codex/instruction-manifest.yaml
  - rules/dev-coding-standards.md
---

# Confidence Gate (95% rule)

Use BEFORE writing any code or modifying any file.

## Objective

Do not make any changes until you have **≥95% confidence** on what needs to be built.
Ask follow-up questions until that confidence is reached.

## Procedure

1. **Detect mode** via the NegritaOS router (LP / AE / TD / MR / CR / EP / DQ / RT).
   - Default to `LP` (Localized Planning) for this gate.
   - If the project has a `mode_map` in `projects/<project>.yaml`, honor it.

2. **State your current understanding** in 3 blocks:
   - **Goal** — what the user wants in one sentence.
   - **Scope** — files/modules/services in/out of scope.
   - **Constraints** — rules from `.codex/rules/` that bind the change
     (naming, file size 1500/1700, security, commit-hygiene, tests).

3. **List unknowns** as numbered questions. For each question, mark:
   - `BLOCKING` — must be answered before any edit.
   - `ASSUMPTION` — proceed with a default, document it, flag for review.

4. **Estimate confidence** explicitly:
   ```
   Confidence: NN%
   Blocking unknowns: N
   Assumptions taken: N
   ```

5. **Decision rule**:
   - If `confidence < 95%` OR any `BLOCKING` unknown remains → STOP and ask.
   - If `confidence ≥ 95%` → produce a 5-line plan and request go-ahead.

## Stop conditions

- Requirements conflict between two `.codex/rules/dev-*.md` files → escalate
  per `ai-behavior.md` §9.
- The change would break a dataset contract (`configs/contracts/*.json`)
  without an explicit version bump.
- Test coverage would drop below the tier floor
  (40% prototype / 60% MVP / 80% production).

## Output contract

A single message containing: **Goal / Scope / Constraints / Unknowns / Confidence / Decision**.
No code edits, no tool calls that mutate files.
