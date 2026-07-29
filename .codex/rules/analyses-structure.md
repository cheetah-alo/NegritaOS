---
id: analyses-structure
domain: analysis-governance
enforcement: strict
priority: critical
depends_on:
  - negritaos-router
  - data-contracts
  - data-sql-governance
provides:
  - canonical-analysis-governance-entrypoint
description: >
  Adapter-discoverable stub for analytical EDA structure and BigQuery source
  quality governance. The canonical rules and skills live in NegritaOS.
version: 1.0.0
applyTo: [repo, agents, prompts, claude, codex, copilot]
---

# Analyses Structure - Adapter Stub

This file is a stub for adapter-aware clients that scan `.codex/rules/`.
Do not duplicate project-specific analysis rules in sibling `.codex/project.yaml`
files.

Load these canonical NegritaOS sources before planning or editing a new or
migrated analysis:

- `rules/analysis/eda_governance_rules.yaml`
- `skills/engineering/analytical_eda_governance.md`
- `skills/engineering/bigquery_analysis_governance.md`
- `templates/bigquery_analysis_source_contract.yaml`

Required resolution order:

```text
.codex/project.yaml
-> negrita_registry
-> projects/<project_id>.yaml
-> skill_profiles/data_source
-> mode_map/agents
-> integrator
-> rules/skills/rubrics
-> source-quality preflight
-> analysis
```

If canonical resolution fails, return `BLOCKED_CONFIG_RESOLUTION`. Do not infer
analysis rules from only the files visible in a sibling repository.
