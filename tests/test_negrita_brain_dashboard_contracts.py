"""Behavioral tests for the NegritaOS 360 dashboard contracts."""

import unittest
from dataclasses import replace

from negrita_brain.dashboard_contracts import (
    UNKNOWN,
    AcceptanceCriterion,
    ClientId,
    ClientRef,
    ClientKind,
    DesignId,
    DesignSpec,
    FeatureId,
    FeatureSpec,
    GoalId,
    GoalSpec,
    MetricDirection,
    PlanId,
    PlanRevision,
    ProjectId,
    ProjectRef,
    RevisionId,
    RevisionKind,
    RevisionRef,
    UnknownValue,
    validate_activation_preflight,
)


def _criterion(name: str = "criterion") -> AcceptanceCriterion:
    return AcceptanceCriterion(
        criterion_id=name,
        revision_id=RevisionId("criterion-r1"),
        condition="observable condition",
        evidence_requirement="receipt",
    )


def _feature(name: str, dependencies: tuple[str, ...] = ()) -> FeatureSpec:
    return FeatureSpec(
        feature_id=FeatureId(name),
        goal_ref=RevisionRef(RevisionKind.GOAL, "goal-1", RevisionId("goal-r1")),
        description="feature",
        inputs=(),
        outputs=(),
        acceptance_criteria=(_criterion(f"criterion-{name}"),),
        design_ref=RevisionRef(RevisionKind.DESIGN, "design-1", RevisionId("design-r1")),
        owner="owner@example.test",
        dependencies=dependencies,
    )


def _plan(**overrides: object) -> PlanRevision:
    values: dict[str, object] = {
        "plan_id": PlanId("plan-1"),
        "revision_id": RevisionId("plan-r1"),
        "project": ProjectRef(ProjectId("project-1"), ClientId("client-1")),
        "client": ClientRef(ClientId("client-1"), "Example client", ClientKind.EXTERNAL),
        "goal": GoalSpec(
            goal_id=GoalId("goal-1"),
            revision_id=RevisionId("goal-r1"),
            purpose="outcome",
            metric="retention",
            unit="percent",
            direction=MetricDirection.INCREASE,
            target=0,
            window="2026-Q4",
            owner="owner@example.test",
            measurement_source="approved source",
        ),
        "design": DesignSpec(
            DesignId("design-1"),
            RevisionId("design-r1"),
            "sha256:" + "a" * 64,
            screens=("overview",),
            states=("ready", "empty"),
            interactions=("open",),
            accessibility=("keyboard",),
        ),
        "features": (_feature("feature-1"),),
        "owner": "owner@example.test",
        "scope": ("read-only",),
        "exclusions": ("no execution",),
    }
    values.update(overrides)
    return PlanRevision(**values)  # type: ignore[arg-type]


