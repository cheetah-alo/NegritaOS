---
id: session-handoff
mode_hint: LP   # Localized Planning — read-only synthesis
loads:
  - .codex/project.yaml
  - .codex/local-overrides.md
  - .codex/instruction-manifest.yaml
  - .codex/skills/memory-protocol/SKILL.md
---

# Session Handoff (Standup)

Produce a **self-contained handoff document** — enough for any contributor or
agent to immediately take over without access to the current chat history.

## When to use

- End of a work session (before context is lost or compacted).
- Before handing off to another developer or agent.
- After a context-compaction event: start a new session with this command.
- On request: "give me a standup", "handoff", "resume", "what's next".

## Procedure

### Step 1 — Read project identity

```
.codex/project.yaml → project_id, archetype, memory_home
.codex/local-overrides.md → active modes, scope restrictions, lexicon
```

### Step 2 — Read memory

```
<memory_home>/index.md                → open threads, latest session pointer
<memory_home>/sessions/<latest>.md   → last session summary
<memory_home>/observations.jsonl     → tail -20 (most recent durable discoveries)
```

If `memory_home` is missing or empty, note it explicitly in the output.

### Step 3 — Read git state

```bash
git log --oneline -15                          # recent commit trail
git diff --name-only HEAD~5 HEAD               # files touched in last 5 commits
git status --short                             # uncommitted work
git stash list                                 # any stashed WIP
```

### Step 4 — Read task tracker (if exists)

```
docs/task_tracker.md → current backlog status (done / wip / todo)
```

If missing, derive task state from git log and memory.

### Step 5 — Synthesize

Produce the output below. Every section is mandatory; write `_(none)_` if empty.
Keep each section tight — bullet points over prose.

---

## Output contract

```markdown
## Session Handoff — <project_id> — <ISO date>

### What was being worked on
<!-- 3-7 bullets: the concrete task, why it matters, current state -->
- [ ] <task>: <one-line status (done|in-progress|blocked)>

### Files modified (this session / branch)
<!-- paths relative to repo root -->
- `path/to/file.py` — <what changed in one line>

### Decisions made
<!-- non-obvious choices that downstream work depends on -->
- <decision>: <rationale in one sentence>

### Blockers / open questions
<!-- things that prevented progress or need resolution before next step -->
- [ ] <blocker>: <why it matters>

### Next steps (ordered)
<!-- exact next actions — specific enough to start without asking questions -->
1. <action> → <file or command> — <expected outcome>
2. …

### Rules / skills required for next steps
<!-- list the NegritaOS rules and skills the next agent must load -->
- Rule: `<rule-id>` — <why>
- Skill: `<skill-id>` — <why>

### Context pitfalls
<!-- things that are easy to get wrong; warn the next agent explicitly -->
- <pitfall>: <how to avoid>

### Resume command
<!-- the one-liner the next agent/developer should run to boot context -->
/load-context  →  then read this document  →  then start at "Next steps #1"
```

---

## Enforcement notes

1. If `memory_home` does not have a session file for the current work, write one
   at `<memory_home>/sessions/YYYY-MM-DD_<slug>.md` BEFORE producing this output.
2. Update `<memory_home>/index.md → Latest session` pointer.
3. If a task tracker exists (`docs/task_tracker.md`), append the session's
   completed and in-progress entries before producing this output.
4. This command is **read-only except for** the memory writes in notes 1-3.
