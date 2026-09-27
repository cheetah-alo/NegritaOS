"""Immutable domain contracts for the NegritaOS 360 tracking slice.

The contracts in this module are deliberately provider-agnostic.  They describe
what may be activated and validate a candidate plan without persistence, I/O, or
side effects.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import NewType, TypeAlias


ClientId = NewType("ClientId", str)
ProjectId = NewType("ProjectId", str)
GoalId = NewType("GoalId", str)
PlanId = NewType("PlanId", str)
DesignId = NewType("DesignId", str)
FeatureId = NewType("FeatureId", str)
CriterionId = NewType("CriterionId", str)
EvidenceId = NewType("EvidenceId", str)
RevisionId = NewType("RevisionId", str)


@dataclass(frozen=True, slots=True)
class UnknownValue:
    """An explicit value state meaning that an observation is unavailable."""

    reason: str = "not_observed"


UNKNOWN = UnknownValue()
MetricValue: TypeAlias = int | float
OptionalMetricValue: TypeAlias = MetricValue | UnknownValue | None


class ClientKind(str, Enum):
    """Classification for a client identity."""

    EXTERNAL = "external"
    INTERNAL = "internal"
    UNASSIGNED = "unassigned"


class PlanStatus(str, Enum):
    """Lifecycle state of a plan revision."""

    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class MetricDirection(str, Enum):
    """How an observed numeric outcome is compared with its target."""

    INCREASE = "increase"
    DECREASE = "decrease"
    AT_LEAST = "at_least"
    AT_MOST = "at_most"
    EXACT = "exact"


class FeatureStatus(str, Enum):
    """Delivery state of a feature definition."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    IN_REVIEW = "in_review"
    ACCEPTED = "accepted"


class EvidenceStatus(str, Enum):
    """Applicability state of evidence bound to a plan revision."""

    APPLICABLE = "applicable"
    STALE = "stale"
    UNKNOWN = "unknown"
    REVOKED = "revoked"


class RevisionKind(str, Enum):
    """Kinds of versioned definitions referenced by evidence."""

    GOAL = "goal"
    PLAN = "plan"
    DESIGN = "design"
    FEATURE = "feature"
    CRITERION = "criterion"


@dataclass(frozen=True, slots=True)
class ClientRef:
    """Stable client identity used for project scoping."""

    client_id: ClientId | UnknownValue
    name: str
    kind: ClientKind = ClientKind.EXTERNAL


@dataclass(frozen=True, slots=True)
class ProjectRef:
    """Stable project identity with exactly one primary client."""

    project_id: ProjectId
    client_id: ClientId | UnknownValue


@dataclass(frozen=True, slots=True)
class RevisionRef:
    """Reference to an immutable version of a domain definition."""

    kind: RevisionKind
    entity_id: str
    revision_id: RevisionId


@dataclass(frozen=True, slots=True)
class GoalSpec:
    """Outcome definition, kept separate from delivery completion."""

    goal_id: GoalId
    revision_id: RevisionId
    purpose: str
    metric: str | UnknownValue | None
    unit: str | UnknownValue | None
    direction: MetricDirection | UnknownValue | None
    target: OptionalMetricValue
    window: str | UnknownValue | None
    owner: str | UnknownValue | None
    measurement_source: str | UnknownValue | None
    baseline: OptionalMetricValue = UNKNOWN


@dataclass(frozen=True, slots=True)
class DesignSpec:
    """Versioned design contract referenced by a plan and its features."""

    design_id: DesignId
    revision_id: RevisionId
    content_hash: str
    screens: tuple[str, ...] = ()
    states: tuple[str, ...] = ()
    interactions: tuple[str, ...] = ()
    accessibility: tuple[str, ...] = ()
    decisions: tuple[str, ...] = ()
    boundaries: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AcceptanceCriterion:
    """A versioned condition that can be checked by evidence."""

    criterion_id: CriterionId
    revision_id: RevisionId
    condition: str | UnknownValue | None
    evidence_requirement: str | UnknownValue | None


