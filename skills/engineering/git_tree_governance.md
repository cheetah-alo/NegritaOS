---
name: git-tree-governance
description: >
  Provider-neutral governance for Git branches, worktrees, pull-request
  lifecycle, recovery, and safe cleanup across NegritaOS projects.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root]
  auto_invoke: "Auditing branches, worktrees, branch debt, or Git recovery"
---

# Git Tree Governance

This is a read-only-first control for repositories managed by NegritaOS. It
prevents anonymous work from being hidden in branches or worktrees and keeps
Git lifecycle decisions separate from code review decisions.

## Required Resolution

Read `.codex/project.yaml`, resolve its `negrita_registry`, and require the
project to declare `integration_branch`. Never infer `main`, `dev`, or
`dev_ml` from an upstream branch. If the declaration is missing or cannot be
resolved, return `BLOCKED_CONFIG_RESOLUTION` and do not mutate Git.

Before a write, commit, rebase, cherry-pick, push, or cleanup, run the Brain
resolution and the corresponding gate. The audit itself must remain
read-only.

## Lifecycle Invariants

- One active objective and one named owner per non-main worktree.
- A feature branch must have a task or decision identifier in its name or
  handoff.
- Open a Draft PR at the first coherent vertical slice, no later than five
  commits or three working days without an explicit exception.
- A detached worktree is a read-only baseline unless explicitly assigned.
- A dirty context must be classified before new work starts.
- Rebase is explicit-only and requires a preservation reference.
- Cherry-pick is limited to atomic commits with source and destination recorded.
- Deletion requires an inventory, preservation reference, and human approval.

## Context States

`CLEAN`, `COMMITTED_WIP`, `PR_OPEN`, `DIRTY_UNCLASSIFIED`,
`RECOVERY_REQUIRED`, `DETACHED_BASELINE`, `STALE_REVIEW`, `STALE_UNOWNED`,
`MERGED_CLEANUP`, and `ORPHANED`.

No worktree may be closed while it is `DIRTY_UNCLASSIFIED` or
`RECOVERY_REQUIRED`.

## Audit Output

The branch/worktree matrix must include repository, worktree, branch, HEAD,
upstream, declared integration branch, merge-base, ahead/behind counts,
staged/unstaged/untracked counts, last commit, PR state when available,
owner/context, classification, preservation reference, and next action.

Persistent Brain events may contain only safe identifiers and hashed paths.
Do not persist prompts, secrets, raw local paths, or file contents.

## Canonical Audit

```bash
python3 scripts/git_tree_audit.py --repo "$PWD"
python3 scripts/git_tree_audit.py --repo "$PWD" --format json
```

The auditor never deletes branches, removes worktrees, rewrites history,
stashes changes, pushes, or creates PRs.

## Decision Rules

| Situation | Required action |
|---|---|
| Dirty worktree without owner | `RECOVERY_REQUIRED`; preserve before continuing |
| More than five commits and no PR evidence | `PR_REQUIRED`; open Draft PR or record exception |
| No upstream or PR | `UNPUBLISHED_NO_PR`; do not create another branch |
| Branch behind integration with no unique commits | `STALE_REVIEW` or `MERGED_CLEANUP` |
| Branch already merged | preserve the audit record, then request cleanup approval |
| Missing integration branch | `BLOCKED_CONFIG_RESOLUTION` |
