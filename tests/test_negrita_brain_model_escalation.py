"""Tests for deterministic Luna/Terra/Sol model routing."""

import copy
import unittest
from pathlib import Path
from unittest.mock import patch

from src.negrita_brain.model_routing import (
    ModelRoutingError,
    load_model_escalation_policy,
    resolve_model_route,
    validate_model_escalation_policy,
)


ROOT = Path(__file__).resolve().parents[1]


class TestModelEscalationPolicy(unittest.TestCase):
    """Locks minimum-tier selection and review boundaries."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load_model_escalation_policy(ROOT)

    def test_policy_is_structurally_valid(self) -> None:
        self.assertEqual(validate_model_escalation_policy(self.policy), [])

    def test_default_delegation_uses_luna_medium(self) -> None:
        route = resolve_model_route(self.policy, provider="codex")
        self.assertEqual(route["tier"], "luna_medium")
        self.assertEqual(route["model"], "gpt-5.6-luna")
        self.assertEqual(route["reasoning_effort"], "medium")

    def test_focused_review_uses_luna_high(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="codex",
            actions=["code_review"],
        )
        self.assertEqual(route["tier"], "luna_high")

    def test_material_semantic_signal_escalates_to_terra(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="codex",
            actions=["code_review"],
            risk_signals=["semantic_contract_change"],
        )
        self.assertEqual(route["tier"], "terra_high")
        self.assertEqual(route["change_impact"], "high")
        self.assertTrue(route["independent_review"]["required"])

    def test_production_signal_cannot_keep_standard_impact(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="codex",
            risk_signals=["production_candidate_final_review"],
        )
        self.assertEqual(route["tier"], "sol_high")
        self.assertEqual(route["requested_change_impact"], "standard")
        self.assertEqual(route["change_impact"], "production_candidate")
        self.assertEqual(
            route["independent_review"]["minimum_reviewer_tier"], "sol_high"
        )
        self.assertIn(
            "manifests", route["independent_review"]["required_evidence"]
        )

    def test_architecture_signal_escalates_to_sol(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="codex",
            risk_signals=["architecture_decision"],
        )
        self.assertEqual(route["tier"], "sol_high")

    def test_reviewer_disagreement_escalates_one_family(self) -> None:
        luna = resolve_model_route(
            self.policy,
            provider="codex",
            actions=["code_review"],
            risk_signals=["reviewer_disagreement"],
        )
        terra = resolve_model_route(
            self.policy,
            provider="codex",
            risk_signals=["semantic_contract_change", "reviewer_disagreement"],
        )
        self.assertEqual(luna["tier"], "terra_high")
        self.assertEqual(terra["tier"], "sol_high")

    def test_high_impact_review_requires_separate_terra_reviewer(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="codex",
            change_impact="high",
            review_role="independent_reviewer",
            review_of_session="NBS-builder",
        )
        self.assertEqual(route["tier"], "terra_high")
        self.assertTrue(route["independent_review"]["required"])

    def test_independent_review_without_builder_session_is_rejected(self) -> None:
        with self.assertRaises(ModelRoutingError):
            resolve_model_route(
                self.policy,
                provider="codex",
                review_role="independent_reviewer",
            )

    def test_non_codex_provider_receives_policy_semantics_not_false_model_claim(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="claude",
            risk_signals=["architecture_decision"],
        )
        self.assertEqual(route["tier"], "sol_high")
        self.assertIsNone(route["model"])
        self.assertEqual(route["recommended_codex_model"], "gpt-5.6-sol")

    def test_project_agent_tier_is_applied(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="codex",
            selected_agents=["casilda_lifecycle_qa_agent"],
        )
        self.assertEqual(route["tier"], "terra_high")
        self.assertIn("agent:casilda_lifecycle_qa_agent", route["selection_reasons"])

    def test_production_candidate_reviewer_uses_sol(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="codex",
            change_impact="production_candidate",
            review_role="independent_reviewer",
            review_of_session="NBS-builder",
        )
        self.assertEqual(route["tier"], "sol_high")
        self.assertEqual(
            route["independent_review"]["minimum_reviewer_tier"], "sol_high"
        )

    def test_explicit_delegation_class_is_applied(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="codex",
            delegation_class="read_only_sql_review",
        )
        self.assertEqual(route["tier"], "luna_high")

    def test_invalid_routing_inputs_fail_closed(self) -> None:
        invalid_cases = (
            {"delegation_class": "unknown"},
            {"risk_signals": ["unknown"]},
            {"change_impact": "unknown"},
            {"review_role": "unknown"},
            {"review_of_session": "NBS-builder"},
        )
        for overrides in invalid_cases:
            with self.subTest(overrides=overrides):
                with self.assertRaises(ModelRoutingError):
                    resolve_model_route(
                        self.policy,
                        provider="codex",
                        **overrides,
                    )

    def test_policy_validator_rejects_broken_references(self) -> None:
        invalid = copy.deepcopy(self.policy)
        invalid["default_tier"] = "missing"
        invalid["action_defaults"]["broken"] = "missing"
        invalid["global_codex_custom_agents"].append("unmapped-agent")
        invalid["provider_application"]["codex"] = "tier_semantics_only"
        invalid["governance"]["larger_model_does_not_replace_evidence"] = False
        invalid["governance"]["missing_required_evidence"] = "ALLOW"
        invalid["independent_review"]["self_review_forbidden"] = False

        errors = validate_model_escalation_policy(invalid)

        self.assertTrue(any("default_tier" in error for error in errors))
        self.assertTrue(any("action_defaults.broken" in error for error in errors))
        self.assertTrue(any("unmapped-agent" in error for error in errors))
        self.assertTrue(any("provider_application.codex" in error for error in errors))
        self.assertTrue(
            any("larger_model_does_not_replace_evidence" in error for error in errors)
        )
        self.assertTrue(any("self_review_forbidden" in error for error in errors))
        self.assertTrue(
            any("missing_required_evidence must be HOLD" in error for error in errors)
        )

    def test_policy_validator_rejects_empty_high_impact_evidence(self) -> None:
        invalid = copy.deepcopy(self.policy)
        invalid["impact_levels"]["high"]["required_evidence"] = []

        errors = validate_model_escalation_policy(invalid)

        self.assertTrue(
            any("high: required_evidence cannot be empty" in error for error in errors)
        )

    def test_policy_validator_rejects_malformed_sections(self) -> None:
        invalid = copy.deepcopy(self.policy)
        invalid["tiers"]["broken"] = "not-a-mapping"
        invalid["tiers"]["luna_medium"]["model"] = ""
        invalid["tiers"]["luna_medium"]["rank"] = 0
        invalid["tiers"]["luna_medium"]["family_rank"] = 0
        invalid["tiers"]["luna_high"]["rank"] = invalid["tiers"]["terra_high"]["rank"]
        invalid["task_classes"] = []
        invalid["escalation_signals"] = {
            "tier-form": {"tier": "luna_medium"},
            "negative-step": {"escalate_family": 0},
            "invalid-form": {"unexpected": True},
            "unknown-tier": "missing",
        }
        invalid["action_defaults"] = []
        invalid["impact_levels"] = {
            "not-a-mapping": "invalid",
            "invalid-contract": {
                "independent_review_required": "yes",
                "minimum_reviewer_tier": "missing",
            },
        }
        invalid["global_codex_custom_agents"] = "luna-worker"

        errors = validate_model_escalation_policy(invalid)

        expected_fragments = (
            "tier broken",
            "model is required",
            "rank must be a positive integer",
            "family_rank must be a positive integer",
            "tier ranks must be unique",
            "task_classes must be a mapping",
            "escalate_family must be positive",
            "invalid tier rule",
            "unknown tier",
            "action_defaults must be a mapping",
            "impact_levels.not-a-mapping",
            "independent_review_required must be boolean",
            "minimum_reviewer_tier is unknown",
            "global_codex_custom_agents must be a string list",
        )
        for fragment in expected_fragments:
            with self.subTest(fragment=fragment):
                self.assertTrue(any(fragment in error for error in errors), errors)

    def test_policy_validator_requires_impact_levels(self) -> None:
        invalid = copy.deepcopy(self.policy)
        invalid["impact_levels"] = {}
        self.assertTrue(
            any(
                "impact_levels must be a non-empty mapping" in error
                for error in validate_model_escalation_policy(invalid)
            )
        )

    def test_policy_loader_fails_closed_for_missing_or_invalid_root(self) -> None:
        with patch("src.negrita_brain.model_routing.load_yaml", return_value={}):
            with self.assertRaises(ModelRoutingError):
                load_model_escalation_policy(ROOT)
        with patch(
            "src.negrita_brain.model_routing.load_yaml",
            return_value={"model_escalation_policy": {"tiers": {}}},
        ):
            with self.assertRaises(ModelRoutingError):
                load_model_escalation_policy(ROOT)

    def test_disagreement_above_sol_stays_at_sol(self) -> None:
        route = resolve_model_route(
            self.policy,
            provider="codex",
            risk_signals=["architecture_decision", "reviewer_disagreement"],
        )
        self.assertEqual(route["tier"], "sol_high")

    def test_resolver_rejects_an_invalid_policy(self) -> None:
        invalid = copy.deepcopy(self.policy)
        invalid["tiers"] = {}
        with self.assertRaises(ModelRoutingError):
            resolve_model_route(invalid, provider="codex")


if __name__ == "__main__":
    unittest.main()
