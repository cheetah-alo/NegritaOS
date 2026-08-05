"""Unit tests for Claude hook mutation classification."""

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "negrita_brain_hook", ROOT / "scripts" / "negrita_brain_hook.py"
)
assert SPEC is not None and SPEC.loader is not None
HOOK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOOK)


class TestHookClassification(unittest.TestCase):
    """Ensures mutating Claude tools reach the fail-closed gate."""

    def test_edit_tool_that_is_classified_as_write(self) -> None:
        action, path = HOOK._action_and_path("Edit", {"file_path": "src/app.py"})
        self.assertEqual(action, "write")
        self.assertEqual(path, Path("src/app.py"))

    def test_mutating_bash_that_is_classified_as_write(self) -> None:
        action, _ = HOOK._action_and_path("Bash", {"command": "git commit -m test"})
        self.assertEqual(action, "write")

    def test_read_only_bash_that_remains_read(self) -> None:
        action, _ = HOOK._action_and_path("Bash", {"command": "git status --short"})
        self.assertEqual(action, "read")

    def test_unknown_bash_that_fails_closed_as_write(self) -> None:
        action, _ = HOOK._action_and_path("Bash", {"command": "custom-tool deploy"})
        self.assertEqual(action, "write")

    def test_shell_redirection_that_is_classified_as_write(self) -> None:
        action, _ = HOOK._action_and_path("Bash", {"command": "echo value > output.txt"})
        self.assertEqual(action, "write")

    def test_bash_deliverable_that_exposes_destination_to_document_gate(self) -> None:
        action, path = HOOK._action_and_path(
            "Bash",
            {
                "command": (
                    "cp source.pdf "
                    "documents/report__updated_20260805_120000.pdf"
                )
            },
        )

        self.assertEqual(action, "write")
        self.assertEqual(
            path,
            Path("documents/report__updated_20260805_120000.pdf"),
        )


if __name__ == "__main__":
    unittest.main()
