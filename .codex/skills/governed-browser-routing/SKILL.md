---
name: governed-browser-routing
description: Resolve and open the approved Brave profile for authenticated BigQuery, GitHub, Jira, documentation, and other external browser work in a NegritaOS-managed project. Use before browser access that depends on an existing account session; anonymous browsing can use the in-app browser.
---

# Governed Browser Routing

Load `.codex/project.yaml`, its canonical project registry, and
`core/orchestration/browser_profile_routing.yaml` before authenticated browser
work.

## Workflow

1. Identify the browser purpose and target URL.
2. Resolve without opening anything:

   ```bash
   python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/open_governed_browser.py \
     --root "$PWD" --purpose bigquery \
     --url "https://console.cloud.google.com/bigquery" --dry-run
   ```

3. Verify the returned project, profile, display name, purpose, and host.
4. Use `--apply` only when the user requested browser navigation or interaction.
5. If resolution blocks, report `BLOCKED_BROWSER_PROFILE_RESOLUTION`; do not
   open a different account or the in-app browser as a substitute.

Current canonical aliases are `cqi_technical`, `cqi_documentation`,
`personal_cheetah_alo`, and explicit-only `azure`. Use aliases rather than raw
Brave directory names in prompts or automation.

The launcher selects the Brave profile but does not authorize actions inside
the account. Never inspect browser credentials or session stores. Apply the
external financial authorization gate before any operation that may change a
plan, billing, paid entitlement, resource size, or incremental cost.
