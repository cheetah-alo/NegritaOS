# AI Agent Skills

This directory contains **Agent Skills** following the [Agent Skills open standard](https://agentskills.io). Skills provide domain-specific patterns, conventions, and guardrails that help AI coding assistants (Claude Code, OpenCode, Cursor, etc.) understand project-specific requirements.

## What Are Skills?

[Agent Skills](https://agentskills.io) is an open standard format for extending AI agent capabilities with specialized knowledge. Originally developed by Anthropic and released as an open standard, it is now adopted by multiple agent products.

Skills teach AI assistants how to perform specific tasks. When an AI loads a skill, it gains context about:

- Critical rules (what to always/never do)
- Code patterns and conventions
- Project-specific workflows
- References to detailed documentation

## Setup

Run the setup script to configure skills for all supported AI coding assistants:

```bash
./skills/setup.sh
```

This creates symlinks so each tool finds skills in its expected location:

| Tool | Symlink Created |
|------|-----------------|
| Claude Code / OpenCode | `.claude/skills/` |
| Codex (OpenAI) | `.codex/skills/` |
| GitHub Copilot | `.github/skills/` |
| Gemini CLI | `.gemini/skills/` |

After running setup, restart your AI coding assistant to load the skills.

## How to Use Skills

Skills are automatically discovered by the AI agent. To manually load a skill during a session:

```
Read skills/{skill-name}/SKILL.md
```

## Available Skills

### Generic Skills

Reusable patterns for common technologies:

| Skill | Description |
|-------|-------------|
| `typescript` | Const types, flat interfaces, utility types |
| `react-19` | React 19 patterns, React Compiler |
| `nextjs-15` | App Router, Server Actions, streaming |
| `tailwind-4` | cn() utility, Tailwind 4 patterns |
| `playwright` | Page Object Model, selectors |
| `pytest` | Fixtures, mocking, markers |
| `django-drf` | ViewSets, Serializers, Filters |
| `zod-4` | Zod 4 API patterns |
| `zustand-5` | Persist, selectors, slices |
| `ai-sdk-5` | Vercel AI SDK patterns |

### Domain Skills

Reusable patterns for common domains:

| Skill | Description |
|-------|-------------|
| `backend-service` | Backend service patterns (Python-first) |
| `frontend-web` | Frontend UI patterns and structure |
| `python-core` | Python coding standards and modules |
| `api-design` | API contract and endpoint design |
| `data-analytics` | Analytics and pipeline conventions |
| `data-contracts` | Dataset schema contracts and validation |
| `data-loading` | Data ingestion, source resolution, lineage |
| `jinja-bigquery` | Safe deterministic Jinja rendering for BigQuery GoogleSQL templates and dynamic query variants |
| `pull-request-risk-review` | Shadow-mode PR risk gate for CI status, security, verification evidence, and Python quality checks |
| `analytical-eda-governance` | Provider-neutral structure, manifests, contracts, immutable runs, and evidence gates for new or migrated EDA |
| `bigquery-analysis-governance` | BigQuery source-quality preflight for grain, capture-to-load latency, freshness, SLA, and evidence |
| `elal-eda-governance` | Opt-in ELAL EDA semantics for operational severity, proxy labels, blocked states, and third subtitle |
| `document-control` | User-selected deliverable routing, timestamping, manifest, and Git-policy governance |
| `cqi-analytical-pptx` | CQI/CQISense analytical PowerPoint delivery, evidence notes, release QA, readability audits, and mobile podcast contracts |
| `cqi-analytical-docx-pdf` | CQI/CQISense analytical Word/PDF reports with APA tables/figures, render QA, visual inspection, and document-control governance |
| `ibc-technical-eda-report` | IBC technical EDA DOCX/PDF reports, source-readiness memos, join-readiness guardrails, and ML-readiness evidence limits |
| `evidence-first-plot-analysis` | Evidence-first interpretation and comparison of plots, charts, dashboard visuals, EDA figures, and model diagnostics for reports and decks |
| `rule-model-documentation` | CQI-style documentation for deterministic rule-based models, scoring layers, boosters, lifecycle behavior, validation plots, and recommendations |
| `dashboard-architecture` | Maintainable modular dashboard architecture; forbids monolithic dashboard HTML as final source |
| `analytics-storytelling-deck` | Finding-first analytical deck structure, baseline alignment, broad-to-narrow evidence zoom, and PPT readability standards |
| `eda-analytics-findings` | Convert EDA plots, cohorts, funnels, and segment summaries into defensible findings |
| `ml-model-findings` | Convert model metrics, thresholds, lift, and explainability outputs into defensible findings |
| `business-proposal-findings` | Convert proposals, ROI narratives, feasibility notes, and decision briefs into structured findings |
| `research-paper-findings` | Convert papers, abstracts, and research reports into evidence-grounded findings |
| `tfm-academic-reviewer` | Standardized final TFM review with rubric scoring, page evidence, and benchmark calibration |
| `tfm-research-advisor` | Research and rank differentiated TFM titles with recent papers and legally validated public data |
| `churn-recall-indicator-audit` | Standard audit and report workflow for recall, churn, DiscReq, retention, recontact, and account journey pressure metrics |
| `mcp-server` | MCP server and tool design |
| `dev-logging` | PhaseLogger, governance JSON, audit dirs |
| `plotting-guidelines` | Labels readiness, title/subtitle/legend standards, chart quality gate |

### Meta Skills

| Skill | Description |
|-------|-------------|
| `skill-creator` | Create new AI agent skills |
| `skill-sync` | Sync skill metadata to AGENTS.md Auto-invoke sections |

### Repository Skills

| Skill | Description |
|-------|-------------|
| `architecture-guardrails` | Boundary and ownership guardrails across backend, analytics, frontend, MCP, and `.codex` |
| `project-structure` | File placement rules for backend, analytics, frontend, tests, and governance assets |
| `business-rules` | Deterministic and traceable business-rule guidance |
| `local-memory-protocol` | Brain-only canonical project memory workflow |
| `docs-alignment` | Keep implementation, docs, prompts, rules, and skills aligned under the documentation-governance structure gate |
| `document-control` | Keep deliverable documents, decks, PDFs, DOCX, HTML, and Notion/Confluence markdown traceable |
| `commit-hygiene` | Commit message and scope discipline |
| `pr-review-deep` | Deep technical review protocol |
| `pull-request-risk-review` | PR risk scoring, merge-gate evidence, CI/check status, and quality-tooling review |
| `sdd-flow` | Spec-driven phased delivery workflow |

### Federated Skill Profiles

The canonical federation catalog is [skills/catalog.yaml](../../skills/catalog.yaml).
It maps reference bundles from `skills/skills_engram/` and `skills/skill_nate/`
to activable `.codex/skills/` wrappers and native `skills/engineering/` agent
guidance.

Project adapters declare `skill_profiles` and `data_source` in their canonical
project registry. Use `scripts/validate_skill_catalog.py` before materializing
an adapter and `scripts/materialize_project_skills.py <repo> --dry-run` before
linking profile-selected skills. Raw imported bundles remain reference-only.

New or migrated BigQuery analyses must also pass the source-quality preflight
defined by `bigquery-analysis-governance`. PostgreSQL, files, API, and academic
projects do not activate that provider-specific gate unless their registry
selects a compatible profile.

The portable catalog synchronizer is:

```bash
python3 scripts/sync_skill_catalog.py --write
```

The legacy `skill-sync` skill remains available for existing project layouts;
the portable synchronizer is the NegritaOS meta-repo path and does not require
macOS Bash associative arrays.

## Directory Structure

```
skills/
├── {skill-name}/
│   ├── SKILL.md              # Required - main instrunsction and metadata
│   ├── scripts/              # Optional - executable code
│   ├── assets/               # Optional - templates, schemas, resources
│   └── references/           # Optional - links to local docs
└── README.md                 # This file
```

## Why Auto-invoke Sections?

**Problem**: AI assistants (Claude, Gemini, etc.) don't reliably auto-invoke skills even when the `Trigger:` in the skill description matches the user's request. They treat skill suggestions as "background noise" and barrel ahead with their default approach.

**Solution**: The `AGENTS.md` files in each directory contain an **Auto-invoke Skills** section that explicitly commands the AI: "When performing X action, ALWAYS invoke Y skill FIRST." This is a [known workaround](https://scottspence.com/posts/claude-code-skills-dont-auto-activate) that forces the AI to load skills.

**Automation**: Instead of manually maintaining these sections, run `skill-sync` after creating or modifying a skill:

```bash
./skills/skill-sync/assets/sync.sh
```

This reads `metadata.scope` and `metadata.auto_invoke` from each `SKILL.md` and generates the Auto-invoke tables in the corresponding `AGENTS.md` files.

## Creating New Skills

Use the `skill-creator` skill for guidance:

```
Read skills/skill-creator/SKILL.md
```

### Quick Checklist

1. Create directory: `skills/{skill-name}/`
2. Add `SKILL.md` with required frontmatter
3. Add `metadata.scope` and `metadata.auto_invoke` fields
4. Keep content concise (under 500 lines)
5. Reference existing docs instead of duplicating
6. Run `./skills/skill-sync/assets/sync.sh` to update AGENTS.md
7. Add to `AGENTS.md` skills table (if not auto-generated)

## Design Principles

- **Concise**: Only include what AI doesn't already know
- **Progressive disclosure**: Point to detailed docs, don't duplicate
- **Critical rules first**: Lead with ALWAYS/NEVER patterns
- **Minimal examples**: Show patterns, not tutorials

## Resources

- [Agent Skills Standard](https://agentskills.io) - Open standard specification
- [Agent Skills GitHub](https://github.com/anthropics/skills) - Example skills
- [Claude Code Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) - Skill authoring guide
- [AGENTS.md](../AGENTS.md) - AI agent general rules
