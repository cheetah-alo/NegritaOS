---
id: tests-unittest-standards
domain: testing
enforcement: strict
depends_on:
  - coding-standards
  - naming-guidelines
  - ml-python
  - error-handling
provides:
  - unittest-style
  - unittest-execution
  - coverage-expectations
  - mocking-strategy
  - test-behavior-rules
description: >
  Canonical standards for Python unit tests in this repository, focused on
  behavior-driven validation of ML pipelines, feature engineering, data splitting,
  type handling, AutoML preparation, and governance logic.
version: 1.2.0
applyTo: [testing, python, unittest]
priority: critical
---

# Tests & Unittest Standards



---

## Purpose

This document defines **how unit tests must be written, structured, named, and executed**
across the repository.

It applies to:

* Backend services and API-supporting logic under `backend/app/`
* Analytics and reporting logic under `data_analytics/`
* MCP-related Python logic under `mcp_server/` or `backend/app/mcp/`
* Feature engineering and transformations
* Time-based and group-based data splitting
* Data validation and type normalization
* General-purpose Python modules in this repository

The objectives are:

* **Prevent data leakage**
* **Ensure deterministic behavior**
* **Validate business-relevant logic**
* **Avoid implementation-coupled tests**
* **Maintain long-term maintainability**

---

## TDD Policy (Mandatory)

All logic changes MUST follow Test Driven Development (TDD):

* Red: write or update a failing test that captures the expected behavior.
* Green: implement the smallest production change required to pass the test.
* Refactor: improve structure while keeping all tests green.

Additional mandatory rules:

* Every bug fix MUST include a regression test that fails before the fix.
* New behavior MUST be represented by tests before or together with implementation changes.

---

## 1. Directory Structure (Mandatory)

All unit tests MUST live under:

```
tests/
```

With one file per logical module or component:

```
tests/
test_pipeline_features.py
test_data_validation.py
test_feature_engineering.py
```

Rules:

* Use `snake_case`
* One responsibility per test file
* Every new or changed production-logic file under `backend/app/`, `data_analytics/`, or `mcp_server/` MUST have corresponding tests when it changes observable behavior
* Split large test suites when a file exceeds reasonable size

---

## 2. Test File Structure (Mandatory)

Each test file MUST contain:

* A **module-level docstring**
* One or more `unittest.TestCase` classes
* A `setUp()` method for shared fixtures
* Clear separation of test sections via comments
* Dosctring must follow google style. 

### Required layout

```python
"""Unit tests for <component under test>."""

import unittest
import pandas as pd
import numpy as np


class TestComponentName(unittest.TestCase):
    """Verifies <high-level behavior being tested>."""

    def setUp(self) -> None:
        """Initialize standard datasets or objects for testing."""
        ...

    def test_behavior_that_expected_result_when_condition(self):
        """Describe the business or ML behavior being validated."""
        ...
```

---

## 3. Naming Conventions (CRITICAL)

### 3.1 Test class naming

```
Test<ComponentName>
```

Examples:

* `TestPipelineFeatures`
* `TestTimeBasedSplitting`
* `TestFeatureTypeNormalization`

---

### 3.2 Test method naming (MANDATORY)

Tests MUST follow the **behavior-driven naming pattern**:

```
test_<behavior>_that_<expected>_when_<condition>
```

This is **non-negotiable**.

The pattern must be enforced before implementation is considered complete.
If a test name does not follow this shape, it is not compliant.

#### ✅ Good examples (from your reference)

```
test_time_split_that_no_leakage_occurs_when_split_by_date
test_time_split_that_proportions_are_correct_when_fraction_is_set
test_int64_conversion_that_dtype_becomes_numpy_int64_when_casted
test_int64_conversion_that_nans_are_filled_with_zero_when_casted
```

#### ❌ Forbidden

```
test_split()
test_casting()
test_pipeline()
```

Names must explain **why the test exists**, not just what function is called.

