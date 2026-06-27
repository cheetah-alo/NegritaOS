---
id: handoff
mode_hint: LP
---

# Handoff

Produces a chat-only handoff summary for the current session so the user can
clear context and a fresh agent can continue without losing continuity.

This is a context-handoff artifact, not a stakeholder status report. The
audience is the next agent instance.

For persistent NegritaOS memory/session writes, use `/session-handoff`.

## When to use

- The user says `/handoff`, "session handoff", "wrap up session", "hand off",
  "handoff summary", "summarize before I clear", or a near-equivalent.
- Before context compaction or `/clear`.
- When a future agent needs enough context to continue from chat alone.

## Procedure

1. Review the whole current conversation, not only the last few turns.
2. Pull only state that is known from this session:
   - plan files referenced in the session
   - current task/checklist state
   - background processes or dev servers started by this agent
   - files this agent created or modified
   - memory files this agent wrote or updated
   - unresolved user questions
3. Do not perform a broad filesystem audit for this command.
4. Do not write files.
5. Do not update memory.

## Output contract

Use exactly this structure:

```markdown
# Session Handoff — <one-line title>

## Where it started
<2-3 sentences: user request, key framing, constraints>

## Decisions locked + what shipped
- <decision or change> — <why, and where it lives using absolute paths when a file matters>

## Key files for next session
- `<absolute path>` — <why the next agent should read this first>
- Plan file: `<absolute path or none>`
- Memory files touched: `<absolute paths or none>`

## Running state
- Background processes: <session IDs + purpose + kill command, or "none">
- Dev servers / ports: <URL + port, or "none">
- Open worktrees / branches: <paths/branches, or "none">

## Verification — how to confirm things still work
- `<command>` — <expected outcome>

## Deferred + open questions
- Deferred: <item> — <why pushed later, or "none">
- Open: <question needing user input, or "none">

## Pick up here
<1-2 sentences: the single most likely next action>
```

## Hard rules

- Chat output only.
- Never invent state.
- Use absolute paths for files that matter to continuation.
- If a section has nothing to report, write `none`.
- Include process/session IDs for any background jobs started in this session.
- No repo-local `docs/handoffs` output from `/handoff`.
