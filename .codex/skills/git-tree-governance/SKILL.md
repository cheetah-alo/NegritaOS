---
name: git-tree-governance
description: >
  Audit and govern NegritaOS Git branches, worktrees, pull-request lifecycle,
  recovery, rebase, cherry-pick, and cleanup. Trigger: git tree review,
  branch audit, worktree audit, branch debt, recover uncommitted work, or
  branch cleanup.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root]
  auto_invoke: "Auditing branches, worktrees, branch debt, or Git recovery"
---

# Git Tree Governance

Use this skill before any branch, worktree, rebase, cherry-pick, PR, or cleanup
decision. It is read-only by default and must not hide, discard, or rewrite
user work.

## First Resolution

1. Read `.codex/project.yaml` and the canonical project registry.
2. Resolve `integration_branch`; never guess the base from `upstream`.
3. Run `negrita_brain.py resolve` and `git_tree_audit.py`.
4. If the base is missing, return `BLOCKED_CONFIG_RESOLUTION`.

## Non-negotiable Rules

- One objective, owner, branch, and worktree context.
- Draft PR by the first coherent slice, five commits, or three working days.
- No new branch while the current context is dirty and unclassified.
- Rebase only with explicit approval and a preservation reference.
- Cherry-pick only atomic commits and record source SHA, destination, and PR.
- Remove a branch/worktree only after inventory, preservation, and approval.

## Required Report

Return a matrix of every branch and worktree with base, merge-base,
ahead/behind, dirty counts, upstream/PR state, last commit, classification,
owner, preservation reference, and recommended action. Separate committed
history from uncommitted files. A clean upstream branch is not proof of
alignment with the project integration branch.

## Commands

```bash
python3 scripts/git_tree_audit.py --repo "$PWD"
python3 scripts/git_tree_audit.py --repo "$PWD" --format json
git status --short --branch
git worktree list --porcelain
```

The skill does not execute `git reset --hard`, `git branch -D`,
`git worktree prune`, `git stash`, rebase, cherry-pick, push, merge, or PR
creation without a separate explicit request and gate.
