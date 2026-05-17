---
name: frontend-web
description: >
  Generic frontend patterns for component layout, state, and UI structure.
  Trigger: When building UI components, pages, or shared UI utilities.
license: Apache-2.0
metadata:
  author: generic
  version: "1.0"
  scope: [root, frontend]
  auto_invoke: "Creating/modifying frontend UI components"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Core Rules

- ALWAYS: Keep components small and composable.
- ALWAYS: Co-locate feature-only code; share only if used in 2+ places.
- NEVER: Mix data fetching with presentation if it bloats components.

## Suggested Structure

```
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── lib/
│   └── styles/
```

## State

- Prefer local state first; lift only when needed.
- Use a store only for cross-feature state.