---

## 4. Behavioral Testing Rules

Unit tests MUST verify **observable behavior**, not implementation details.

### Tests MUST validate:

* Correct outcomes
* Absence of data leakage
* Correct branching and conditions
* Edge cases and failure paths
* Type correctness and schema guarantees

### Tests MUST NOT:

* Inspect private attributes
* Assert internal intermediate variables
* Depend on execution order
* Reproduce production code logic verbatim

---

## 5. Dataset-Based Testing (ML-Specific)

### 5.1 Time-based splitting (CRITICAL)

When testing time-based splits:

* Use **sorted temporal columns**
* Assert **strict inequality** between train and test boundaries
* Explicitly test for leakage prevention

Example pattern:

```python
self.assertLess(
    train_df["date"].max(),
    test_df["date"].min(),
    "Leakage detected: future data present in training set"
)
```

---

### 5.2 Type normalization & casting

When validating dtype logic:

* Start from realistic Pandas dtypes (`Int64`, `boolean`, `category`)
* Simulate pipeline transformations
* Assert final NumPy-compatible dtypes

Example:

```python
self.assertEqual(df["col"].dtype, np.int64)
```

---

## 6. setUp() and Fixtures

`setUp()` MUST be used to:

* Build deterministic datasets
* Create reusable DataFrames
* Initialize shared constants
* Avoid duplication across tests

Rules:

* No randomness without fixed seeds
* No shared mutable state between tests
* Keep fixtures small and readable

---

## 7. Assertions (STRICT)

Rules:

* **Max 3 assertions per test**
* Assertions must be explicit and intention-revealing
* Prefer semantic assertions over boolean tricks

### Approved assertions

```python
self.assertEqual(a, b)
self.assertLess(a, b)
self.assertGreater(a, b)
self.assertTrue(condition)
self.assertFalse(condition)
self.assertIsInstance(obj, pd.DataFrame)
self.assertRaises(ValueError)
```

### Forbidden

```python
self.assertTrue(x == y)
print(x)
assert x == y
```

---

## 8. Mocking & Isolation Rules

* Unit tests MUST NOT perform:

  * real file I/O
  * DB access
  * API calls
  * model training
* Use `MagicMock` and `patch` to isolate dependencies
* Patch heavy constructors if needed
* Always clean patches using `addCleanup`

---

## 9. Running Tests

### Standard runner

```
python -m unittest discover -s tests
```

Run a specific file:

```
python -m unittest tests/test_pipeline_features.py
```

Run a specific test:

```
python -m unittest tests.test_pipeline_features.TestPipelineFeatures.test_time_split_that_no_leakage_occurs_when_split_by_date
```

---

## 10. Coverage Requirements

Coverage is mandatory for production code.

```
coverage run -m unittest discover -s tests
coverage report --show-missing --fail-under=60
```

### Minimum thresholds

| Stage      | Coverage |
| ---------- | -------- |
| Prototype  | 40%      |
| MVP        | 60%      |
| Production | **80%**  |

Any file under **60%** coverage MUST be flagged.

---

## 11. VS Code Integration

1. Open Command Palette
2. Select **Python: Discover Tests**
3. Choose `unittest` (primary) or `pytest`
4. Set `tests/` as the root folder

Use the Testing sidebar to run and debug.

---

## Learnings

* Test **behavior**, not implementation. (2)
* Use realistic datasets to catch ML edge cases early. (2)
* Prevent leakage explicitly in time-based splits. (2)
* Strong naming is part of test correctness. (1)
* Deterministic tests are mandatory for AutoML pipelines. (1)

---

## Changelog

```
v1.3.0 — Added mandatory TDD policy (Red-Green-Refactor) and regression-test
         requirements for all logic changes and bug fixes.
v1.2.0 — Aligned test naming, structure, and examples with behavior-driven ML
         pipeline testing (time splits, dtype normalization, leakage prevention).
```
