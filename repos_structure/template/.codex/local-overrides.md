# .codex/local-overrides.md — repo-specific overrides for <PROJECT_NAME>

This file overrides any path, lexicon, or domain assumption inherited from
`.codex/system.md` when the `.codex/` folder was copied from a sibling project.

## 1. Actual repo paths (authoritative)
List the top-level folders that exist in THIS repo. Replace examples below.

- `<folder>/` — `<purpose>`
- `<folder>/` — `<purpose>`

## 2. Paths that DO NOT exist in this repo
Tell the agent to ignore any rule that references these (often inherited from a
churn ML baseline):

- `backend/app/` — N/A unless the repo has a backend service
- `data_analytics/` — N/A unless the repo runs analytics pipelines
- `mcp_server/` — N/A unless the repo exposes an MCP server

## 3. Lexicon overrides
Replace the default domain vocabulary with this repo's domain:

- Default: `customer`, `churn`, `tenure_months`
- This repo: `<term>`, `<term>`, `<term>`

## 4. Active operational modes
Modes this repo will commonly route to (others remain valid but rarer):

- `<MODE_CODE>` — `<reason>`

## 5. Test runner
- Primary: `<unittest|pytest>`
- Discovery root: `<tests/>`

## 6. Anything else that diverges from `.codex/system.md`
- `<note>`
