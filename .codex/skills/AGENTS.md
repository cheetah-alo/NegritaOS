# Repository Guidelines (Skills Router)

## How to Use This Guide

- Start here for cross-repo norms about skills and agent routing.
- Skills are optional workflows; rules are mandatory and live under `.codex/rules/`.
- Every skill folder must contain a `SKILL.md`; only router-enabled skills also include an `AGENTS.md`.
- If no profile is specified, select a fallback profile based on intent.

## Available Skills

Use these skills for detailed patterns on-demand:

| Skill | Description | URL |
|-------|-------------|-----|
| `rule-compliance-gate` | Mandatory pre-flight checklist enforcing active profile rules | [SKILL.md](rule-compliance-gate/SKILL.md) |
| `memory-protocol` | Repository-local memory workflow for recall, durable discoveries, and session closure | [SKILL.md](memory-protocol/SKILL.md) |
| `architecture-guardrails` | Boundary and ownership rules across backend, analytics, frontend, MCP, and `.codex` | [SKILL.md](architecture-guardrails/SKILL.md) |
| `project-structure` | File placement rules for backend, analytics, frontend, tests, and governance assets | [SKILL.md](project-structure/SKILL.md) |
| `business-rules` | Deterministic and traceable business-rule guidance across backend, frontend, and analytics | [SKILL.md](business-rules/SKILL.md) |
| `docs-alignment` | Keep implementation, docs, prompts, rules, and skills in sync | [SKILL.md](docs-alignment/SKILL.md) |
| `document-control` | Govern deliverable documents, decks, PDFs, DOCX, HTML, and Notion/Confluence markdown under timestamped `documents/` outputs | [SKILL.md](document-control/SKILL.md) |
| `dashboard-architecture` | Enforce maintainable modular dashboard architecture and forbid monolithic dashboard HTML as final source | [SKILL.md](dashboard-architecture/SKILL.md) |
| `commit-hygiene` | Commit scope and message quality rules for this repository | [SKILL.md](commit-hygiene/SKILL.md) |
| `pr-review-deep` | Deep review checklist for risky or user-visible changes | [SKILL.md](pr-review-deep/SKILL.md) |
| `sdd-flow` | Phased spec-driven workflow for non-trivial changes | [SKILL.md](sdd-flow/SKILL.md) |
| `data-contracts` | Raw/derived contracts, schema validation, casting, and errors | [SKILL.md](data-contracts/SKILL.md) |
| `data-loading` | Local/BQ loading, lineage hashing, source resolution | [SKILL.md](data-loading/SKILL.md) |
| `analytics-storytelling-deck` | Finding-first analytical deck structure, baseline alignment, broad-to-narrow evidence zoom, and PPT readability standards | [SKILL.md](analytics-storytelling-deck/SKILL.md) |
| `eda-analytics-findings` | Convert EDA plots, cohorts, funnels, and segment summaries into defensible findings | [SKILL.md](eda-analytics-findings/SKILL.md) |
| `ml-model-findings` | Convert model metrics, thresholds, lift, and explainability outputs into defensible findings | [SKILL.md](ml-model-findings/SKILL.md) |
| `business-proposal-findings` | Convert proposals, ROI narratives, feasibility notes, and decision briefs into structured findings | [SKILL.md](business-proposal-findings/SKILL.md) |
| `research-paper-findings` | Convert papers, abstracts, and research reports into evidence-grounded findings | [SKILL.md](research-paper-findings/SKILL.md) |
| `eda-reports` | EDA execution (analytics + pre-ML): ingestion, metrics, plots, run outputs | [SKILL.md](eda-reports/SKILL.md) |
| `churn-recall-indicator-audit` | Standard audit and report workflow for recall, churn, DiscReq, retention, recontact, and account journey pressure metrics | [SKILL.md](churn-recall-indicator-audit/SKILL.md) |
| `create-unittest` | Create/convert Python unit tests using `unittest` + behavior-driven naming | [SKILL.md](create-unittest/SKILL.md) |
| `dev-logging` | PhaseLogger usage, governance JSON structure, phase names, audit file layout | [SKILL.md](dev-logging/SKILL.md) |
| `plotting-guidelines` | Labels readiness, title/subtitle with N & KPI, legend placement, chart PR checklist | [SKILL.md](plotting-guidelines/SKILL.md) |

## Auto-invoke Skills

When performing these actions, invoke the corresponding skill first:

| Action | Skill |
|--------|-------|
| Before writing/modifying code or repo files | `rule-compliance-gate` |
| User asks to remember, recall, or continue prior work | `memory-protocol` |
| Task references prior decisions, open bugs, or ongoing features | `memory-protocol` |
| Before ending a substantive session | `memory-protocol` |
| Creating or updating repository documentation | `docs-alignment` |
| Creating or updating README, AGENTS, runbooks, ADRs, rules, skills, prompts, or templates | `docs-alignment` |
| Documenting behavior, workflows, contracts, APIs, architecture, setup, operations, or governance changes | `docs-alignment` |
| Reviewing documentation consistency | `docs-alignment` |
| Changing Python logic under `backend/app/`, `data_analytics/`, or `mcp_server/` with test impact | `create-unittest` |
| Create, refactor, or extend unit tests under `tests/` | `create-unittest` |
| Convert existing tests (pytest-style) into `unittest.TestCase` | `create-unittest` |
| Standardize test naming/structure (behavior-driven pattern) | `create-unittest` |
| Modify dataset contracts or schema validation | `data-contracts` |
| Change data ingestion or source resolution | `data-loading` |
| Create or edit analytical PPTs, finding decks, or metric-driven storylines | `analytics-storytelling-deck` |
| Convert EDA plots, cohorts, funnels, segments, or outcome rates into claims | `eda-analytics-findings` |
| Convert model metrics, thresholds, lift, SHAP, or leakage review into claims | `ml-model-findings` |
| Convert business proposals, ROI narratives, feasibility notes, or decision briefs into claims | `business-proposal-findings` |
| Convert research papers, abstracts, or literature reviews into claims | `research-paper-findings` |
| Create or update deliverable documents, PPT/PDF/DOCX/HTML artifacts, or Notion/Confluence-ready markdown | `document-control` |
| Create or modify dashboards, dashboard HTML, BI-style frontend pages, chart-heavy report UIs, or dashboard generators | `dashboard-architecture` |
| Modify EDA outputs, plots, dashboards, or run-scoped output layout | `eda-reports` |
| Review or create churn, recall, DiscReq, retention, recontact, or account journey pressure metrics | `churn-recall-indicator-audit` |
| Instrument code with logging, add PhaseLogger, write governance JSON | `dev-logging` |
| Create or modify matplotlib/seaborn/plotly charts or plot helpers | `plotting-guidelines` |

## Rule vs Skill Precedence

When rules and skills conflict, apply this order:

1. `system.md` (highest)
2. Active profile rules (`priority: critical`)
3. Active profile rules (`priority: warning`)
4. Skill guidance (procedural only)

## Profile Fallback (Intent Classifier)

If the user does not specify a profile, select one:

- **Run analytics (SQL -> DF -> plots -> report)** → `analysis-run`
- **EDA before ML (profiling + plots + dataset readiness)** → `eda-pre-ml`
- **Review/audit** → `review`
- **Refactor/cleanup** → `refactor`
