---
name: pr-review-deep
description: >
  Deep technical review protocol for this repository.
  Trigger: Reviewing any external or internal contribution before merge.
license: Apache-2.0
metadata:
  author: local
  version: "2.0"
---

## When to Use

Use this skill when:
- Evaluating pull requests from contributors
- Reviewing risky refactors or data-governance changes
- Deciding merge versus request-changes

## Review Protocol

1. For real pull requests, run `pull-request-risk-review` first and carry its
   risk score, hard stops, CI status, and quality-check evidence into this
   review.
2. Read the full diff, not only the summary.
3. Check alignment with `system.md`, active profile rules, and relevant skills.
4. Verify tests, especially regression coverage for bug fixes and logic changes.
5. Validate contracts, APIs, and user-visible semantics against implementation.
6. Check docs, prompts, and `.codex` guidance for drift.
7. Flag commit hygiene or scope problems separately from functional issues.

## Merge Gate

Merge only when:
- checks are green or the gap is explicitly understood
- risk is understood
- blockers are resolved
- scope is coherent
- the change remains deterministic and auditable

Otherwise request changes with actionable items.

In NegritaOS v1, PR risk review is shadow/recommendation only: do not approve,
merge, dismiss checks, or post external comments without an explicit user action.