class TestDashboardContracts(unittest.TestCase):
    def test_unknown_is_distinct_from_zero(self) -> None:
        self.assertIsInstance(UNKNOWN, UnknownValue)
        self.assertNotEqual(UNKNOWN, 0)
        self.assertEqual(_plan().goal.target, 0)

    def test_plan_is_immutable_and_new_revision_is_required_for_change(self) -> None:
        with self.assertRaises((AttributeError, TypeError)):
            _plan().owner = "other@example.test"  # type: ignore[misc]
        changed = _plan(revision_id=RevisionId("plan-r2"), parent_revision=RevisionId("plan-r1"))
        self.assertEqual(changed.parent_revision, RevisionId("plan-r1"))
        self.assertNotEqual(changed.revision_id, _plan().revision_id)

    def test_preflight_accepts_complete_plan_with_zero_target(self) -> None:
        self.assertEqual(validate_activation_preflight(_plan()), ())

    def test_preflight_reports_missing_owner_goal_fields_and_design(self) -> None:
        goal = _plan().goal
        incomplete_goal = GoalSpec(
            goal_id=goal.goal_id,
            revision_id=goal.revision_id,
            purpose=goal.purpose,
            metric=UNKNOWN,
            unit=None,
            direction=goal.direction,
            target=UNKNOWN,
            window="",
            owner=goal.owner,
            measurement_source=goal.measurement_source,
        )
        issues = validate_activation_preflight(_plan(owner=UNKNOWN, goal=incomplete_goal, design=None))
        codes = {issue.code for issue in issues}
        self.assertTrue(
            {
                "missing_owner",
                "missing_goal_metric",
                "missing_goal_target",
                "missing_goal_unit",
                "missing_goal_window",
                "missing_design",
            }.issubset(codes)
        )

    def test_preflight_reports_missing_criterion_and_duplicate_dependency(self) -> None:
        feature = _feature("feature-1", (FeatureId("feature-2"), FeatureId("feature-2")))
        feature = FeatureSpec(
            feature_id=feature.feature_id,
            goal_ref=feature.goal_ref,
            description=feature.description,
            inputs=feature.inputs,
            outputs=feature.outputs,
            acceptance_criteria=(),
            design_ref=feature.design_ref,
            owner=feature.owner,
            dependencies=feature.dependencies,
        )
        codes = {issue.code for issue in validate_activation_preflight(_plan(features=(feature,)))}
        self.assertIn("missing_feature_criterion", codes)
        self.assertIn("duplicate_dependency", codes)
        self.assertIn("missing_dependency", codes)

    def test_preflight_reports_dependency_cycle(self) -> None:
        features = (_feature("feature-1", (FeatureId("feature-2"),)), _feature("feature-2", (FeatureId("feature-1"),)))
        codes = {issue.code for issue in validate_activation_preflight(_plan(features=features))}
        self.assertIn("dependency_cycle", codes)

    def test_preflight_reports_client_project_mismatch(self) -> None:
        client = ClientRef(ClientId("client-2"), "Other")
        codes = {issue.code for issue in validate_activation_preflight(_plan(client=client))}
        self.assertIn("client_project_mismatch", codes)

    def test_preflight_blocks_unknown_client_without_treating_it_as_internal(self) -> None:
        project = ProjectRef(ProjectId("project-1"), UNKNOWN)
        client = ClientRef(UNKNOWN, "Unassigned", ClientKind.UNASSIGNED)
        codes = {issue.code for issue in validate_activation_preflight(_plan(project=project, client=client))}
        self.assertIn("missing_client", codes)

    def test_preflight_rejects_reference_to_another_design(self) -> None:
        feature = _feature("feature-1")
        other = FeatureSpec(feature.feature_id, feature.goal_ref, feature.description, feature.inputs,
                            feature.outputs, feature.acceptance_criteria,
                            RevisionRef(RevisionKind.DESIGN, "other", RevisionId("design-r1")),
                            feature.owner)
        codes = {issue.code for issue in validate_activation_preflight(_plan(features=(other,)))}
        self.assertIn("design_reference_mismatch", codes)

    def test_preflight_rejects_nonfinite_or_nonnumeric_target(self) -> None:
        for target in (float("nan"), float("inf"), True, "unknown"):
            with self.subTest(target=target):
                goal = replace(_plan().goal, target=target)
                codes = {issue.code for issue in validate_activation_preflight(_plan(goal=goal))}
                self.assertIn("invalid_goal_target", codes)

    def test_preflight_rejects_none_client_even_when_both_refs_match(self) -> None:
        project = ProjectRef(ProjectId("project-1"), None)  # type: ignore[arg-type]
        client = ClientRef(None, "Unknown", ClientKind.UNASSIGNED)  # type: ignore[arg-type]
        codes = {issue.code for issue in validate_activation_preflight(_plan(project=project, client=client))}
        self.assertIn("missing_client", codes)

    def test_preflight_rejects_blank_feature_id(self) -> None:
        feature = replace(_feature("feature-1"), feature_id=FeatureId(""))
        codes = {issue.code for issue in validate_activation_preflight(_plan(features=(feature,)))}
        self.assertIn("invalid_feature_id", codes)

    def test_preflight_rejects_unknown_design_hash(self) -> None:
        design = replace(_plan().design, content_hash=UNKNOWN)  # type: ignore[arg-type]
        codes = {issue.code for issue in validate_activation_preflight(_plan(design=design))}
        self.assertIn("incomplete_design", codes)

    def test_preflight_rejects_blank_revision_ids_even_with_matching_refs(self) -> None:
        plan = _plan()
        cases = [
            (replace(plan, revision_id=RevisionId("")), "invalid_plan_revision"),
            (
                replace(
                    plan,
                    goal=replace(plan.goal, revision_id=RevisionId("")),
                    features=(replace(plan.features[0], goal_ref=replace(
                        plan.features[0].goal_ref, revision_id=RevisionId("")
                    )),),
                ),
                "invalid_goal_revision",
            ),
            (
                replace(
                    plan,
                    design=replace(plan.design, revision_id=RevisionId("")),
                    features=(replace(plan.features[0], design_ref=replace(
                        plan.features[0].design_ref, revision_id=RevisionId("")
                    )),),
                ),
                "invalid_design_revision",
            ),
        ]
        for candidate, expected in cases:
            with self.subTest(expected=expected):
                codes = {issue.code for issue in validate_activation_preflight(candidate)}
                self.assertIn(expected, codes)

    def test_preflight_rejects_blank_goal_design_and_criterion_ids(self) -> None:
        plan = _plan()
        feature = plan.features[0]
        candidate = replace(
            plan,
            goal=replace(plan.goal, goal_id=GoalId("")),
            design=replace(plan.design, design_id=DesignId("")),
            features=(replace(feature, acceptance_criteria=(
                replace(feature.acceptance_criteria[0], criterion_id="", revision_id=RevisionId("")),
            )),),
        )
        codes = {issue.code for issue in validate_activation_preflight(candidate)}
        self.assertTrue({"invalid_goal_id", "invalid_design_id", "invalid_criterion_id"}.issubset(codes))
        self.assertIn("invalid_criterion_revision", codes)

    def test_preflight_rejects_blank_scope_and_exclusion_entries(self) -> None:
        candidate = _plan(scope=(" ",), exclusions=("",))
        codes = {issue.code for issue in validate_activation_preflight(candidate)}
        self.assertIn("missing_scope", codes)
        self.assertIn("missing_exclusions", codes)

    def test_preflight_rejects_blank_required_design_content(self) -> None:
        design = replace(
            _plan().design,
            screens=("",),
            states=(" ",),
            interactions=("",),
            accessibility=(" ",),
        )
        codes = {issue.code for issue in validate_activation_preflight(_plan(design=design))}
        self.assertIn("incomplete_design", codes)

    def test_preflight_rejects_duplicate_criterion_ids_across_features(self) -> None:
        first = _feature("feature-1")
        second = replace(_feature("feature-2"), acceptance_criteria=first.acceptance_criteria)
        codes = {issue.code for issue in validate_activation_preflight(_plan(features=(first, second)))}
        self.assertIn("duplicate_criterion_id", codes)

    def test_preflight_rejects_internal_id_with_external_kind(self) -> None:
        client = ClientRef(ClientId("internal"), "Internal", ClientKind.EXTERNAL)
        project = ProjectRef(ProjectId("project-1"), ClientId("internal"))
        codes = {issue.code for issue in validate_activation_preflight(_plan(client=client, project=project))}
        self.assertIn("client_classification_mismatch", codes)


if __name__ == "__main__":
    unittest.main()
