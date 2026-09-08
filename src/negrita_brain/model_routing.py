"""Deterministic subagent model escalation for every NegritaOS project."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from .config import NEGRITAOS_ROOT, load_yaml


POLICY_PATH = Path("core/orchestration/model_escalation_policy.yaml")
VALID_REVIEW_ROLES = {"builder", "independent_reviewer"}


class ModelRoutingError(ValueError):
    """Raised when model selection would require guessing or violate policy."""


def load_model_escalation_policy(
    negritaos_root: Path = NEGRITAOS_ROOT,
) -> dict[str, Any]:
    """Load and validate the canonical model escalation policy."""
    data = load_yaml(negritaos_root / POLICY_PATH)
    policy = data.get("model_escalation_policy")
    if not isinstance(policy, dict):
        raise ModelRoutingError("model_escalation_policy root is missing")
    errors = validate_model_escalation_policy(policy)
    if errors:
        raise ModelRoutingError(errors[0])
    return policy


def _validate_tiers(policy: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    """Validate tier definitions and return the usable tier mapping."""
    tiers = policy.get("tiers")
    if not isinstance(tiers, dict) or not tiers:
        errors.append("model escalation tiers must be a non-empty mapping")
        return {}

    ranks: list[int] = []
    for tier_id, tier in tiers.items():
        if not isinstance(tier, dict):
            errors.append(f"tier {tier_id}: must be a mapping")
            continue
        for key in ("model", "reasoning_effort"):
            if not isinstance(tier.get(key), str) or not tier[key].strip():
                errors.append(f"tier {tier_id}: {key} is required")
        rank = tier.get("rank")
        family_rank = tier.get("family_rank")
        if not isinstance(rank, int) or rank <= 0:
            errors.append(f"tier {tier_id}: rank must be a positive integer")
        else:
            ranks.append(rank)
        if not isinstance(family_rank, int) or family_rank <= 0:
            errors.append(f"tier {tier_id}: family_rank must be a positive integer")
    if len(ranks) != len(set(ranks)):
        errors.append("model escalation tier ranks must be unique")
    if policy.get("default_tier") not in tiers:
        errors.append("default_tier must reference a declared tier")
    return tiers


def _validate_tier_mapping(
    policy: dict[str, Any],
    tiers: dict[str, Any],
    name: str,
    errors: list[str],
) -> None:
    """Validate one policy mapping whose values resolve to model tiers."""
    mapping = policy.get(name, {})
    if not isinstance(mapping, dict):
        errors.append(f"{name} must be a mapping")
        return
    for key, value in mapping.items():
        if isinstance(value, str):
            target = value
        elif isinstance(value, dict) and isinstance(value.get("tier"), str):
            target = value["tier"]
        elif isinstance(value, dict) and isinstance(value.get("escalate_family"), int):
            if value["escalate_family"] <= 0:
                errors.append(f"{name}.{key}: escalate_family must be positive")
            continue
        else:
            errors.append(f"{name}.{key}: invalid tier rule")
            continue
        if target not in tiers:
            errors.append(f"{name}.{key}: unknown tier {target!r}")


def _validate_action_defaults(policy: dict[str, Any], errors: list[str]) -> None:
    """Validate action-to-task-class references."""
    task_classes = policy.get("task_classes", {})
    action_defaults = policy.get("action_defaults", {})
    if not isinstance(action_defaults, dict):
        errors.append("action_defaults must be a mapping")
        return
    if not isinstance(task_classes, dict):
        return
    for action, task_class in action_defaults.items():
        if task_class not in task_classes:
            errors.append(
                f"action_defaults.{action}: unknown task class {task_class!r}"
            )


def _validate_impact_level_entry(
    impact: str,
    config: dict[str, Any],
    tiers: dict[str, Any],
    errors: list[str],
) -> int | None:
    """Validate one impact-level entry and return its usable rank."""
    rank = config.get("rank")
    if not isinstance(rank, int) or rank <= 0:
        errors.append(f"impact_levels.{impact}: rank must be a positive integer")
        rank = None
    if not isinstance(config.get("independent_review_required"), bool):
        errors.append(
            f"impact_levels.{impact}: independent_review_required must be boolean"
        )
    if config.get("minimum_reviewer_tier") not in tiers:
        errors.append(f"impact_levels.{impact}: minimum_reviewer_tier is unknown")
    evidence = config.get("required_evidence")
    if not isinstance(evidence, list) or not all(
        isinstance(item, str) and item.strip() for item in evidence
    ):
        errors.append(
            f"impact_levels.{impact}: required_evidence must be a string list"
        )
    elif impact in {"high", "production_candidate"} and not evidence:
        errors.append(f"impact_levels.{impact}: required_evidence cannot be empty")
    return rank


def _validate_impact_contract(
    impact_levels: dict[str, Any], errors: list[str]
) -> None:
    """Require the canonical standard/high/production review progression."""
    required_levels = {"standard", "high", "production_candidate"}
    missing_levels = sorted(required_levels - set(impact_levels))
    if missing_levels:
        errors.append("impact_levels missing: " + ", ".join(missing_levels))
    high = impact_levels.get("high", {})
    production = impact_levels.get("production_candidate", {})
    if isinstance(high, dict) and high.get("independent_review_required") is not True:
        errors.append("impact_levels.high must require independent review")
    if (
        isinstance(production, dict)
        and production.get("independent_review_required") is not True
    ):
        errors.append("impact_levels.production_candidate must require independent review")
    if isinstance(high, dict) and isinstance(production, dict):
        high_evidence = high.get("required_evidence", [])
        production_evidence = production.get("required_evidence", [])
        if isinstance(high_evidence, list) and isinstance(production_evidence, list):
            if not set(high_evidence).issubset(production_evidence):
                errors.append(
                    "production_candidate evidence must include every high-impact category"
                )


def _validate_impact_levels(
    policy: dict[str, Any], tiers: dict[str, Any], errors: list[str]
) -> None:
    """Validate independent-review requirements for every impact level."""
    impact_levels = policy.get("impact_levels", {})
    if not isinstance(impact_levels, dict) or not impact_levels:
        errors.append("impact_levels must be a non-empty mapping")
        return
    ranks: list[int] = []
    for impact, config in impact_levels.items():
        if not isinstance(config, dict):
            errors.append(f"impact_levels.{impact}: must be a mapping")
            continue
        rank = _validate_impact_level_entry(impact, config, tiers, errors)
        if rank is not None:
            ranks.append(rank)
    if len(ranks) != len(set(ranks)):
        errors.append("impact level ranks must be unique")
    _validate_impact_contract(impact_levels, errors)


def _validate_impact_routes(policy: dict[str, Any], errors: list[str]) -> None:
    """Validate task-class and signal mappings into declared impact levels."""
    impacts = policy.get("impact_levels", {})
    for mapping_name, source_name in (
        ("task_class_impacts", "task_classes"),
        ("signal_impacts", "escalation_signals"),
        ("agent_impacts", "custom_agent_tiers"),
    ):
        mapping = policy.get(mapping_name, {} if mapping_name == "agent_impacts" else None)
        source = policy.get(source_name)
        if not isinstance(mapping, dict):
            errors.append(f"{mapping_name} must be a mapping")
            continue
        if not isinstance(source, dict):
            continue
        for key, impact in mapping.items():
            if key not in source:
                errors.append(f"{mapping_name}.{key}: unknown {source_name} key")
            if impact not in impacts:
                errors.append(f"{mapping_name}.{key}: unknown impact {impact!r}")


def _validate_independent_review(policy: dict[str, Any], errors: list[str]) -> None:
    """Require immutable independent-review controls."""
    review = policy.get("independent_review")
    if not isinstance(review, dict):
        errors.append("independent_review must be a mapping")
        return
    for key in (
        "separate_session_required",
        "self_review_forbidden",
        "reviewer_must_attempt_falsification",
        "disagreement_escalates_one_family",
    ):
        if review.get(key) is not True:
            errors.append(f"independent_review.{key} must be true")
    if review.get("pass_status") != "PASS":
        errors.append("independent_review.pass_status must be PASS")
    if review.get("evidence_reference_format") != (
        "category=(repo|memory):relative_receipt.json@sha256:<64_hex>"
    ):
        errors.append("independent_review.evidence_reference_format is invalid")
    if review.get("evidence_receipt_schema_version") != 1:
        errors.append("independent_review.evidence_receipt_schema_version must be 1")


def _validate_evidence_categories(policy: dict[str, Any], errors: list[str]) -> None:
    """Require policy for every evidence category used by an impact level."""
    evidence_categories = policy.get("evidence_categories")
    if not isinstance(evidence_categories, dict) or not evidence_categories:
        errors.append("evidence_categories must be a non-empty mapping")
        return
    required_categories = {
        category
        for impact in policy.get("impact_levels", {}).values()
        if isinstance(impact, dict)
        for category in impact.get("required_evidence", [])
        if isinstance(category, str)
    }
    for category in sorted(required_categories):
        config = evidence_categories.get(category)
        if not isinstance(config, dict):
            errors.append(f"evidence_categories.{category} must be a mapping")
        elif not isinstance(config.get("not_applicable_allowed"), bool):
            errors.append(
                f"evidence_categories.{category}.not_applicable_allowed must be boolean"
            )


def _validate_governance(policy: dict[str, Any], errors: list[str]) -> None:
    """Require evidence, authorization, and independent-review controls."""
    _validate_independent_review(policy, errors)
    _validate_evidence_categories(policy, errors)
    governance = policy.get("governance")
    if not isinstance(governance, dict):
        errors.append("governance must be a mapping")
        return
    for key in (
        "missing_required_evidence",
        "skipped_gate",
        "unverified_lineage",
        "failed_validation",
        "unresolved_material_ambiguity",
    ):
        if governance.get(key) != "HOLD":
            errors.append(f"governance.{key} must be HOLD")
    for key in (
        "larger_model_does_not_replace_evidence",
        "larger_model_does_not_replace_user_authorization",
        "approved_contracts_remain_authoritative",
        "bounded_work_may_return_to_luna_after_decision",
        "distinguish_observation_inference_recommendation",
        "prohibit_opportunistic_upscaling",
    ):
        if governance.get(key) is not True:
            errors.append(f"governance.{key} must be true")


def _validate_global_agents(policy: dict[str, Any], errors: list[str]) -> None:
    """Validate global agent declarations and direct Codex routing."""
    global_agents = policy.get("global_codex_custom_agents", [])
    custom_agent_tiers = policy.get("custom_agent_tiers", {})
    if not isinstance(global_agents, list) or not all(
        isinstance(item, str) and item.strip() for item in global_agents
    ):
        errors.append("global_codex_custom_agents must be a string list")
    elif isinstance(custom_agent_tiers, dict):
        for name in global_agents:
            if name not in custom_agent_tiers:
                errors.append(f"global custom agent {name}: tier override is required")

    applications = policy.get("provider_application", {})
    if (
        not isinstance(applications, dict)
        or applications.get("codex") != "direct_model_selection"
    ):
        errors.append("provider_application.codex must be direct_model_selection")


def validate_model_escalation_policy(policy: dict[str, Any]) -> list[str]:
    """Return structural and referential errors in one model policy."""
    errors: list[str] = []
    tiers = _validate_tiers(policy, errors)
    if not tiers:
        return errors
    for name in ("task_classes", "escalation_signals", "custom_agent_tiers"):
        _validate_tier_mapping(policy, tiers, name, errors)
    _validate_action_defaults(policy, errors)
    _validate_impact_levels(policy, tiers, errors)
    _validate_impact_routes(policy, errors)
    _validate_governance(policy, errors)
    _validate_global_agents(policy, errors)
    evaluation = policy.get("evaluation", {})
    if not isinstance(evaluation, dict):
        errors.append("evaluation must be a mapping")
    return errors


def _tier_rank(policy: dict[str, Any], tier_id: str) -> int:
    return int(policy["tiers"][tier_id]["rank"])


def _higher_tier(policy: dict[str, Any], current: str, candidate: str) -> str:
    return candidate if _tier_rank(policy, candidate) > _tier_rank(policy, current) else current


def _next_family_tier(policy: dict[str, Any], current: str, steps: int) -> str:
    tiers = policy["tiers"]
    current_family = int(tiers[current]["family_rank"])
    target_family = current_family + steps
    candidates = [
        (int(config["rank"]), tier_id)
        for tier_id, config in tiers.items()
        if int(config["family_rank"]) >= target_family
    ]
    if not candidates:
        return max(tiers, key=lambda tier_id: int(tiers[tier_id]["rank"]))
    return min(candidates)[1]


def _higher_impact(policy: dict[str, Any], current: str, candidate: str) -> str:
    """Return the impact level with the stricter review contract."""
    impacts = policy["impact_levels"]
    return (
        candidate
        if int(impacts[candidate]["rank"]) > int(impacts[current]["rank"])
        else current
    )


def _effective_change_impact(
    policy: dict[str, Any],
    requested: str,
    actions: Iterable[str],
    delegation_class: str | None,
    risk_signals: Iterable[str],
    selected_agents: Iterable[str] = (),
) -> tuple[str, list[str]]:
    """Raise impact from declared task classes and material risk signals."""
    effective = requested
    reasons: list[str] = []
    for agent in selected_agents:
        candidate = policy.get("agent_impacts", {}).get(agent)
        if isinstance(candidate, str):
            updated = _higher_impact(policy, effective, candidate)
            if updated != effective:
                reasons.append(f"agent:{agent}->{candidate}")
                effective = updated
    action_defaults = policy.get("action_defaults", {})
    task_impacts = policy.get("task_class_impacts", {})
    task_classes = [action_defaults.get(action) for action in actions]
    if delegation_class is not None:
        task_classes.append(delegation_class)
    for task_class in task_classes:
        candidate = task_impacts.get(task_class)
        if isinstance(candidate, str):
            updated = _higher_impact(policy, effective, candidate)
            if updated != effective:
                reasons.append(f"task_class:{task_class}->{candidate}")
                effective = updated
    signal_impacts = policy.get("signal_impacts", {})
    for signal in risk_signals:
        candidate = signal_impacts.get(signal)
        if isinstance(candidate, str):
            updated = _higher_impact(policy, effective, candidate)
            if updated != effective:
                reasons.append(f"risk_signal:{signal}->{candidate}")
                effective = updated
    return effective, reasons


def _apply_candidate(
    policy: dict[str, Any],
    tier: str,
    candidate: str,
    reasons: list[str],
    reason: str,
) -> str:
    """Apply one minimum-tier candidate and record why it changed."""
    updated = _higher_tier(policy, tier, candidate)
    if updated != tier:
        reasons.append(reason)
    return updated


def _apply_task_routes(
    policy: dict[str, Any],
    tier: str,
    actions: Iterable[str],
    selected_agents: Iterable[str],
    delegation_class: str | None,
    reasons: list[str],
) -> str:
    """Apply action, explicit task-class, and custom-agent tier routes."""
    task_classes = policy["task_classes"]
    action_defaults = policy.get("action_defaults", {})
    for action in actions:
        task_class = action_defaults.get(action)
        if isinstance(task_class, str):
            tier = _apply_candidate(
                policy,
                tier,
                str(task_classes[task_class]),
                reasons,
                f"action:{action}->{task_class}",
            )
    if delegation_class is not None:
        if delegation_class not in task_classes:
            raise ModelRoutingError(f"unknown delegation class: {delegation_class}")
        tier = _apply_candidate(
            policy,
            tier,
            str(task_classes[delegation_class]),
            reasons,
            f"delegation_class:{delegation_class}",
        )
    custom_tiers = policy.get("custom_agent_tiers", {})
    for agent in selected_agents:
        candidate = custom_tiers.get(agent)
        if isinstance(candidate, str):
            tier = _apply_candidate(
                policy, tier, candidate, reasons, f"agent:{agent}"
            )
    return tier


def _apply_risk_signals(
    policy: dict[str, Any],
    tier: str,
    risk_signals: Iterable[str],
    reasons: list[str],
) -> tuple[str, list[str]]:
    """Apply fixed and relative-family escalation signals."""
    rules = policy["escalation_signals"]
    normalized: list[str] = []
    dynamic: list[tuple[str, int]] = []
    for signal in risk_signals:
        if signal not in rules:
            raise ModelRoutingError(f"unknown escalation signal: {signal}")
        if signal not in normalized:
            normalized.append(signal)
        rule = rules[signal]
        if isinstance(rule, str):
            tier = _apply_candidate(
                policy, tier, rule, reasons, f"risk_signal:{signal}"
            )
        else:
            dynamic.append((signal, int(rule["escalate_family"])))
    for signal, steps in dynamic:
        family = int(policy["tiers"][tier]["family_rank"])
        maximum = max(int(item["family_rank"]) for item in policy["tiers"].values())
        if family + steps > maximum:
            reasons.append(f"escalation_ceiling_reached:{signal}")
        tier = _apply_candidate(
            policy,
            tier,
            _next_family_tier(policy, tier, steps),
            reasons,
            f"risk_signal:{signal}",
        )
    return tier, normalized


def _validate_route_request(
    policy: dict[str, Any],
    change_impact: str,
    review_role: str,
    review_of_session: str | None,
) -> None:
    """Fail closed on unsupported impact or independent-review parameters."""
    if review_role not in VALID_REVIEW_ROLES:
        raise ModelRoutingError(f"unsupported review role: {review_role}")
    impacts = policy["impact_levels"]
    if change_impact not in impacts:
        raise ModelRoutingError(f"unknown change impact: {change_impact}")
    if review_role == "independent_reviewer" and not review_of_session:
        raise ModelRoutingError(
            "independent review requires --review-of-session from the builder contract"
        )
    if review_role == "builder" and review_of_session:
        raise ModelRoutingError("builder role cannot declare --review-of-session")


def resolve_model_route(
    policy: dict[str, Any],
    *,
    provider: str,
    actions: Iterable[str] = (),
    selected_agents: Iterable[str] = (),
    delegation_class: str | None = None,
    risk_signals: Iterable[str] = (),
    change_impact: str = "standard",
    review_role: str = "builder",
    review_of_session: str | None = None,
) -> dict[str, Any]:
    """Resolve the minimum justified model tier without opportunistic upscaling."""
    errors = validate_model_escalation_policy(policy)
    if errors:
        raise ModelRoutingError(errors[0])
    actions, selected_agents, risk_signals = tuple(actions), tuple(selected_agents), tuple(risk_signals)
    _validate_route_request(
        policy, change_impact, review_role, review_of_session
    )
    effective_impact, impact_reasons = _effective_change_impact(
        policy,
        change_impact,
        actions,
        delegation_class,
        risk_signals,
        selected_agents,
    )
    impact = policy["impact_levels"][effective_impact]

    tier = str(policy["default_tier"])
    reasons = [f"default:{tier}"]
    tier = _apply_task_routes(
        policy,
        tier,
        actions,
        selected_agents,
        delegation_class,
        reasons,
    )
    tier, normalized_signals = _apply_risk_signals(
        policy, tier, risk_signals, reasons
    )
    review_required = bool(impact["independent_review_required"])
    minimum_reviewer_tier = str(impact["minimum_reviewer_tier"])
    if review_role == "independent_reviewer":
        tier = _apply_candidate(
            policy,
            tier,
            minimum_reviewer_tier,
            reasons,
            f"review_minimum:{effective_impact}",
        )

    tier_config = policy["tiers"][tier]
    direct = policy["provider_application"].get(provider) == "direct_model_selection"
    return {
        "policy": str(POLICY_PATH),
        "scope": policy.get("scope", "all_registered_projects"),
        "tier": tier,
        "model": tier_config["model"] if direct else None,
        "reasoning_effort": tier_config["reasoning_effort"] if direct else None,
        "recommended_codex_model": tier_config["model"],
        "recommended_reasoning_effort": tier_config["reasoning_effort"],
        "provider_application": policy["provider_application"].get(
            provider, "tier_semantics_only"
        ),
        "selection_reasons": reasons,
        "unresolved_at_ceiling": any(reason.startswith("escalation_ceiling_reached:") for reason in reasons),
        "runtime_model_check": policy["governance"].get("runtime_model_availability_check", "required_before_spawn"),
        "evaluation": dict(policy.get("evaluation", {})),
        "delegation_class": delegation_class,
        "risk_signals": normalized_signals,
        "requested_change_impact": change_impact,
        "change_impact": effective_impact,
        "impact_escalation_reasons": impact_reasons,
        "independent_review": {
            "role": review_role,
            "required": review_required,
            "minimum_reviewer_tier": minimum_reviewer_tier,
            "separate_session_required": True,
            "review_of_session": review_of_session,
            "reviewer_must_attempt_falsification": True,
            "required_evidence": list(impact["required_evidence"]),
            "model_does_not_replace_evidence": policy["governance"][
                "larger_model_does_not_replace_evidence"
            ],
            "model_does_not_replace_user_authorization": policy["governance"][
                "larger_model_does_not_replace_user_authorization"
            ],
        },
    }
