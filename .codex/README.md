# Codex Rule System (`.codex`)

This directory defines the authoritative governance, architecture,
and behavior rules for this repository.

We are not allowed to delete any file. We can override rules by creating new ones with the same ID and higher version, but we cannot delete or modify existing rules, skills, profiles.

We must keep canonical memory updated under `~/.negritaos/memory/`.
Repository-local `.codex/memory/` is treated as legacy or adapter-local memory
unless a project registry explicitly makes it canonical.

It is used by:

- Human developers
- AI assistants
- Automated tooling
- CI validation pipelines

The goal is deterministic, auditable ML engineering.

---

# Purpose of the Codex System

The `.codex` directory exists to:

1. Define rules once (single source of truth)
2. Ensure consistent behavior across human and AI contributors
3. Prevent architectural and ML governance drift
4. Enable deterministic onboarding
5. Support automated reasoning by agents
6. Guarantee reproducible ML engineering practices

---

# High-Level Structure

.codex/
│
├── system.md
├── instruction-manifest.yaml
├── rules/
├── profiles/
├── skills/
├── project.yaml                  Optional repo adapter pointer to NegritaOS
└── examples/

---

# Core Concepts

## 1️⃣ Rules (`rules/`)

Rules define mandatory constraints.

Each rule:

- Has a stable `id`
- Declares dependencies
- Defines enforcement level
- Is versioned
- Is never duplicated

Rules define laws.

---

## 2️⃣ Instruction Manifest (`instruction-manifest.yaml`)

The manifest is the ontology.

It defines:

- Which rule IDs exist
- Their dependency graph
- Enforcement levels
- Resolution priority
- Versioning

All rule resolution flows through the manifest.

---

## 3️⃣ Profiles (`profiles/`)

Profiles define runtime rule selection.

Rules are permanent.
Profiles are runtime projections.

Active execution profiles:

- `analysis-run`
- `eda-pre-ml`
- `review`
- `refactor`

Profile fallback based on intent:

- SQL → DF → plots → report → `analysis-run`
- Dataset hardening before ML → `eda-pre-ml`
- Review / audit → `review`
- Refactor / structural cleanup → `refactor`

---

## 4️⃣ Skills (`skills/`)

Skills define procedural workflows.

They:

- Do NOT override rules
- Implement repeatable execution patterns
- Are auto-invoked via router when appropriate

Examples:

- `rule-compliance-gate`
- `eda-reports`
- `create-unittest`
- `data-loading`
- `feature-engineering`

Precedence:

1. system.md
2. Active profile rules (strict + critical)
3. Active profile rules (advisory + warning)
4. Skills

Rules always win.

---

## 5️⃣ System (`system.md`)

Defines global non-negotiable behavior:

- Determinism
- Strong typing
- No print statements
- Structured logging
- No architectural invention
- Separation of EDA / FE / training / evaluation
- Unittest-first testing discipline
- Test Driven Development (Red-Green-Refactor) for logic changes

---

## Local Memory

NegritaOS-managed projects use private local memory outside repositories:

```text
~/.negritaos/memory/projects/<project_id>/
```

The repo `.codex` folder may contain `project.yaml` to point at the matching
NegritaOS registry file and memory location. This prevents durable context from
being lost when work happens in branches, worktrees, or ignored local agent
folders.

---

## 6️⃣ Commit & PR Governance

Commit structure:

<type>(<scope>): <description>

PRs must:

- Declare profile used
- Declare impacted rule IDs
- Confirm deterministic behavior
- Confirm test coverage when applicable

---

## Enforcement Levels

strict → must comply
advisory → recommended, deviations justified

---

## Rule Resolution Order

1. system.md
2. Active profile rules (strict + critical)
3. Active profile rules (advisory + warning)
4. Skills

---

## Why This Exists

This prevents:

- Data leakage
- Architectural drift
- Inconsistent AI behavior
- ML reproducibility failures
- Multi-project cross-contamination

This repository is a governed ML operating system.
