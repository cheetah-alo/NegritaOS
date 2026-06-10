---
id: handoff
mode_hint: LP
---

# Quick Handoff Summary

Produces a lightweight handoff document for this project session and writes it
to `docs/handoffs/YYYY-MM-DD-<slug>.md`.

For the full NegritaOS-format handoff (reads memory, git, task tracker, writes
session file), use `/session-handoff` instead.

## When to use

- End of a focused work session (one feature, one bug, one analysis)
- Before hitting a usage limit — run **early**, not last
- As a running log: append incrementally as tasks complete during a long session

## Procedure

### Step 1 — Gather state

```bash
git status --short
git log --oneline -10
python -m unittest discover -s tests -q 2>&1 | tail -3
```

### Step 2 — Write the document

Create `docs/handoffs/YYYY-MM-DD-<slug>.md` with this structure:

```markdown
## Handoff — <project> — <ISO date> — <slug>

### Completed Work
- [ ] <task>: <one-line status>

### Files Changed
| File | Change |
|------|--------|
| `path/to/file.py` | <what changed> |

### Tests
- Command: `python -m unittest discover -s tests -p "test_*.py" -v`
- Result: N/N passing

### Known Issues / Partial Work
- <anything incomplete or blocked>

### Next Steps (ordered)
1. <specific action> → `<file or command>` — <expected outcome>
```

### Step 3 — Confirm

State which file was written and the test result summary in your response.

## Notes

- Keep each section to bullet points, not prose.
- If tests are failing, list the failing test names explicitly.
- Do not include speculation about future work beyond the immediate next steps.
