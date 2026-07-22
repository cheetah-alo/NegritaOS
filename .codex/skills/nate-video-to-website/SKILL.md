---
name: nate-video-to-website
description: >
  Use only when the user explicitly asks to turn a video into a scroll-driven
  website or video-backed frontend experience.
license: Apache-2.0
disable-model-invocation: true
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, frontend]
---

# Nate Video To Website Adapter

This is an explicit adaptation of
`skills/skill_nate/video-to-website/SKILL.md`. Treat it as a specialized
frontend generation workflow, not a default dashboard architecture.

Before running it, verify that `ffmpeg`, `ffprobe`, Node.js, the browser
runtime, and any GSAP/Lenis dependencies are available. Use portable commands
and the active project's package manager; never assume a Windows executable
path or CDN availability. Keep the editable source modular and put extracted
frames and generated artifacts under an ignored or project-approved output
directory. Run the project's frontend tests and browser QA before delivery.
