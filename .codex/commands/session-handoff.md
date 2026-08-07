---
id: session-handoff
mode_hint: LP
loads:
  - .codex/project.yaml
  - .codex/local-overrides.md
  - .codex/instruction-manifest.yaml
  - .codex/skills/local-memory-protocol/SKILL.md
---

# Persistent Session Handoff

Produce a self-contained continuation handoff and persist it through Negrita
Brain. Do not write project memory files directly.

## Procedure

1. Resolve project identity through `.codex/project.yaml` and its canonical
   registry. Treat registry `project.memory_home` as authoritative.
2. Run `negrita_brain.py memory status --root "$PWD" --provider <provider>`.
3. Read the canonical index, latest relevant durable session, recent reusable
   observations, Git state, and task tracker when present.
4. Synthesize the output contract below. Use `_(none)_` for empty sections.
5. Persist exactly one handoff with `negrita_brain.py memory handoff`, mapping
   each section to its corresponding repeated CLI argument.
6. Close the runtime session with `negrita_brain.py close ... --durable-ref
   <returned_ref>`. Runtime closure stores no narrative summary.

## Output Contract

```markdown
## Session Handoff - <project_id> - <ISO date>

### What was being worked on
- [ ] <task>: <done|in-progress|blocked and concise status>

### Files modified
- `path/to/file.py` - <what changed>

### Decisions made
- <decision>: <rationale>

### Blockers / open questions
- [ ] <blocker>: <why it matters>

### Next steps
1. <action> -> <file or command> -> <expected outcome>

### Rules / skills required
- Skill: `<skill-id>` - <why>

### Context pitfalls
- <pitfall>: <how to avoid>

### Resume command
/load-context -> /brain status -> start at Next steps #1
```

## Enforcement

- `memory handoff` is the only writer for the durable session and managed index.
- Do not create `docs/handoffs/*` or edit memory `sessions/`/`index.md` manually.
- Do not persist raw chat, prompts, responses, tool outputs, file contents, or secrets.
- On `MEMORY_WRITE_PERMISSION`, request elevated permission or configure Codex;
  do not report `BLOCKED_CONFIG_RESOLUTION`.
