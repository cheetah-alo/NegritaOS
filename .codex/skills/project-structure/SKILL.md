---
name: project-structure
description: >
  Repository structure and placement rules for moneyflowlist.
  Trigger: Creating files, packages, handlers, services, tests, analytics
  assets, frontend modules, or governance docs in this repo.
license: Apache-2.0
metadata:
  author: local
  version: "2.0"
---

## When to Use

Use this skill when:
- Creating a new package, file, or directory
- Deciding where code belongs
- Adding tests, assets, analytics outputs, or contributor docs

## Placement Rules

1. Put HTTP and request-boundary code in `backend/app/api/`.
2. Put domain logic, stores, engines, and reusable workflows in `backend/app/services/`.
3. Put declarative rule assets in `backend/app/rules/` and contracts or config data in `backend/app/configs/`.
4. Put analytics and reporting flows in `data_analytics/`; keep exploratory notebook work out of production modules.
5. Put frontend application code in `frontend/src/`.
6. Put MCP-specific transport code in `mcp_server/` or `backend/app/mcp/`, not inside unrelated business modules.
7. Put repository governance, prompts, and agent behavior under `.codex/`.
8. Put backend tests in `tests/` and frontend test assets in `frontend/tests/` when they are browser-facing.

## File Creation Rules

- New API route -> router module + service logic + focused tests
- New persistence or state behavior -> service/store module + focused tests
- New analytics pipeline or report -> `data_analytics/` module + run/output conventions + tests where applicable
- New frontend feature -> `frontend/src/` module + relevant UI tests
- New governance guidance -> `.codex/` and any affected README or `doc/` page in the same change

## Anti-Patterns

- Do not mix transport, business logic, and persistence in one file.
- Do not duplicate business rules across API, analytics, MCP, and frontend layers.
- Do not place production logic in notebooks.
- Do not create new package layers unless they remove real coupling.