@dataclass(frozen=True, slots=True)
class FeatureSpec:
    """Feature definition with explicit acceptance criteria and dependencies."""

    feature_id: FeatureId
    goal_ref: RevisionRef
    description: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    acceptance_criteria: tuple[AcceptanceCriterion, ...]
    design_ref: RevisionRef | None
    owner: str | UnknownValue | None
    dependencies: tuple[FeatureId, ...] = ()


@dataclass(frozen=True, slots=True)
class PlanRevision:
    """Immutable plan version whose replacement must be a new revision."""

    plan_id: PlanId
    revision_id: RevisionId
    project: ProjectRef
    client: ClientRef
    goal: GoalSpec
    design: DesignSpec | None
    features: tuple[FeatureSpec, ...]
    owner: str | UnknownValue | None
    scope: tuple[str, ...] = ()
    exclusions: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    parent_revision: RevisionId | None = None


@dataclass(frozen=True, slots=True)
class ActivationRecord:
    """An authorization event separate from the immutable plan definition."""

    plan_id: PlanId
    revision_id: RevisionId
    previous_active_revision: RevisionId | None
    actor_id: str
    occurred_at: str
    source_hash: str


@dataclass(frozen=True, slots=True)
class GoalObservation:
    """Measured outcome, never inferred from feature delivery state."""

    goal_ref: RevisionRef
    project: ProjectRef
    value: MetricValue | UnknownValue
    unit: str
    window_start: str
    window_end: str
    source_hash: str | None


@dataclass(frozen=True, slots=True)
class EvidenceReceipt:
    """Evidence bound to a project, feature, criterion, and exact revisions."""

    evidence_id: EvidenceId
    project: ProjectRef
    feature_ref: RevisionRef
    criterion_ref: RevisionRef
    design_ref: RevisionRef
    source_hash: str
    status: EvidenceStatus
    observed_at: str | None = None


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """Pure preflight finding; it does not imply any provider or persistence call."""

    code: str
    message: str
    feature_id: FeatureId | None = None


def _missing(value: object) -> bool:
    """Return whether a required value is absent or explicitly unknown."""

    return value is None or isinstance(value, UnknownValue) or (
        isinstance(value, str) and not value.strip()
    )


def _valid_id(value: object) -> bool:
    """Accept a bounded opaque ID with no whitespace or path separators."""

    return isinstance(value, str) and len(value) <= 128 and re.fullmatch(
        r"[A-Za-z][A-Za-z0-9_.-]*", value
    ) is not None


def _valid_text(value: object) -> bool:
    """Require actual text for a human-readable contract field."""

    return isinstance(value, str) and bool(value.strip())


def _valid_text_tuple(value: object) -> bool:
    """Reject empty or whitespace-only contract lists."""

    return isinstance(value, tuple) and bool(value) and all(_valid_text(item) for item in value)


def _feature_dependency_issues(features: tuple[FeatureSpec, ...]) -> list[ValidationIssue]:
    """Validate feature IDs, dependency references, and dependency cycles."""

    issues: list[ValidationIssue] = []
    feature_ids = [feature.feature_id for feature in features]
    known_ids = set(feature_ids)
    for feature_id in {item for item in feature_ids if feature_ids.count(item) > 1}:
        issues.append(ValidationIssue("duplicate_feature_id", f"duplicate feature: {feature_id}"))

    for feature in features:
        if not _valid_id(feature.feature_id):
            issues.append(
                ValidationIssue("invalid_feature_id", "feature needs a stable ID", feature.feature_id)
            )
        if len(feature.dependencies) != len(set(feature.dependencies)):
            issues.append(
                ValidationIssue(
                    "duplicate_dependency",
                    f"feature {feature.feature_id} repeats a dependency",
                    feature.feature_id,
                )
            )
        for dependency in feature.dependencies:
            if dependency not in known_ids:
                issues.append(
                    ValidationIssue(
                        "missing_dependency",
                        f"feature {feature.feature_id} depends on unknown feature {dependency}",
                        feature.feature_id,
                    )
                )

    graph = {feature.feature_id: set(feature.dependencies) for feature in features}
    visiting: set[FeatureId] = set()
    visited: set[FeatureId] = set()

    def visit(feature_id: FeatureId) -> None:
        if feature_id in visiting:
            issues.append(ValidationIssue("dependency_cycle", f"dependency cycle includes {feature_id}", feature_id))
            return
        if feature_id in visited or feature_id not in graph:
            return
        visiting.add(feature_id)
        for dependency in graph[feature_id]:
            visit(dependency)
        visiting.remove(feature_id)
        visited.add(feature_id)

    for feature_id in graph:
        visit(feature_id)
    return issues


