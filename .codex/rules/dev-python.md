---
id: ml-python
domain: ml
enforcement: advisory
depends_on:
  - coding-standards
  - naming-guidelines
  - logging
  - error-handling
provides:
  - ml-python-patterns
  - training-loop-guidelines
  - reproducibility-rules
version: 1.0.2
priority: warning
---

# Python ML Guidelines (Telecom Churn)

## TDD Policy (Mandatory)
- Write tests BEFORE implementing major functions.
- Every bug fix MUST include a regression test.
- `unittest` is the canonical framework.

## Style & Toolchain
- snake_case, max line length 120, no dead code or debug prints.
- `print()`/`display()` forbidden in production modules; use structured logging.
- All public functions require type hints passing `mypy --strict`.
- Google-style docstrings on all public symbols.
- Avoid mutable defaults: use `items: list | None = None; items = items or []`.

| Tool    | Purpose                              |
| ------- | ------------------------------------ |
| ruff    | linting + formatting                 |
| mypy    | static typing (strict)               |
| vulture | unused-code detection                |
| mccabe  | cyclomatic complexity < 10           |

## Feature Engineering Rules
- All features must comply with feature-naming and feature-engineering conventions.
- No leakage: no future data in any feature; respect temporal splits.
- Validate column names, dtypes, null rates, and allowed ranges against dataset contracts.

## EDA Checks (Mandatory before training)
Log to MLflow: row counts, missing-value report, target distribution, categorical cardinality, numerical summary.

## Training Loop Requirements
- Use `model.train()` before batches; `model.eval()` + `torch.no_grad()` for evaluation.
- Zero gradients explicitly before backward pass.
- Track metrics via observables; trigger lifecycle events (`on_step`, `on_epoch_start`, `on_epoch_end`).
- Do not store GPU tensors globally.

## AutoML Usage
- Treat AutoML outputs as baselines, not production models.
- Validate feature leakage manually after AutoML fit.
- Wrap predictors in `AutoMLDisposable` for cleanup.

## MLflow — Mandatory Logging
Log: parameters, metrics, artifacts (plots, confusion matrices, SHAP), feature lists, model binaries.
Never log: raw datasets, PII, file paths with secrets.

## Reproducibility
- Fixed random seeds declared in config.
- Deterministic SQL queries, explicit dependency versions in pyproject.toml.

## Notebooks
- Notebooks for EDA/prototyping only; extract validated logic into production modules.
- See `notebooks.md` for governance rules.

## Learnings
- Strict typing and reproducibility improve reliability of churn models. (4)
- AutoML baselines must be audited carefully to avoid leakage and overfitting. (2)
- All deep-learning resources must be explicitly disposed to avoid GPU memory leaks. (3)

## Changelog
v1.0.2 — Compressed. Full examples and DL sections removed.
