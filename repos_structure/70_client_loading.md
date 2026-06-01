# 70 — How clients discover and load these files

## Claude Code (CLI)
- Auto-reads `AGENTS.md` at repo root.
- Auto-loads everything under `.claude/` (which is `.codex/` via symlink).
- Skill discovery: scans `.claude/skills/*/SKILL.md`.
- Memory: respects whatever `AGENTS.md` instructs (we point to `memory_home`
  from `.codex/project.yaml`).

## Codex CLI
- Auto-reads `AGENTS.md` at repo root.
- Auto-loads `.codex/instruction-manifest.yaml` and resolves rule load order.
- Skill discovery: `.codex/skills/*/SKILL.md`.

## VS Code Copilot Chat
- Reads `.github/copilot-instructions.md` if present (optional).
- Reads per-file instructions from `.claude/rules/*.md` based on their YAML
  frontmatter (`description`, `applyTo`).
- Reads skills from `.claude/skills/*/SKILL.md`.
- The current session's prelude already surfaces all of these (visible at the
  top of every Copilot Chat turn).

## How to trigger loading in a fresh session
**You don't need to.** Opening the repo is the trigger. What you need to
guarantee is that the four discovery surfaces exist:

| Surface | File |
|---|---|
| Entry pointer | `AGENTS.md` |
| Manifest | `.codex/instruction-manifest.yaml` |
| Router stub | `.codex/rules/negritaos-router.md` |
| Router skill | `.codex/skills/negritaos-mode-router/SKILL.md` |

## Optional client-specific shims

| Need | Add |
|---|---|
| Claude Desktop ignores `AGENTS.md` | `ln -s AGENTS.md CLAUDE.md` |
| Some Codex versions look for `CODEX.md` | `ln -s AGENTS.md CODEX.md` |
| VS Code Copilot needs an explicit top-level instruction | create `.github/copilot-instructions.md` that just says "See AGENTS.md and follow the NegritaOS router." |

## How to verify it actually loaded
- Claude Code: `/agents` (lists discovered agents/skills).
- Codex CLI: `codex rules list` (or equivalent for your version).
- VS Code Copilot: the chat panel shows the `<instructions>` and `<skills>`
  blocks at session start — verify `negritaos-router` and
  `negritaos-mode-router` appear.
