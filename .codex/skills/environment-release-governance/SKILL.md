---
name: environment-release-governance
description: >
  Govern exact-commit deployments and independent functional QA across DEV,
  UAT, and production. Trigger: deploying an environment, promoting a release,
  validating a deployed URL, or deciding whether an environment is READY.
license: Apache-2.0
metadata:
  author: NegritaOS
  version: "1.0"
  scope: [root]
  auto_invoke: "Deploying or validating DEV, UAT, or production environments"
---

## When To Use

Use this skill when a request involves:

- deploying an exact commit to DEV, UAT, or production;
- checking release prerequisites, migrations, health, or rollback readiness;
- running functional browser QA against a deployed URL;
- promoting or holding an environment based on test evidence.

Read the canonical contract at
`skills/engineering/environment_release_governance.md` before acting.

## Mandatory Sequence

1. Resolve NegritaOS context and the project release profile.
2. Identify the target environment and immutable commit SHA.
3. Verify branch policy, required CI, configuration, migration, and rollback evidence.
4. Require explicit human approval before any production mutation or promotion.
5. Deploy only the identified commit through the project-approved mechanism.
6. Verify provider status and runtime health.
7. Hand the deployed URL and commit to an independent functional QA agent.
8. Mark the environment `READY` only after QA returns `PASS`.

## Non-Negotiable Boundaries

- Deployment and functional acceptance are separate responsibilities.
- Missing access is `BLOCKED_ACCESS`, not permission to improvise.
- Production browser checks are read-only.
- DEV/UAT destructive tests require isolated users and data.
- The deployed revision must be proven, not inferred from a branch name.
- Failed or missing QA returns `HOLD`; it never promotes automatically.
- Test expectations are not weakened to obtain a pass.

## Output

Report the environment, commit, CI result, migration status, deployment ID,
URL, health evidence, QA result, approval evidence, rollback reference, and
remaining blockers. Redact secrets and keep generated QA artifacts outside Git
unless the project explicitly routes them to a governed evidence location.
