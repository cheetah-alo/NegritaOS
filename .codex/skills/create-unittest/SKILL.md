---
name: create-unittest
description: >
  Create or refactor Python unit tests using unittest-first (pytest optional runner),
  aligned with .codex/rules/tests-unittest-standards.md and repo dev rules.
  Use when adding/changing Python logic under backend/app, data_analytics,
  mcp_server, or validating ML/EDA behaviors.
---

# Create Unit Tests (unittest-first)

## When to use

Invoke this skill when you need to create or refactor unit tests for repository Python logic, especially for:

- New/changed module or function in `backend/app/`, `data_analytics/`, or `mcp_server/`
- Bug fix that needs regression coverage
- Refactor that risks behavior drift
- Data transforms: casting, bucketing, splitting, grouping, leakage guards
- Plot input normalization and metric computations used to build EDA artifacts

## Hard constraints (non-negotiable)

- Follow `.codex/rules/tests-unittest-standards.md` (strict).
- Tests are **unittest-first**: written as `unittest.TestCase`.
- **No** real network/DB/API/file I/O in unit tests (mock instead).
- Deterministic fixtures (no randomness unless seeded).
- Behavior-driven test names:
  `test_<behavior>_that_<expected>_when_<condition>`
- Test class names must be `Test<ComponentName>`.
- Do not write pytest-style free test functions as the primary pattern in this repository.
- Max **3 assertions per test**.
- No `print()`, no bare `assert`.
- Do not test implementation details (private attrs, intermediates, ordering).

## Allowed runners

- Primary (canonical):
  `python -m unittest discover -s tests`

- Optional runner/coverage tool (tests remain unittest):
  `pytest --cov=backend/app --cov=mcp_server --cov=data_analytics --cov-report=term-missing`

## Repository constraints (imports + structure)

- Test files must live under `tests/` and be named `test_<component>.py`.
- Prefer absolute imports matching the package layout (avoid path hacks).
- If a module requires env/config, patch it at the boundary (do not rely on local machine state).

## Inputs (what you need before writing tests)

1. Target module path (e.g., `backend/app/services/ingestion.py`)
2. Public API surface to test (functions/classes)
3. Behaviors to lock:
   - expected outputs
   - edge cases
   - failure modes
4. External boundaries to patch:
   - BigQuery client calls
   - filesystem reads/writes
   - environment variables
   - time (`datetime.now`)
   - random seeds

## Outputs (what you must produce)

A test file under `tests/` containing:

- module docstring
- one or more `unittest.TestCase` classes
- `setUp()` fixtures
- behavior-driven method names
- minimal mocking with explicit patch scope

## Target mapping (this repo)

Common targets:

- Backend services and stores:
  - `backend/app/services/**`
- API-supporting logic that still needs direct unit coverage:
  - `backend/app/api/**`
- Analytics and reporting helpers:
  - `data_analytics/**`
- MCP helpers and tool code:
  - `mcp_server/**`
- Analysis runners with isolated logic:
  - `analyses/**/run_queries.py`

## Workflow

### 1) Identify observable behaviors (Given / When / Then)

Write a short list:

- Given inputs + preconditions
- When calling the public function/method
- Then verify observable outcomes

Examples:

- Given a time column and split date, when splitting, then `train_max < test_min` (no leakage).
- Given nullable Int64, when normalizing, then dtype becomes `np.int64` and NaNs are filled per policy.
- Given invalid config, when building query, then `ValueError` is raised with a stable message.
- Given a naming rule, when writing the test, then the method name follows `test_<behavior>_that_<expected>_when_<condition>`.

### 2) Decide boundaries (unit vs integration)

Unit tests isolate dependencies. If the module touches:

- BigQuery / DB
- filesystem
- network
- model training
- heavy plotting backends

…patch the boundary.

Approved tools:

- `unittest.mock.patch`
- `unittest.mock.MagicMock`

### 3) Create the skeleton (canonical structure)

```python
"""Unit tests for <component under test>."""

import unittest
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd


class Test<ComponentName>(unittest.TestCase):
    """Verifies <high-level behavior being tested>."""

    def setUp(self) -> None:
        """Initialize deterministic fixtures for testing."""
        ...

    def test_<behavior>_that_<expected>_when_<condition>(self) -> None:
        """Describe the business or ML behavior being validated."""
        ...
```

### 4) Compliance check before finishing

Before finishing, verify:

- file name is `test_<component>.py`
- class name is `Test<ComponentName>`
- every test method follows `test_<behavior>_that_<expected>_when_<condition>`
- tests live under `tests/`
- bug fixes include a regression test
