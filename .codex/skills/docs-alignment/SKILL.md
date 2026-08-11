---
name: docs-alignment
description: >
  Documentation alignment rules for this repository.
  Trigger: creating, updating, reorganizing, or reviewing repository
  documentation; documenting code, workflows, contracts, APIs, architecture,
  operations, prompts, rules, skills, or governance changes.
license: Apache-2.0
metadata:
  author: local
  version: "2.1"
  scope: [root]
  auto_invoke:
    - "Creating or updating repository documentation"
    - "Creating or updating README, AGENTS, runbooks, ADRs, rules, skills, prompts, or templates"
    - "Documenting behavior, workflows, contracts, APIs, architecture, setup, operations, or governance changes"
    - "Reviewing documentation consistency"
---

## When to Use

Use this skill when:
- Changing APIs, workflows, prompts, rules, or setup behavior
- Updating contracts, examples, or operational guidance
- Writing contributor guidance under `.codex/`, `doc/`, or repository READMEs
- Creating or updating runbooks, ADRs, decision records, technical memos, or
  architecture notes
- Reviewing whether documentation is current, structured, and traceable

## Mandatory Companion Rule

Before creating or substantially updating documentation, apply
[documentation-governance](../../rules/documentation-governance.md). It defines
the required document class decision, minimum structure, template policy, and
quality gates.

For stakeholder deliverables (`.md`, `.pptx`, `.ppt`, `.pdf`, `.docx`, `.doc`,
or `.html`), also apply `document-control`.

## Document Class Decision

| Document class | Examples | Required action |
|---|---|---|
| Source documentation | `README.md`, `docs/*.md`, `.codex/*`, `rules/*`, `skills/*`, templates | Keep beside source of truth and update in the same change set. |
| Deliverable documentation | Notion/Confluence markdown, stakeholder report, deck, PDF, DOCX, HTML | Use `document-control`; select the output path, preserve versioning, and use a manifest when tracked. |
| Decision documentation | ADR, decision memo, architecture note | Use the closest template and record context, decision, alternatives, impact, and update trigger. |
| Analytical documentation | EDA report, model review, KPI explanation, findings memo | Use the relevant findings/reporting skill and cite source paths or run IDs. |

## Minimum Structure Gate

New or substantially rewritten docs must include:

1. Title.
2. Purpose.
3. Audience and scope.
4. Source of truth or provenance.
5. Current behavior or contract.
6. Procedure, examples, schema, or command usage.
7. Quality gates or validation.
8. Ownership and update trigger.
9. Open questions or limitations, when applicable.

Small docs can compress these sections, but they must still make purpose,
scope, source of truth, current behavior, and validation explicit.

## Alignment Rules

1. Docs must describe current behavior, not intended behavior.
2. Update docs in the same change set as the behavior change.
3. Keep repository paths, commands, and examples executable as documented.
4. Do not let `.codex/system.md`, rules, profiles, prompts, and skills contradict each other.
5. Remove references to deprecated files, routes, scripts, or workflows.
6. Use an existing template under `templates/` when one matches the document type.
7. Do not create root-level ad hoc docs when a scoped `docs/`, `.codex/`, or
   package-specific location exists.

## Verification

- [ ] File paths match the repository
- [ ] Commands and examples still work as written
- [ ] API and contract names match implementation
- [ ] `.codex` rules and skills are internally consistent
- [ ] Document class is explicit: source documentation or deliverable documentation
- [ ] Required structure is present or intentionally compressed for a small doc
- [ ] Deliverables use the selected output path, timestamp naming, and applicable manifest records
- [ ] Open questions, future work, and limitations are labeled as such
