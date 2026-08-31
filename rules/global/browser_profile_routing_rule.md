---
id: browser-profile-routing
domain: external-access
enforcement: strict
priority: critical
depends_on:
  - negritaos-router
provides:
  - governed-browser-profile-selection
  - account-session-isolation
description: >
  Routes authenticated browser work to the approved Brave profile for the
  active NegritaOS project and purpose without inspecting session data.
version: 1.0.0
applyTo: [repo, agents, prompts, claude, codex]
canonical_location: rules/global/browser_profile_routing_rule.md
adapter_stubs:
  - .codex/rules/browser-profile-routing.md
---

# Governed Browser Profile Routing

Before opening an authenticated browser surface, resolve the active project
through `.codex/project.yaml` and use
`core/orchestration/browser_profile_routing.yaml`.

1. An explicit canonical profile selected by the user wins.
2. A recognized GitHub organization routes to its declared account profile.
3. Otherwise, resolve URL purpose and requested purpose inside the project's
   `browser_context.account_scope`.
4. If no specific purpose applies, use the project's declared default.
5. Any conflict, unknown profile, unsafe URL, or missing declaration returns
   `BLOCKED_BROWSER_PROFILE_RESOLUTION`. Never fall back to another account.

Use `scripts/open_governed_browser.py` for authenticated Brave work. The Codex
in-app browser may be used for anonymous or non-profile work, but it must not be
treated as access to Brave sessions. Do not inspect cookies, passwords, local
storage, or session tokens. Never print URL queries or fragments.

Browser authentication never grants financial authority. The external app
financial control remains mandatory for purchases, plan changes, paid resource
creation, scaling, or any operation with possible incremental cost.
