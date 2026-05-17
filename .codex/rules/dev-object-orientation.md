---
id: object-orientation
domain: dev
applyTo: python, ml, data, deep-learning, automl
enforcement: strict
depends_on:
- coding-standards
- naming-guidelines
provides:
- oop-architecture
- class-design-rules
- trainer-interfaces
- pipeline-abstractions
description: 'Object-Oriented Programming rules for ML-as-code systems. Ensures modularity,
  disposability, extensibility, and safe resource handling for training, pipelines,
  models, feature engineering, and AutoML runtimes.

  '
version: 1.0.1
priority: critical
---

#  **Object-Orientation `object-orientation.instructions.md`**


# Object-Oriented Design Rules for ML Codebases

OOP in ML must improve:

- clarity  
- maintainability  
- testability  
- resource safety  
- pipeline modularity  

These rules govern **all Python ML code**, including models, trainers, AutoML, ETL pipelines,
feature engineering, resource managers, and telecom churn modeling components.

---

# 1. Class Responsibilities (Single Responsibility Principle)

Each class MUST represent **one and only one concern**.

### Valid responsibilities:

- **Model architecture** (forward pass only)  
- **Dataset / DataModule** (splits, loaders, transforms)  
- **Trainer** (training loop + optimization + evaluation)  
- **Metrics** (encapsulation of metric logic)  
- **Pipeline stage** (feature engineering, validation, scoring)  
- **AutoML wrapper**  
- **Disposable resource manager**  

### Anti-patterns (forbidden):

- Mixing training logic inside a model  
- Mixing DataLoader logic inside a trainer  
- Mixing ETL logic inside model or trainer  
- Keeping GPU state in global scope  

Example (correct separation):

```python
class TelecomChurnModel(nn.Module): ...
class TelecomDataModule: ...
class ChurnTrainer: ...
class ChurnMetrics: ...
class AutoMLChurnRunner:  → wrapper around AutoML lifecycle  

**Never mix dataset logic inside a model class** or **training logic inside a dataset**.


## 2. Initialization Rules

Object constructors (`__init__`) must:

- Not perform heavy computation  
- Not download data  
- Not allocate GPU resources  
- Not mutate global state  

Instead, constructors should **define structure**, while heavy operations move to:

```python
setup(), prepare(), initialize(), build(), fit(), load()
````

Example:

```python
class ImageClassifier:
    def __init__(self, num_classes: int):
        self.num_classes = num_classes
        self.model = None

    def build(self):
        self.model = torchvision.models.resnet18(num_classes=self.num_classes)
```

---

## 3. Composition > Inheritance

Prefer **composition** unless inheritance is absolutely necessary.

 Good:

```python
class Trainer:
    def __init__(self, model: Model, datamodule: DataModule):
        self.model = model
        self.data = datamodule
```

 Bad inheritance:

```python
class ModelTrainer(Model):  # never inherit model+trainer
    ...
```

Inheritance is reserved for:

* Base trainer classes
* Shared evaluation mixins
* Dataset skeletons
* Abstract models

---

## 4. Abstract Base Classes (ABCs)

Use `abc.ABC` and `@abstractmethod` for defining ML interfaces.

```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def forward(self, x): ...

    @abstractmethod
    def predict(self, x): ...
```

This enforces structure across:

* Models
* Trainers
* AutoML wrappers
* Pipeline stages

---

## 5. Encapsulation Rules

### Private attributes must use `_` prefix:

```python
self._optimizer
self._train_loader
self._current_epoch
```

### Never expose raw internal state directly unless safe.

 Allowed:

```python
@property
def num_parameters(self) -> int:
    return sum(p.numel() for p in self.model.parameters())
```

---

## 6. Factory Patterns for ML Components

Use factories for:

* Loading pretrained models
* Creating datasets
* Creating optimizers
* Building AutoML configurations

Example:

```python
class ModelFactory:
    @staticmethod
    def create_resnet(num_classes: int):
        return torchvision.models.resnet18(num_classes=num_classes)
```

Factories ensure:

* Consistency
* Avoiding duplicate instantiations
* Easier mocking for tests

---

## 7. OOP + Disposables (Integrated Rule)

Any class that allocates resources must **inherit from `Disposable`**.

Examples:

* PyTorch models
* AutoGluon predictors
* Temporary cache creators
* DataLoader worker managers

```python
class TrainSession(Disposable):
    def __init__(self):
        self.model = ...
        self.optimizer = ...
        self.tmp_dir = ...

    def dispose(self):
        del self.model
        del self.optimizer
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
```

---

## 8. Polymorphism for Pipelines and Trainers

Every ML pipeline step must implement the same API so they can be swapped.

Example:

```python
class BaseTrainer(ABC):
    @abstractmethod
    def fit(self): ...

    @abstractmethod
    def evaluate(self): ...
```

Concrete trainers:

* `SupervisedTrainer`
* `SelfSupervisedTrainer`
* `AutoMLTrainer`
* `DistributedTrainer`

This enables:

* Automated testing
* Higher reuse
* Stable interfaces
* Agent-based orchestration

---

## 9. Immutability Rule (When Possible)

Flags, config objects, and hyperparameters must be **immutable** to avoid side effects.

 Use `@dataclass(frozen=True)` for config:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TrainConfig:
    lr: float
    batch_size: int
    epochs: int
```

Configuration mutability leads to silent bugs.

---

## 10. Built-In Learnings (Examples)

### (1) Always isolate model architecture from training code

Keeps models testable and reduces coupling.

### (2) Never hold GPU tensors in global variables

Prevents memory leaks in long-running jobs.

### (3) Use ABCs to enforce consistent model/trainer APIs

Improves interoperability between experiments.

### (4) Use composition when mixing model, data, and metrics

Avoids fragile inheritance hierarchies.

---

# Summary

Python ML code must be:

* Modular
* Disposable-aware
* Interface-driven
* Extensible without rewriting
* Safe in resource handling
* Predictable and testable

This file defines the OOP rules that make ML codebases scalable and maintainable.
