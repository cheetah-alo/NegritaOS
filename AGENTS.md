<!-- NEGRITA_BRAIN:START -->
## Negrita Brain Runtime

This workspace is governed by NegritaOS. Before substantive work:

1. Read `.codex/project.yaml` and its `negrita_registry`.
2. Run `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve --root "$PWD" --provider codex --action <action>`.
3. Use the resolved modes, agents, profile closure, rules, skills, artifact route, browser context, commit identity policy, model route, and gates.
4. Before writes or commits, run `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py gate --root "$PWD" --provider codex --action write|commit [--path PATH]`.
5. New deliverables use a user-selected output path. Keep the `<slug>__updated_YYYYMMDD_HHMMSS.<ext>` version suffix; external binary artifacts are not added to Git by default.
6. Persist only reusable findings with `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py memory remember|handoff --root "$PWD" --provider codex ...`.
7. Close substantive work with `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py close --root "$PWD" --provider codex`. Pass `--durable-ref REF` only after a Brain handoff.

A `BLOCK` decision is mandatory. A `WARN` decision must be surfaced before proceeding. If canonical memory returns `PERMISSION_REQUIRED`, retry with elevated permission or run `configure codex --apply`; do not report it as configuration resolution failure. Authenticated browser work must use the resolved `browser_context` and `scripts/open_governed_browser.py`; on ambiguity return `BLOCKED_BROWSER_PROFILE_RESOLUTION` instead of opening another profile. For delegated work, use the resolved `model_route`: default to Luna medium, escalate only for declared Terra/Sol signals, and require a separate falsification-oriented reviewer task for high-impact work. Independent PASS must include SHA-256-bound evidence receipts and match the current worktree fingerprint at commit time. A larger model never replaces missing evidence or authorization. External account access never grants financial authority: do not change a plan, subscription, billing method, paid entitlement, or perform an operation that may incur an incremental charge without the user's explicit authorization for that exact operation. If cost is unknown, return `BLOCKED_FINANCIAL_AUTHORIZATION` and ask. Never log prompts, responses, file contents, tool outputs, or secrets.
<!-- NEGRITA_BRAIN:END -->
