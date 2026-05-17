---
name: docs-alignment
description: >
  Documentation alignment rules for this repository.
  Trigger: Any code, workflow, contract, or governance change that affects
  contributor or user-facing behavior.
license: Apache-2.0
metadata:
  author: local
  version: "2.0"
---

## When to Use

Use this skill when:
- Changing APIs, workflows, prompts, rules, or setup behavior
- Updating contracts, examples, or operational guidance
- Writing contributor guidance under `.codex/`, `doc/`, or repository READMEs

## Alignment Rules

1. Docs must describe current behavior, not intended behavior.
2. Update docs in the same change set as the behavior change.
3. Keep repository paths, commands, and examples executable as documented.
4. Do not let `.codex/system.md`, rules, profiles, prompts, and skills contradict each other.
5. Remove references to deprecated files, routes, scripts, or workflows.

## Verification

- [ ] File paths match the repository
- [ ] Commands and examples still work as written
- [ ] API and contract names match implementation
- [ ] `.codex` rules and skills are internally consistent
