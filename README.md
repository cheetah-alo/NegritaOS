# NegritaOS

**Version:** 1.0.0
**Type:** Modular Cognitive Operating System

A production-grade operating system for senior technical leadership in Data Science,
ML governance, academic evaluation, executive communication, and AI/Blockchain research.

---

## System Philosophy

> "AI should amplify expert reasoning, not replace critical thinking."

NegritaOS is not a general-purpose assistant. It is a specialized system with:
- Defined agents for defined problem types
- Explicit quality gates on every output
- Governance-first orientation
- Full traceability from input to output

---

## Architecture Overview

```
NEGRITAOS/
│
├── core/                          System-level contracts
│   ├── identity/                  System identity and persona definition
│   ├── memory/                    Memory architecture and context policy
│   ├── ontology/                  Shared vocabulary across all agents
│   ├── orchestration/             Metaagent router + execution policy
│   ├── principles/                15 cognitive operating principles
│   └── standards/                 Naming conventions + output standards
│
├── academic-layer/                Academic evaluation agents
│   ├── paper-synthesizer/
│   ├── proposal-validator/
│   └── tfm-evaluator/
│
├── intelligence-layer/            Research and trend intelligence agents
│   ├── ai-trend-synthesizer/
│   ├── blockchain-ai-watcher/
│   └── research-radar/
│
├── strategic-layer/               Leadership, communication, and decision agents
│   ├── decision-support/
│   ├── executive-presenter/
│   └── team-lead-ds/
│
├── technical-layr/                ML, code, and data quality agents
│   ├── code-reviewer/
│   ├── data-quality-sentinel/
│   ├── eda-reviewer/
│   └── model-reviewer/
│
├── agents/                        Agent registry and navigation
│   └── README.md
│
├── skills/                        Reusable cognitive skills
│   ├── transversal/               Cross-agent skills (reasoning, evidence, TL;DR)
│   ├── ml/                        ML-specific skills (model review, EDA, leakage)
│   ├── academic/                  Academic skills (TFM eval, paper synthesis)
│   ├── executive/                 Executive communication skills
│   ├── writing/                   Documentation skills
│   ├── governance/                Risk framing, hype review
│   └── engineering/               Code and SQL review skills
│
├── rules/                         Domain rule sets (YAML)
│   ├── global/
│   ├── ml/
│   ├── academic/
│   ├── governance/
│   ├── engineering/
│   ├── presentation/
│   └── writing/
│
├── rubrics/                       Scoring rubrics for quality gates
├── templates/                     Output templates by document type
├── archetypes/                    Reusable project operating patterns
├── projects/                      Local project registry and memory routing
│
├── integrator.yaml                Master agent registry (full agent definitions)
└── core/core-principles.md        15 core operational principles
```

---

## Metaagent Router — Mode Reference

| Mode ID | Mode | Agent |
|---------|------|-------|
| LP | Leadership Planning | team_lead_ds_agent |
| AE | Academic Evaluation | tfm_evaluator_agent |
| TD | Technical Documentation | technical_writer_agent |
| MR | ML / EDA / Model Review | model_review_agent |
| CR | Code / Repository Work | code_review_agent |
| EP | Executive Presentation | presentation_agent |
| DQ | Data Quality / Escalation | data_quality_sentinel_agent |
| RT | Research / TFM Generation | ai_trend_radar_agent |

For mixed-mode requests, agents execute in a defined pipeline sequence.
See: `core/orchestration/metaagent_router.yaml`

---

## Quick Start — Invoking the System

1. **Classify your request** using the mode table above (or let the router classify it)
2. **Optionally specify an agent directly:** `@agent:MR review this churn model`
3. **For mixed requests:** the pipeline executes automatically in sequence
4. **Load project context** if needed: provide `project_context.md` at session start

---

## Key Files

| File | Purpose |
|------|---------|
| `core/orchestration/metaagent_router.yaml` | Request classification and dispatch |
| `core/orchestration/execution_policy.yaml` | End-to-end execution contract |
| `core/identity/negrita_identity.md` | System identity and boundaries |
| `core/ontology/domain_ontology.yaml` | Shared vocabulary |
| `core/principles/cognitive_principles.md` | 15 operating principles |
| `core/standards/output_standards.yaml` | Output structure requirements |
| `agents/README.md` | Full agent registry |
| `integrator.yaml` | Master agent definitions |
| `projects/README.md` | Project registry and memory load order |
| `archetypes/README.md` | Reusable project operating patterns |
| `prompts/` | Reusable operational prompts for NegritaOS workflows |
| `docs/daily_usage_manual.md` | Daily workflow for loading project adapters and memory |
| `docs/presentation_and_notion_workflow.md` | Presentation and Notion output workflow |
| `scripts/validate_registry_paths.py` | Validates that registry and governance file references resolve |
| `scripts/bootstrap_project_adapter.sh` | Creates a new project registry, memory home, and `.codex` adapter |

---

## Local Memory Model

NegritaOS uses a private local memory root outside project repositories:

```text
~/.negritaos/memory/
```

Repository `.codex` folders are adapters. They may point to local memory, but
they are not the canonical durable memory store. This prevents losing project
history when work happens in temporary branches or worktrees.

---

*NegritaOS v1.0 — built for operational rigor, not AI theater.*
