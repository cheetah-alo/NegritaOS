---
id: ml-python
domain: ml
enforcement: advisory
depends_on:
  - ai-behavior
  - coding-standards
  - naming-guidelines
  - logging
  - error-handling
  - ml-disposables
  - ml-observability
  - ml-pipelines
provides:
  - ml-python-patterns
  - training-loop-guidelines
  - churn-ml-specific-practices
  - reproducibility-rules
description: >
  Canonical Python ML guidelines for churn model development. Defines training loops,
  data loading, evaluation, reproducibility, AutoML usage, governance integration,
  and best practices for working with feature engineering and pipelines.
version: 1.0.1
applyTo: [python, ml, training, evaluation, feature-engineering]
priority: warning
---

#  **ML - Python `ml-python.instructions.md`**



# Python ML Guidelines (Telecom Churn)

These rules define how Python must be used across the ML lifecycle for telecom churn models:
training, evaluation, feature engineering integration, AutoML, and reproducibility.

Environment setup must use **uv** (https://docs.astral.sh/uv/) and enforce strict linting
(mypy, ruff/flake8, mccabe complexity).

---

# 1. General Python Coding Practices

## 1.1 Tests First (TDD-oriented)
- Write tests **before** implementing major functions.
- Ensure all tests pass before merging code.
- Use `unittest` as the default framework.

## 1.2 Style & Formatting
Enforced via **flake8 + ruff**:
- snake_case everywhere
- max line length = 120
- clear, descriptive names
- remove dead code, commented blocks, debug prints
- `print()`/`display()` are forbidden in production modules and tests; use structured logging.

## 1.3 Type Hints (Mandatory)
All public functions must include type signatures and pass:

```

mypy --strict

````

Example:

```python
def process(data: pd.DataFrame) -> pd.DataFrame: ...
````

## 1.4 Avoid Mutable Defaults

Correct pattern:

```python
def func(items: list | None = None):
    items = items or []
```

## 1.5 Google-Style Docstrings

```python
def calculate_mean(values: list[float]) -> float:
    """Compute mean of numeric list.

    Args:
        values: List of numeric values.

    Returns:
        The arithmetic mean.
    """
```

## 1.6 Error Handling

Use explicit exceptions and log via the central logger:

```python
try:
    result = fn()
except Exception as ex:
    logger.error("Failed processing batch", exc_info=ex)
    raise
```

---

# 2. Code Quality Tooling

| Tool    | Purpose                             |
| ------- | ----------------------------------- |
| ruff    | linting + formatting (fast)         |
| flake8  | style rules                         |
| mypy    | static typing (strict)              |
| vulture | unused-code detection               |
| mccabe  | enforce cyclomatic complexity (<10) |
| pylint  | structural analysis                 |

All checks must pass in CI.

---

# 3. Data Science & Feature Engineering Practices

## 3.1 Pandas/Numpy Standards

* Prefer vectorized operations
* Use `.loc` and `.iloc` explicitly
* Groupby-based aggregations over loops

## 3.2 Feature Engineering Integration

* All generated features must comply with:

  * `feature-naming.instructions.md`
  * `ml-feature-engineering.instructions.md`
* No leakage:

  * No future data in any feature
  * Respect temporal splits

## 3.3 Dataset Contracts

* Python transformations must not violate schema contracts.
* Validate:

  * column names
  * dtypes
  * null rates
  * allowed ranges

## 3.4 Exploratory Data Checks (Mandatory)

Always compute:

* row counts
* missing-value report
* target distribution
* categorical cardinality
* numerical distribution summary

These must be logged in MLflow (under `audit/data_preparation/`).

---

# 4. Training Loop Guidelines

Python ML training loops must comply with `ml-pipelines.instructions.md`.

## 4.1 Training Loop Requirements

* Use `model.train()` before batches
* Zero gradients explicitly
* Track metrics using **observables**
* Trigger lifecycle events:

  * `on_step`
  * `on_epoch_start`
  * `on_epoch_end`
* Do not store GPU tensors globally

Minimal example:

```python
for epoch in range(cfg.epochs):
    trainer.on_epoch_start.trigger()
    for x, y in dataloader:
        loss = model.train_step(x, y)
        trainer.loss.set(loss)
        trainer.on_step.trigger()
    trainer.on_epoch_end.trigger()
```

## 4.2 Evaluation Loop Requirements

* Use `.eval()` mode
* Disable autograd
* Push metrics into observables

```python
with torch.no_grad():
    model.eval()
    for x, y in val_loader:
        preds = model(x)
        val_acc.set(compute_accuracy(preds, y))
```

---

# 5. AutoML Usage (AutoGluon, FLAML)

AutoML must follow:

* `automl.instructions.md`
* MLflow + telemetry integration
* Full audit directory structure

## 5.1 AutoGluon Example

```python
from autogluon.tabular import TabularPredictor

predictor = TabularPredictor(label="target").fit(
    train_data=df,
    presets="best_quality",
    time_limit=3600,
)
```

Rules:

* Treat AutoML as **baselines**, not production models
* Validate feature leakage manually
* Log leaderboard, feature importance, and trial metrics
* Wrap predictors in **AutoMLDisposable**

---

# 6. Jupyter Notebook Standards

* Use notebooks only for exploration or storyboarding
* Keep cells short and modular
* Use descriptive Markdown headings
* `print()` and `display()` are allowed only inside notebooks or `# %%` interactive scripts
* Export finalized logic into Python modules (never keep production logic inside notebooks)
* Visualizations must always include:

  * title
  * axis labels
  * legend (when applicable)

---

# 7. Performance & Optimization

* Use categorical dtypes when applicable
* Profile with:

  * `cProfile`
  * `line_profiler`
  * PyTorch Profiler (GPU workloads)
* Optimize only after identifying bottlenecks

---

# 8. Core Dependencies

Baseline ML stack:

* pandas
* numpy
* scikit-learn
* matplotlib
* seaborn
* tqdm
* AutoGluon
* PyTorch (when DL is required)
* transformers / diffusers (for advanced NLP/vision tasks)
* mlflow
* uv (environment and package management)

---

# 9. Deep Learning / Transformers / Diffusion

## 9.1 PyTorch Standards

* All models inherit from `nn.Module`
* Forward pass must be pure
* No `.to(device)` inside `forward()`
* Resources must be disposed via `ModelDisposable`

## 9.2 Transformer Standards

Use HuggingFace:

* Prefer parameter-efficient fine-tuning (LoRA, Prefix Tuning)
* Log tokenizer vocab + preprocessing pipeline in audit folder

## 9.3 Diffusion Models

* Use HuggingFace diffusers
* Save scheduler, noise settings, and seed for reproducibility

---

# 10. MLflow Tracking Requirements

### Must log:

* parameters
* metrics
* artifacts (plots, confusion matrices, SHAP)
* feature lists
* data snapshots (JSON summary only)
* model binaries

### Must not log:

* raw datasets
* PII
* file paths revealing secrets

Use:

```python
mlflow.set_experiment("churn_model")
```

---

# 11. Conventions for ML Projects

1. Start with problem + dataset definition
2. Organize code into:

   * `models/`
   * `training/`
   * `data/`
   * `utils/`
3. Use YAML or immutable dataclasses for config
4. Track experiments in MLflow
5. Use Git + PR workflow + branch protections

---

# Learnings

## Learnings
* Strict typing, linting, and reproducibility improve reliability of churn models. (4)
* Observables unify metrics streaming between training, AutoML, and telemetry systems. (3)
* AutoML baselines must be audited carefully to avoid leakage and overfitting. (2)
* All deep-learning resources must be explicitly disposed to avoid GPU memory leaks. (3)

## Changelog
v1.0.1 — Updated line-length guidance to align with repo lint settings.
