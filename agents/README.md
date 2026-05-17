# NegritaOS — Agent Registry

All registered agents in NegritaOS. Each agent is a specialized cognitive module
with a defined contract, skill set, rule set, and output interface.

For routing logic, see: `core/orchestration/metaagent_router.yaml`
For execution policy, see: `core/orchestration/execution_policy.yaml`

---

## Agent Index

| ID | Agent | Layer | Router Mode | Description |
|----|-------|-------|-------------|-------------|
| LP | team_lead_ds_agent | strategic | Leadership Planning | Converts ambiguity into structured tasks, roadmaps, and escalations |
| AE | tfm_evaluator_agent | academic | Academic Evaluation | Evaluates TFM proposals, milestones, and final defense documents |
| AE | paper_review_agent | academic | Academic Evaluation | Synthesizes and operationalizes academic and industry papers |
| AE | proposal_validator_agent | academic | Academic Evaluation | Pre-review filter for research proposal structural soundness |
| TD | technical_writer_agent | strategic | Technical Documentation | Produces Notion/Confluence-ready technical documentation |
| MR | model_review_agent | technical | ML / EDA / Model Review | Reviews ML models, EDA, explainability, and operational readiness |
| MR | eda_reviewer_agent | technical | ML / EDA / Model Review | Focused EDA completeness and correctness review |
| CR | code_review_agent | technical | Code / Repository Work | Reviews Python, SQL, and ML pipelines for production readiness |
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

## Layer Map

```
NEGRITAOS/
├── academic-layer/
│   ├── paper-synthesizer/      → paper_review_agent
│   ├── proposal-validator/     → proposal_validator_agent
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
│   ├── team-lead-ds/           → team_lead_ds_agent
│   └── technical-writer/       → technical_writer_agent
│
├── technical-layr/
│   ├── code-reviewer/          → code_review_agent
│   ├── data-quality-sentinel/  → data_quality_sentinel_agent
│   ├── eda-reviewer/           → eda_reviewer_agent
│   └── model-reviewer/         → model_review_agent
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
  router_mode:      # Router mode ID (LP / AE / TD / MR / CR / EP / DQ / RT)
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
