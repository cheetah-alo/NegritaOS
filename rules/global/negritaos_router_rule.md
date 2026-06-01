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
  to any agent client operating in this repository. Defines the 8 operational
  modes (LP/AE/TD/MR/CR/EP/DQ/RT), their routing keywords, and the contract
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

## 2. Eight operational modes

| Mode ID | Label | Agent in `integrator.yaml` | Primary triggers |
|---|---|---|---|
| **LP** | Leadership Planning | `team_lead_ds_agent` | roadmap, sprint, jira, escalation, OKR, blocker |
| **AE** | Academic Evaluation | `tfm_evaluator_agent` | thesis, TFM, tribunal, proposal, methodology review |
| **TD** | Technical Documentation | `technical_writer_agent` | notion doc, confluence, technical memo, postmortem |
| **MR** | ML / EDA / Model Review | `model_review_agent` | model review, EDA, SHAP, leakage, XGBoost, AutoGluon, EBM, churn |
| **CR** | Code / Repository Work | `code_review_agent` | code review, PR, refactor, SQL, pipeline, MLflow |
| **EP** | Executive Presentation | `presentation_agent` | deck, slides, executive summary, board, one-pager |
| **DQ** | Data Quality / Escalation | `data_quality_sentinel_agent` | data quality, schema drift, KPI anomaly, RCA, incident |
| **RT** | Research / Trends / TFM Topics | `ai_trend_radar_agent` | AI trend, paper review, blockchain watch, TFM topic |

Full trigger lists live in
[core/orchestration/metaagent_router.yaml](../../core/orchestration/metaagent_router.yaml).

### 2.1 Per-project `mode_map` override

When a project's `projects/<project_id>.yaml` declares a `mode_map`, the router
MUST resolve the active mode in this order:

1. If the user message contains a `mode_map` intent key (e.g. "new feature",
   "new analysis", "data incident"), use the mapped mode directly.
2. Otherwise, fall back to the global trigger table in §2.
3. Cross-check that the resolved mode's agent is listed in the project's
   `agents:` block. If not, raise a routing warning and ask the user.

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

- NegritaOS-only modes (**AE, RT, EP, LP, TD**) execute against NegritaOS
  `rules/` + `skills/` only. Adapter rules under `.codex/rules/dev-*.md` are
  not loaded for these modes.
- Engineering modes (**MR, CR, DQ**) execute against NegritaOS rules **plus**
  the adapter rules required by the active codex profile.
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

## 8. Anti-patterns

- Loading `.codex/rules/dev-*.md` for AE/RT/EP/LP/TD modes.
- Writing memory to `.codex/memory/` when a canonical project home exists.
- Producing analytical reports without the mandatory section order.
- Bypassing the `quality_gate` of the active agent.
- Treating the duplicated `.claude/` tree as a separate source of truth.

## Learnings

- Federation, not integration, keeps NegritaOS agents stable while letting
  engineering agents reuse shared rules. (1)
- Wiring `integrator.yaml` via a top-level rule prevents agent clients from
  silently falling back to repo-local defaults. (1)
