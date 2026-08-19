# NegritaOS

**Version:** 1.1.0
**Type:** Modular Cognitive Operating System for senior technical work
**Domains:** Data Science · ML governance · Academic evaluation · Executive communication · AI/Blockchain research

> "AI should amplify expert reasoning, not replace critical thinking."

NegritaOS is **not a chatbot**. It is a governance-first operating layer that sits between you and any AI client
(Claude, Codex, Copilot, …) and forces every request through a fixed pipeline:

```
classify mode → load agent → load rules → load skills → load rubrics → generate → quality-gate → answer
```

Same prompt, same client, same answer. Drift is engineered out.

---

## Table of Contents

1. [Mental Model — the 5 building blocks](#1-mental-model)
2. [Repository Map](#2-repository-map)
3. [The Operational Modes](#3-the-operational-modes)
4. [Agents — what each one does](#4-agents)
5. [Skills — reusable cognitive units](#5-skills)
6. [Rules — non-negotiable contracts](#6-rules)
7. [Rubrics, Templates, Archetypes](#7-rubrics-templates-archetypes)
8. [Memory Model](#8-memory-model)
9. [Sibling-Repo Adapter (`.codex` / `.claude`)](#9-sibling-repo-adapter)
10. [Step-by-Step — opening a project session](#10-step-by-step--opening-a-project-session)
11. [Step-by-Step — adding a new project](#11-step-by-step--adding-a-new-project)
12. [Step-by-Step — extending the system](#12-step-by-step--extending-the-system)
13. [Validation & CI scripts](#13-validation--ci-scripts)
14. [Conflict Resolution Order](#14-conflict-resolution-order)
15. [Daily Cheat Sheet](#15-daily-cheat-sheet)

---

## 1. Mental Model

Five building blocks. Memorize these and the rest follows.

| Block | What it is | Where it lives | Mutable? |
|---|---|---|---|
| **Agents** | Personas with a fixed job (e.g. *code reviewer*, *model reviewer*). | [integrator.yaml](integrator.yaml) + [agents/](agents/) | Add new agents in `integrator.yaml`. |
| **Skills** | Reusable cognitive procedures an agent can invoke (e.g. *leakage detection*, *tldr writer*). | [skills/](skills/) (cognitive layer) and [.codex/skills/](.codex/skills/) (IDE/engineering layer). | Yes — markdown files. |
| **Rules** | Hard contracts that constrain output (style, logging, naming, security). | [rules/](rules/) (NegritaOS) and [.codex/rules/](.codex/rules/) (engineering). | Yes — versioned, never silent. |
| **Rubrics / Templates** | Quality gates and output skeletons. | [rubrics/](rubrics/), [templates/](templates/) | Yes. |
| **Memory** | Durable, per-project session state. | `~/.negritaos/memory/projects/<project_id>/` | Yes — outside any repo. |

Analogy from [docs/daily_usage_manual.md](docs/daily_usage_manual.md): NegritaOS is the school, each project is a
classroom, `.codex/project.yaml` is the nameplate on the classroom door, and `~/.negritaos/memory/…` is your personal
notebook that survives any branch switch or worktree.

---

## 2. Repository Map

```
NegritaOS/
├── integrator.yaml                 ⭐ master agent registry — START HERE
├── README.md                       this file
│
├── core/                           system-level contracts
│   ├── identity/                   who NegritaOS is
│   ├── memory/                     memory policy
│   ├── ontology/                   shared vocabulary
│   ├── orchestration/              metaagent router + execution policy
│   ├── principles/                 15 cognitive principles
│   └── standards/                  output standards (sections, fields)
│
├── agents/                         agent registry + docs
│
├── skills/                         NegritaOS cognitive skills
│   ├── transversal/  ml/  academic/  executive/  writing/
│   └── governance/   engineering/   business/   bussiness-teleco/
│
├── rules/                          NegritaOS rules (yaml + md)
│   ├── global/    analysis/   writing/    governance/
│   ├── ml/        academic/   engineering/ presentation/
│   ├── branding/  interaction/ bussiness_awereness/
│
├── rubrics/                        scoring rubrics for quality gates
├── templates/                      output templates (reports, decks, memos)
├── archetypes/                     reusable project operating patterns
├── projects/                       per-project registry → memory + paths
│
├── academic-layer/                 academic agents (paper, proposal, TFM)
├── intelligence-layer/             research / trend agents
├── strategic-layer/                leadership / communication agents
├── technical-layr/                 ML / code / data-quality agents
│
├── business-layer/  brands/        domain & brand packs
│
├── .codex/                         canonical engineering adapter (loaded by Claude/Codex/Copilot)
│   ├── rules/                      22 dev-* rules (naming, logging, errors, …)
│   ├── skills/                     IDE-time skills (typescript, react-19, dev-logging, plotting-guidelines, …)
│   ├── agents/                     Claude-native aliases for NegritaOS router modes
│   ├── commands/                   slash-commands (load-context, system-audit, handoff, roast, run-quality-checks, …)
│   └── instruction-manifest.yaml   manifest read by Claude/Codex/Copilot
├── .claude -> .codex               Claude compatibility alias; never a separate source of truth
│
├── prompts/                        reusable operational prompts
├── docs/                           user-facing guides
└── scripts/                        bootstrap + validation tooling
```

---

## 3. The Operational Modes

Every request is classified into exactly one mode (mixed requests run a pipeline).

| Mode | Label | Agent | When to use it |
|---|---|---|---|
| **LP** | Leadership Planning | `team_lead_ds_agent` | Roadmaps, Jira epics, sprint plans, escalations, OKRs |
| **AE** | Academic Evaluation | `tfm_evaluator_agent` | Thesis / TFM tribunal reviews, methodology critique |
| **TD** | Technical Documentation | `technical_writer_agent` | Notion / Confluence pages, technical memos, postmortems |
| **MR** | ML / EDA / Model Review | `model_review_agent` | Model review, EDA, SHAP, leakage, XGBoost / AutoGluon / EBM |
| **CR** | Code / Repository Work | `code_review_agent` | Code review, PRs, refactors, SQL, pipelines, MLflow |
| **PRR** | Pull Request Risk Review | `pull_request_reviewer_agent` | PR risk, merge gates, CI/check evidence |
| **QG** | Quality Bar Gauntlet | `quality_gauntlet_agent` | Benchmark-driven builder/critic loops against a named reference |
| **PA** | Evidence-First Plot Analysis | `plot_analysis_agent` | Plot, chart, dashboard, and model visual interpretation |
| **EP** | Executive Presentation | `presentation_agent` | Decks, board summaries, one-pagers |
| **DQ** | Data Quality / Escalation | `data_quality_sentinel_agent` | Schema drift, KPI anomaly, RCA, incidents |
| **RT** | Research / Trends / TFM | `ai_trend_radar_agent` + `tfm_research_advisor_agent` | AI trend digests, paper reviews, evidence-backed TFM topic proposals |

Canonical definition: [rules/global/negritaos_router_rule.md](rules/global/negritaos_router_rule.md).
Full trigger keywords: [core/orchestration/metaagent_router.yaml](core/orchestration/metaagent_router.yaml).

You can force a mode in any prompt: `@agent:MR review this churn model` or
`@agent:QG gauntlet this against <reference>`.

Claude Code native agent selection uses lowercase aliases: `--agent prr`,
`--agent td`, `--agent mr`, etc. Uppercase IDs remain the NegritaOS router
modes. See [docs/claude-agent-aliases.md](docs/claude-agent-aliases.md).

---

## 4. Agents

All agents are defined in [integrator.yaml](integrator.yaml) with the same shape:

```yaml
<agent_name>:
  description:   one-line purpose
  persona:       [who_the_agent_is]
  skills:        [list of skills/*.md to load]
  rules:         [list of rules/*.yaml to enforce]
  rubrics:       [scoring rubrics applied to output]
  templates:     [output skeletons]
  output_modes:  [allowed output shapes]
  quality_gate:  [boolean checks that must pass before answering]
```

| Agent | Job |
|---|---|
| `presentation_agent` | Executive & technical decks. Quality gate: every slide has one core message; every chart has a takeaway. |
| `paper_review_agent` | Digests, reviews and operationalizes academic papers. |
| `tfm_research_advisor_agent` | Ranks differentiated TFM topics using recent papers, legal public data, and proposal comparison. |
| `tfm_evaluator_agent` | Master's thesis proposals, milestones, tribunal reports. |
| `model_review_agent` | ML model review with explicit leakage, split-strategy and target-definition checks. |
| `code_review_agent` | Python / SQL / pipeline review, MLOps readiness, reproducibility. |
| `quality_gauntlet_agent` | Benchmarked quality loop with separate builder and critic against a real reference. |
| `technical_writer_agent` | Notion / Confluence docs with explicit assumptions & next actions. |
| `team_lead_ds_agent` | Ambiguity → requirements → tasks → roadmap → escalation. |
| `ai_trend_radar_agent` | AI / blockchain trend & paper radar with hype-vs-reality classification. |
| `data_quality_sentinel_agent` | DQ incidents, RCAs, escalation logs. |

To inspect an agent: open [integrator.yaml](integrator.yaml) and search its name.

---

## 5. Skills

Skills are markdown procedures an agent reads at runtime. Two layers:

### 5.1 NegritaOS skills (cognitive)
Under [skills/](skills/). Organized by intent:

```
skills/
  transversal/    structured_reasoning, tldr_writer, evidence_framing
  ml/             model_review, eda_review, leakage_detection, explainability_review
  academic/       paper_synthesizer, tfm_evaluation, methodology_review
  executive/      presentation_storyline, executive_summary
  writing/        notion_report, academic_feedback_writer
  governance/     risk_framing, hype_vs_reality_review
  engineering/    python_quality_review, sql_bigquery_review, reproducibility_review
  business/       project-specific business skills
```

### 5.2 Engineering skills (IDE-time)
Under [.codex/skills/](.codex/skills/). Auto-discovered by Claude / Codex / Copilot when working in code:
`negritaos-mode-router`, `rule-compliance-gate`, `create-unittest`, `python-core`, `typescript`,
`nextjs-15`, `react-19`, `zod-4`, `tailwind-4`, `playwright`, `mcp-server`, `sdd-flow`,
`commit-hygiene`, `pr-review-deep`, `local-memory-protocol`, `eda-reports`, `data-contracts`,
`dev-logging`, `plotting-guidelines`, `data-loading`, `data-analytics`, `docs-alignment`,
`document-control`, `cqi-analytical-pptx`, `rule-model-documentation`,
`dashboard-architecture`, `analytical-eda-governance`,
`bigquery-analysis-governance`, `jinja-bigquery`, `quality-bar-gauntlet`, …

Each skill is a folder with a `SKILL.md` describing **when to trigger** and **what to do**.

Federated skills from Engram and Nate are mapped in
[skills/catalog.yaml](skills/catalog.yaml). Project registries select profiles
such as `analytical-dashboard`, `data-source-bigquery`, or
`data-source-postgresql`. The academic profile `academic-tfm-review` provides
the final TFM reviewer and read-only benchmark calibration. The
`academic-tfm-research` profile proposes differentiated TFM titles with recent
literature, validated public datasets, and explicit feasibility gates. Raw imported
bundles remain reference-only.

Use `quality-bar-gauntlet` when an artifact must be compared against a named,
fetchable, comparable bar. It works for code, PRs, dashboards, plots, PPTX,
DOCX/PDF, Markdown, and research deliverables. The usage guide is
[docs/quality-bar-gauntlet.md](docs/quality-bar-gauntlet.md).

Profile resolution supports parent-first `extends` with cycle detection. The
catalog default `document-delivery` activates `docs-alignment`,
`document-control`, and `local-memory-protocol` for every project. Analytical decks then inherit
`analytical-deck-delivery` -> `cqi-analytical-pptx` -> the project-specific
ELAL or IBC profile.

### 5.3 Negrita Brain runtime

The executable kernel lives in [src/negrita_brain/](src/negrita_brain/) with a
thin CLI at [scripts/negrita_brain.py](scripts/negrita_brain.py). Use `resolve`,
`gate`, `event`, `decision`, `memory`, `close`, `doctor`, `configure`,
`catalog-legacy`, and `install` to turn project configuration into hashed
provider-scoped contracts, enforce writes, and maintain canonical project
memory without duplicating runtime summaries. The full operating contract is
[docs/negrita-brain-runtime.md](docs/negrita-brain-runtime.md).

### 5.3 IDE-time commands (slash-commands)
Under [.codex/commands/](.codex/commands/). Available as `/command-name` in any IDE client:

| Command | Purpose |
|---|---|
| `load-context` | Load project context at session start |
| `system-audit` | Health check — rules, skills, memory alignment |
| `code-review-harden` | Deep security + quality code review |
| `confidence-gate` | Pre-answer confidence self-check |
| `task-tracker` | In-session task planning and progress tracking |
| `handoff` | Chat-only continuation summary before clearing context |
| `session-handoff` | Persistent NegritaOS handoff with canonical memory writes |
| `brain` | Project memory status, remember, handoff, doctor, and migration wrapper |
| `roast` | Adversarial idea council for pressure-testing ideas |
| `commit-push-pr` | Full commit → push → PR workflow with quality gate |
| `run-quality-checks` | Local QA gate (unittest → coverage → ruff/mypy → gitleaks) |

---

## 6. Rules

Rules are the **non-negotiable** layer. They live in two places:

### 6.1 NegritaOS rules ([rules/](rules/))
Cross-domain governance: writing, presentation, branding, academic, ML, business awareness.
The most important one is [rules/global/negritaos_router_rule.md](rules/global/negritaos_router_rule.md) —
it binds every client to the mode/agent matrix.

### 6.2 Engineering rules ([.codex/rules/](.codex/rules/))
Loaded into IDE clients for coding tasks. 22 files total (globally loaded; several compressed to stubs that reference skills for full detail):

| File | Status | Purpose |
|---|---|---|
| [ai-behavior.md](.codex/rules/ai-behavior.md) | full | Tone, depth, escalation rules |
| [dev-coding-standards.md](.codex/rules/dev-coding-standards.md) | full | Python style, file-size caps, KPI boundaries |
| [dev-naming-conventions.md](.codex/rules/dev-naming-conventions.md) | compressed | Legible-word rule, constants, booleans |
| [dev-error-handling.md](.codex/rules/dev-error-handling.md) | compressed | No bare except, exception hierarchy, governance JSON |
| [dev-logging.md](.codex/rules/dev-logging.md) | compressed → skill | `PhaseLogger`, governance JSON, audit dirs — full spec in `dev-logging` skill |
| [dev-python.md](.codex/rules/dev-python.md) | compressed | Canonical ML Python (uv, mypy, ruff) |
| [dev-object-orientation.md](.codex/rules/dev-object-orientation.md) | full | SRP, composition, ABCs, disposables |
| [dev-observables.md](.codex/rules/dev-observables.md) | expanded | Observable contracts, state transitions, dispose rules |
| [dev-tree-widgets.md](.codex/rules/dev-tree-widgets.md) | expanded | Tree-state purity, stable keys, virtualization |
| [dev-commit-hygiene.md](.codex/rules/dev-commit-hygiene.md) | full | Atomic commits, trailer format, coverage reporting |
| [dev-security.md](.codex/rules/dev-security.md) | full | Secrets, PII, OWASP, `.env` hygiene |
| [dev-learnings.md](.codex/rules/dev-learnings.md) | full | `## Learnings` block protocol |
| [data-contracts.md](.codex/rules/data-contracts.md) | full | Dataset schema contracts |
| [data-contracts-lite.md](.codex/rules/data-contracts-lite.md) | stub | Quick-reference → `data-contracts` skill |
| [data-validation.md](.codex/rules/data-validation.md) | full | Structural + domain + statistical checks |
| [data-sql-governance.md](.codex/rules/data-sql-governance.md) | full | BigQuery CTE layering, determinism |
| [ml-telemetry.md](.codex/rules/ml-telemetry.md) | expanded | ML run telemetry — run IDs, SHAP artifacts, drift JSON |
| [pipelines.md](.codex/rules/pipelines.md) | expanded | Phase declarations, idempotency, observability |
| [notebooks.md](.codex/rules/notebooks.md) | full | Notebook governance (EDA only) |
| [plotting-guidelines.md](.codex/rules/plotting-guidelines.md) | compressed → skill | Labels readiness, title/subtitle, legend placement — full spec in `plotting-guidelines` skill |
| [tests-unittest-standards.md](.codex/rules/tests-unittest-standards.md) | compressed | TDD, behavior-driven naming, coverage thresholds |
| [negritaos-router.md](.codex/rules/negritaos-router.md) | stub | Adapter stub → canonical router |

Every rule file has YAML frontmatter with `enforcement: strict|advisory`, `applyTo`, `depends_on`, `provides`.
Compressed rules keep the non-negotiable bullets in global context; full detail lives in the referenced skill.

---

## 7. Rubrics, Templates, Archetypes

- **[rubrics/](rubrics/)** — YAML scoring grids per output type (code quality, EDA, model review,
  presentation quality, DQ, academic TFM, …). Agents apply them automatically at the quality-gate step.
- **[templates/](templates/)** — Markdown skeletons (code review report, decision memo, escalation log,
  Confluence page, EDA report, …). Loaded based on `output_mode`.
- **[archetypes/](archetypes/)** — Reusable project operating patterns (`data-platform.yaml`,
  `eda-analytics.yaml`, `ml-automl.yaml`, `product-app.yaml`). Each project's registry references one.

---

## 8. Memory Model

Memory **never lives in a repo**. Repos may have `.codex/memory/` directories, but those are adapters.

Canonical store:

```
~/.negritaos/memory/
├── personal/                       cross-project preferences
└── projects/
    └── <project_id>/
        ├── index.md                quick state snapshot
        ├── observations.jsonl      reusable facts and constraints
        ├── sessions/               session-by-session notes
        ├── decisions/              durable architectural decisions
        ├── tasks/                  in-flight tasks
        ├── catalog/                immutable legacy memory inventory
        └── runtime/                non-narrative contracts, events, and pointers
```

Negrita Brain is the only writer. The governing skill is
[.codex/skills/local-memory-protocol/SKILL.md](.codex/skills/local-memory-protocol/SKILL.md).
Codex native memory under `~/.codex/memories/` is separate and is not synchronized.

Load order at session start (enforced by the router):

```
1. .codex/project.yaml                          the doormat in the current repo
2. ~/.negritaos/memory/personal                 your preferences
3. ~/.negritaos/memory/projects/<project_id>    durable memory
4. .codex/local-overrides.md                    per-repo deviations (if any)
5. Task-specific profile / archetype
```

---

## 9. Sibling-Repo Adapter

Every project repository that wants NegritaOS governance becomes an **adapter**:

```
<sibling-repo>/
├── AGENTS.md                         managed Codex runtime entrypoint
├── CLAUDE.md                         imports AGENTS.md
├── .codex/
│   ├── project.yaml                  declares project_id + negrita_registry path
│   ├── settings.json                 shared Claude lifecycle hooks
│   ├── rules/*.md     → symlinks    →  NegritaOS/.codex/rules/*.md
│   ├── agents/*.md    → symlinks    →  NegritaOS/.codex/agents/*.md
│   ├── skills/AGENTS.md             →  NegritaOS canonical
│   ├── skills/negritaos-mode-router →  NegritaOS canonical
│   ├── commands/      → symlink     →  NegritaOS/.codex/commands/
│   └── instruction-manifest.yaml → symlink → NegritaOS canonical
└── .claude -> .codex                 Claude compatibility alias
```

Why symlinks: when NegritaOS rules evolve, **every sibling sees the change instantly**. No drift.

Current sibling repos (registered under [projects/](projects/)):

- `proj_data_analytics` → `/Users/jackyb-cqi/repos/proj_data_analytics`
- `composer_local_dev` → `/Users/jackyb-cqi/repos/composer-local-dev`
- `moneyflowlist` → `/Users/jackyb-cqi/repos/backup_repos/moneyflowlist`
- `ml_automl_autogluon` → `/Users/jackyb-cqi/repos/autogloun/ml_automl_autogluon`
- `ds_onedrive_workspace` → `/Users/jackyb-cqi/Library/CloudStorage/OneDrive-Personal/ds`
- `elal_journey_dashboard` → `/Users/jackyb-cqi/repos/internal-ia-rawdata-dasboard`
- `hot_archeotype_proposal_demo` → `/Users/jackyb-cqi/repos/hot_archeotype_proposal_demo`
- `hot_onedrive_workspace` → `/Users/jackyb-cqi/Library/CloudStorage/OneDrive-Personal/CQI Documents/Projects/HOT`
- `hotmobile_diamond_report` → `/Users/jackyb-cqi/repos/hotmobile-diamond-report`
- `team_ds_trackwork` → `/Users/jackyb-cqi/Library/CloudStorage/OneDrive-Personal/CQI Documents/Projects/00_TeamDataScientist`
- `ibc_fiber_network` → `/Users/jackyb-cqi/repos/ibc_fiber_network`
- `fiber_network_trap_analytics` → `/Users/jackyb-cqi/repos/fiber-network-trap-analytics`
- `fiber_hourly_analytics_sql` → `/Users/jackyb-cqi/repos/fiber-hourly-analytics-sql`
- `proj_data_o` → `/Users/jackyb-cqi/repos/backup_repos/proj_data_o`
- `tepulume_workspace` → `/Users/jackyb-cqi/repos/backup_repos/tepulume`
- `tepulume_landing` → `/Users/jackyb-cqi/repos/backup_repos/tepulume/tepulume-landing`
- `tepulume_social` → `/Users/jackyb-cqi/repos/backup_repos/tepulume/tepulume-social`
- `vene` → `/Users/jackyb-cqi/repos/backup_repos/vene`
- `hot_frictions`, `negritaos` (meta)

All siblings are validated by [scripts/validate_alignment.py](scripts/validate_alignment.py).

---

## 10. Step-by-Step — opening a project session

This is the daily flow. Use it verbatim.

### Step 1 — open the project repo (not NegritaOS)
```bash
cd /Users/jackyb-cqi/repos/<project_id>
code .   # or your editor of choice
```

### Step 2 — open a chat with your AI client and paste the activation prompt

```text
Estoy en <project_id>.
Carga .codex/project.yaml → lee /Users/jackyb-cqi/repos/NegritaOS/projects/<project_id>.yaml
→ activa agentes (integrator.yaml), skills, rules (rules/global + dev-*)
→ carga memoria ~/.negritaos/memory/projects/<project_id> (index.md, sessions/, decisions/, tasks/)
→ aplica execution_policy + metaagent_router para clasificar la request
→ load rubrics + quality_gates → ejecuta según persona + output_standards.
Listo para trabajar con governance-first approach.
Quiero continuar con [TU TAREA].
```

A shorter version works too — the router will still pick the right agent from your task description.

### Step 3 — name the mode if you want full control
- `@agent:MR …` for model review
- `@agent:CR …` for code review
- `@agent:PRR …` for pull-request risk review
- `@agent:QG …` for benchmarked quality-bar gauntlets
- `@agent:DQ …` for data-quality incidents
- `@agent:EP …` for presentations
- … see [§3](#3-the-operational-modes)

### Step 4 — accept the answer flow
Every reply should follow the `default_output_contract` declared in [integrator.yaml](integrator.yaml) for its agent:
TLDR → Context → Objective → … → Risks → Recommendations → Next_Actions.
If a section is missing, ask the agent to re-run with the quality gate enforced.

### Step 5 — close the session
At the end, persist a handoff only when another task needs continuation:

```text
Run /brain handoff following local-memory-protocol. Include decisions, blockers,
ordered next actions, and relevant files; then close with the durable_ref.
```

---

## 11. Step-by-Step — adding a new project

### Step 1 — bootstrap registry + adapter
```bash
cd /Users/jackyb-cqi/repos/NegritaOS
./scripts/bootstrap_project_adapter.sh <project_id> /absolute/path/to/repo
```
This creates:
- `projects/<project_id>.yaml` (registry entry)
- `~/.negritaos/memory/projects/<project_id>/` (canonical memory)
- `<repo>/.codex/project.yaml` (adapter)

### Step 2 — link the adapter to NegritaOS canonical
```bash
./scripts/migrate_sibling_to_canonical.sh /absolute/path/to/repo
```
This is **idempotent and safe to re-run**. It:
- Backs up any pre-existing `.claude/` to `.claude.bak.<timestamp>/`
- Symlinks every `.codex/rules/*.md` to NegritaOS canonical
- Symlinks `commands/`, `instruction-manifest.yaml`, router skill, `AGENTS.md`
- Creates `.claude → .codex` symlink
- Appends backup patterns to the repo's `.gitignore`

### Step 3 — verify alignment
```bash
cd /Users/jackyb-cqi/repos/NegritaOS
python3 scripts/validate_alignment.py --sibling /absolute/path/to/repo
```
Expect all checks to pass. If anything fails, the script prints the exact
missing symlink, alias, rule, skill, memory path, or registry reference.

### Step 4 — commit NegritaOS changes
The only file you should commit in NegritaOS is the new `projects/<project_id>.yaml`.
The sibling repo gets `.codex/project.yaml` (real file) and a `.gitignore` entry — symlinks are local.

If Claude-native agents are needed immediately, refresh aliases with:

```bash
python3 scripts/sync_claude_agent_aliases.py --repo /absolute/path/to/repo --write
python3 scripts/validate_claude_agent_aliases.py --repo /absolute/path/to/repo
```

---

## 12. Step-by-Step — extending the system

### Add a new skill
1. Decide layer: cognitive (`skills/<bucket>/<name>.md`) vs IDE (`.codex/skills/<name>/SKILL.md`).
2. Follow [.codex/skills/skill-creator/SKILL.md](.codex/skills/skill-creator/SKILL.md) — frontmatter is mandatory.
3. Register its path, scope, profile, dependencies, and side-effect policy in [skills/catalog.yaml](skills/catalog.yaml).
4. Reference native agent guidance from any relevant agent in [integrator.yaml](integrator.yaml) under `skills:`.
5. Validate with `python3 scripts/validate_skill_catalog.py` and synchronize the canonical profile section with `python3 scripts/sync_skill_catalog.py --write`.

### Add a new rule
1. Create `<file>.md` under [rules/](rules/) (NegritaOS) or [.codex/rules/](.codex/rules/) (engineering).
2. Mandatory YAML frontmatter: `id`, `domain`, `enforcement`, `applyTo`, `depends_on`, `provides`, `description`, `version`, `priority`.
3. Bump version in the file and add a `## Changelog` line.
4. Run `python3 scripts/validate_alignment.py` to verify no sibling repo breaks.

### Add a new agent
1. Append an entry to [integrator.yaml](integrator.yaml) using the canonical shape (§4).
2. Add a row to the mode table in [rules/global/negritaos_router_rule.md](rules/global/negritaos_router_rule.md).
3. Add a routing keyword block in `routing_rules.if_user_asks_for`.
4. Provide a rubric in [rubrics/](rubrics/) and a template in [templates/](templates/) if the output is novel.
5. Add the agent to the relevant `projects/<project>.yaml` registry and declare
   any selected `skill_profiles`.
6. Validate: `python3 scripts/validate_config_resolution.py` and
   `python3 scripts/validate_registry_paths.py`.

### Add a new rubric / template
1. Create the YAML / MD file in the right folder.
2. Reference it from the agent in `integrator.yaml`.
3. Make sure every `required_section` / `required_field` is enforceable by the agent's quality gate.

---

## 13. Validation & CI scripts

| Script | What it does |
|---|---|
| [scripts/validate_alignment.py](scripts/validate_alignment.py) | Verifies NegritaOS ↔ every sibling adapter. Modes: default (all), `--only-meta`, `--sibling <path>`. **Run before every commit.** |
| [scripts/validate_config_resolution.py](scripts/validate_config_resolution.py) | Resolves `.codex/project.yaml` → project registry → profiles/mode map/agents → integrator assets → catalog and wrappers. **Run before answering or committing config changes.** |
| [scripts/validate_registry_paths.py](scripts/validate_registry_paths.py) | Verifies every path referenced in `integrator.yaml`, rubrics, templates, skills resolves on disk. |
| [scripts/validate_skill_catalog.py](scripts/validate_skill_catalog.py) | Validates federated skill IDs, frontmatter, profiles, sources, and project data-source declarations. |
| [scripts/sync_claude_agent_aliases.py](scripts/sync_claude_agent_aliases.py) | Generates `.codex/agents/<mode>.md` wrappers so NegritaOS modes are invocable as Claude native aliases. |
| [scripts/validate_claude_agent_aliases.py](scripts/validate_claude_agent_aliases.py) | Validates Claude aliases for NegritaOS and registered sibling project adapters. |
| [scripts/validate_source_quality_contract.py](scripts/validate_source_quality_contract.py) | Validates logical grain, keys, timestamp roles, latency/freshness semantics, SLA, and source-quality evidence for new or migrated BigQuery analyses. |
| [scripts/materialize_project_skills.py](scripts/materialize_project_skills.py) | Dry-runs or links profile-selected canonical skills into a sibling adapter with backups. |
| [scripts/sync_skill_catalog.py](scripts/sync_skill_catalog.py) | Synchronizes federated profiles into the canonical `.codex/skills/AGENTS.md`. |
| [scripts/bootstrap_project_adapter.sh](scripts/bootstrap_project_adapter.sh) | Creates project registry + memory home + `.codex/project.yaml`. |
| [scripts/migrate_sibling_to_canonical.sh](scripts/migrate_sibling_to_canonical.sh) | Idempotent: turns any sibling repo into a symlink-based adapter. |

Recommended pre-commit:
```bash
python3 scripts/validate_config_resolution.py && python3 scripts/validate_alignment.py && python3 scripts/validate_registry_paths.py && python3 scripts/validate_skill_catalog.py
```

For a new or migrated BigQuery analysis, also validate its logical source
contract before calling the run validated or `production-ready`:

```bash
python3 scripts/validate_source_quality_contract.py --contract <source-contract.yaml>
```

---

## 14. Conflict Resolution Order

When two rules disagree, resolve top-down:

1. **Security & correctness** ([.codex/rules/dev-security.md](.codex/rules/dev-security.md), contract validation) — always wins.
2. **NegritaOS router** ([rules/global/negritaos_router_rule.md](rules/global/negritaos_router_rule.md)) — mode + agent binding.
3. **NegritaOS global rules** (`rules/global/*.yaml`).
4. **Agent-specific rules** (declared in `integrator.yaml`).
5. **Engineering adapter rules** (`.codex/rules/dev-*.md`).
6. **Sibling repo overrides** (`.codex/local-overrides.md`).
7. **Skills** (procedural — never override rules).

If steps 3–6 disagree on something non-trivial, the agent **must ask** before proceeding
(per [.codex/rules/ai-behavior.md](.codex/rules/ai-behavior.md) §10 — escalation rule).

---

## 15. Daily Cheat Sheet

```text
# Open a project session
cd ~/repos/<project_id> && code .
# then in chat:
@agent:<MODE> <task>
# in Claude native agent picker/CLI:
--agent <mode-lowercase>   # example: --agent prr
# or paste the full activation block from §10

# Validate the system after edits
cd ~/repos/NegritaOS
python3 scripts/validate_alignment.py
python3 scripts/validate_registry_paths.py

# Add a new project
./scripts/bootstrap_project_adapter.sh <project_id> /abs/path
./scripts/migrate_sibling_to_canonical.sh /abs/path
python3 scripts/validate_alignment.py --sibling /abs/path

# Persist only a continuation handoff
/brain handoff
```

Modes (quick recall):
**LP** lead · **AE** academic · **TD** docs · **MR** model · **CR** code · **PRR** PR risk · **QG** gauntlet · **PA** plots · **EP** present · **DQ** data-quality · **RT** research

---

## Key Files Index

| File | Purpose |
|---|---|
| [integrator.yaml](integrator.yaml) | Master agent registry (read first) |
| [core/orchestration/metaagent_router.yaml](core/orchestration/metaagent_router.yaml) | Request → mode classification |
| [core/orchestration/execution_policy.yaml](core/orchestration/execution_policy.yaml) | End-to-end execution contract |
| [core/identity/negrita_identity.md](core/identity/negrita_identity.md) | System identity |
| [core/ontology/domain_ontology.yaml](core/ontology/domain_ontology.yaml) | Shared vocabulary |
| [core/principles/cognitive_principles.md](core/principles/cognitive_principles.md) | 15 operating principles |
| [core/standards/output_standards.yaml](core/standards/output_standards.yaml) | Output structure requirements |
| [.codex/rules/documentation-governance.md](.codex/rules/documentation-governance.md) | Documentation structure and quality gates |
| [rules/global/negritaos_router_rule.md](rules/global/negritaos_router_rule.md) | Canonical router rule |
| [projects/README.md](projects/README.md) | Project registry & memory load order |
| [docs/daily_usage_manual.md](docs/daily_usage_manual.md) | Daily workflow walkthrough |
| [docs/presentation_and_notion_workflow.md](docs/presentation_and_notion_workflow.md) | EP / TD workflow |
| [docs/context-management-audit.md](docs/context-management-audit.md) | Full audit of 22 rule files — size, overlap, migration plan |
| [docs/context-management.md](docs/context-management.md) | Architecture guide: what belongs in rules vs skills vs commands |
| [archetypes/README.md](archetypes/README.md) | Reusable project archetypes |
| [agents/README.md](agents/README.md) | Full agent registry |

---

*NegritaOS v1.0 — built for operational rigor, not AI theater.*
