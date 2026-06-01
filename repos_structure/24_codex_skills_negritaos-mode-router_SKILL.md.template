---
name: negritaos-mode-router
description: >
  Procedure for detecting the NegritaOS operational mode of an incoming request,
  loading the matching agent block from integrator.yaml, merging NegritaOS rules
  with `.codex` adapter rules, and enforcing the output contract. Trigger this
  skill at the start of any non-trivial session in a NegritaOS-managed repository.
metadata:
  scope: repo
  auto_invoke: true
---

# NegritaOS Mode Router — Session-Entry Procedure

Run this 7-step procedure at the **start of every non-trivial session**.

## Step 1 — Detect project
- Read `.codex/project.yaml` → capture `project_id`, `archetype`, `memory_home`.
- If missing, refuse to proceed and ask the user to bootstrap the repo
  (see `repos_structure/50_bootstrap_checklist.md` in NegritaOS).

## Step 2 — Classify mode
Map the user's request to one of the 8 modes:

| Code | Trigger keywords |
|---|---|
| LP | "plan", "scope", "draft outline" |
| AE | "paper", "abstract", "citation", "review literature" |
| TD | "spec", "doc", "ADR", "README" |
| MR | "model review", "metrics", "leakage", "SHAP" |
| CR | "code review", "refactor", "fix bug", "implement" |
| EP | "executive summary", "deck", "slides", "stakeholder" |
| DQ | "data quality", "contract", "validation", "schema" |
| RT | "incident", "on-call", "production down", "triage" |

If ambiguous, ask the user to confirm.

## Step 3 — Load agent block from integrator
- Read `integrator.yaml` (in NegritaOS repo or `~/.negritaos/`).
- Find the agent definition for the classified mode.
- Pull its persona, output contract, and quality bar.

## Step 4 — Merge rules
- Load all rules from `rules/global/` and `rules/<mode>/` (NegritaOS canonical).
- If mode ∈ {MR, CR, DQ}: additionally load `.codex/rules/dev-*.md` adapters
  listed in `.codex/instruction-manifest.yaml`.
- Apply `.codex/local-overrides.md` last.
- On conflict, NegritaOS rules win (see conflict order in router rule).

## Step 5 — Enforce output contract
- Use the output format declared by the agent block in `integrator.yaml`.
- If the mode requires a rubric (`rubrics/<name>.yaml`), include the scoring
  section.

## Step 6 — Quality gate
- Before sending the final response, self-check against:
  - `rules/global/global_rules.yaml` quality bar
  - mode-specific rubric (if any)
  - `.codex/skills/rule-compliance-gate/SKILL.md` (if engineering mode)

## Step 7 — Memory hooks
- If the session produced a durable decision or learning, write to:
  `<memory_home>/sessions/YYYY-MM-DD-<slug>.md`
- Update `<memory_home>/index.md` with the new session and any open threads.
- NEVER write to `.codex/memory/`.
