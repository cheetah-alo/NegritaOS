---
name: architecture-guardrails
description: >
  Repository architecture guardrails for moneyflowlist across backend services,
  API routers, analytics code, frontend, MCP surfaces, and `.codex` governance.
  Trigger: Any change that affects boundaries, ownership, state flow, or
  cross-package responsibilities.
license: Apache-2.0
metadata:
  author: local
  version: "2.0"
---

## When to Use

Use this skill when:
- Adding a new subsystem or major package
- Moving responsibilities between backend, analytics, frontend, MCP, or governance layers
- Changing source-of-truth rules, persistence boundaries, or execution flow

## Core Guardrails

1. Keep transport boundaries thin: request handling belongs in routers, not in service logic.
2. Keep domain behavior in Python services under `backend/app/services/`.
3. Keep rule definitions and static contracts declarative under `backend/app/rules/` and `backend/app/configs/`.
4. Reuse service logic across API, analytics, and MCP surfaces instead of duplicating it.
5. New features must preserve deterministic behavior, traceability, and auditability.
6. Do not mix ingestion, normalization, classification, KPI, forecasting, and persistence concerns in the same module unless the existing design already does so intentionally.

## Decision Rules

- HTTP or REST boundary -> `backend/app/api/`
- Domain logic, stores, engines, and orchestration -> `backend/app/services/`
- Manual rules and rule assets -> `backend/app/rules/`
- Config contracts and logging config -> `backend/app/configs/`
- Analytics or reporting flows -> `data_analytics/`
- MCP transport and tool exposure -> `mcp_server/` or `backend/app/mcp/`
- Frontend rendering and browser concerns -> `frontend/src/`
- Governance, prompts, skills, and workflow rules -> `.codex/`

## Validation

- Add or update regression tests when boundaries change.
- Verify the same behavior is preserved across backend APIs, services, analytics outputs, and MCP surfaces when they touch the same concept.
- Check that logging, contracts, and docs still reflect the chosen source of truth.
