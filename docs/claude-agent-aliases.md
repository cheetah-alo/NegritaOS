# Claude Agent Aliases

NegritaOS router modes and Claude Code subagents are not the same registry.
NegritaOS owns the canonical mode and agent contracts in
`core/orchestration/metaagent_router.yaml` and `integrator.yaml`. Claude Code
discovers native subagents from local markdown files under `.codex/agents/` or
`.claude/agents/`.

This bridge exposes every NegritaOS mode as a thin Claude-native alias:

```text
.codex/agents/<mode-lowercase>.md
```

The alias files are generated wrappers. They are not a second source of truth.
If mode routing changes, update the router/integrator first, then regenerate the
aliases.

## How To Invoke

Use uppercase mode IDs in NegritaOS prompts:

```text
@agent:PRR review PR #25 as a risk gate
@agent:TD publish this documentation plan
@agent:QG gauntlet this deck against the reference
```

Use lowercase aliases in Claude native agent selection:

```text
--agent prr
--agent td
--agent qg
```

Claude may still receive a prompt that says `PRR: ...`. The selected alias must
treat that as the canonical PRR router mode and must not ask what `PRR` means
before running config resolution.

## Current Aliases

| NegritaOS Mode | Claude Alias | Canonical Agent |
|---|---|---|
| `LP` | `lp` | `team_lead_ds_agent` |
| `AE` | `ae` | `tfm_evaluator_agent` |
| `TD` | `td` | `technical_writer_agent` |
| `MR` | `mr` | `model_review_agent` |
| `CR` | `cr` | `code_review_agent` |
| `PRR` | `prr` | `pull_request_reviewer_agent` |
| `QG` | `qg` | `quality_gauntlet_agent` |
| `PA` | `pa` | `plot_analysis_agent` |
| `EP` | `ep` | `presentation_agent` |
| `DQ` | `dq` | `data_quality_sentinel_agent` |
| `RT` | `rt` | `ai_trend_radar_agent` |

## Bootstrap Contract

Every alias must run canonical resolution before answering or editing:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve --root "$PWD" --provider claude --action <action>
```

If the result is `BLOCK`, the alias responds `BLOCKED_CONFIG_RESOLUTION` and
reports the reason. If the active project registry does not declare the
canonical agent, the alias responds `ROUTING_UNAVAILABLE`.

## Synchronize

Generate or refresh the canonical aliases in NegritaOS:

```bash
python3 scripts/sync_claude_agent_aliases.py --canonical-only --write
```

Dry-run every registered project:

```bash
python3 scripts/sync_claude_agent_aliases.py --all-projects
```

Apply to every registered project adapter:

```bash
python3 scripts/sync_claude_agent_aliases.py --all-projects --write
```

The sync links aliases into sibling `.codex/agents/` folders and preserves
project-local agents such as `brene`, `max`, or `variable-calc-explainer`.
Conflicting files are backed up with `.preAlias.<timestamp>`.

## Validate

Validate NegritaOS aliases only:

```bash
python3 scripts/validate_claude_agent_aliases.py
```

Validate all registered projects:

```bash
python3 scripts/validate_claude_agent_aliases.py --all-projects
```

`scripts/validate_alignment.py` also checks the alias bridge for the meta-repo
and each registered project. A missing `prr.md` or stale wrapper is therefore a
system alignment failure, not a prompt interpretation issue.
