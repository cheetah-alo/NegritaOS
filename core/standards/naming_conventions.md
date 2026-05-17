# NegritaOS — Naming Conventions

## Files and Folders

| Type | Convention | Example |
|---|---|---|
| Folders | `kebab-case` | `ml-reviewer`, `team-lead-ds` |
| Rule files | `snake_case.yaml` | `ml_rules.yaml`, `global_rules.yaml` |
| Agent contracts | `agent.yaml` (one per agent folder) | `academic-layer/tfm-evaluator/agent.yaml` |
| Skill files | `snake_case.md` | `model_review.md`, `tldr_writer.md` |
| Template files | `snake_case_template.md` | `model_review_report_template.md` |
| Rubric files | `snake_case_rubric.yaml` | `academic_tfm_rubric.yaml` |
| Prompt files | `snake_case_prompt.md` | `tfm_evaluation_prompt.md` |
| Context files | `project_context.md` | one per project |

## Agent IDs

| Layer | Agent | ID |
|---|---|---|
| strategic | team_lead_ds_agent | LP |
| academic | tfm_evaluator_agent | AE |
| strategic | technical_writer_agent | TD |
| technical | model_review_agent | MR |
| technical | code_review_agent | CR |
| strategic | presentation_agent | EP |
| technical | data_quality_sentinel_agent | DQ |
| intelligence | ai_trend_radar_agent | RT |

Agent IDs map directly to router modes (see `metaagent_router.yaml`).

## Output Mode Labels

Output modes use `snake_case` identifiers. Examples:
- `notion_doc`
- `executive_summary`
- `tribunal_report`
- `dq_incident`
- `code_review_report`

These identifiers must match template filenames:
`templates/<output_mode>_template.md`

## YAML Schema Conventions

- Top-level key = component name
- `version` field required on all yaml contracts
- `description` field required on all yaml contracts
- Boolean flags: `true` / `false` (not `yes`/`no`)
- Lists: use block sequence style (dash notation)
- No inline comments in production yaml contracts; use `description` fields instead

## Versioning

- All contracts: semantic versioning `MAJOR.MINOR.PATCH`
- MAJOR: breaking change to schema or agent behavior
- MINOR: new field or capability added
- PATCH: correction or clarification

## Anti-Patterns in Naming

- Do not use vague names: `agent1.yaml`, `stuff.md`, `temp_rules.yaml`
- Do not mix camelCase and snake_case in the same layer
- Do not use dates in filenames — use version fields inside the file
- Do not prefix files with layer names (`ml_ml_rules.yaml` is wrong)
