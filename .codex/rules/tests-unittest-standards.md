---
id: tests-unittest-standards
domain: testing
enforcement: strict
depends_on:
  - coding-standards
  - naming-guidelines
provides:
  - unittest-style
  - unittest-execution
  - coverage-expectations
  - mocking-strategy
  - test-behavior-rules
version: 1.3.0
priority: critical
---

# Tests & Unittest Standards

## TDD Policy (Mandatory)
- Red: write a failing test capturing expected behavior.
- Green: implement the smallest production change to pass.
- Refactor: improve structure with all tests green.
- Every bug fix MUST include a regression test.

## Directory Structure
All tests under `tests/`. One file per logical module. `snake_case` filenames.
Every new/changed production file must have corresponding tests when it changes observable behavior.

## Test File Structure
```python
"""Unit tests for <component>."""
import unittest

class TestComponentName(unittest.TestCase):
    """Verifies <high-level behavior>."""

    def setUp(self) -> None: ...

    def test_behavior_that_expected_result_when_condition(self): ...
```

## Naming Convention (CRITICAL — non-negotiable)
```
test_<behavior>_that_<expected>_when_<condition>
```
Good: `test_time_split_that_no_leakage_occurs_when_split_by_date`
Forbidden: `test_split()`, `test_casting()`, `test_pipeline()`

## Behavioral Testing Rules
- Test observable behavior, NOT implementation details.
- Never inspect private attributes or internal intermediate variables.
- Tests must not depend on execution order.

## Dataset-Based Testing (ML-Specific)
Time-based splits: assert strict inequality between train/test date boundaries.
```python
self.assertLess(train_df["date"].max(), test_df["date"].min(), "Leakage detected")
```

## setUp() and Fixtures
- Use `setUp()` for shared deterministic fixtures (no randomness without fixed seeds).
- No shared mutable state between tests.

## Assertions
- Max 3 assertions per test.
- Use semantic assertions (`assertEqual`, `assertLess`, `assertIsInstance`, `assertRaises`).
- Forbidden: `self.assertTrue(x == y)`, `print(x)`, bare `assert`.

## Mocking
- No real file I/O, DB access, API calls, or model training in unit tests.
- Use `MagicMock` and `patch`; always clean patches with `addCleanup`.

## Running Tests
Canonical runner:
```
python -m unittest discover -s tests
```
Coverage harness (pytest allowed ONLY for coverage, must not break unittest runner):
```
pytest --cov=backend/app --cov=data_analytics --cov=mcp_server --cov-report=term-missing tests/
```

## Coverage Thresholds
| Stage      | Floor |
| ---------- | ----- |
| Prototype  | 40%   |
| MVP        | 60%   |
| Production | 80%   |

## Learnings
- Test behavior, not implementation. (2)
- Prevent leakage explicitly in time-based splits. (2)
- Strong naming is part of test correctness. (1)

## Changelog
```
v1.3.0 — Compressed. Code examples and VS Code integration section removed.
```
