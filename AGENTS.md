<!-- NEGRITA_BRAIN:START -->
## Negrita Brain Runtime

This workspace is governed by NegritaOS. Before substantive work:

1. Read `.codex/project.yaml` and its `negrita_registry`.
2. Run `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py resolve --root "$PWD" --provider codex --action <action>`.
3. Use the resolved modes, agents, profile closure, rules, skills, artifact route, and gates.
4. Before writes or commits, run `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py gate --root "$PWD" --action write|commit [--path PATH]`.
5. New deliverables use `documents/<slug>__updated_YYYYMMDD_HHMMSS.<ext>` and `documents/document_manifest.jsonl`.
6. Close substantive work with `python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/negrita_brain.py close --root "$PWD" --summary "..."`.

A `BLOCK` decision is mandatory. A `WARN` decision must be surfaced before proceeding. Never log prompts, responses, file contents, tool outputs, or secrets.
<!-- NEGRITA_BRAIN:END -->
