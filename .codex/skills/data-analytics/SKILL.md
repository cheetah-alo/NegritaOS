---
name: data-analytics
description: >
  Data analytics and pipeline conventions (Python-first).
  Trigger: When building data pipelines, ETL jobs, or analytics workflows.
license: Apache-2.0
metadata:
  author: generic
  version: "1.0"
  scope: [root, data_analytics]
  auto_invoke: "Building data analytics pipelines"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Core Rules

- ALWAYS: Separate extraction, transformation, and loading steps.
- ALWAYS: Validate input schemas and null handling.
- ALWAYS: Make pipelines idempotent where possible.
- NEVER: Hardcode environment-specific paths.

## Reproducibility

- Record parameters and versions.
- Store intermediate artifacts in a structured location.
