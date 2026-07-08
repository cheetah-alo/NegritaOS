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
* **Module Boundaries:** Keep `.py` files under **1500 lines** (preferred). Files between **1500 and 1700 lines** are accepted only if the additional length is justified by cohesive single-responsibility logic. Files **above 1700 lines MUST be refactored** (e.g., `trainer.py` -> `trainer_utils.py`, `trainer_core.py`). This threshold is the single source of truth for file size across this repo.
* **Type Safety:** Mandatory Type Hints for all signatures. Use `Pandas-Type-Checks` where possible to define expected DataFrame schemas.

### 1.2.1 Pre-Generation File-Size Gate (MANDATORY — applies to AI agents)

> **Before generating any new Python file, the agent MUST estimate its line count.**
> If the estimate exceeds **1000 lines**, STOP and propose a module split plan first.
> Do NOT generate the file until the split is approved (explicitly or implicitly by the user continuing).

Split heuristics:
- One class → one file.
- Helpers/utils extracted to `<module>_utils.py`.
- Constants extracted to `<module>_constants.py` or `config/constants.py`.
- Pipeline phases extracted to separate stage files.

For non-dashboard and non-frontend source files, if the user explicitly requests a single-file output that will exceed 1700 lines, generate it AND immediately append a `## Refactor Plan` section inside the file explaining how it must be split before merging.

Dashboard/frontend source override:
- NEVER create or accept a dashboard as one monolithic source `.html` file with inline CSS, JavaScript, data, and thousands of lines.
- Dashboard source MUST be modular across data loading, normalization, state, filters, layout, chart components, styles, and build/export code.
- A single static dashboard `.html` is allowed only as generated output under `dist/`, `build/`, `outputs/`, or a repo-approved artifact directory, with modular source and a documented generation command.
- Codex, Claude, and other NegritaOS adapters MUST reject monolithic dashboard HTML as a final implementation.

**Generating a file > 1700 lines without a Refactor Plan is a rule violation.**
**Generating a file > 3000 lines for any reason is forbidden.**

### 1.3 Automated Quality Enforcement (The Toolchain)

Readability is not subjective; it is measured by our CI/CD pipeline. Every PR must pass:

1. **Ruff:** For lightning-fast PEP 8 and logic linting.
2. **MyPy:** For static type validation.
3. **Vulture:** To identify and prune "Dead Code" (unused features or abandoned experiments).
4. **DeepSource/SonarQube:** To flag "Cognitive Complexity" hotspots.
5. **Cyclomatic Complexity:** Must be below 10 for all functions (enforced by Ruff + DeepSource).

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
- See §1.2 Structural Guardrails for the canonical thresholds (1500 preferred, 1700 hard cap).
- Keep files cohesive and modular; split by responsibility, not by line count alone.
- Dashboards must follow the `dashboard-architecture` skill: source modules are the editable truth, generated bundled HTML is an artifact only, and monolithic dashboard HTML is not accepted as final source.

## 8. Mocking & Test Integrity
- Mock data only within the **test** suite.
- Never place stubs, fakes, or dummy values in dev/prod code paths.
- Ensure tests reflect realistic data flows.
- Apply Test Driven Development (TDD) for logic changes: start with a failing test, implement the minimum passing change, then refactor.
- Bug fixes must include a regression test proving the failure scenario is covered.

## 9. Sensitive Files
- Never overwrite `.env` or secrets without explicit confirmation.
- Treat all config files as potentially sensitive—protect accordingly.
- For the full secrets / PII / credential-scanning policy see [dev-security.md](dev-security.md).

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
