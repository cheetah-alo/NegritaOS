---
name: local-memory-protocol
description: >
  Repository-local persistent memory discipline for Codex contributors.
  Trigger: Recall requests, durable discoveries, decisions, bugfixes,
  preferences, session closure, or recovery after compaction.
license: Apache-2.0
metadata:
  author: local
  version: "2.0"
---

## Purpose

Use this skill to preserve context across chats without any external memory service.
For NegritaOS, canonical durable memory lives outside project repositories under
`~/.negritaos/memory/` so it survives branch changes, temporary worktrees, and
repo-local `.codex` churn.

Repository-local `.codex/memory/` directories are legacy or adapter-local memory
unless a project registry explicitly says otherwise.

## Storage Contract

- Personal memory: `~/.negritaos/memory/personal/`
- Project memory: `~/.negritaos/memory/projects/<project_id>/`
- Observations: `~/.negritaos/memory/projects/<project_id>/observations.jsonl`
- Session summaries: `~/.negritaos/memory/projects/<project_id>/sessions/YYYY-MM-DD-session.md`
- Decisions: `~/.negritaos/memory/projects/<project_id>/decisions/`
- Task state: `~/.negritaos/memory/projects/<project_id>/tasks/`
- Working index: `~/.negritaos/memory/projects/<project_id>/index.md`
- Legacy imports: `~/.negritaos/memory/projects/<project_id>/legacy_import/`

## When to Use

Use this skill when:
- The user asks to remember, recall, or continue prior work
- The task references a feature, bug, or design that may have prior context
- You make a durable decision, fix a non-obvious bug, or discover an important constraint
- You are closing a substantive session
- You need to recover after compaction or context loss

## Search Rules

At session start or before overlapping work:
- Identify the project via `projects/<project_id>.yaml` or repo-local `.codex/project.yaml`
- Read the matching `~/.negritaos/memory/projects/<project_id>/index.md`
- Read relevant personal memory under `~/.negritaos/memory/personal/`
- Read the latest relevant file under the project `sessions/`
- Search the project memory with `rg` using project, feature, bug, or file keywords

On recall requests:
1. Check the project memory `index.md`
2. Search the project memory with `rg`
3. Open the matching session summary or observations

## Save Rules

Append one JSON object to the project `observations.jsonl` after:
- architecture or implementation decisions
- bug fixes with non-obvious causes
- discoveries, constraints, or user preferences
- meaningful config or workflow changes

Use a compact and searchable structure:
- `timestamp`
- `project`
- `type`
- `title`
- `tags`
- `files`
- `summary`
- `learned`

Write only durable information. Do not dump raw chat history or transient notes.

## Session Close Rules

Before ending a substantive session:
1. Write or update a dated file under the project `sessions/`
2. Include:
   - Goal
   - Discoveries
   - Accomplished
   - Next Steps
   - Relevant Files
3. Update the project `index.md` with the latest session and current focus

## Recovery Rules

After compaction or context loss:
1. Read the project memory `index.md`
2. Read the latest relevant session summary
3. Continue only after recovering the current goal, discoveries, and next steps

## Writing Guidance

- Keep titles short and searchable
- Prefer facts over narrative
- Include file paths when they matter
- Keep `learned` limited to the non-obvious part
- One observation should fit on one JSON line
