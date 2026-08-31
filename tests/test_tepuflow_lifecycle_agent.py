"""Contract tests for the TepuFlow lifecycle adversarial QA agent."""

import tomllib
import unittest
from pathlib import Path

from scripts.validate_skill_catalog import _load_yaml


ROOT = Path(__file__).resolve().parents[1]


class TestTepuFlowLifecycleAgent(unittest.TestCase):
    """Keep the skill, router, registry, and native aliases aligned."""

    def test_catalog_and_project_activate_lifecycle_profile(self) -> None:
        catalog = _load_yaml(ROOT / "skills/catalog.yaml")
        project = _load_yaml(ROOT / "projects/moneyflowlist.yaml")["project"]
        profile = catalog["profiles"]["tepuflow-lifecycle-qa"]

        self.assertEqual(profile["extends"], "tepuflow-release-operations")
        self.assertEqual(
            profile["required_agents"], ["casilda_lifecycle_qa_agent"]
        )
        self.assertIn("tepuflow-lifecycle-adversarial-qa", profile["skills"])
        self.assertIn("tepuflow-lifecycle-qa", project["skill_profiles"])
        self.assertIn("casilda_lifecycle_qa_agent", project["agents"])
        self.assertIn("casilda-flows", project["codex_custom_agents"])
        self.assertEqual(project["mode_map"]["lifecycle_qa"], "LQA")

    def test_router_and_integrator_resolve_lqa(self) -> None:
        router = _load_yaml(
            ROOT / "core/orchestration/metaagent_router.yaml"
        )["metaagent_router"]
        integrator = _load_yaml(ROOT / "integrator.yaml")["negrita_os"]
        mode = router["modes"]["tepuflow_lifecycle_qa"]

        self.assertEqual(mode["id"], "LQA")
        self.assertEqual(mode["native_alias"], "casilda-flows")
        self.assertEqual(mode["project_scope"], ["moneyflowlist"])
        self.assertEqual(mode["agent"], "casilda_lifecycle_qa_agent")
        self.assertIn("casilda_lifecycle_qa_agent", integrator["agents"])
        self.assertEqual(
            integrator["routing_rules"]["if_user_asks_for"]
            ["tepuflow_lifecycle_qa"]["use_agent"],
            "casilda_lifecycle_qa_agent",
        )

    def test_native_agents_preserve_safety_contract(self) -> None:
        codex_agent = tomllib.loads(
            (ROOT / ".codex/agents/casilda-flows.toml").read_text(
                encoding="utf-8"
            )
        )
        claude_alias = (ROOT / ".codex/agents/casilda-flows.md").read_text(
            encoding="utf-8"
        )
        wrapper = (
            ROOT / ".codex/skills/tepuflow-lifecycle-adversarial-qa/SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertEqual(codex_agent["name"], "casilda-flows")
        self.assertIn("Production is read-only", codex_agent["developer_instructions"])
        self.assertIn("BLOCKED_FINANCIAL_AUTHORIZATION", codex_agent["developer_instructions"])
        self.assertIn("canonical_mode: LQA", claude_alias)
        self.assertIn("UF-00", wrapper)
        self.assertIn("UF-13", wrapper)
        self.assertIn("Never weaken tests", wrapper)


if __name__ == "__main__":
    unittest.main()
