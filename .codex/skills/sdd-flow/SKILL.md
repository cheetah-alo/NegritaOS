---
name: sdd-flow
description: >
  Spec-Driven Development workflow for this repository.
  Trigger: When the user requests SDD or when a non-trivial change needs
  explicit phased planning and verification.
license: Apache-2.0
metadata:
  author: local
  version: "2.0"
---

## When to Use

Use this skill when:
- Starting non-trivial changes
- Coordinating discovery, design, implementation, and validation
- Running command-based or document-based phased delivery

## Canonical Phase Order

1. `explore` - understand existing behavior, constraints, and rule interactions
2. `propose` - define intent, scope, and risks
3. `apply` - implement the approved change set
4. `verify` - validate behavior, regressions, and rule compliance
5. `archive` - summarize what changed and what remains

Never skip a phase without explicit rationale.

## Artifacts per Phase

- Explore: findings, touched systems, and risks
- Propose: bounded plan with acceptance criteria
- Apply: code, configs, docs, and tests
- Verify: evidence of validation
- Archive: summary, follow-ups, and durable learnings if relevant

## Exit Criteria

- [ ] Scope and risks understood before implementation
- [ ] Tests or equivalent validation prove expected behavior
- [ ] Verification covers regressions and rule compliance
- [ ] Important learnings are captured for later work
