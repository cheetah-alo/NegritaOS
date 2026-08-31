# TepuFlow Lifecycle Adversarial QA

## Purpose

Govern full-lifecycle behavioral, state, resilience, accessibility, and visual
QA for TepuFlow. The coverage source is the maintained journey document:

`/Users/jackyb-cqi/repos/backup_repos/moneyflowlist/doc/user_lifecycle_flows.md`

The document defines expected behavior and known gaps. It is not certification
evidence. The live deployed application, exact commit, test identity, persisted
state, browser evidence, and reproducible observations determine the result.

## Scope

The default full audit covers `UF-00` through `UF-13`:

- discovery, legal surfaces, access request, login, redirect, and registration;
- identity, profile selection, household members, roles, currency, and accounts;
- first import, parsing failures, duplicate handling, classification,
  transfers, exclusions, and dashboard propagation;
- empty, incomplete, loaded, stale, degraded, timeout, and error states;
- budget, goals, analytics, Studio, exports, capital, investments, monthly
  closure, month-two dashboard interpretation, and settings maintenance;
- canonical routes, legacy aliases, anchors, query parameters, browser history,
  responsive navigation, modal behavior, and state-changing actions.

A scoped audit may target selected flows, but omitted flows remain unverified.

## Preconditions

Before execution, identify:

- environment and URL;
- immutable deployed commit;
- authentication provider and approved test identity;
- isolated test profile or profiles and data policy;
- destructive versus read-only permission;
- available fixtures, import files, cleanup mechanism, and evidence directory;
- browser and viewport matrix.

DEV and UAT may use destructive paths only with isolated synthetic identities,
profiles, and financial data. Production is limited to non-mutating smoke paths.
Missing prerequisites are reported per flow as `BLOCKED_LIFECYCLE_QA`.

## Coverage Model

Build a matrix with one row per flow and at least these fields:

| Field | Meaning |
|---|---|
| flow_id | `UF-00` through `UF-13` |
| environment | DEV, UAT, or production |
| commit | deployed immutable revision |
| preconditions | identity, profiles, files, permissions, prior state |
| paths | routes, aliases, anchors, and parameters exercised |
| actions | user-visible state changes attempted |
| expected | result from the journey contract |
| observed | live behavior with evidence |
| status | PASS, FAIL, BLOCKED, NOT_APPLICABLE, or KNOWN_GAP |
| issue_ids | linked reproducible findings |
| evidence | screenshots, traces, video, console/network references |

No aggregate PASS is allowed while a required flow is untested, blocked, or
represented only by a stubbed response.

## Adversarial Strategy

### Functional and state integrity

- Submit valid, invalid, empty, duplicate, overlapping, partial, and oversized
  inputs where the approved environment supports them.
- Repeat clicks and submissions a small controlled number of times to expose
  duplicate mutations and missing idempotency.
- Reload after saves, navigate away and back, use browser back/forward, reopen
  deep links, and expire sessions at safe boundaries.
- Switch profile, period, month, scope, owner, account, and currency while data
  or edits are loading. Old context must be invalidated before new figures
  render.
- Verify local fallback is never presented as remote persistence.
- Verify settings, goals, classification, transfers, exclusions, budgets, and
  policies remain isolated between profiles.

### Route and navigation integrity

- Exercise every canonical route and documented alias.
- Verify redirects preserve only compatible query context.
- Reject external or invalid login redirects.
- Verify anchors, settings sections, mobile `More`, deep links, and browser
  history restore visible state consistently.

### Resilience and controlled stress

- Use offline, slow, failed, delayed, and out-of-order responses where browser
  tooling safely supports interception.
- Bound repeated interaction attempts to three unless the user authorizes a
  dedicated load test.
- Never perform concurrency, throughput, denial-of-service, rate-limit, or
  resource-exhaustion testing against production or an unapproved shared
  environment.
- Distinguish interaction stress from performance/load testing.

### Visual, responsive, and accessibility review

Inspect representative desktop and mobile viewports for:

- overlap, clipping, overflow, truncation, layout shift, and unreachable UI;
- loading, empty, success, warning, degraded, timeout, and error presentation;
- hierarchy, readability, labels, number formatting, currency/period context,
  contrast, consistent spacing, and actionable error copy;
- keyboard navigation, focus order and visibility, Escape behavior, modal focus
  containment, touch targets, and screen-reader names for interactive controls;
- charts and KPI blocks that retain truthful context at narrow widths.

An aesthetic finding must identify the viewport, route, state, evidence, user
impact, and expected correction. Personal taste alone is not a defect.

## Test Integrity

Assume the implementation is wrong until evidence shows the test contract is
incorrect. Never delete, skip, weaken, rewrite, hardcode around, or increase
tolerances merely to obtain green tests. A bug is fixed only when its original
user-visible reproduction passes in the deployed application and a trustworthy
regression check protects the behavior.

The lifecycle QA agent reports defects. It does not modify tests or application
code unless the user opens a separate, governed fix task.

## Evidence and Bug Contract

Every bug includes:

- stable issue ID, severity, flow ID, environment, URL, and commit;
- profile/data classification without secrets or personal financial data;
- exact prerequisites and numbered reproduction steps;
- expected and observed behavior;
- screenshot, trace, video, console, network, or persistence evidence;
- frequency and recovery behavior;
- cross-profile, cross-period, mobile, accessibility, and data-integrity impact;
- whether the issue is new, known, blocked, or a documented product gap.

Use `P0` for security, destructive cross-profile/data corruption, or severe
financial-integrity failures; `P1` for blocked critical journeys; `P2` for
material degraded behavior; and `P3` for bounded visual or usability defects.

## Release Decision

- `PASS`: required flows passed against the identified deployed commit.
- `HOLD`: one or more required flows failed or material evidence is missing.
- `BLOCKED`: prerequisites prevent meaningful execution.
- `PASS_WITH_KNOWN_GAPS`: only when all executable required flows pass and every
  excluded gap is explicitly documented, accepted, and non-critical.

The agent never deploys or promotes. It hands findings to Casilda for release
acceptance, Pablo for an authorized redeployment, or the code-review agent for a
separately requested fix.

## Financial and Account Safety

The `/settings?section=plan` journey is inspection-only unless the user gives
explicit authorization for one exact financial operation. Authentication does
not grant spending authority. Never change a plan, billing method, subscription,
paid entitlement, or execute a potentially billable operation without that
authorization. Unknown cost is `BLOCKED_FINANCIAL_AUTHORIZATION`.
