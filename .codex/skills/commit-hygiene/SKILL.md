---
name: commit-hygiene
description: >
  Commit standards for this repository.
  Trigger: Any commit creation, review, or staged-change cleanup.
license: Apache-2.0
metadata:
  author: local
  version: "2.0"
---

## When to Use

Use this skill when:
- Creating commits
- Reviewing commit history in a PR
- Cleaning up staged changes before commit

## Rules

1. Use the repository commit format: `<type>(<scope>): <description>`.
2. Keep one logical change per commit.
3. The message should explain why, not only what changed.
4. Do not commit generated, temporary, local, or secret-bearing artifacts.
5. Do not hide unrelated refactors inside a bug fix or feature commit.
6. Before mutating work or creating/reviewing commits, report branch state from `git status --short --branch`.
7. Report pending commits against the remote base, using `git log --oneline origin/main..HEAD` when applicable.
8. State the branch decision explicitly: continue current branch, create a new branch, or open PR before continuing.
9. If the branch has more than 5 unmerged commits, recommend opening a PR and continuing new work on a fresh branch.

## Pre-Commit Checklist

- [ ] Branch state was checked with `git status --short --branch`
- [ ] Pending commit count was checked against the remote base
- [ ] Branch decision is explicit: continue, create branch, or open PR
- [ ] Diff matches the commit scope
- [ ] No secrets, tokens, or credentials
- [ ] No cache, coverage, build, or scratch artifacts
- [ ] Relevant tests or checks for the change were run
- [ ] Commit message is clear and scoped
