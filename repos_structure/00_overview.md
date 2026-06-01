# 00 — Overview & mental model

## What NegritaOS does
NegritaOS is the **metaagent router**: it classifies every incoming session into
one of 8 operational modes and binds the agent to a specific rule + skill set.

| Code | Mode | When |
|---|---|---|
| LP | Light Planning | quick scoping |
| AE | Academic Editor | research / writing |
| TD | Technical Drafting | docs / specs |
| MR | Model Review | ML diagnostics |
| CR | Code Review | engineering review |
| EP | Executive Presenter | exec-level synthesis |
| DQ | Data Quality | data validation / contracts |
| RT | Realtime Triage | incident / on-call |

Canonical rule: `rules/global/negritaos_router_rule.md` in the NegritaOS repo
(or `~/.negritaos/rules/global/` if vendored globally).

## Federation principle
- **Pure NegritaOS modes** (LP, AE, TD, EP, RT) → load only NegritaOS rules.
- **Engineering modes** (MR, CR, DQ) → load NegritaOS rules first, then activate
  `.codex/rules/dev-*.md` and craft skills as a supporting layer. NegritaOS
  rules always win on conflict.

## Why `.codex/` (not `.claude/` or both)
- Two folders inevitably drift.
- `.codex/` is the **single source of truth**. `.claude` is a relative symlink
  to `.codex` so any Claude-based client sees the same content.

## Why `AGENTS.md` (not `CLAUDE.md` / `CODEX.md`)
- `AGENTS.md` is the shared standard both Claude Code and Codex CLI read.
- Only create `CLAUDE.md` / `CODEX.md` as **symlinks** to `AGENTS.md` if a
  specific client version refuses to find it.

## Memory home
- Canonical: `~/.negritaos/memory/projects/<project_id>/`
- Repo-local `.codex/memory/` is **adapter scratch only**, gitignored, and must
  NOT contain sessions for any other project.

## Conflict resolution order
1. `rules/global/` (NegritaOS canonical)
2. `rules/<mode>/` (mode-specific)
3. `.codex/rules/negritaos-router.md` (adapter stub)
4. `.codex/rules/*` (craft adapters)
5. `.codex/local-overrides.md` (repo-specific)
