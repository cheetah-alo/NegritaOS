"""Tests for ML and analytical-rule governance-card contracts."""

import copy
import unittest

from scripts.validate_model_governance_card import validate_model_governance_card


def valid_card(kind: str = "ml_predictive") -> dict:
    ml = {
        "target_definition": "churn within 30 days",
        "prediction_horizon": "30 days",
        "feature_cutoff": "strictly before prediction_time",
        "algorithm": "gradient boosted trees",
        "feature_count": 20,
        "config_ref": "config/model.yaml@sha256:abc",
        "split_strategy": "temporal train validation holdout",
        "entity_time_isolation": "account cannot cross split boundary",
        "imbalance_strategy": "class weights",
        "threshold_policy": "selected on validation utility",
        "calibration": "isotonic on validation only",
    }
    rules = {
        "rule_catalog_version": "rules-v1",
        "input_grain": "one row per account-day",
        "eligibility_policy": "active accounts only",
        "score_or_band_definition": "sum verified rule points then apply bands",
        "precedence_policy": "exit rules before friction rules",
        "overlap_conflict_policy": "highest-priority active rule wins",
        "missing_value_policy": "missing remains unknown and never becomes zero",
        "state_persistence_policy": "state expires after 30 inactive days",
        "change_approval_policy": "owner review and versioned backtest",
    }
    return {
        "model_governance_card": {
            "schema_version": 1,
            "card_id": "card-model-v1",
            "card_version": "1.0.0",
            "created_at": "2026-09-04T12:00:00+02:00",
            "updated_at": "2026-09-04T12:00:00+02:00",
            "evidence_cutoff": "2026-09-04T11:00:00+02:00",
            "supersedes": None,
            "model": {
                "id": "model-v1",
                "name": "Model V1",
                "version": "1.0.0",
                "kind": kind,
                "lifecycle_status": "VALIDATED",
                "business_objective": "Prioritize retention review",
                "decision_supported": "Queue ordering",
                "scope": "eligible active accounts",
                "parent_model": None,
            },
            "owners": {
                "business_owner": "Retention Lead",
                "technical_owner": "Data Science",
                "validation_owner": "Model QA",
                "deployment_owner": "MLOps",
                "monitoring_owner": "Model QA",
            },
            "evidence": {
                "source_revision": "commit:abc123",
                "run_ids": ["run-1"],
                "config_hashes": ["sha256:abc"],
                "query_hashes": [],
                "artifact_refs": ["model.bin@sha256:def"],
                "validation_refs": ["validation.json@sha256:ghi"],
            },
            "data": {
                "sources": ["logical_customer_features"],
                "transformations": ["aggregate to account-day"],
                "grain": "one row per account-day",
                "entity_keys": ["account_id", "reference_date"],
                "prediction_or_scoring_time": "reference_date start",
                "target_or_outcome_time": "disconnect event time",
                "temporal_window": {"start": "2025-01-01", "end": "2026-01-01"},
                "eligibility": ["active account"],
                "exclusions": ["post-outcome rows"],
                "population_counts": {
                    "source": 1000,
                    "eligible": 900,
                    "train_or_backtest": 600,
                    "validation": 150,
                    "test": 150,
                    "scored": None,
                    "reconciliation_status": "VERIFIED",
                },
                "quality_checks": [
                    {
                        "name": "entity key uniqueness",
                        "result": "no duplicates in eligible population",
                        "evidence_ref": "quality.json@sha256:jkl",
                        "status": "VERIFIED",
                    }
                ],
            },
            "logic": {
                "ml": ml if kind in {"ml_predictive", "hybrid"} else None,
                "rules": rules if kind in {"analytical_rule", "hybrid"} else None,
                "hybrid_interface": "rules gate model action" if kind == "hybrid" else None,
            },
            "validation": {
                "status": "VERIFIED",
                "design": "temporal holdout",
                "leakage_assessment": {
                    "status": "VERIFIED",
                    "summary": "no post-outcome features",
                    "evidence_ref": "leakage.json@sha256:mno",
                    "reason": None,
                },
                "baseline": "current operational queue",
                "metrics": [
                    {
                        "name": "recall",
                        "definition": "true positives over actual positives",
                        "dataset": "holdout",
                        "support": "150 rows, 20 positives",
                        "threshold": 0.42,
                        "threshold_reason": "",
                        "value": 0.7,
                        "unit": "ratio",
                        "baseline": "0.5",
                        "evidence_ref": "validation.json@sha256:ghi",
                        "interpretation": "captures 70 percent of positives",
                        "limitation": "small positive support",
                        "status": "VERIFIED",
                    }
                ],
                "sensitivity_or_ablation": [],
                "interpretation": "improves recall with bounded support",
                "limitations": ["requires live shadow validation"],
            },
            "explainability": {
                "status": "OBSERVED",
                "method": "SHAP" if kind != "analytical_rule" else "rule trace",
                "findings": [],
                "limitations": ["not causal"],
            },
            "operational_evaluation": {
                "status": "PENDING",
                "action_policy": "human-reviewed queue",
                "capacity_or_cost": "not yet measured",
                "human_review": "required before action",
                "limitations": [],
            },
            "monitoring": {"status": "PENDING", "indicators": []},
            "governance": {
                "status": "PENDING",
                "deployment_revision": None,
                "approval_ref": None,
                "rollback_policy": "restore prior version",
                "retraining_or_change_policy": "new card and validation for every change",
                "decision_history": [],
                "allowed_claim": "validated offline candidate",
                "prohibited_claim": "production impact",
            },
        }
    }


class TestModelGovernanceCard(unittest.TestCase):
    def test_valid_ml_rule_and_hybrid_cards(self) -> None:
        for kind in ("ml_predictive", "analytical_rule", "hybrid"):
            with self.subTest(kind=kind):
                self.assertEqual(validate_model_governance_card(valid_card(kind)), [])

    def test_placeholders_and_inherited_production_are_rejected(self) -> None:
        card = valid_card()
        root = card["model_governance_card"]
        root["model"]["lifecycle_status"] = "DEPLOYED"
        root["logic"]["ml"]["algorithm"] = "[add value]"

        errors = validate_model_governance_card(card)

        self.assertTrue(any("placeholder" in error for error in errors))
        self.assertTrue(any("VERIFIED monitoring" in error for error in errors))
        self.assertTrue(any("deployment_revision" in error for error in errors))

    def test_rule_card_requires_precedence_and_missing_value_policy(self) -> None:
        card = valid_card("analytical_rule")
        rules = card["model_governance_card"]["logic"]["rules"]
        rules["precedence_policy"] = ""
        rules["missing_value_policy"] = ""

        errors = validate_model_governance_card(card)

        self.assertTrue(any("precedence_policy" in error for error in errors))
        self.assertTrue(any("missing_value_policy" in error for error in errors))

    def test_verified_metric_requires_complete_context(self) -> None:
        card = copy.deepcopy(valid_card())
        metric = card["model_governance_card"]["validation"]["metrics"][0]
        metric["dataset"] = ""
        metric["evidence_ref"] = ""
        metric["threshold"] = None

        errors = validate_model_governance_card(card)

        self.assertTrue(any("dataset" in error for error in errors))
        self.assertTrue(any("evidence_ref" in error for error in errors))
        self.assertTrue(any("threshold or threshold_reason" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
