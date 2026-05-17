---
name: api-design
description: >
  API design conventions (REST/JSON APIs).
  Trigger: When creating or modifying API endpoints, schemas, or contracts.
license: Apache-2.0
metadata:
  author: generic
  version: "1.0"
  scope: [root, backend]
  auto_invoke: "Creating API endpoints"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Core Rules

- ALWAYS: Version APIs (path or header).
- ALWAYS: Validate and sanitize inputs.
- ALWAYS: Return consistent error shapes.
- NEVER: Break backward compatibility without a version bump.

## Pagination & Filtering

- Use explicit paging parameters.
- Support stable sorting keys.

## Docs

- Keep an API contract (OpenAPI/JSON schema).
- Include examples for critical endpoints.
