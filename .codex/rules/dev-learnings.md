---
id: learnings
domain: meta
enforcement: advisory
applyTo: "**"
depends_on:
  - ai-behavior
  - coding-standards
provides:
  - learning-rules
  - counters
  - adaptation-mechanism
description: >
  Meta-instructions defining how learnings are created, validated, stored, versioned,
  and applied across all ML instruction files. Supports adaptive behavior for the
  ML-as-code churn platform.
version: 1.1.0
priority: warning
---

#  **Learnings `data-validation.instructions.md`**



# Learnings System for the ML-as-Code Platform

Learnings represent **incremental improvements in AI behavior** that accumulate across
development sessions. Each learning captures a mistake, why it mattered, how it was fixed,
and how similar issues must be handled in the future.

Learnings must be:

- extracted from interactions  
- expressed concisely  
- stored in the most relevant `.instructions.md` file  
- tracked with usage counters  
- applied consistently to future output  
- removed or downgraded when harmful or obsolete  

This allows your agent ecosystem to **self-improve** while remaining deterministic,
auditable, and consistent with ML governance rules.

---

# 1. Learning Structure

Every instruction file may include a section:

Requirements:

Each learning must be:
- short (1–4 sentences)
- actionable
- ML-relevant
- directly derived from an identified mistake or improvement
- counted using (1), (2), (3), …

Example:

## Learnings
* Always validate schema before any feature engineering step. (3)
* Dispose AutoML predictors to avoid runaway temporary disk usage. (2)

Counters indicate reliability and historical usefulness.

## 1. Learnings System for Python ML Projects

This document defines how learnings must be:

- extracted from interactions
- explained clearly to the user
- stored in the appropriate instruction file
- tracked with usage counters
- incremented or decremented when helpful or harmful
- applied consistently in future responses

Learnings represent **improvements in the AI's behavior** when reasoning about:
- ML code
- OOP design
- model training
- observables/callbacks
- data pipelines
- AutoML
- telemetry
- disposables/resource management
- Python coding practices
- configuration + environments

They function as persistent, evolving domain knowledge.

---

# 2. When the User Says “learn!”

The AI must:

## Step 1 → Identify **a problem created earlier**

Example:

* incorrect reasoning about ML metrics
* wrong tensor shapes
* misuse of DataLoader workers
* unsafe AutoML file management
* confusion between training/validation states
* forgetting to update GPU resources

## Step 2 → Explain **why it was a problem**

Example:

> “This caused incorrect validation metrics because the model remained in training mode.”

## Step 3 → Explain **how it was fixed**

Example:

> “You instructed me to switch the model to `.eval()` before inference.”

## Step 4 → Convert this to a **learning**

A 1–4 sentence actionable rule.

Example:

> “Switching models into `.eval()` mode before evaluation prevents batchnorm and dropout from corrupting validation metrics.”

## Step 5 → Present the learning to the user

In a clear, concise summary.

## Step 6 → Store the learning

Add it to the **most relevant `.instructions.md` file**, under `## Learnings`.

## Step 7 → Adjust the counter

* Increase counter if it was helpful and correct.
* Reduce counter if the learning was misleading or caused regressions.

Counters convey **relative reliability** of the learning.

---

# 3. Where Learnings Go (Python ML Context)

Learnings must be added to the **closest matching instruction file**:

| Instruction File                     | Relevant Learnings                     |
| ------------------------------------ | -------------------------------------- |
| `python.rules.instructions.md`       | Python syntax, OOP, typing, tests      |
| `ml-disposables.instructions.md`     | GPU cleanup, loaders, AutoML disposal  |
| `observables.instructions.md`        | reactive metrics, callbacks            |
| `telemetry.instructions.md`          | MLflow/OpenTelemetry best practices    |
| `tree-widgets.instructions.md`       | dataset/model tree patterns            |
| `object-orientation.instructions.md` | OOP structure, inheritance, patterns   |
| `automl.instructions.md`             | AutoGluon, FLAML, hyperparameter logic |
| `pipelines.instructions.md`          | end-to-end pipeline design             |

Learnings about **meta-behavior** remain in this file.

---

# 4. Rules for Writing Learnings

A learning MUST:

###  Be actionable

Good:

> “Avoid creating DataLoaders inside the training loop to prevent worker leaks.”

Bad:

> “Be careful with DataLoaders.”

###  Be testable

The rule must have a clear, observable effect.

###  Be ML-specific

Avoid vague software generalities.

###  Reflect actual observed mistakes

Not hypothetical ones.

###  Stay short

1–4 sentences.

###  Increase reliability on future ML tasks

Learnings are meant to *improve consistent behavior*.

---

# 5. When to Increase or Decrease Counters

### Increase counter when:

* the learning prevented a real error
* it improved ML reasoning quality
* it aligned with standard ML engineering practices
* it clarified resource management, metrics, modes, or pipeline state
* the user explicitly relied on it later

### Decrease counter when:

* the learning produced unintended behavior
* it complicated the reasoning
* it became outdated (e.g., new MLflow/OpenTelemetry APIs replace a rule)
* it is superseded by a more correct learning

### Remove a learning completely only when:

* it is categorically unsafe
* it was fundamentally incorrect
* it violates the privacy/telemetry rules
* it contradicts project instructions

---

# 6. Example “Learn!” Flow (Python ML)

### User tells AI:

> “learn!”

### AI must respond:

**1. Identify issue**

> “Earlier, I mixed training and eval modes during inference.”

**2. Explain impact**

> “This caused validation metrics to be inconsistent due to dropout and batchnorm.”

**3. Explain correction**

> “You instructed me to switch the model to `.eval()` before computing validation metrics.”

**4. Create learning**

> “Always set models to `.eval()` during validation/inference to ensure correct behavior of batchnorm and dropout.” (1)

**5. Add to corresponding instruction file**
→ appended to `deep-learning.instructions.md` under **Learnings**

---

# 7. High-Value ML Learning Categories

Learnings are especially important for:

| Category             | Example                                                      |
| -------------------- | ------------------------------------------------------------ |
| Data pipelines       | “Always validate schema before transforms.”                  |
| Model training       | “Zero gradients before backward pass.”                       |
| Evaluation           | “Never shuffle validation sets.”                             |
| Distributed training | “Broadcast config before spawning workers.”                  |
| AutoML               | “Cache cleanup required after trials.”                       |
| Metrics              | “Record wall-clock step time separately from GPU time.”      |
| OOP structure        | “Separate model logic from training logic.”                  |
| Memory management    | “Delete tensors referencing GPU memory before reallocation.” |

---

# 8. Example Learnings (Seed Set)

These serve as examples and may be adapted:

```markdown
## Learnings
* Always wrap GPU models in a Disposable to avoid memory leaks during repeated training cycles. (3)
* Never use `.to(device)` inside the forward pass; move tensors before calling the model. (2)
* Recompute derived metrics only after batched updates to avoid reactive glitches. (1)
* Persist hyperparameters as immutable dataclasses for reproducible experiments. (4)
* AutoML predictors accumulate large temporary directories — dispose them at the end of each run. (3)
```

---

# Summary

This file governs how the AI adapts over time:

* extracting ML-relevant learnings
* documenting them clearly
* storing them in the appropriate `.instructions.md`
* maintaining counters
* removing low-value or harmful patterns

This system creates **continually improving ML-specific behavior** across the entire Python instruction set.
