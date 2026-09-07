---
id: negritaos-router
domain: meta
enforcement: strict
priority: critical
depends_on:
  - ai-behavior
provides:
  - negritaos-mode-routing
  - integrator-binding
  - output-contract-enforcement
description: >
  Binds NegritaOS' master agent registry (integrator.yaml) and metaagent router
  to any agent client operating in this repository. Defines the operational
  and specialist modes (LP/HOURS/AE/TD/MR/MCARD/CR/PRR/DEP/FQA/LQA/QG/PA/EP/DQ/RT), their routing keywords, and the contract
  resolution order between NegritaOS-native rules and repo-local adapter rules.
version: 1.0.0
applyTo: [repo, agents, prompts, claude, codex, copilot]
canonical_location: rules/global/negritaos_router_rule.md
adapter_stubs:
  - .codex/rules/negritaos-router.md
---

# NegritaOS Router — Mandatory Mode Binding

This rule is the **single entry point** for any agent client (Claude, Codex,
Copilot, or any other) operating inside a NegritaOS-managed repository.
It is canonical. The file under `.codex/rules/negritaos-router.md` is a stub
that points back here.

## 1. Master registry

The master agent registry lives in [integrator.yaml](../../integrator.yaml).
Before producing output, an agent MUST:

1. Identify the request mode using §2.
2. Load the matching agent block from `integrator.yaml`.
3. Apply that agent's `rules` + `skills` + `quality_gate` in addition to repo
   adapter rules under `.codex/rules/`.
4. Honor the output contract declared in
   [core/standards/output_standards.yaml](../../core/standards/output_standards.yaml)
   and the global style in [integrator.yaml](../../integrator.yaml) →
   `global_style`.

## 2. Operational And Specialist Modes

| Mode ID | Label | Agent in `integrator.yaml` | Primary triggers |
|---|---|---|---|
| **LP** | Leadership Planning | `team_lead_ds_agent` | roadmap, sprint, jira, escalation, OKR, blocker |
| **HOURS** | Project Hours Tracking | `project_hours_tracker_agent` | Gisel, tracking hours, workload estimate, overtime, Gantt workbook |
| **AE** | Academic Evaluation | `tfm_evaluator_agent` | thesis, TFM, tribunal, proposal, methodology review |
| **TD** | Technical Documentation | `technical_writer_agent` | notion doc, confluence, technical memo, postmortem |
| **MR** | ML / EDA / Model Review | `model_review_agent` | model review, EDA, SHAP, leakage, XGBoost, AutoGluon, EBM, churn |
| **MCARD** | Model Governance Card | `model_governance_card_agent` | Vera, model card, rule-model card, validation, deployment, monitoring, lifecycle |
| **CR** | Code / Repository Work | `code_review_agent` | code review, PR, refactor, SQL, pipeline, MLflow |
| **PRR** | Pull Request Risk Review | `pull_request_reviewer_agent` | PR risk review, merge gate, CI status, auto approve request |
| **DEP** | TepuFlow Deployment Operations | `pablo_deployment_operator_agent` | deploy TepuFlow, exact commit, DEV/UAT/production promotion |
| **FQA** | TepuFlow Functional Environment QA | `casilda_functional_qa_agent` | validate deployed URL, release acceptance, production smoke |
| **LQA** | TepuFlow Lifecycle Adversarial QA | `casilda_lifecycle_qa_agent` | Casilda Flows, UF-00 to UF-13, route/state stress, visual/accessibility QA |
| **QG** | Quality Bar Gauntlet | `quality_gauntlet_agent` | QG, gauntlet this, compare against benchmark, quality bar review |
| **PA** | Plot Analysis | `plot_analysis_agent` | plot analysis, chart critique, figure narrative, visualization evidence |
| **EP** | Executive Presentation | `presentation_agent` | deck, slides, executive summary, board, one-pager |
| **DQ** | Data Quality / Escalation | `data_quality_sentinel_agent` | data quality, schema drift, KPI anomaly, RCA, incident |
| **RT** | Research / Trends / TFM Topics | `ai_trend_radar_agent` or specialist `tfm_research_advisor_agent` | AI trend, paper review, blockchain watch, TFM topic |

Full trigger lists live in
[core/orchestration/metaagent_router.yaml](../../core/orchestration/metaagent_router.yaml).
Specific requests for new TFM titles, legal public datasets, proposal
differentiation, or publication-oriented topics resolve to the academic
`tfm_research_advisor_agent` specialist within RT.

### 2.1 Per-project `mode_map` override

When a project's `projects/<project_id>.yaml` declares a `mode_map`, the router
MUST resolve the active mode in this order:

1. If the user message contains a `mode_map` intent key (e.g. "new feature",
   "new analysis", "data incident"), use the mapped mode directly.
2. Otherwise, fall back to the global trigger table in §2.
3. Cross-check that the resolved mode's agent is listed in the project's
   `agents:` block or declared `global_agent: true` by the canonical router. If
   neither applies, raise a routing warning and ask the user.

Example (`projects/proj_data_analytics.yaml`):

```yaml
mode_map:
  new_feature: CR
  new_analysis: MR
  data_incident: DQ
  planning: LP
  writeup: TD
  deck: EP
  research: RT
```

This lets each project pin the meaning of common task verbs to its own
operational vocabulary without editing the global router.

## 3. Output contracts (enforced)

When the agent emits an analytical report, it MUST cover the sections in
`default_output_contract.analytical_report` (TLDR → Next_Actions). When it
interprets a plot, it MUST emit `plot_interpretation` fields (what_it_shows,
how_to_read_it, why_it_matters, operational_takeaway). When it describes a
task, it MUST emit `task_output` fields (objective, scope, inputs, outputs,
dependencies, risks, acceptance_criteria).

