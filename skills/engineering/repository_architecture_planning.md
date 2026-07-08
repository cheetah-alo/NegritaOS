# Repository Architecture Planning

Use this skill when designing a new repository, reorganizing an existing repo,
or reviewing whether a repo is maintainable enough to begin feature work.

## Operating Principle

Start with the expected workflows, then design boundaries. Do not begin with a
folder tree detached from how the repo will be built, tested, deployed, reviewed,
and maintained.

## Required Architecture Pass

1. Define the repository purpose in one sentence.
2. List the primary workflows the repo must support.
3. Identify the dominant stack and runtime entrypoints.
4. Define module boundaries and ownership.
5. Define dependency direction between modules.
6. Define configuration, secret, and environment strategy.
7. Define testing layers before implementation begins.
8. Define documentation surfaces and update responsibilities.
9. Define quality gates and the command that verifies each gate.
10. Produce the first three implementation steps in dependency order.

## Minimum Maintainability Contract

A repo is not ready for normal feature work until it reaches at least `80/100`
on this scorecard and has no unresolved P0/P1 architecture blockers.

| Dimension | Points | Gate |
|---|---:|---|
| Modularity | 20 | Module boundaries and dependency direction are explicit. |
| Documentation | 15 | README, architecture notes, and public interfaces are documented. |
| Tests | 20 | Unit, integration, and smoke-test expectations are defined. |
| Configuration | 10 | Environment values and secrets are externalized. |
| Observability | 10 | Logging, errors, and run metadata are visible. |
| Reproducibility | 10 | Dependencies, seeds, and data/runtime assumptions are pinned or documented. |
| Dependency hygiene | 10 | Imports/dependencies are acyclic or exceptions are justified. |
| Developer experience | 5 | Setup/test commands are clear and short. |

## Default Repo Shape

Use this as a baseline, then adapt to the stack:

```text
.
├── README.md
├── AGENTS.md
├── docs/
│   ├── architecture.md
│   └── decisions/
├── src/
├── tests/
├── scripts/
├── configs/
└── pyproject.toml or package.json
```

## Review Rules

- Prefer fewer top-level folders with clear ownership over many vague buckets.
- Keep domain logic separate from CLI, API, UI, storage, and orchestration code.
- Put reusable contracts and schemas near the boundary they protect.
- Do not bury production code in notebooks, one-off scripts, or output folders.
- Require tests for transformation logic, public interfaces, and critical flows.
- Require documentation for setup, architecture, decisions, and quality gates.
- Mark generated artifacts and local outputs as non-source unless explicitly
  promoted.

## Output Requirements

Return:

- repository purpose;
- proposed tree;
- module boundary table;
- dependency-direction rules;
- quality score estimate;
- blocker list;
- first three implementation steps;
- validation commands.
