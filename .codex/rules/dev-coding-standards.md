---
id: coding-standards
domain: dev
enforcement: strict
applyTo: [python, frontend, repo, architecture]
depends_on:
  - ai-behavior
  - naming-guidelines
  - error-handling
  - logging
provides:
  - python-style
  - refactoring-rules
  - repo-structure
description: >
  Repository-wide coding standards for the ML-as-code churn platform. Defines Python
  style, module layout, acceptable complexity, refactoring expectations, and hygiene
  rules under a strict–moderate enforcement model.
version: 1.2.0
priority: critical
---

#  **Coding Standars `coding-standards.instructions.md`**



# Coding Standards for Python Dev

These standards apply to **all Python modules**, **pipelines**, **validators**, **feature engineering code**, and **model training components**.  
They ensure: readability, maintainability, correctness, and alignment with the rest of the instruction system.


---

# 1. Simplicity & Operational Readability**Core Principle:** 

We write code for the *next* developer (often yourself in 6 months). If an ML engineer cannot audit the logic of a transformation in under 120 seconds, the code is too complex.

### 1.1 Explicit Intent & Zero-Ambiguity* **No Magic Values:** 
All thresholds (e.g., `0.9617` leakage threshold or `300s` time limit) must reside in a `config.json` or a `Constants` class. No allowed literal strings in the code, all must be named constants.

* **Semantic Naming:** Variable names must describe their data state.
* *Bad:* `df2 = preprocess(df)`
* *Good:* `churn_encoded_df = encoder.transform(raw_telecom_df)`
* *Bad:* `k`
* *Good:* `key_customer_id`
* *Bad:* `cfg`
* *Good:* `config`


* **Functional Purity:** Utility functions must be "Stateless." They should not modify global variables or hidden state. Input \rightarrow Output.

### 1.2 Structural Guardrails
To maintain a lean codebase, we enforce the following hard limits:

* **Complexity Gate:** Functions must have a **Cyclomatic Complexity < 10**. If your `if/else` logic branches more than 10 times, refactor into a Strategy pattern. Avoid deeply nested conditionals.
* **Module Boundaries:** Keep `.py` files under **800 lines**. If a file exceeds this, it is likely doing too much (violating Single Responsibility) and must be split (e.g., `trainer.py` \rightarrow `trainer_utils.py`, `trainer_core.py`).
* **Type Safety:** Mandatory Type Hints for all signatures. Use `Pandas-Type-Checks` where possible to define expected DataFrame schemas.

### 1.3 Automated Quality Enforcement (The Toolchain)

Readability is not subjective; it is measured by our CI/CD pipeline. Every PR must pass:

1. **Ruff:** For lightning-fast PEP 8 and logic linting.
2. **MyPy:** For static type validation.
3. **Vulture:** To identify and prune "Dead Code" (unused features or abandoned experiments).
4. **DeepSource/SonarQube:** To flag "Cognitive Complexity" hotspots.

### 1.4 Self-Documenting Architecture* **Public Contracts:** 

Every public class/function requires a Google-style docstring explaining the *Why*, not just the *How*.
* **Traceability:** Every function that transforms data must log its "Phase" (e.g., `[PHASE START] DATA_CLEANING`) to ensure the execution log remains a readable map for debugging.

---

# 2. Avoid Duplication

- Before implementing new functionality, check:
  - `utils/`
  - existing feature engineering modules
  - existing validators / model wrappers
- If a pattern already exists, reuse it.
- If similar logic is duplicated across files:
  - extract a shared helper module
  - enforce consistent naming & signatures.

Duplication is considered a **refactoring violation** and must be resolved promptly.

---

# 3. Environment-Aware Structure

Code must run cleanly in **dev**, **test**, and **prod** environments.

Rules:

- All environment configuration must come from:
  - environment variables,
  - tenant JSON files,
  - or central config modules.
- No hardcoded paths or environment-specific logic in modules.
- Determinism across environments is required:
  - stable seeds,
  - reproducible SQL queries,
  - explicit versions in metadata.

Example:

```python
ENV = os.getenv("ENV", "dev")
if ENV == "prod":
    DATA_PATH = "/mnt/prod/data/"
else:
    DATA_PATH = "./data/"
```

- Avoid hardcoded environment-specific behaviors in source files.

## 4. Safe, Minimal Changes
- Implement only what is explicitly requested or logically required.
- Introduce new tools/tech only when:
  - Justified,
  - Fully replaces existing logic,
  - And reduces maintenance burden.

## 5. Codebase Hygiene
- Enforce consistent naming conventions and directory layout.
- Remove:
  - Dead code
  - Commented-out blocks
  - Temporary debugging artifacts
- Keep commits focused and atomic.

## 6. Script & Notebook Policy
- Prefer one-off scripts run locally or in notebooks.
- Avoid committing ephemeral or exploratory artifacts to the repository.

## 7. File Size & Organization
- Keep files concise and modular.
- Split files exceeding ~300 lines into self-contained modules.

## 8. Mocking & Test Integrity
- Mock data only within the **test** suite.
- Never place stubs, fakes, or dummy values in dev/prod code paths.
- Ensure tests reflect realistic data flows.
- Apply Test Driven Development (TDD) for logic changes: start with a failing test, implement the minimum passing change, then refactor.
- Bug fixes must include a regression test proving the failure scenario is covered.

## 9. Sensitive Files
- Never overwrite `.env` or secrets without explicit confirmation.
- Treat all config files as potentially sensitive—protect accordingly.

## 9. Size Files
- 800 - 900 lines of coding is the maximum acceptable size for any single file realated with the task/main functionality.

## 10. KPI Authority Boundary (Backend Canonical)
- Canonical financial/business KPIs MUST be computed in backend services and exposed via API contracts.
- Frontend MUST consume canonical KPI values from backend and MUST NOT recompute those formulas as fallback logic.
- Frontend MAY compute UI-derived indicators only for presentation/interaction:
  - sorting ranks,
  - visual deltas,
  - chart helpers,
  - drilldown counters tied to local UI state.
- Any KPI that drives alerts, actions, persisted decisions, exports, or cross-page consistency is backend-only by definition.
- If a new KPI is needed:
  - define formula and ownership in backend first,
  - expose it in the API payload,
  - then render it in frontend.
- When frontend computes a derived metric from canonical KPIs, it must be explicitly UI-only and must not modify backend state or decision flows.
