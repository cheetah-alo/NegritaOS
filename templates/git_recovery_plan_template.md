# Git Tree Recovery Plan

## Scope

- Repository:
- Project:
- Integration branch:
- Owner:

## Recovery Matrix

| Context | Current state | Preservation reference | Decision | Approval |
|---|---|---|---|---|
| `<branch/worktree>` | `<dirty/unpublished/stale>` | `<ref or pending>` | `<continue/PR/archive>` | `<owner>` |

## Safety Rules

- No reset, deletion, prune, rebase, or cherry-pick without explicit approval.
- Uncommitted and committed evidence remain separate.
- Cleanup occurs only after the context is clean and its disposition is recorded.
