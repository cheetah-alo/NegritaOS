---
name: backend-service
description: >
  Generic backend service patterns (Python-first).
  Trigger: When designing backend services, workers, data access layers, or service boundaries.
license: Apache-2.0
metadata:
  author: generic
  version: "1.0"
  scope: [root, backend]
  auto_invoke: "Creating/modifying backend services"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Core Rules

- ALWAYS: Keep business logic in services, not in controllers/routes.
- ALWAYS: Add type hints for public functions and return types.
- ALWAYS: Validate inputs at the boundary (request, message, job).
- NEVER: Mix persistence logic into request handlers.

## Recommended Structure

```
backend/
├── app/
│   ├── api/            # request handlers/controllers
│   ├── services/       # business logic
│   ├── models/         # domain models
│   ├── data/           # repositories/adapters
│   └── config/         # settings
```

## Error Handling

- Use structured errors (code + message + details).
- Map internal errors to stable API responses.

## Observability

- Add request ID and correlation IDs.
- Log at boundaries; avoid logging secrets.
