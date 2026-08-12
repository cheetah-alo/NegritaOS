# Repository Guidelines (Skills Router)

## How to Use This Guide

- Start here for cross-repo norms about skills and agent routing.
- Skills are optional workflows; rules are mandatory and live under `.codex/rules/`.
- Every skill folder must contain a `SKILL.md`; only router-enabled skills also include an `AGENTS.md`.
- Directly invocable skills must be exposed as `.codex/skills/<skill-id>/SKILL.md`; native `skills/engineering/` and reference bundles are not adapter entrypoints.
- If no profile is specified, select a fallback profile based on intent.

## Available Skills

Use these skills for detailed patterns on-demand:

| Skill | Description | URL |
|-------|-------------|-----|
| `rule-compliance-gate` | Mandatory pre-flight checklist enforcing active profile rules | [SKILL.md](rule-compliance-gate/SKILL.md) |
| `local-memory-protocol` | Brain-only canonical project memory for recall, reusable findings, and handoffs | [SKILL.md](local-memory-protocol/SKILL.md) |
| `architecture-guardrails` | Boundary and ownership rules across backend, analytics, frontend, MCP, and `.codex` | [SKILL.md](architecture-guardrails/SKILL.md) |
| `project-structure` | File placement rules for backend, analytics, frontend, tests, and governance assets | [SKILL.md](project-structure/SKILL.md) |
| `business-rules` | Deterministic and traceable business-rule guidance across backend, frontend, and analytics | [SKILL.md](business-rules/SKILL.md) |
| `docs-alignment` | Keep implementation, docs, prompts, rules, and skills in sync | [SKILL.md](docs-alignment/SKILL.md) |
| `document-control` | Govern user-selected deliverable paths, timestamping, manifests, and Git policy for documents, decks, PDFs, DOCX, HTML, and markdown | [SKILL.md](document-control/SKILL.md) |
| `cqi-analytical-pptx` | CQI/CQISense analytical PowerPoint creation, editing, evidence notes, release QA, readability audits, and mobile podcast contracts | [SKILL.md](cqi-analytical-pptx/SKILL.md) |
| `cqi-analytical-docx-pdf` | CQI/CQISense analytical Word/PDF reports with APA tables/figures, render QA, visual inspection, and document-control governance | [SKILL.md](cqi-analytical-docx-pdf/SKILL.md) |
| `ibc-technical-eda-presentation` | IBC technical EDA, bridge-readiness, and ML-readiness decks using CQI visual/evidence standards | [SKILL.md](ibc-technical-eda-presentation/SKILL.md) |
| `ibc-technical-eda-report` | IBC technical EDA DOCX/PDF reports, source-readiness memos, join-readiness guardrails, and ML-readiness evidence limits | [SKILL.md](ibc-technical-eda-report/SKILL.md) |
| `rule-model-documentation` | Create CQI-style documents for deterministic rule-based models, scoring layers, boosters, persistence, validation, plots, and recommendations | [SKILL.md](rule-model-documentation/SKILL.md) |
| `tfm-academic-reviewer` | Standardized final TFM reviewer with 0–4 scoring, 1–10 grade, and benchmark calibration | [SKILL.md](tfm-academic-reviewer/SKILL.md) |
| `tfm-research-advisor` | Propose differentiated TFM titles from recent papers, validated public data, and a read-only proposal corpus | [SKILL.md](tfm-research-advisor/SKILL.md) |
| `jira-bulk-import-hierarchy` | Create, validate, repair, and document Jira Cloud bulk-import CSVs for issue hierarchies and rescue imports | [SKILL.md](jira-bulk-import-hierarchy/SKILL.md) |
| `dashboard-architecture` | Enforce maintainable modular dashboard architecture and forbid monolithic dashboard HTML as final source | [SKILL.md](dashboard-architecture/SKILL.md) |
| `analytical-dashboard-architecture` | Provider-neutral boundaries and quality gates for data-backed dashboards | [SKILL.md](analytical-dashboard-architecture/SKILL.md) |
| `data-source-adapters` | BigQuery, PostgreSQL, and provider-neutral source adapter governance | [SKILL.md](data-source-adapters/SKILL.md) |
| `jinja-bigquery` | Safe deterministic Jinja rendering for BigQuery GoogleSQL templates, dynamic clauses, identifiers, and query variants | [SKILL.md](jinja-bigquery/SKILL.md) |
| `branch-pr` | Provider-neutral branch and PR workflow using the project-declared base branch | [SKILL.md](branch-pr/SKILL.md) |
| `testing-coverage` | Backend, frontend, contract, browser, and coverage gates without provider assumptions | [SKILL.md](testing-coverage/SKILL.md) |
| `pull-request-risk-review` | Shadow-mode PR risk gate for CI status, security, verification evidence, and code-quality tooling | [SKILL.md](pull-request-risk-review/SKILL.md) |
| `nate-skill-builder` | NegritaOS adaptation of skill authoring and audit guidance | [SKILL.md](nate-skill-builder/SKILL.md) |
| `nate-frontend-design` | Opt-in domain-specific frontend design guidance | [SKILL.md](nate-frontend-design/SKILL.md) |
| `nate-excalidraw-diagram` | Explicit editable Excalidraw diagram workflow | [SKILL.md](nate-excalidraw-diagram/SKILL.md) |
| `nate-excalidraw-visuals` | Explicit external-API raster visual generation workflow | [SKILL.md](nate-excalidraw-visuals/SKILL.md) |
| `nate-video-to-website` | Explicit video-backed frontend generation workflow | [SKILL.md](nate-video-to-website/SKILL.md) |
| `commit-hygiene` | Commit scope and message quality rules for this repository | [SKILL.md](commit-hygiene/SKILL.md) |
| `pr-review-deep` | Deep review checklist for risky or user-visible changes | [SKILL.md](pr-review-deep/SKILL.md) |
| `sdd-flow` | Phased spec-driven workflow for non-trivial changes | [SKILL.md](sdd-flow/SKILL.md) |
| `data-contracts` | Raw/derived contracts, schema validation, casting, and errors | [SKILL.md](data-contracts/SKILL.md) |
| `data-loading` | Local/BQ loading, lineage hashing, source resolution | [SKILL.md](data-loading/SKILL.md) |
| `analytics-storytelling-deck` | Finding-first analytical deck structure, baseline alignment, broad-to-narrow evidence zoom, and PPT readability standards | [SKILL.md](analytics-storytelling-deck/SKILL.md) |
| `evidence-first-plot-analysis` | Evidence-first plot, chart, dashboard, EDA figure, and model diagnostic interpretation for reports and decks | [SKILL.md](evidence-first-plot-analysis/SKILL.md) |
| `eda-analytics-findings` | Convert EDA plots, cohorts, funnels, and segment summaries into defensible findings | [SKILL.md](eda-analytics-findings/SKILL.md) |
| `ml-model-findings` | Convert model metrics, thresholds, lift, and explainability outputs into defensible findings | [SKILL.md](ml-model-findings/SKILL.md) |
| `business-proposal-findings` | Convert proposals, ROI narratives, feasibility notes, and decision briefs into structured findings | [SKILL.md](business-proposal-findings/SKILL.md) |
| `research-paper-findings` | Convert papers, abstracts, and research reports into evidence-grounded findings | [SKILL.md](research-paper-findings/SKILL.md) |
| `eda-reports` | EDA execution (analytics + pre-ML): ingestion, metrics, plots, run outputs | [SKILL.md](eda-reports/SKILL.md) |
| `churn-recall-indicator-audit` | Standard audit and report workflow for recall, churn, DiscReq, retention, recontact, and account journey pressure metrics | [SKILL.md](churn-recall-indicator-audit/SKILL.md) |
| `create-unittest` | Create/convert Python unit tests using `unittest` + behavior-driven naming | [SKILL.md](create-unittest/SKILL.md) |
| `dev-logging` | PhaseLogger usage, governance JSON structure, phase names, audit file layout | [SKILL.md](dev-logging/SKILL.md) |
| `plotting-guidelines` | Labels readiness, title/subtitle with N & KPI, legend placement, chart PR checklist | [SKILL.md](plotting-guidelines/SKILL.md) |

