---
id: documentation-governance
domain: documentation
enforcement: strict
depends_on:
  - ai-behavior
provides:
  - documentation-structure
  - documentation-quality-gates
  - documentation-placement
description: >
  Governs source documentation and deliverable documentation so every new or
  updated document has a clear purpose, structure, provenance, and validation.
version: 1.0.0
applyTo: [docs, readme, agents, rules, skills, prompts, templates, deliverables]
priority: critical
---

# Documentation Governance

## Activation

This rule is active whenever an agent creates, updates, reorganizes, reviews, or
generates documentation, including:

- repository `README.md`, `AGENTS.md`, and setup docs;
- `docs/*.md`, runbooks, architecture notes, ADRs, and decision records;
- `.codex/rules/*`, `.codex/skills/*`, `.codex/prompts/*`, and templates;
- Notion, Confluence, memo, report, handoff, PPT, PDF, DOCX, or HTML
  deliverables;
- any behavior, workflow, contract, API, dashboard, model, analysis, or
  governance change that needs matching documentation.

## Document Class Decision

| Class | Examples | Required governance |
|---|---|---|
| Source documentation | `README.md`, `docs/*.md`, `AGENTS.md`, rules, skills, prompts, templates | Load `docs-alignment`; keep docs beside the behavior they describe. |
| Deliverable documentation | Stakeholder `.md`, Notion/Confluence markdown, `.pptx`, `.pdf`, `.docx`, `.html` | Load `document-control`; write under `documents/` with timestamp and manifest. |
| Decision documentation | ADRs, decision memos, architecture notes | Load `docs-alignment`; use a decision template when available. |
| Analytical documentation | EDA reports, model reviews, finding reports | Load `docs-alignment` plus the relevant findings/reporting skill. |

If a document fits more than one class, apply all relevant governance. For
example, a stakeholder-ready markdown report uses both `docs-alignment` and
`document-control`.

## Minimum Structure

New or substantially rewritten documentation must include, in this order unless
an existing template defines a stricter order:

1. Title: exact subject, not a vague label.
2. Purpose: why this document exists and what decision or workflow it supports.
3. Audience and scope: who should use it and what is intentionally excluded.
4. Source of truth: paths, commands, data sources, or systems the doc describes.
5. Current behavior or contract: what is true now, not hoped-for behavior.
6. Procedure, structure, or examples: the usable steps, schema, API, or pattern.
7. Quality gates or validation: how to verify the doc and the thing it documents.
8. Ownership and update trigger: who/what owns it and when it must be updated.
9. Open questions or limitations: only when unresolved issues remain.

Small docs may compress sections, but they cannot omit purpose, scope, source of
truth, current behavior, and validation.

## Template Policy

- Use the closest existing template under `templates/` before inventing a new
  structure.
- If no template exists, use the minimum structure above.
- Do not create a new template unless the pattern will be reused.
- Keep examples executable and paths real.

## Quality Gates

Before finalizing documentation, verify:

- Paths, commands, IDs, router modes, and agent names exist in the repo.
- The document does not contradict `.codex/system.md`, active rules, skills,
  profiles, prompts, or project config.
- Future work is labeled as planned or open, not written as current behavior.
- Deprecated workflows are removed or clearly marked as deprecated.
- Deliverables comply with `document-control` placement, timestamp, metadata,
  and manifest rules.
- Generated docs include provenance: source files, evidence, commands, or input
  artifacts used.
- The document is readable without relying on hidden chat context.

## Prohibited Patterns

- Unstructured free-form docs with no purpose, scope, or validation.
- Documentation dumped in the repo root when a scoped folder already exists.
- Docs that describe aspirational behavior as if it already works.
- Stale paths, non-existent commands, or references to removed files.
- Deliverable documents outside `documents/` unless the user explicitly
  overrides the policy.