## 4. Federation principle (no integration)

Per `zsmash/revision_de_claude.md`:

- NegritaOS-only modes (**AE, RT, EP, LP, HOURS, TD**) execute against NegritaOS
  `rules/` + `skills/` only. Adapter rules under `.codex/rules/dev-*.md` are
  not loaded for these modes.
- Engineering modes (**MR, MCARD, CR, PRR, DEP, FQA, LQA, DQ**) execute against NegritaOS rules **plus**
  the adapter rules required by the active codex profile.
- Specialist quality mode **QG** loads the domain rules of the artifact under
  review: code/PR/data QG loads engineering rules; PPTX/DOCX/PDF QG loads
  document and presentation rules; plot/EDA QG loads plot and source-quality
  rules.
- If a NegritaOS rule and an adapter rule disagree, the NegritaOS rule wins.
  Surface the conflict in the response.

## 5. Memory contract

Memory rules are governed by
[core/memory/memory_architecture.yaml](../../core/memory/memory_architecture.yaml).
Repository-local `.codex/memory/` is adapter-only. Canonical project memory
lives under `~/.negritaos/memory/projects/<project_id>/`. The active
`project_id` is declared in `.codex/project.yaml` and the matching NegritaOS
registry under `projects/<project_id>.yaml`.

## 6. Quality gates

Each agent in `integrator.yaml` declares an explicit `quality_gate` block.
The agent MUST self-check against that block before returning the response.
A response that fails any gate item must be revised or labeled with the
unmet criterion and a remediation suggestion.

## 7. Conflict resolution order (highest → lowest)

1. User explicit instruction.
2. NegritaOS-native rules referenced by the active agent's `rules` list.
3. `rules/global/global_rules.yaml`.
4. Adapter rules under `.codex/rules/` permitted by the active profile.
5. System defaults in `.codex/system.md`.

## 8. Browser Profile Resolution

Before authenticated browser work, load the resolved project's
`browser_context` and
[browser_profile_routing.yaml](../../core/orchestration/browser_profile_routing.yaml).
Use `scripts/open_governed_browser.py` to select the declared Brave profile.
The in-app browser is limited to anonymous or non-profile work and is not a
substitute for an authenticated Brave session.

If project, purpose, URL, or GitHub organization cannot resolve to one profile,
return `BLOCKED_BROWSER_PROFILE_RESOLUTION`. Never fall back across account
profiles and never inspect cookies, passwords, local storage, or session tokens.

## 9. External App Financial Authority

Access to an authenticated account does not grant financial authority. This
rule applies to every agent and every external access path, including MCP,
app connectors, browser automation, CLI tools, APIs, SDKs, and cloud consoles.

Without explicit user authorization for the specific operation, an agent MUST
NOT:

- change an account plan, tier, subscription, or billing method;
- start or convert a paid trial;
- purchase credits, tokens, add-ons, domains, seats, licenses, or services;
- create or scale resources that are billable or enable metered paid features;
- accept a quote, contract, recurring commitment, or any operation known or
  likely to incur an incremental charge.

Authorization is never inferred from an account connection, authenticated
session, request to use an app, prior authorization, existing subscription, or
stored payment method. It is valid for one specific operation only. Before
asking, report the provider, account or workspace, exact operation, known price,
currency, recurrence, and billing effect. If cost is unknown or ambiguous,
return `BLOCKED_FINANCIAL_AUTHORIZATION` and ask the user before proceeding.

Read-only inspection of existing plan, usage, or billing status is permitted
only when the inspection itself has no known incremental charge. Never expose
secrets or full payment details.

## 10. Delegated Model Routing

Every delegated Codex task must follow
`core/orchestration/model_escalation_policy.yaml` and the `model_route` returned
by Negrita Brain. Luna medium is the default. Escalation to Luna high, Terra,
or Sol requires an explicit task class, policy signal, impact level, agent
override, or independent-review minimum. Do not upscale opportunistically.

An independent review must use a separate provider session and attempt to
falsify the implementation. High-impact work requires Terra or higher;
production-candidate final integration requires Sol. Missing evidence remains
`HOLD` and cannot be repaired through model selection.

## 11. Anti-patterns

- Loading `.codex/rules/dev-*.md` for AE/RT/EP/LP/TD modes.
- Writing memory to `.codex/memory/` when a canonical project home exists.
- Producing analytical reports without the mandatory section order.
- Bypassing the `quality_gate` of the active agent.
- Treating the duplicated `.claude/` tree as a separate source of truth.
- Treating `LQA` or `casilda-flows` as an unregistered local persona instead of
  resolving `casilda_lifecycle_qa_agent` through the canonical project registry.
- Treating `Gisel` as project-local or unavailable instead of resolving the
  globally routed `project_hours_tracker_agent`.
- Treating `Vera` as optional after a material model or analytical-rule change
  instead of updating the globally routed governance card.
- Treating an authenticated external account as authorization to spend money or
  change its plan.
- Opening authenticated work in a default or in-app browser without resolving
  the project's governed Brave profile first.
- Selecting Terra or Sol without a declared escalation signal or impact.
- Allowing a builder session to certify its own work as independently reviewed.

## Learnings

- Federation, not integration, keeps NegritaOS agents stable while letting
  engineering agents reuse shared rules. (1)
- Wiring `integrator.yaml` via a top-level rule prevents agent clients from
  silently falling back to repo-local defaults. (1)
