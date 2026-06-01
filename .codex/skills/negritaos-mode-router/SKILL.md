---
name: negritaos-mode-router
description: >
  Procedure for detecting the NegritaOS operational mode of an incoming
  request, loading the matching agent block from integrator.yaml, merging
  NegritaOS rules with `.codex` adapter rules, and enforcing the output
  contract. Trigger this skill at the start of any non-trivial session in a
  NegritaOS-managed repository.
version: 1.0.0
---

# Skill: NegritaOS Mode Router

This skill operationalizes the rule
[rules/global/negritaos_router_rule.md](../../../rules/global/negritaos_router_rule.md).
It tells an agent client *how* to enter a session correctly.

## When to invoke

Invoke this skill when ANY of the following is true:

- A new chat session starts in this repository.
- The request matches one of the 8 mode trigger lists in
  [core/orchestration/metaagent_router.yaml](../../../core/orchestration/metaagent_router.yaml).
- The user mentions an agent name from
  [integrator.yaml](../../../integrator.yaml).
- The user asks for `notion`, `confluence`, `deck`, `slides`, `paper review`,
  `code review`, `model review`, `escalation`, `roadmap`, or `TFM`.
- The current task crosses mode boundaries (e.g. model review + executive
  presentation).

## Step 1 — Detect the project

1. Read `.codex/project.yaml` (this repo's adapter pointer).
2. Read the canonical registry referenced there: `projects/<project_id>.yaml`.
3. Note the `agents`, `archetypes`, and `expected_outputs` declared.

If `.codex/project.yaml` is missing, the active project is `negritaos` and
the registry is [projects/negritaos.yaml](../../../projects/negritaos.yaml).

## Step 2 — Classify the mode

Match the request against the mode triggers in
[core/orchestration/metaagent_router.yaml](../../../core/orchestration/metaagent_router.yaml).
Apply the policy declared at the top of that file:

- `ambiguity_handling: classify_to_closest_mode_and_state_assumption`
- `multi_mode_threshold: if_two_or_more_modes_detected_use_pipeline`
- `fallback_mode: technical_documentation`

State the chosen mode explicitly in the response if non-obvious.

## Step 3 — Load the agent block

From [integrator.yaml](../../../integrator.yaml) → `agents.<agent_id>`,
read and apply:

- `persona`
- `skills`
- `rules`
- `rubrics`
- `templates`
- `output_modes`
- `quality_gate`

The agent's `rules` list is **authoritative** for this turn. They are
NegritaOS-native (e.g. `rules/ml/ml_rules.yaml`), not `.codex/rules/dev-*.md`.

## Step 4 — Merge with adapter rules (engineering modes only)

If the active mode is **MR**, **CR**, or **DQ**:

1. Load the active codex profile from `.codex/profiles/`.
2. Load the rules it activates from `.codex/rules/`.
3. Merge with NegritaOS rules using the conflict order from the canonical
   router rule (NegritaOS wins).

If the active mode is **AE**, **RT**, **EP**, **LP**, or **TD**:

- Do NOT load `.codex/rules/dev-*.md`. Use NegritaOS skills only.

## Step 5 — Enforce the output contract

From [integrator.yaml](../../../integrator.yaml) →
`default_output_contract`:

- `analytical_report`: required sections from TLDR through Next_Actions.
- `plot_interpretation`: required fields (what_it_shows, how_to_read_it,
  why_it_matters, operational_takeaway).
- `task_output`: required fields (objective, scope, inputs, outputs,
  dependencies, risks, acceptance_criteria).

The output type comes from the agent's `output_modes`. Refuse to skip
required sections; if information is missing, mark it explicitly.

## Step 6 — Quality gate self-check

Before sending the response, walk through `quality_gate` of the active
agent. If any gate item fails, either fix the response or annotate the
unmet criterion + remediation in the output.

## Step 7 — Memory hooks

After meaningful durable work, follow the `memory-protocol` skill and
write to `~/.negritaos/memory/projects/<project_id>/`, not to
`.codex/memory/`.

## Multi-mode pipelines

If two or more modes are detected, execute them in the order declared by
`pipeline_sequence` in
[core/orchestration/metaagent_router.yaml](../../../core/orchestration/metaagent_router.yaml).
Use a structured context handoff between modes — pass `input_summary`,
`key_findings`, `open_questions`, `quality_gate_results`,
`recommended_next_agent_focus`.

## Common pitfalls

- Forgetting Step 4's exclusion list and loading churn-style engineering
  rules for an academic evaluation.
- Skipping Step 5 and producing free-form prose for an `analytical_report`.
- Treating `.claude/` as a separate source of truth — it is a symlink or
  sync target of `.codex/`.
- Writing session summaries into `.codex/memory/sessions/` instead of the
  canonical project memory home.

## Examples

- *"review this XGBoost notebook for leakage"* → **MR**,
  `model_review_agent`, output `technical_review`, quality gate includes
  `leakage_risk_is_assessed`.
- *"draft a notion doc for the HOT EDA findings"* → **TD**,
  `technical_writer_agent`, output `notion_doc`, no `.codex/rules/dev-*.md`.
- *"create slides for the steering committee"* → **EP**,
  `presentation_agent`, output `slide_outline`, no adapter engineering
  rules.
- *"refactor the BigQuery pipeline"* → **CR**, `code_review_agent`, merge
  NegritaOS engineering rules + adapter `data-sql-governance.md`.
