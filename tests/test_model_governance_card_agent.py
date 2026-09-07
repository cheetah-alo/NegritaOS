"""Contract tests for Vera and the model-governance-card skill."""

import tomllib
import unittest
from pathlib import Path

from scripts.sync_claude_agent_aliases import _load_modes
from scripts.validate_skill_catalog import _load_yaml


ROOT = Path(__file__).resolve().parents[1]


class TestModelGovernanceCardAgent(unittest.TestCase):
    def test_catalog_exposes_default_model_governance_profile(self) -> None:
        catalog = _load_yaml(ROOT / "skills/catalog.yaml")

        self.assertIn("model-governance-card", catalog["defaults"]["profiles"])
        profile = catalog["profiles"]["model-governance-card"]
        self.assertEqual(profile["skills"], ["model-governance-card"])
        self.assertIn("model_governance_card_agent", profile["required_agents"])

    def test_router_and_integrator_resolve_vera_globally(self) -> None:
        router = _load_yaml(
            ROOT / "core/orchestration/metaagent_router.yaml"
        )["metaagent_router"]
        integrator = _load_yaml(ROOT / "integrator.yaml")["negrita_os"]
        mode = router["modes"]["model_governance_card"]

        self.assertEqual(mode["id"], "MCARD")
        self.assertEqual(mode["native_alias"], "vera")
        self.assertIs(mode["global_agent"], True)
        self.assertEqual(mode["agent"], "model_governance_card_agent")
        self.assertIn("model_governance_card_agent", integrator["agents"])
        self.assertIn("vera", [row["alias"] for row in _load_modes(ROOT)])

    def test_vera_preserves_evidence_and_client_boundaries(self) -> None:
        agent = tomllib.loads(
            (ROOT / ".codex/agents/vera.toml").read_text(encoding="utf-8")
        )
        skill = (
            ROOT / ".codex/skills/model-governance-card/SKILL.md"
        ).read_text(encoding="utf-8")
        calibration = (
            ROOT
            / ".codex/skills/model-governance-card/references/reference-calibration.md"
        ).read_text(encoding="utf-8")

        self.assertEqual(agent["name"], "vera")
        self.assertEqual(agent["model"], "gpt-5.6-terra")
        normalized_instructions = " ".join(agent["developer_instructions"].split())
        self.assertIn("Never fill a missing field", normalized_instructions)
        self.assertIn("ml_predictive", skill)
        self.assertIn("analytical_rule", skill)
        self.assertIn("hybrid", skill)
        self.assertIn("89f75bb394782ef3", calibration)  # pragma: allowlist secret
        self.assertIn("11.7M versus 1.2M", calibration)

    def test_rubric_and_template_cover_model_lifecycle(self) -> None:
        rubric = _load_yaml(ROOT / "rubrics/model_governance_card_rubric.yaml")
        template = _load_yaml(ROOT / "templates/model_governance_card_template.yaml")

        self.assertIn(
            "model_governance_card_agent",
            rubric["rubric"]["applicable_agents"],
        )
        card = template["model_governance_card"]
        self.assertIn("monitoring", card)
        self.assertIn("governance", card)
        self.assertIn("logic", card)


if __name__ == "__main__":
    unittest.main()
