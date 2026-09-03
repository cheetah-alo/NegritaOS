# NegritaOS — Agent Registry

All registered agents in NegritaOS. Each agent is a specialized cognitive module
with a defined contract, skill set, rule set, and output interface.

For routing logic, see: `core/orchestration/metaagent_router.yaml`
For execution policy, see: `core/orchestration/execution_policy.yaml`
For Claude-native aliases, see: `docs/claude-agent-aliases.md`

---

## Agent Index

| ID | Agent | Layer | Router Mode | Description |
|----|-------|-------|-------------|-------------|
| LP | team_lead_ds_agent | strategic | Leadership Planning | Converts ambiguity into structured tasks, roadmaps, and escalations |
| HOURS | project_hours_tracker_agent | strategic | Project Hours Tracking | Gisel creates evidence-based XLSX workload and overtime trackers from project history |
| LP | jira_import_agent | strategic | Leadership Planning | Prepares Jira bulk-import CSV hierarchies, rescue imports, and audit evidence |
| AE | tfm_evaluator_agent | academic | Academic Evaluation | Evaluates TFM proposals, milestones, and final defense documents |
| AE | paper_review_agent | academic | Academic Evaluation | Synthesizes and operationalizes academic and industry papers |
| AE | proposal_validator_agent | academic | Academic Evaluation | Pre-review filter for research proposal structural soundness |
| RT | tfm_research_advisor_agent | academic | Research / TFM Generation | Proposes differentiated TFM topics from papers, legal public data, and proposal comparison |
| TD | technical_writer_agent | strategic | Technical Documentation | Produces Notion/Confluence-ready technical documentation |
| MR | model_review_agent | technical | ML / EDA / Model Review | Reviews ML models, EDA, explainability, and operational readiness |
| MR | eda_reviewer_agent | technical | ML / EDA / Model Review | Focused EDA completeness and correctness review |
| CR | code_review_agent | technical | Code / Repository Work | Reviews Python, SQL, and ML pipelines for production readiness |
| CR | software_architect_agent | technical | Code / Repository Work | Designs maintainable modular repo structures with quality score >=80 |
| PRR | pull_request_reviewer_agent | technical | Pull Request Risk Review | Evaluates CI, risk, security, and verification evidence before merge decisions |
| QG | quality_gauntlet_agent | strategic | Quality Bar Gauntlet | Runs benchmarked builder/critic loops against named reference bars |
| DEP | pablo_deployment_operator_agent | technical | TepuFlow Deployment Operations | Deploys an approved exact commit and records provider and health evidence |
| FQA | casilda_functional_qa_agent | technical | TepuFlow Functional Environment QA | Tests a deployed revision independently and returns PASS, HOLD, or BLOCKED |
| LQA | casilda_lifecycle_qa_agent | technical | TepuFlow Lifecycle Adversarial QA | Attempts UF-00 through UF-13, route, state, persistence, visual, accessibility, and controlled-stress failures |
| EP | presentation_agent | strategic | Executive Presentation | Builds top-down executive and technical presentations |
| EP | decision_support_agent | strategic | Leadership Planning | Structures complex decisions for senior leadership |
| DQ | data_quality_sentinel_agent | technical | Data Quality / Escalation | Detects, documents, and escalates data quality incidents |
| RT | ai_trend_radar_agent | intelligence | Research / TFM Generation | Tracks AI/ML/Blockchain trends and generates TFM topic candidates |
| RT | blockchain_ai_watcher_agent | intelligence | Research / TFM Generation | Specializes in Blockchain × AI intersection |
| RT | research_radar_agent | intelligence | Research / TFM Generation | Broad research intelligence and gap analysis |
| BZ_MF | moneyflow_analyst_agent | business | MoneyFlow Analytics | Revenue, ARPU, billing analytics para operadores telecom |
| BZ_HOT | hot_operations_agent | business | Hot / HotMobile Operations | Churn, segmentación, NPS y entregas CQISense para Hot |
| BZ_UVI | uvi_master_ia_agent | business | UVI Máster IA | Evaluación y tutoría de TFMs — Máster IA UVI |

---

## Claude Native Invocation

NegritaOS modes are uppercase router IDs. Claude Code native subagents are
lowercase markdown aliases generated under `.codex/agents/`.

| Use case | Invocation |
|---|---|
| NegritaOS prompt routing | `@agent:PRR review PR #25` |
| Claude native agent selection | `--agent prr` |
| Claude command palette | select `prr`, `td`, `mr`, `qg`, etc. |
| TepuFlow deployment operator | select `pablo` or write `@agent:DEP` |
| TepuFlow functional QA | select `casilda` or write `@agent:FQA` |
| TepuFlow lifecycle adversarial QA | select `casilda-flows` or write `@agent:LQA` |
| Project hours tracker | select `gisel`, write `@agent:Gisel`, or spawn `gisel` in Codex |

Gisel authors and renders XLSX files in Codex Desktop through the Codex app MCP
workspace dependency loader. In Claude, missing spreadsheet tooling produces a
`BLOCKED_SPREADSHEET_RUNTIME` handoff to Codex, never an unverified XLSX or an
automatic `openpyxl`/`xlsxwriter` substitution.

Do not create one-off local agents for canonical modes. Update
`core/orchestration/metaagent_router.yaml` and `integrator.yaml`, then run:

