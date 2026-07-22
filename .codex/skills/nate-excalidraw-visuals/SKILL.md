---
name: nate-excalidraw-visuals
description: >
  Use only when the user explicitly requests a generated Excalidraw-style PNG
  visual or hand-drawn visual explanation.
license: Apache-2.0
disable-model-invocation: true
metadata:
  author: negritaos
  version: "1.0"
  scope: [root]
---

# Nate Excalidraw Visuals Adapter

This is an explicit, user-invoked adaptation of
`skills/skill_nate/excalidraw-visuals/SKILL.md`. It generates raster output and
does not replace an editable diagram or source documentation.

Dependencies and safeguards:

- Require `KIE_AI_API_KEY` in an ignored `.env`; never write a key to a skill,
  catalog, commit, log, or generated artifact.
- Confirm the user wants an external API call before invoking the bundled
  generator under `skills/skill_nate/excalidraw-visuals/`.
- Use the bundled style guide and brand assets where available; do not invent
  brand marks or use a missing asset silently.
- Write generated images only to the project's approved output directory.
- Report dependency failures and API failures without retrying indefinitely.

The canonical source bundle contains the style guide and brand assets under
`skills/skill_nate/excalidraw-visuals/excalidraw-visuals/`; load those assets
before generation when the requested visual depends on them.
