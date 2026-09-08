# Git Identity Governance

Every CQI checkout selects `local_commit_identity: jacky_cqi` in its canonical
project registry. The profile in `core/orchestration/commit_identity_policies.yaml`
requires `jacky.barraza@cqisense.com` for the effective local author and committer.
Git environment overrides and `git commit --author` are checked as well.

The repository-wide contributor policy remains corporate-domain based:
`cqisense.com` and approved subdomains. This permits colleagues' corporate
commits without attributing their work to Jacky. A project can tighten CI to an
explicit `ci_allowed_emails` policy list after its contributor list is approved.
No identities are approved from historical commit metadata alone.

## Install And Check

Run from the canonical checkout:

```bash
python3 scripts/negrita_brain.py configure git-identity --all
python3 scripts/negrita_brain.py configure git-identity --all --apply --with-ci
python3 scripts/negrita_brain.py configure git-identity --all --check --with-ci
```

Omit `--all` and use `--root /absolute/repository` to target one checkout.
Without `--apply` or `--check`, the command only reports its proposed changes.
The operation changes repo-local `user.email`, `user.useConfigOnly`, and
`core.hooksPath`. It never changes global Git configuration. All existing linked
worktrees are discovered through Git. Missing worktree adapters resolve by their
shared Git directory and registered primary checkout.

Private Git metadata contains a launcher directory, installation receipt,
SHA-256 fingerprints and timestamped backups. Original hooks remain in place.
The dispatchers execute a private immutable distribution of canonical code,
addressed by its SHA-256 hash, then chain the original hook with
its arguments and, for pre-push, the original stdin. Other existing hooks remain
reachable through symlinks. A retained hook can still reject an operation.
Installed policy and runtime remain usable when the canonical checkout changes
branches. `--check` detects source/policy updates; `--apply` installs a new
version. The runtime distribution is private Git metadata, never tracked code.
The launcher uses the system Python interpreter, independent of the quality
venv. Activation is transactional: errors restore owned configuration keys,
dispatchers, receipts and CI files, including earlier checkouts in an `--all`
operation. Conflicting worktree-specific configuration is reported before any
shared config is changed. Stale worktrees marked prunable by Git are reported by
Git inventory but are neither modified nor pruned by this installer.

To restore original repo-local keys and reactivate the original hooks:

```bash
python3 scripts/negrita_brain.py configure git-identity --root /absolute/repository --restore
```

Restoration retains backups and CI files. It does not rewrite any commit.

## Commit And Push Checks

`pre-commit` calls `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT`.
It blocks when either differs from the configured exact identity.

`pre-push` consumes every ref update supplied by Git. Existing refs are checked
from remote SHA to local SHA. For new refs, it excludes only branch history
advertised by `git ls-remote` for that destination. An empty remote has no
legacy exemption. Ref deletion introduces no commits. Missing remote objects,
shallow history or unavailable metadata stop the check; fetch the necessary
history and retry. The check never fetches, amends, rebases or pushes on behalf
of the user. Reports contain commit SHA, role and masked email only.

Changes made by cherry-pick, rebase, plumbing commands or `--no-verify` must
still pass the introduced-commit scan. Local hooks are prevention, not an
unbypassable server control. PRR must also review the deterministic CI evidence.

## Repository CI

`--with-ci` materializes three neutral files from canonical sources:

- `scripts/check_git_identity.py`: a standalone Python standard-library checker.
- `.github/commit-identity-policy.json`: the repository contributor policy.
- `.github/workflows/commit-identity.yml`: the PR identity workflow.

These files contain no private local paths or system branding. Their provenance
hashes stay in Git's private installation receipt. Locally edited generated
files are preserved and reported as conflicts, never silently overwritten.

The workflow uses `pull_request_target` and branch pushes with read-only repository
permission. For PRs it checks out the trusted base SHA; for existing branch
pushes it uses the pre-push SHA, and for new branches the default branch as its
explicit baseline. It fetches incoming objects and reads their metadata;
it never checks out or executes incoming code. Credentials are restricted to the
read-only GitHub token needed for private-repository fetches. No package install
or third-party Python dependency is needed.

The workflow starts protecting PRs after it is merged into their base/default
branch. Configure `commit-identity` as a required check in the remote ruleset
and protect the workflow/checker/policy with review ownership. Until that remote
configuration and a real workflow run are verified, report `NOT_VERIFIED` for
server enforcement. The separate `identity-push-audit` job is advisory: its
workflow definition comes from the pushed branch and can itself be modified by
that push. It is never a trusted replacement for the PR gate. A push workflow
runs after publication; it cannot reject receipt of the push. Protected branches must require checks and prohibit
unreviewed direct pushes. The local installer does not claim remote protection or
publish changes automatically. Existing repository CI guards remain in place
until their replacement has been separately validated.

## Health And Boundaries

Brain contracts expose the selected local identity and allowed exact email.
Doctor and alignment report config, hook and CI drift. Drift is a warning at
general analysis startup so it does not block unrelated read-only work; the Git
hooks and PRR identity gate block the relevant Git operation.

Git metadata is self-declared and does not authenticate a human. GitHub login,
SSH identity, `gh`, `gcloud`, ADC and browser-profile selection are separate
controls. No provider account or global Git identity is switched by this feature.

References: [Git hooks](https://git-scm.com/docs/githooks),
[Git configuration](https://git-scm.com/docs/git-config), and
[GitHub event semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).
