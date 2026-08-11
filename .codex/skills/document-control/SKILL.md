---
name: document-control
description: >
  Governs creation and update of deliverable documents, decks, PDFs, DOCX files,
  HTML deliverables, and Notion/Confluence markdown. Trigger: creating or
  updating .md, .pptx, .ppt, .pdf, .docx, .doc, or .html deliverables.
license: Apache-2.0
metadata:
  author: local
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Creating or updating deliverable documents"
    - "Creating or updating PPT/PDF/DOCX/HTML deliverables"
    - "Writing Notion or Confluence-ready markdown"
---

## When to Use

Use this skill before creating or updating deliverable artifacts:

- Markdown reports, Notion docs, Confluence docs, handoff docs, executive briefs.
- PowerPoint decks: `.pptx`, `.ppt`.
- Exported PDFs: `.pdf`.
- Word documents: `.docx`, `.doc`.
- HTML deliverables intended for stakeholders, reviews, or presentations.

Do not use this skill for source documentation such as repository `README.md`,
`.codex/*`, `rules/*`, `skills/*`, `templates/*`, or code-adjacent developer
docs unless the user explicitly says that file is a deliverable artifact.
Do not classify routine plot HTML under `plots/` as a document deliverable.

## Critical Patterns

1. The user selects the output path before a deliverable is created. The path
   may be inside the repository or in an external delivery/evidence folder.
   `documents/` remains a compatible repository-local default, not a global
   requirement.
2. Every deliverable filename includes a visible update timestamp unless the
   user explicitly supplies another versioning convention:
   `<slug>__updated_YYYYMMDD_HHMMSS.<ext>`.
3. Use Europe/Madrid local time for `YYYYMMDD_HHMMSS`.
4. Updating a deliverable creates a new timestamped version. Never overwrite or
   rename the previous version.
5. For repository-local tracked deliverables, maintain the applicable manifest
   with one JSON object per deliverable version. For external binaries, a repo
   manifest is optional; report the exact path, SHA-256, storage scope, and Git
   policy in the Brain catalog or an external sidecar manifest.
6. Markdown deliverables must also keep the YAML frontmatter required by
   `core/standards/document_metadata_standards.yaml`.

## Work Root Decision

Use the narrowest project folder that owns the deliverable:

| Context | `documents/` location |
|---|---|
| Work happens inside an analysis package | `<analysis-package>/documents/` |
| Work happens at a project/repo root | `<repo-root>/documents/` |
| User gives an explicit output root | Use the exact user-selected root; do not append `documents/` |

For the HOT Orange pilot, the work root is:
`/Users/jackyb-cqi/repos/proj_data_analytics/analyses/poc_hot_orange_tsr_csr`.

## Filename Rules

- Slug format: lowercase words, digits, and single underscores.
- Keep slugs descriptive but short: `hot_cx_storytelling_deck`, not a full
  sentence.
- Required regex:

```text
^[a-z0-9][a-z0-9_]*__updated_[0-9]{8}_[0-9]{6}\.(md|pptx|ppt|pdf|docx|doc|html)$
```

Examples:

```text
documents/hot_cx_storytelling_deck__updated_20260627_163500.pptx
documents/journey_validation_report__updated_20260627_163500.md
documents/executive_brief__updated_20260627_163500.pdf
```

## Manifest Contract

For a tracked repository artifact, append one JSON object per version to the
applicable manifest (the compatible default is `documents/document_manifest.jsonl`):

```json
{
  "document_id": "hot_cx_storytelling_deck",
  "title": "HOT CX Storytelling Deck",
  "artifact_type": "pptx",
  "file_path": "documents/hot_cx_storytelling_deck__updated_20260627_163500.pptx",
  "created_at": "2026-06-27T16:35:00+02:00",
  "updated_at": "2026-06-27T16:35:00+02:00",
  "supersedes": null,
  "project_id": "proj_data_analytics",
  "agent_id": "presentation_agent",
  "router_mode": "EP",
  "source_paths": [],
  "quality_gates_status": "PASSED"
}
```

Rules:

- `file_path` is relative to the work root when possible.
- `supersedes` is the prior timestamped file path when this is an update.
- `source_paths` lists local evidence, plots, SQL, notebook, or previous
  document paths that materially informed the artifact.
- `quality_gates_status` must be one of `PASSED`, `PASSED_WITH_WARNINGS`, or
  `FAILED`.

## Update Workflow

1. Identify the user-selected output root.
2. Create the output root only when the user has authorized creation there.
3. Choose or reuse `document_id`.
4. Resolve the previous version from the applicable manifest or the newest
   matching timestamped file.
5. Write the new file as `<document_id>__updated_YYYYMMDD_HHMMSS.<ext>` unless the user supplied another versioning convention.
6. Append a manifest record for tracked repository artifacts, or record the external path and hash in Brain memory/sidecar metadata.
7. In the final response, report the new path and the superseded path, if any.

## Audit Workflow

Use the read-only auditor to find existing drift:

```bash
python3 scripts/audit_document_control.py /path/to/work-root
```

The audit reports repository-local deliverables outside `documents/` for
visibility and deliverables missing the timestamp suffix. Explicitly selected
paths are valid; the audit does not move or edit files.