```bash
python3 scripts/sync_claude_agent_aliases.py --all-projects --write
python3 scripts/validate_claude_agent_aliases.py --all-projects
```

The generated files are wrappers only; the source of truth remains the router,
integrator, rules, skills, and project registry.

## Codex Subagent Model Tiers

Negrita Brain returns a `model_route` for delegated work. Use the minimum
justified tier and invoke the corresponding global custom agent:

| Agent | Tier | Invocation |
|---|---|---|
| `luna-worker` | Luna medium | `Spawn luna-worker to inventory ...` |
| `luna-reviewer` | Luna high | `Spawn luna-reviewer to review ...` |
| `terra-reviewer` | Terra high | `Spawn terra-reviewer as an independent reviewer ...` |
| `sol-integrator` | Sol high | `Spawn sol-integrator for final integration ...` |
| `gisel` | Luna high | `Spawn gisel to update the project-hours tracker ...` |
| `pablo` | Luna high | `Spawn pablo for TepuFlow deployment preflight ...` |
| `casilda` | Terra high | `Spawn casilda for TepuFlow functional QA ...` |
| `casilda-flows` | Terra high | `Spawn casilda-flows for TepuFlow lifecycle QA ...` |

High-impact independent review must use a separate provider-native Brain task,
close as PASS with the required evidence categories, and match the current
worktree fingerprint at commit time. A larger model cannot replace missing
evidence, failed gates, or user authorization. See
`docs/subagent-model-escalation.md`.

All canonical TOML profiles are materialized in every registered adapter and
in `~/.codex/agents`. Pablo and both Casilda profiles remain operationally
scoped to `moneyflowlist`; visibility does not grant cross-project authority.

## External App Financial Authority

All agents operate with zero implied spending authority. Authentication through
MCP, an app connector, browser, CLI, API, SDK, or cloud console permits access
only; it does not permit an agent to change plans, subscriptions, billing
methods, paid entitlements, or perform an operation that can incur an
incremental charge.

The user must explicitly authorize each specific financial operation after the
agent states the provider, account or workspace, exact operation, and known
price, currency, recurrence, and billing effect. Prior approval does not carry
forward. Unknown cost produces `BLOCKED_FINANCIAL_AUTHORIZATION`.

---

## Layer Map

```
NEGRITAOS/
├── academic-layer/
│   ├── paper-synthesizer/      → paper_review_agent
│   ├── proposal-validator/     → proposal_validator_agent
│   ├── tfm-research-advisor/   → tfm_research_advisor_agent
│   └── tfm-evaluator/          → tfm_evaluator_agent
│
├── intelligence-layer/
│   ├── ai-trend-synthesizer/   → ai_trend_radar_agent
│   ├── blockchain-ai-watcher/  → blockchain_ai_watcher_agent
│   └── research-radar/         → research_radar_agent
│
├── strategic-layer/
│   ├── decision-support/       → decision_support_agent
│   ├── executive-presenter/    → presentation_agent
│   ├── jira-import/            → jira_import_agent
│   ├── project-hours-tracker/  → project_hours_tracker_agent (Gisel)
│   ├── quality-gauntlet/       → quality_gauntlet_agent
│   ├── team-lead-ds/           → team_lead_ds_agent
│   └── technical-writer/       → technical_writer_agent
│
├── technical-layr/
│   ├── code-reviewer/          → code_review_agent
│   ├── data-quality-sentinel/  → data_quality_sentinel_agent
│   ├── eda-reviewer/           → eda_reviewer_agent
│   ├── model-reviewer/         → model_review_agent
│   ├── tepuflow-deployment-operator/ → pablo_deployment_operator_agent
│   ├── tepuflow-functional-qa/ → casilda_functional_qa_agent
│   ├── tepuflow-lifecycle-qa/ → casilda_lifecycle_qa_agent
│   └── software-architect/     → software_architect_agent
│
└── business-layer/
    ├── moneyflow/              → moneyflow_analyst_agent
    ├── hot-operations/         → hot_operations_agent
    └── uvi-master-ia/          → uvi_master_ia_agent
```

---

## Agent Contract Structure

Every `agent.yaml` contains:

```yaml
agent:
  id:               # Unique agent identifier
  router_mode:      # Router mode ID (LP / HOURS / AE / TD / MR / CR / PRR / DEP / FQA / LQA / QG / PA / EP / DQ / RT)
  version:          # Semantic version
  layer:            # academic / intelligence / strategic / technical
  description:      # What this agent does and what it does NOT do
  persona:          # Role identity list
  skills:           # Skill files this agent activates
  rules:            # Inherited global + domain-specific rules
  rubrics:          # Scoring rubrics for output quality gates
  templates:        # Output templates by output_mode
  output_modes:     # Named output types this agent can produce
  quality_gate:     # Self-check criteria — failures are reported, not suppressed
  input_types:      # What this agent accepts as input
  handoff:          # Which agents this agent can feed into (pipeline support)
```

---

## Mixed-Mode Pipeline Reference

When a request triggers multiple modes, agents execute in this sequence:
1. Reviewer (MR / CR / AE)
2. Structurer (LP / TD / RT)
3. Writer (TD / EP)
4. Executive Summarizer (EP)
5. Task Generator (LP / DQ)

See full pipeline examples in: `core/orchestration/metaagent_router.yaml`

---

*NegritaOS v1.0 | agents/README.md*
