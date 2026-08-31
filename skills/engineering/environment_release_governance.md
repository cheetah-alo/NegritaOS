# Environment Release Governance

## Purpose

Govern deployment and functional verification across development, UAT, and
production without conflating release authority with QA authority.

## Release Contract

Every deployment request must identify:

- project and target environment;
- immutable commit SHA;
- source branch and required CI status;
- migration and rollback posture;
- expected configuration version without exposing secret values;
- deployment provider and application URL;
- named human approver when the target is production.

Never deploy an unspecified working tree, a moving branch reference, or a
commit whose required checks are incomplete. A deployment is not `READY`
until runtime health and the environment-specific QA gate both pass.

## Separation Of Duties

The deployment operator may inspect release evidence, trigger an authorized
deployment, wait for health, and collect provider evidence. The operator must
not self-certify functional acceptance.

The functional QA agent may exercise an already deployed URL and collect test
evidence. It must not deploy, promote, roll back, change infrastructure, or
weaken tests to obtain a pass.

## Environment Policy

| Environment | Test policy | Promotion policy |
|---|---|---|
| DEV | Destructive tests allowed only with isolated test data and credentials. | No production claim. |
| UAT | Destructive tests allowed only in the approved UAT tenant and dataset. | Requires full functional PASS before production consideration. |
| Production | Read-only smoke tests only. No imports, deletes, resets, or synthetic authentication. | Explicit human approval is mandatory. |

Production validation must not create technical cookies, delete user sessions,
reset profiles, import fixtures, mutate financial data, or exercise any flow
whose side effects are not demonstrably read-only.

## Evidence Contract

The deployment operator reports:

- target environment and exact commit;
- CI and migration status;
- deployment identifier and provider status;
- URL and health-check evidence;
- relevant log references with secrets redacted;
- rollback reference;
- handoff status to functional QA.

The functional QA agent reports:

- target URL, environment, commit, and test identity;
- exact commands and suite selection;
- user journeys exercised;
- pass/fail/blocked counts;
- screenshots, video, traces, and logs when failures occur;
- destructive or read-only classification;
- final decision: `PASS`, `HOLD`, or `BLOCKED`.

Artifacts use a user-selected local path and remain outside Git by default.
Do not publish screenshots, traces, videos, cookies, tokens, or user data
without explicit authorization and redaction review.

## Fail-Closed Conditions

Return `HOLD` or `BLOCKED` when:

- the commit is missing, ambiguous, or differs from the deployed revision;
- required CI checks are pending or failed;
- environment credentials or provider access are unavailable;
- a migration lacks backup, rollback, or compatibility evidence;
- health checks do not stabilize within the declared timeout;
- production approval is missing;
- the available production suite is destructive;
- functional QA fails or cannot establish which build it tested.

## Test Integrity

A green suite is not the objective. Correct application behavior with
trustworthy tests is the objective. Do not delete, skip, weaken, rewrite, or
add tolerances to tests merely to make a deployment pass. A fix is verified
only when the original user-visible reproduction path passes against the
deployed application.
