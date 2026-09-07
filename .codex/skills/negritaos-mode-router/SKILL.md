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
- The request matches one of the operational or specialist mode trigger lists in
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

## Step 3a — Claude native alias bridge

Claude Code native subagents are discovered from `.codex/agents/*.md` and use
lowercase names. Treat the NegritaOS mode ID as the canonical concept and the
Claude file as a thin adapter:

- `PRR` → `.codex/agents/prr.md` → `pull_request_reviewer_agent`
- `TD` → `.codex/agents/td.md` → `technical_writer_agent`
- `MR` → `.codex/agents/mr.md` → `model_review_agent`
- `QG` → `.codex/agents/qg.md` → `quality_gauntlet_agent`
- `DEP` → `.codex/agents/pablo.md` → `pablo_deployment_operator_agent`
- `FQA` → `.codex/agents/casilda.md` → `casilda_functional_qa_agent`
- `LQA` → `.codex/agents/casilda-flows.md` → `casilda_lifecycle_qa_agent`
- `HOURS` → `.codex/agents/gisel.md` → `project_hours_tracker_agent`
- `MCARD` → `.codex/agents/vera.md` → `model_governance_card_agent`

If a user writes `@agent:PRR` or `PRR: ...`, do not ask what `PRR` means. Run
canonical resolution first. Only report `ROUTING_UNAVAILABLE` when the
canonical agent is neither declared by `projects/<project_id>.yaml` nor marked
as a global agent by the router.

## Step 4 — Merge with adapter rules (engineering modes only)

If the active mode is **MR**, **MCARD**, **CR**, **PRR**, **DEP**, **FQA**, **LQA**, or
**DQ**:

1. Load the active codex profile from `.codex/profiles/`.
2. Load the rules it activates from `.codex/rules/`.
3. Merge with NegritaOS rules using the conflict order from the canonical
   router rule (NegritaOS wins).

If the active mode is **QG**, load the domain rules for the artifact under
review: code/PR/data QG uses engineering rules; PPTX/DOCX/PDF QG uses document
and presentation rules; plot/EDA QG uses plot and source-quality rules.

If the active mode is **AE**, **RT**, **EP**, **LP**, **HOURS**, **TD**, or **PA**:

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

## Step 6a — External app financial gate

Before using MCP, an app connector, browser automation, a CLI, API, SDK, or
cloud console, determine whether the intended operation can change a plan,
subscription, billing method, paid entitlement, resource size, seat count, or
incur any incremental charge.

- Connected or authenticated does not mean financially authorized.
- A request to use an app does not authorize a purchase or plan change.
- Previous approval does not carry forward to another operation.
- Ask for explicit authorization for the exact operation and state provider,
  account or workspace, known price, currency, recurrence, and billing effect.
- If cost is unknown or ambiguous, stop with
  `BLOCKED_FINANCIAL_AUTHORIZATION`.
- Read-only account inspection is allowed only when it has no known incremental
  charge; never expose full payment details or secrets.

## Step 6b — Browser profile gate

Before browser work that depends on an authenticated account, read the
`browser_context` returned by Negrita Brain and invoke
`governed-browser-routing`. Resolve project + purpose + URL with
`scripts/open_governed_browser.py --dry-run` before opening Brave.

- Use the in-app browser only for anonymous or non-profile work.
- Never substitute another profile when routing is unresolved.
- Return `BLOCKED_BROWSER_PROFILE_RESOLUTION` on ambiguity or conflict.
- Never inspect cookies, passwords, local storage, or session tokens.

## Step 6c — Delegated model gate

For every Codex subagent, use the `model_route` returned by Negrita Brain and
load `core/orchestration/model_escalation_policy.yaml`.

- Default bounded work to `luna_medium`.
- Use `luna_high` for focused review and approved-contract validation.
- Pass explicit `--risk-signal` values when Terra or Sol criteria are present.
- Material signals automatically raise `change_impact`; pass an explicit higher
  value when the impact is known before the signal is selected.
- An independent reviewer must use `--review-role independent_reviewer` and the
  builder's `--review-of-session`; another alias in the same provider task is
  rejected.
- Close reviewer PASS with every required
  `--evidence-ref category=(repo|memory):receipt.json@sha256:<64_hex>`.
  The commit gate verifies reviewer tier, native task identity, receipt hash,
  receipt contents, and the current SHA-256 worktree fingerprint.
- Re-run `resolve` before commit when Brain reports that the session predates
  model routing; legacy contracts never inherit review authorization.
- Missing evidence stays `HOLD` regardless of model tier.

Claude applies the same escalation semantics but must not claim to execute a
GPT-5.6 model. Use the canonical Codex agents when the exact Luna/Terra/Sol
model is required.

## Step 7 — Memory hooks

After meaningful durable work, follow `local-memory-protocol` and use the
`negrita_brain.py memory` API. Never write either canonical project memory or
`.codex/memory/` directly.

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
- Treating `PRR` as missing because Claude native selection expects
  lowercase `--agent prr`.
- Treating Gisel as missing because the project registry does not duplicate the
  globally routed `project_hours_tracker_agent`.
- Treating Vera as missing because the project registry does not duplicate the
  globally routed `model_governance_card_agent`.
- Writing any project memory file directly instead of using the canonical
  `negrita_brain.py memory` API.

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
- *"review PR #12 as a merge gate"* → **PRR**,
  `pull_request_reviewer_agent`, output `risk_review`, shadow recommendation.
- *"Casilda Flows: test UF-00 through UF-13 in UAT"* → **LQA**,
  `casilda_lifecycle_qa_agent`, output `lifecycle_qa_report`; production stays
  read-only and omitted or blocked flows cannot pass.
- *"QG gauntlet this DOCX against the CQI report template"* → **QG**,
  `quality_gauntlet_agent`, load document-control and the relevant DOCX/PDF
  skill before judging against the reference.
- *"analyze this heatmap"* → **PA**, `plot_analysis_agent`, output
  evidence-first plot interpretation.
- *"Gisel, update the tracking-hours workbook for this repo"* → **HOURS**,
  `project_hours_tracker_agent`, output `updated_project_hours_tracker`.
- *"Vera, create the governance card for this rule model"* → **MCARD**,
  `model_governance_card_agent`, output `model_governance_card_yaml`.
