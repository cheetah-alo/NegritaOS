"""Tests for project-scoped Claude aliases generated from router modes."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.sync_claude_agent_aliases import _load_modes


class TestClaudeAgentAliasScope(unittest.TestCase):
    """Ensures product-specific aliases do not leak into unrelated adapters."""

    def _root(self, base: Path) -> Path:
        (base / "core" / "orchestration").mkdir(parents=True)
        (base / "core" / "orchestration" / "metaagent_router.yaml").write_text(
            "metaagent_router:\n"
            "  modes:\n"
            "    global_review:\n"
            "      id: CR\n"
            "      agent: code_review_agent\n"
            "    deployment:\n"
            "      id: DEP\n"
            "      native_alias: pablo\n"
            "      project_scope: [moneyflowlist]\n"
            "      agent: pablo_deployment_operator_agent\n"
            "    lifecycle_qa:\n"
            "      id: LQA\n"
            "      native_alias: casilda-flows\n"
            "      project_scope: [moneyflowlist]\n"
            "      agent: casilda_lifecycle_qa_agent\n",
            encoding="utf-8",
        )
        (base / "integrator.yaml").write_text(
            "negrita_os:\n"
            "  agents:\n"
            "    code_review_agent: {}\n"
            "    pablo_deployment_operator_agent: {}\n"
            "    casilda_lifecycle_qa_agent: {}\n",
            encoding="utf-8",
        )
        return base

    def test_scoped_alias_is_available_to_declared_project(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = self._root(Path(temporary_directory))
            aliases = [row["alias"] for row in _load_modes(root, "moneyflowlist")]
            self.assertEqual(aliases, ["cr", "pablo", "casilda-flows"])

    def test_scoped_alias_is_hidden_from_other_projects(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = self._root(Path(temporary_directory))
            aliases = [row["alias"] for row in _load_modes(root, "academic")]
            self.assertEqual(aliases, ["cr"])

    def test_invalid_scope_does_not_become_global(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = self._root(Path(temporary_directory))
            router = root / "core" / "orchestration" / "metaagent_router.yaml"
            router.write_text(
                router.read_text(encoding="utf-8").replace(
                    "project_scope: [moneyflowlist]",
                    "project_scope: {project: moneyflowlist}",
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "project_scope"):
                _load_modes(root, "academic")


if __name__ == "__main__":
    unittest.main()
