# TepuFlow Release Agents: Pablo, Casilda, And Casilda Flows

## Scope

NegritaOS defines three persistent project agents for TepuFlow. They coordinate
release evidence without forming a separate agent application.

- **Pablo** owns deployment preflight and exact-commit deployment evidence.
- **Casilda** owns independent functional QA against the deployed URL.
- **Casilda Flows** owns adversarial lifecycle coverage across `UF-00` through
  `UF-13`, including route aliases, state transitions, persistence, profile
  isolation, controlled interaction stress, responsive UI, accessibility, and
  visual quality.

The approved UAT topology is a dedicated Vercel frontend project following
`origin/main`, a Cloudflare Tunnel, and a local Docker backend. The operational
source of truth is the Moneyflowlist `doc/vercel-uat-workflow.md` runbook.
Provider OAuth is configured, but the Vercel project, tunnel resource, local
tunnel token, and Clerk test identity still require one-time setup.

## Operating Flow

```text
Human requests environment + exact commit
                 |
                 v
        Pablo validates and deploys
                 |
                 v
 Casilda Flows tests the lifecycle contract
                 |
                 v
      Casilda accepts deployed revision
                 |
       +---------+----------+
       |                    |
     PASS                 FAIL/BLOCKED
       |                    |
    READY                  HOLD
```

Pablo cannot self-certify the release. Casilda Flows cannot deploy, promote,
or fix application code autonomously. Casilda cannot deploy or promote the
release. Production promotion always requires explicit human approval.

## Invocation

From a Codex task opened in the TepuFlow repository:

```text
Spawn pablo to prepare a DEV deployment of commit <sha>.
Spawn casilda to validate <url> in UAT for commit <sha>.
Spawn casilda-flows to test UF-00 through UF-13 against <url> for commit <sha>.
```

Codex custom agents inherit the parent task's approval policy. Their TOML
files can request a sandbox posture, but they cannot bypass a parent denial or
a Negrita Brain `BLOCK` decision.

From Claude Code after the adapter is synchronized:

```text
claude --agent pablo
claude --agent casilda
claude --agent casilda-flows
```

NegritaOS direct routing also accepts:

```text
@agent:DEP deploy commit <sha> to DEV
@agent:FQA validate <url> in UAT for commit <sha>
@agent:LQA test UF-00 through UF-13 against <url> for commit <sha>
```

## Adapter Distribution

After Negrita Brain returns `READY` for Moneyflowlist, materialize the project
profile and both native agent formats for all three agents:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/materialize_project_skills.py \
  /Users/jackyb-cqi/repos/backup_repos/moneyflowlist
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/sync_claude_agent_aliases.py \
  --repo /Users/jackyb-cqi/repos/backup_repos/moneyflowlist --write
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/sync_codex_custom_agents.py \
  --repo /Users/jackyb-cqi/repos/backup_repos/moneyflowlist --write
```

Validate the adapter with:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/validate_claude_agent_aliases.py \
  --repo /Users/jackyb-cqi/repos/backup_repos/moneyflowlist
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/validate_codex_custom_agents.py \
  --repo /Users/jackyb-cqi/repos/backup_repos/moneyflowlist
```

The sync commands preserve a conflicting local file with a timestamped backup
before linking the canonical agent. They do not remove undeclared local agents.

## TepuFlow Test Boundary

Casilda's DEV/UAT coverage includes login, navigation, import, KPIs,
categories, budget, goals, capital, and export when isolated test users and
data are available.

Production uses a separate read-only smoke suite. The existing
`real-financial-workflow.spec.ts` is not production-safe because it creates a
technical authentication cookie and deletes the selected profile session
before importing data. It may be adapted for isolated DEV/UAT, but must not be
the production suite.

The current Playwright configuration already supports an external URL through
`PLAYWRIGHT_BASE_URL` with `PLAYWRIGHT_EXTERNAL_WEB=1`. The current deployment
script recognizes only DEV and production, so persistent UAT support remains a
future Moneyflowlist change.

## Lifecycle Adversarial Boundary

Casilda Flows reads the maintained contract at
`doc/user_lifecycle_flows.md` in full before planning execution. The default
scope is every flow from `UF-00` through `UF-13`; a requested subset is allowed,
but omitted flows remain unverified and cannot contribute to an aggregate PASS.

The lifecycle agent explores headed when visual or interaction discovery is
needed and replays stable regressions headlessly. It exercises valid, invalid,
interrupted, repeated, reload, browser-history, profile-switch, period-switch,
permission, loading, stale, degraded, timeout, responsive, keyboard, focus, and
error paths. Controlled repetition is capped at three by default and is not
load, denial-of-service, or rate-limit testing.

Production remains strictly read-only. Destructive DEV/UAT paths require an
isolated synthetic identity, profile, and dataset. The agent reports defects
and hands them to the appropriate owner; application or test changes require a
separate governed fix request. Documentation, route matrices, screenshots, and
stubbed responses are not E2E certification.

## Deferred Implementation

A later, separately reviewed PR in Moneyflowlist should complete:

- `.github/workflows/deploy.yml` with manual environment and commit inputs;
- `.github/workflows/e2e-environment.yml` for Casilda's deployed-URL checks;
- the dedicated Vercel project `tepuflow-uat` with Root Directory `frontend`;
- the Cloudflare Tunnel route for `api-uat.tepuflow.com/api/*`;
- isolated DEV/UAT Playwright users and data;
- a non-destructive production smoke suite;
- persistent UAT support in the deployment tooling.

That PR must not claim UAT readiness until GitHub, Vercel, Cloudflare, Clerk
test users, and approval ownership are configured and verified.

## Access Readiness

Pablo remains `BLOCKED_ACCESS` until the approved GitHub, Vercel, and
Cloudflare connections are authenticated and their required UAT resources are
visible to the active task. Casilda remains `BLOCKED_ACCESS` for authenticated
flows until the separate UAT test user exists. Configuring an MCP endpoint is
not evidence that its OAuth session or target resource is active.

The TOML agents intentionally declare no per-agent MCP servers. They inherit
the authenticated GitHub, Vercel, and Cloudflare access of the parent Codex
task, subject to the parent approval policy and least-privilege review.
