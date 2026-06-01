## Build Unit Tests (unittest)

Use this prompt when creating or refactoring tests in this repository.

Mandatory policy:
- Follow `.codex/rules/tests-unittest-standards.md`.
- Use Python `unittest` (`unittest.TestCase`) as the canonical framework.
- Keep tests deterministic and isolated.

Execution command:

```bash
uv run python -m unittest discover -s tests -p "test_*.py" -v
```
