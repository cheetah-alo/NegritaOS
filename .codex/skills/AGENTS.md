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
| `commit-hygiene` | Commit scope and message quality rules for this repository | [SKILL.md](commit-hygiene/SKILL.md) |
| `pr-review-deep` | Deep review checklist for risky or user-visible changes | [SKILL.md](pr-review-deep/SKILL.md) |
| `sdd-flow` | Phased spec-driven workflow for non-trivial changes | [SKILL.md](sdd-flow/SKILL.md) |
| `data-contracts` | Raw/derived contracts, schema validation, casting, and errors | [SKILL.md](data-contracts/SKILL.md) |
| `data-loading` | Local/BQ loading, lineage hashing, source resolution | [SKILL.md](data-loading/SKILL.md) |
| `eda-reports` | EDA execution (analytics + pre-ML): ingestion, metrics, plots, run outputs | [SKILL.md](eda-reports/SKILL.md) |
| `create-unittest` | Create/convert Python unit tests using `unittest` + behavior-driven naming | [SKILL.md](create-unittest/SKILL.md) |

## Auto-invoke Skills

When performing these actions, invoke the corresponding skill first:

| Action | Skill |
|--------|-------|
| Before writing/modifying code or repo files | `rule-compliance-gate` |
| User asks to remember, recall, or continue prior work | `memory-protocol` |
| Task references prior decisions, open bugs, or ongoing features | `memory-protocol` |
| Before ending a substantive session | `memory-protocol` |
| Changing Python logic under `backend/app/`, `data_analytics/`, or `mcp_server/` with test impact | `create-unittest` |
| Create, refactor, or extend unit tests under `tests/` | `create-unittest` |
| Convert existing tests (pytest-style) into `unittest.TestCase` | `create-unittest` |
| Standardize test naming/structure (behavior-driven pattern) | `create-unittest` |
| Modify dataset contracts or schema validation | `data-contracts` |
| Change data ingestion or source resolution | `data-loading` |
| Modify EDA outputs, plots, dashboards, or run-scoped output layout | `eda-reports` |

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
