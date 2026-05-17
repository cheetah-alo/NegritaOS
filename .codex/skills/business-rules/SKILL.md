---
name: business-rules
description: >
  Repository business-rule and governance guardrails for moneyflowlist.
  Trigger: Any change that affects classification, budgeting, sessions,
  forecasting, alerts, rule semantics, or user-visible data behavior.
license: Apache-2.0
metadata:
  author: local
  version: "2.0"
---

## When to Use

Use this skill when:
- Changing business logic with user-visible effects
- Modifying rule semantics, thresholds, or data interpretation
- Touching workflows that must remain auditable across backend, frontend, and analytics

## Product Rules

1. Never invent business semantics that are not grounded in rules, contracts, tests, or explicit user guidance.
2. User-visible classifications, KPIs, alerts, budgets, and forecasts must have a traceable implementation path.
3. Manual rules, session behavior, and persistence logic must be deterministic and testable.
4. Shared definitions must stay consistent across backend services, API responses, analytics outputs, and frontend displays.
5. Behavior changes with business impact require tests and matching documentation or rule updates.

## Decision Rules

- If semantics are unclear, ask instead of inferring.
- Prefer declarative contracts or rule files when the behavior is policy-like.
- Prefer service-layer logic when the behavior is computed or stateful.
- When behavior affects multiple surfaces, centralize the definition and reuse it.

## Validation

- Add or update regression coverage for the changed business behavior.
- Verify that affected API, analytics, and frontend outputs still agree on names and semantics.
- Confirm the change can be explained using repository rules, configs, or tests.
