# Pipeline Rules

- Pipelines must declare inputs, outputs, dependencies, and failure behavior before implementation.
- Each phase must be independently observable: wrap with `PhaseLogger` and emit start/end/failed events.
- Runtime outputs must use repo-defined output folders (`audit/`, `artifacts/`); never write ad-hoc files to the repo root.
- Pipeline steps must be independently testable; never mix extraction, transformation, and loading in one function.
- Pipelines must be idempotent: re-running on the same input must produce identical output.
- On partial failure, log the failed phase with its context and raise a typed exception; do not silently continue.
- All pipeline parameters (date ranges, tenant IDs, thresholds) must come from config, not hardcoded literals.