## Federated Skill Profiles

Generated from `skills/catalog.yaml`; update the catalog first.

| Profile | Skills |
|---|---|
| `academic-tfm-research` | `docs-alignment`, `document-control`, `local-memory-protocol`, `tfm-research-advisor` |
| `academic-tfm-review` | `docs-alignment`, `document-control`, `local-memory-protocol`, `tfm-academic-reviewer` |
| `analytical-dashboard` | `docs-alignment`, `document-control`, `local-memory-protocol`, `analytical-dashboard-architecture`, `data-source-adapters`, `dashboard-architecture`, `frontend-web`, `api-design`, `data-contracts`, `playwright`, `commit-hygiene`, `pr-review-deep`, `sdd-flow`, `branch-pr`, `testing-coverage` |
| `analytical-deck-delivery` | `docs-alignment`, `document-control`, `local-memory-protocol`, `analytics-storytelling-deck` |
| `analytical-eda` | `docs-alignment`, `document-control`, `local-memory-protocol`, `analytical-eda-governance`, `data-contracts`, `data-loading`, `testing-coverage` |
| `cqi-analytical-docx-pdf` | `docs-alignment`, `document-control`, `local-memory-protocol`, `cqi-analytical-docx-pdf` |
| `cqi-analytical-pptx` | `docs-alignment`, `document-control`, `local-memory-protocol`, `analytics-storytelling-deck`, `cqi-analytical-pptx` |
| `data-source-bigquery` | `docs-alignment`, `document-control`, `local-memory-protocol`, `data-source-adapters`, `bigquery-analysis-governance`, `jinja-bigquery`, `data-contracts`, `data-loading` |
| `data-source-postgresql` | `docs-alignment`, `document-control`, `local-memory-protocol`, `data-source-adapters`, `data-contracts`, `data-loading` |
| `document-delivery` | `docs-alignment`, `document-control`, `local-memory-protocol` |
| `elal-analytical-deck` | `docs-alignment`, `document-control`, `local-memory-protocol`, `analytics-storytelling-deck`, `cqi-analytical-pptx`, `elal-eda-governance` |
| `elal-eda-governance` | `docs-alignment`, `document-control`, `local-memory-protocol`, `analytical-eda-governance`, `bigquery-analysis-governance`, `elal-eda-governance` |
| `evidence-first-plot-analysis` | `docs-alignment`, `document-control`, `local-memory-protocol`, `evidence-first-plot-analysis` |
| `fastapi-nextjs` | `docs-alignment`, `document-control`, `local-memory-protocol`, `backend-service`, `api-design`, `frontend-web`, `nextjs-15`, `react-19`, `typescript`, `playwright` |
| `ibc-technical-eda-presentation` | `docs-alignment`, `document-control`, `local-memory-protocol`, `analytics-storytelling-deck`, `cqi-analytical-pptx`, `ibc-technical-eda-presentation` |
| `ibc-technical-eda-report` | `docs-alignment`, `document-control`, `local-memory-protocol`, `cqi-analytical-docx-pdf`, `ibc-technical-eda-report`, `analytical-eda-governance`, `data-contracts` |
| `pull-request-risk-review` | `docs-alignment`, `document-control`, `local-memory-protocol`, `pull-request-risk-review`, `pr-review-deep` |
| `rule-model-documentation` | `docs-alignment`, `document-control`, `local-memory-protocol`, `rule-model-documentation` |
| `visual-delivery` | `docs-alignment`, `document-control`, `local-memory-protocol`, `nate-frontend-design`, `nate-excalidraw-diagram`, `nate-excalidraw-visuals`, `nate-video-to-website` |