def validate_activation_preflight(plan: PlanRevision) -> tuple[ValidationIssue, ...]:
    """Purely validate whether ``plan`` contains the minimum activation contract.

    The function only inspects the supplied immutable object.  It performs no
    writes, persistence access, provider calls, or inference from external data.
    """

    issues: list[ValidationIssue] = []
    required_plan_values = (
        ("missing_plan_id", plan.plan_id),
        ("missing_project_id", plan.project.project_id),
    )
    if not _valid_text(plan.owner):
        issues.append(ValidationIssue("missing_owner", "plan needs an owner"))
    issues.extend(
        ValidationIssue(code, f"plan is missing {code.removeprefix('missing_')}")
        for code, value in required_plan_values
        if _missing(value)
    )
    if _missing(plan.client.client_id) or _missing(plan.project.client_id):
        issues.append(ValidationIssue("missing_client", "project needs an explicit client before activation"))
    elif not _valid_id(plan.client.client_id) or not _valid_id(plan.project.client_id):
        issues.append(ValidationIssue("invalid_client", "client needs a stable identifier"))
    elif plan.client.client_id != plan.project.client_id:
        issues.append(ValidationIssue("client_project_mismatch", "project must have exactly one matching client"))
    if (
        not isinstance(plan.client.kind, ClientKind)
        or plan.client.kind == ClientKind.UNASSIGNED
        or (plan.client.kind == ClientKind.INTERNAL) != (plan.client.client_id == "internal")
    ):
        issues.append(
            ValidationIssue("client_classification_mismatch", "client kind and ID disagree")
        )
    if not _valid_id(plan.plan_id) or not _valid_id(plan.project.project_id):
        issues.append(ValidationIssue("invalid_plan_scope", "plan and project need stable IDs"))
    if not _valid_id(plan.revision_id):
        issues.append(ValidationIssue("invalid_plan_revision", "plan needs a revision ID"))
    if plan.parent_revision is not None and (
        not _valid_id(plan.parent_revision) or plan.parent_revision == plan.revision_id
    ):
        issues.append(ValidationIssue("invalid_parent_revision", "parent revision is invalid"))

    for code, value in (("missing_scope", plan.scope), ("missing_exclusions", plan.exclusions)):
        if not _valid_text_tuple(value):
            issues.append(ValidationIssue(code, f"plan is missing {code.removeprefix('missing_')}"))

    required_goal_text = (
        ("missing_goal_purpose", plan.goal.purpose),
        ("missing_goal_metric", plan.goal.metric),
        ("missing_goal_unit", plan.goal.unit),
        ("missing_goal_window", plan.goal.window),
        ("missing_goal_owner", plan.goal.owner),
        ("missing_goal_source", plan.goal.measurement_source),
    )
    issues.extend(
        ValidationIssue(code, f"goal is missing {code.removeprefix('missing_goal_')}")
        for code, value in required_goal_text
        if not _valid_text(value)
    )
    if _missing(plan.goal.direction):
        issues.append(ValidationIssue("missing_goal_direction", "goal is missing direction"))
    if not _valid_id(plan.goal.goal_id):
        issues.append(ValidationIssue("invalid_goal_id", "goal needs a stable ID"))
    if not _valid_id(plan.goal.revision_id):
        issues.append(ValidationIssue("invalid_goal_revision", "goal needs a revision ID"))
    if not _missing(plan.goal.direction) and not isinstance(plan.goal.direction, MetricDirection):
        issues.append(ValidationIssue("invalid_goal_direction", "goal direction is not supported"))
    target = plan.goal.target
    if _missing(target):
        issues.append(ValidationIssue("missing_goal_target", "goal is missing target"))
    elif (
        isinstance(target, bool)
        or not isinstance(target, (int, float))
        or not isfinite(target)
    ):
        issues.append(ValidationIssue("invalid_goal_target", "goal target must be a finite number"))
    baseline = plan.goal.baseline
    if baseline is None or (
        not isinstance(baseline, UnknownValue)
        and (
            isinstance(baseline, bool)
            or not isinstance(baseline, (int, float))
            or not isfinite(baseline)
        )
    ):
        issues.append(ValidationIssue("invalid_goal_baseline", "baseline must be numeric or unknown"))
    if plan.design is None:
        issues.append(ValidationIssue("missing_design", "plan is missing a design revision"))
    else:
        if not _valid_id(plan.design.design_id):
            issues.append(ValidationIssue("invalid_design_id", "design needs a stable ID"))
        if not _valid_id(plan.design.revision_id):
            issues.append(ValidationIssue("invalid_design_revision", "design needs a revision ID"))
        if not isinstance(plan.design.content_hash, str) or re.fullmatch(
            r"sha256:[0-9a-f]{64}", plan.design.content_hash
        ) is None:
            issues.append(ValidationIssue("incomplete_design", "design needs a SHA-256 hash"))
        for field in ("screens", "states", "interactions", "accessibility"):
            value = getattr(plan.design, field)
            if not _valid_text_tuple(value):
                issues.append(ValidationIssue("incomplete_design", f"design is missing {field}"))

    if not plan.features:
        issues.append(ValidationIssue("missing_features", "plan has no features"))
    criterion_ids = [
        criterion.criterion_id
        for feature in plan.features
        for criterion in feature.acceptance_criteria
    ]
    if len(criterion_ids) != len(set(criterion_ids)):
        issues.append(ValidationIssue("duplicate_criterion_id", "criterion IDs must be unique"))
    for feature in plan.features:
        if not _valid_text(feature.owner) or not _valid_text(feature.description):
            issues.append(
                ValidationIssue(
                    "incomplete_feature", "feature needs owner and description", feature.feature_id
                )
            )
        if (
            feature.goal_ref.kind != RevisionKind.GOAL
            or feature.goal_ref.entity_id != plan.goal.goal_id
            or feature.goal_ref.revision_id != plan.goal.revision_id
        ):
            issues.append(
                ValidationIssue(
                    "goal_reference_mismatch",
                    "feature must reference the plan goal revision",
                    feature.feature_id,
                )
            )
        if not feature.acceptance_criteria:
            issues.append(
                ValidationIssue("missing_feature_criterion", "feature has no acceptance criterion", feature.feature_id)
            )
        for criterion in feature.acceptance_criteria:
            if not _valid_id(criterion.criterion_id):
                issues.append(
                    ValidationIssue("invalid_criterion_id", "criterion needs a stable ID", feature.feature_id)
                )
            if not _valid_id(criterion.revision_id):
                issues.append(
                    ValidationIssue(
                        "invalid_criterion_revision", "criterion needs a revision ID", feature.feature_id
                    )
                )
            if not _valid_text(criterion.condition) or not _valid_text(
                criterion.evidence_requirement
            ):
                issues.append(
                    ValidationIssue(
                        "missing_feature_criterion_detail",
                        f"feature {feature.feature_id} has an incomplete acceptance criterion",
                        feature.feature_id,
                    )
                )
        if feature.design_ref is None:
            issues.append(
                ValidationIssue(
                    "missing_feature_design", "feature is missing a design revision", feature.feature_id
                )
            )
        elif plan.design is not None and (
            feature.design_ref.kind != RevisionKind.DESIGN
            or feature.design_ref.entity_id != plan.design.design_id
            or feature.design_ref.revision_id != plan.design.revision_id
        ):
            issues.append(
                ValidationIssue(
                    "design_reference_mismatch",
                    "feature must reference the plan design revision",
                    feature.feature_id,
                )
            )
    issues.extend(_feature_dependency_issues(plan.features))
    return tuple(issues)
