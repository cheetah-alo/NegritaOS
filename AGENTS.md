<!-- NEGRITA_BRAIN:START -->
## Negrita Brain Runtime

This workspace is governed by NegritaOS. Before substantive work:

1. Read `.codex/project.yaml` and its `negrita_registry`.
2. Run `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve --root "$PWD" --provider codex --action <action>`.
3. Use the resolved modes, agents, profile closure, rules, skills, artifact route, and gates.
4. Before writes or commits, run `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py gate --root "$PWD" --provider codex --action write|commit [--path PATH]`.
5. New deliverables use a user-selected output path. Keep the `<slug>__updated_YYYYMMDD_HHMMSS.<ext>` version suffix; external PPTX/DOCX/PDF artifacts are not added to Git by default.
6. Persist only reusable findings with `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py memory remember|handoff --root "$PWD" --provider codex ...`.
7. Close substantive work with `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py close --root "$PWD" --provider codex`. Pass `--durable-ref REF` only after a Brain handoff.

A `BLOCK` decision is mandatory. A `WARN` decision must be surfaced before proceeding. If canonical memory returns `PERMISSION_REQUIRED`, retry with elevated permission or run `configure codex --apply`; do not report it as configuration resolution failure. Never log prompts, responses, file contents, tool outputs, or secrets.
<!-- NEGRITA_BRAIN:END -->
