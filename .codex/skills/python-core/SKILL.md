---
name: python-core
description: >
  Generic Python coding standards and module patterns.
  Trigger: When writing or refactoring Python modules, libraries, or scripts.
license: Apache-2.0
metadata:
  author: generic
  version: "1.0"
  scope: [root, backend, data_analytics]
  auto_invoke: "Writing Python modules"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Core Rules

- ALWAYS: Use type hints for public functions.
- ALWAYS: Add docstrings for public classes and functions.
- ALWAYS: Keep modules focused (single responsibility).
- NEVER: Rely on implicit global state.

## Layout

```
package/
├── __init__.py
├── core.py
├── services.py
└── utils.py
```

## Error Handling

- Raise typed exceptions with clear messages.
- Avoid swallowing exceptions; re-raise with context.
