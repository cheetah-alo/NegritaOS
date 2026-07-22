---
name: nate-skill-builder
description: >
  Use when creating, auditing, or optimizing an agent skill and when deciding
  whether a workflow belongs in a skill, rule, command, or project profile.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root]
---

# Nate Skill Builder Adapter

This is the NegritaOS adaptation of the Nate skill-builder source. Use the
existing `skill-creator` and `skill-sync` contracts as authoritative for
frontmatter, registration, scope, and auto-invocation.

Before creating a skill:

1. Confirm the pattern is reusable and does not belong in a mandatory rule.
2. Choose a unique lowercase hyphenated name matching its directory.
3. Define natural-language triggers, inputs, outputs, dependencies, side
   effects, and explicit non-goals.
4. Keep the main `SKILL.md` concise and move detailed material to local
   references or assets.
5. Test direct invocation, natural-language triggering, missing inputs, and
   dependency failures.
6. Register the skill in the canonical catalog and `AGENTS.md`.

Use `.codex`, `AGENTS.md`, project registries, and NegritaOS memory vocabulary.
Do not assume Claude-only `CLAUDE.md` paths, undocumented slash commands, or
external tools that are not declared by the active project profile.