## Auto-invoke Skills

When performing these actions, invoke the corresponding skill first:

| Action | Skill |
|--------|-------|
| Before writing/modifying code or repo files | `rule-compliance-gate` |
| User asks to remember, recall, or continue prior work | `local-memory-protocol` |
| Task references prior decisions, open bugs, or ongoing features | `local-memory-protocol` |
| A substantive session needs a continuation handoff | `local-memory-protocol` |
| Creating or updating repository documentation | `docs-alignment` |
| Starting a new or migrated exploratory analysis | `analytical-eda-governance` |
| Starting a new or migrated BigQuery analysis or source-quality preflight | `bigquery-analysis-governance` |
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
| Create, edit, audit, release, or podcast a CQI/CQISense analytical PPTX deck | `cqi-analytical-pptx` |
| Create, edit, audit, export, or visually QA a CQI/CQISense analytical DOCX/PDF report | `cqi-analytical-docx-pdf` |
| Create or edit an IBC technical EDA, bridge-readiness, or ML-readiness PPTX deck | `ibc-technical-eda-presentation` |
| Create or edit an IBC technical EDA DOCX/PDF report, source-readiness memo, join-readiness memo, or ML-readiness evidence pack | `ibc-technical-eda-report` |
| Interpret, compare, review, or write about plots, charts, dashboard visuals, EDA figures, model diagnostic plots, or plot-backed claims | `evidence-first-plot-analysis` |
| Convert EDA plots, cohorts, funnels, segments, or outcome rates into claims | `eda-analytics-findings` |
| Convert model metrics, thresholds, lift, SHAP, or leakage review into claims | `ml-model-findings` |
| Create documentation for rule-based models, rules engines, scoring, boosters, persistence, sticky logic, decay, sensitivity analysis, or validation plots | `rule-model-documentation` |
| Convert business proposals, ROI narratives, feasibility notes, or decision briefs into claims | `business-proposal-findings` |
| Convert research papers, abstracts, or literature reviews into claims | `research-paper-findings` |
| Create or update deliverable documents, PPT/PDF/DOCX/HTML artifacts, or Notion/Confluence-ready markdown | `document-control` |
| Review a TFM PDF, prepare a tribunal report, or calibrate an academic score against benchmark theses | `tfm-academic-reviewer` |
| Investigate or propose new TFM titles, research gaps, public datasets, or publication-oriented thesis topics | `tfm-research-advisor` |
| Create, validate, repair, or document Jira Cloud bulk-import CSVs, issue hierarchies, or rescue imports | `jira-bulk-import-hierarchy` |
| Create or modify dashboards, dashboard HTML, BI-style frontend pages, chart-heavy report UIs, or dashboard generators | `dashboard-architecture` |
| Design or modify data-backed dashboard boundaries, provider routing, or logical dashboard contracts | `analytical-dashboard-architecture` |
| Change BigQuery, PostgreSQL, or other data-source adapters and physical object routing | `data-source-adapters` |
| Write or review Jinja templates that render BigQuery SQL, dynamic CTEs, filters, projections, joins, identifiers, or query variants | `jinja-bigquery` |
| Prepare a branch, choose a PR base, or assemble review evidence | `branch-pr` |
| Review a pull request, evaluate PR risk, check merge readiness, assess auto-approval, or inspect GitHub PR checks | `pull-request-risk-review` |
| Change behavior, contracts, visual states, or browser flows requiring coverage evidence | `testing-coverage` |
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
