---
name: branch-pr
description: >
  Provider-neutral branch and pull-request workflow for NegritaOS projects.
  Use when preparing a change for review, selecting a base branch, or writing
  validation evidence.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root]
---

# Branch And Pull Request Workflow

Read the active project registry before creating or reviewing a branch. Use
the declared `integration_branch`; do not assume `main`, `dev`, or `dev_ml`.
The ELAL registry declares `dev_ml` as its integration branch.

Required evidence:

- current branch and worktree status;
- intended base branch and any explicit override;
- focused scope and risk notes;
- exact validation commands, counts, coverage, and E2E results;
- confirmation that temporary, coverage, output, secret, and local files are
  excluded.

Keep one logical change per branch and do not publish, push, or create a PR
unless the user or project workflow explicitly requests that action.
