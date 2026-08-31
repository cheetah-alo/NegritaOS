---
name: tepuflow-lifecycle-adversarial-qa
description: >
  Run adversarial TepuFlow lifecycle E2E and visual QA against the governed
  UF-00 to UF-13 journey contract. Use for full user-flow audits, route and
  alias coverage, profile-isolation testing, persistence checks, controlled
  stress, accessibility, responsive UI review, and reproducible bug evidence.
license: Apache-2.0
metadata:
  author: NegritaOS
  version: "1.0"
  scope: [root, frontend]
  auto_invoke: "Testing or attempting to break TepuFlow user lifecycle flows"
---

# TepuFlow Lifecycle Adversarial QA

Read the canonical protocol at
`skills/engineering/tepuflow_lifecycle_adversarial_qa.md` before acting. Then
read the current TepuFlow journey contract in full:

`/Users/jackyb-cqi/repos/backup_repos/moneyflowlist/doc/user_lifecycle_flows.md`

Treat that document as a maintained coverage contract, not proof that the
application works.

## Required Inputs

- deployed URL and environment;
- exact deployed commit;
- approved test identity and profile scope;
- whether destructive testing is permitted;
- requested flow subset, or all `UF-00` through `UF-13` by default.

If identity, environment, commit, or safe data isolation is missing, return
`BLOCKED_LIFECYCLE_QA` for affected flows instead of fabricating a pass.

## Execution Contract

1. Inventory the documented routes, aliases, anchors, query parameters,
   state-changing actions, error branches, and known product gaps.
2. Explore headed first when visual or interaction discovery is needed.
3. Replay stable regressions headlessly with existing Page Objects where
   available.
4. Exercise valid, invalid, interrupted, repeated, back/forward, reload,
   profile-switch, period-switch, permission, and stale-response paths.
5. Inspect desktop and mobile layout, keyboard/focus behavior, copy, loading,
   empty/error states, clipping, overlap, hierarchy, and visual consistency.
6. Record results per flow as `PASS`, `FAIL`, `BLOCKED`, `NOT_APPLICABLE`, or
   `KNOWN_GAP` with evidence and exact reproduction steps.

## Safety Boundaries

- Production is read-only and receives no destructive, stress, import, reset,
  profile mutation, or synthetic-authentication test.
- Controlled repetition in DEV/UAT is not load testing. Do not create
  unbounded loops, denial-of-service pressure, or rate-limit abuse.
- Never deploy, promote, roll back, change infrastructure, or fix application
  code unless the user separately requests and authorizes that work.
- Never weaken tests to obtain a pass.
- Never change a plan or perform a billable action without the user's explicit
  authorization for that exact operation. Unknown cost is
  `BLOCKED_FINANCIAL_AUTHORIZATION`.

## Output

Report the tested environment, commit, identity class, data isolation, flow
matrix, bugs by severity, aesthetic/accessibility findings, evidence paths,
exact commands and counts, blocked coverage, known gaps, and release decision.
Stubbed routes or screenshots alone cannot certify lifecycle behavior.
