"""Deterministic Brave profile routing for NegritaOS projects."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .config import NEGRITAOS_ROOT, load_yaml


ROUTING_CONFIG = Path("core/orchestration/browser_profile_routing.yaml")


class BrowserRoutingError(ValueError):
    """Raised when a browser profile cannot be selected without guessing."""


@dataclass(frozen=True)
class BrowserRoute:
    """Resolved profile metadata without URL secrets or browser session data."""

    project_id: str
    account_scope: str
    purpose: str | None
    profile: str
    display_name: str
    profile_directory: str
    target_host: str | None
    resolution_source: str
    blocked_state: str

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-safe route description."""
        return asdict(self)


def load_browser_routing_config(
    negritaos_root: Path = NEGRITAOS_ROOT,
) -> dict[str, Any]:
    """Load the canonical browser profile routing mapping."""
    data = load_yaml(negritaos_root / ROUTING_CONFIG)
    root = data.get("browser_profile_routing")
    if not isinstance(root, dict):
        raise BrowserRoutingError("browser_profile_routing root is missing")
    return root


def _profile_ids(config: dict[str, Any]) -> set[str]:
    profiles = config.get("profiles", {})
    return set(profiles) if isinstance(profiles, dict) else set()


def validate_browser_routing_config(config: dict[str, Any]) -> list[str]:
    """Return structural errors in the canonical browser routing config."""
    errors: list[str] = []
    profiles = config.get("profiles")
    scopes = config.get("account_scopes")
    if not isinstance(profiles, dict) or not profiles:
        return ["browser routing profiles must be a non-empty mapping"]
    if not isinstance(scopes, dict) or not scopes:
        return ["browser routing account_scopes must be a non-empty mapping"]

    for profile_id, profile in profiles.items():
        if not isinstance(profile, dict):
            errors.append(f"profile {profile_id}: must be a mapping")
            continue
        for key in ("display_name", "profile_directory", "account_scope"):
            if not isinstance(profile.get(key), str) or not profile[key].strip():
                errors.append(f"profile {profile_id}: {key} is required")

    known_profiles = _profile_ids(config)
    for scope_id, scope in scopes.items():
        if not isinstance(scope, dict):
            errors.append(f"account scope {scope_id}: must be a mapping")
            continue
        default_profile = scope.get("default_profile")
        if default_profile not in known_profiles:
            errors.append(
                f"account scope {scope_id}: unknown default profile {default_profile!r}"
            )
        purpose_profiles = scope.get("purpose_profiles", {})
        if not isinstance(purpose_profiles, dict):
            errors.append(f"account scope {scope_id}: purpose_profiles must be a mapping")
            continue
        for purpose, profile_id in purpose_profiles.items():
            if profile_id not in known_profiles:
                errors.append(
                    f"account scope {scope_id}: purpose {purpose} references "
                    f"unknown profile {profile_id!r}"
                )

    organizations = config.get("github_organizations", {})
    if not isinstance(organizations, dict):
        errors.append("github_organizations must be a mapping")
    else:
        for organization, profile_id in organizations.items():
            if organization != str(organization).lower():
                errors.append(f"GitHub organization {organization!r} must be lowercase")
            if profile_id not in known_profiles:
                errors.append(
                    f"GitHub organization {organization}: unknown profile {profile_id!r}"
                )

    rules = config.get("domain_purpose_rules", [])
    if not isinstance(rules, list):
        errors.append("domain_purpose_rules must be a list")
    else:
        for index, rule in enumerate(rules):
            if not isinstance(rule, dict) or not isinstance(rule.get("purpose"), str):
                errors.append(f"domain_purpose_rules[{index}]: purpose is required")
                continue
            hosts = rule.get("host_suffixes")
            if not isinstance(hosts, list) or not all(
                isinstance(host, str) and host.strip() for host in hosts
            ):
                errors.append(
                    f"domain_purpose_rules[{index}]: host_suffixes must be a string list"
                )
    return errors


def validate_project_browser_context(
    project: dict[str, Any], config: dict[str, Any]
) -> list[str]:
    """Return errors for one project's browser routing declaration."""
    project_id = str(project.get("id", "unknown"))
    context = project.get("browser_context")
    if not isinstance(context, dict):
        return [f"project {project_id}: browser_context is required"]
    if context.get("routing_policy") != "governed":
        return [f"project {project_id}: browser_context.routing_policy must be governed"]

    errors: list[str] = []
    scopes = config.get("account_scopes", {})
    profiles = config.get("profiles", {})
    account_scope = context.get("account_scope")
    default_profile = context.get("default_profile")
    if account_scope not in scopes:
        errors.append(
            f"project {project_id}: unknown browser account_scope {account_scope!r}"
        )
    if default_profile not in profiles:
        errors.append(
            f"project {project_id}: unknown browser default_profile {default_profile!r}"
        )
    if account_scope in scopes and default_profile in profiles:
        scope_default = scopes[account_scope].get("default_profile")
        if default_profile != scope_default:
            errors.append(
                f"project {project_id}: default_profile {default_profile!r} differs "
                f"from account scope default {scope_default!r}"
            )
    return errors


def browser_context_summary(
    project: dict[str, Any], config: dict[str, Any]
) -> dict[str, Any]:
    """Return the browser contract included in a Brain session resolution."""
    errors = [
        *validate_browser_routing_config(config),
        *validate_project_browser_context(project, config),
    ]
    if errors:
        raise BrowserRoutingError(errors[0])
    context = project["browser_context"]
    profile = config["profiles"][context["default_profile"]]
    safety = config.get("safety", {})
    return {
        "routing_policy": "governed",
        "account_scope": context["account_scope"],
        "default_profile": context["default_profile"],
        "default_display_name": profile["display_name"],
        "launcher": "scripts/open_governed_browser.py",
        "config": str(ROUTING_CONFIG),
        "blocked_state": config.get(
            "blocked_state", "BLOCKED_BROWSER_PROFILE_RESOLUTION"
        ),
        "in_app_browser_policy": safety.get("in_app_browser_policy"),
        "authenticated_browser_policy": safety.get("authenticated_browser_policy"),
    }


def _normalize_purpose(config: dict[str, Any], purpose: str | None) -> str | None:
    if purpose is None:
        return None
    normalized = purpose.strip().lower().replace("-", "_").replace(" ", "_")
    if not normalized:
        return None
    aliases = config.get("purpose_aliases", {})
    if isinstance(aliases, dict):
        normalized = str(aliases.get(normalized, normalized))
    return normalized


def _host_matches(host: str, suffix: str) -> bool:
    normalized = suffix.strip().lower().lstrip(".")
    return host == normalized or host.endswith(f".{normalized}")


def _validated_url(
    config: dict[str, Any], url: str | None
) -> tuple[str | None, str | None, str | None]:
    """Return host, GitHub organization, and inferred purpose."""
    if url is None:
        return None, None, None
    parsed = urlsplit(url)
    safety = config.get("safety", {})
    allowed_schemes = set(safety.get("allowed_schemes", ["https"]))
    local_hosts = set(safety.get("local_http_hosts", []))
    host = (parsed.hostname or "").lower()
    if parsed.username is not None or parsed.password is not None:
        raise BrowserRoutingError("URLs containing user information are prohibited")
    if parsed.scheme not in allowed_schemes:
        if not (parsed.scheme == "http" and host in local_hosts):
            raise BrowserRoutingError(
                f"URL scheme {parsed.scheme!r} is not permitted for browser routing"
            )
    if not host:
        raise BrowserRoutingError("browser URL must include a host")

    github_org = None
    if host == "github.com":
        parts = [part for part in parsed.path.split("/") if part]
        github_org = parts[0].lower() if parts else None

    inferred_purpose = None
    for rule in config.get("domain_purpose_rules", []):
        if not isinstance(rule, dict):
            continue
        if any(
            _host_matches(host, suffix)
            for suffix in rule.get("host_suffixes", [])
            if isinstance(suffix, str)
        ):
            purpose = str(rule.get("purpose", "")).strip()
            if inferred_purpose is not None and inferred_purpose != purpose:
                raise BrowserRoutingError(
                    f"host {host} matches conflicting browser purposes"
                )
            inferred_purpose = purpose
    return host, github_org, inferred_purpose


def resolve_browser_route(
    project: dict[str, Any],
    config: dict[str, Any],
    *,
    purpose: str | None = None,
    url: str | None = None,
    explicit_profile: str | None = None,
) -> BrowserRoute:
    """Resolve a Brave profile without inspecting browser session state."""
    errors = [
        *validate_browser_routing_config(config),
        *validate_project_browser_context(project, config),
    ]
    if errors:
        raise BrowserRoutingError(errors[0])

    context = project["browser_context"]
    profiles = config["profiles"]
    account_scope = context["account_scope"]
    normalized_purpose = _normalize_purpose(config, purpose)
    host, github_org, inferred_purpose = _validated_url(config, url)

    if explicit_profile is not None:
        profile_id = explicit_profile.strip()
        if profile_id not in profiles:
            raise BrowserRoutingError(f"unknown explicit browser profile {profile_id!r}")
        source = "explicit_profile"
    else:
        org_profiles = config.get("github_organizations", {})
        org_profile = org_profiles.get(github_org) if github_org else None
        if org_profile is not None:
            if normalized_purpose not in {None, "github"}:
                raise BrowserRoutingError(
                    f"GitHub organization {github_org} conflicts with purpose "
                    f"{normalized_purpose!r}"
                )
            profile_id = org_profile
            normalized_purpose = "github"
            source = f"github_organization:{github_org}"
        else:
            scope = config["account_scopes"][account_scope]
            purpose_profiles = scope.get("purpose_profiles", {})
            if inferred_purpose and normalized_purpose and inferred_purpose != normalized_purpose:
                requested_profile = purpose_profiles.get(normalized_purpose)
                inferred_profile = purpose_profiles.get(inferred_purpose)
                if requested_profile is None or requested_profile != inferred_profile:
                    raise BrowserRoutingError(
                        f"URL purpose {inferred_purpose!r} conflicts with requested purpose "
                        f"{normalized_purpose!r}"
                    )
                effective_purpose = inferred_purpose
            else:
                effective_purpose = normalized_purpose or inferred_purpose
            if effective_purpose is not None:
                profile_id = purpose_profiles.get(effective_purpose)
                if profile_id is None:
                    raise BrowserRoutingError(
                        f"account scope {account_scope} has no route for purpose "
                        f"{effective_purpose!r}"
                    )
                normalized_purpose = effective_purpose
                source = f"purpose:{effective_purpose}"
            else:
                profile_id = context["default_profile"]
                source = "project_default"

    profile = profiles[profile_id]
    if profile.get("explicit_only") and explicit_profile is None:
        raise BrowserRoutingError(
            f"browser profile {profile_id!r} requires explicit selection"
        )
    return BrowserRoute(
        project_id=str(project["id"]),
        account_scope=account_scope,
        purpose=normalized_purpose,
        profile=profile_id,
        display_name=str(profile["display_name"]),
        profile_directory=str(profile["profile_directory"]),
        target_host=host,
        resolution_source=source,
        blocked_state=str(
            config.get("blocked_state", "BLOCKED_BROWSER_PROFILE_RESOLUTION")
        ),
    )


def verify_local_brave_profiles(config: dict[str, Any]) -> list[str]:
    """Verify configured profile directories and display names, not session data."""
    browser = config.get("browser", {})
    state_path = Path(str(browser.get("profile_state_file", ""))).expanduser()
    if not state_path.is_file():
        return [f"Brave profile state file is missing: {state_path}"]
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot read Brave profile metadata: {exc}"]
    cache = state.get("profile", {}).get("info_cache", {})
    if not isinstance(cache, dict):
        return ["Brave profile metadata has no profile.info_cache mapping"]
    errors: list[str] = []
    for profile_id, profile in config.get("profiles", {}).items():
        directory = profile.get("profile_directory")
        actual = cache.get(directory)
        if not isinstance(actual, dict):
            errors.append(f"{profile_id}: Brave directory {directory!r} is missing")
            continue
        expected_name = profile.get("display_name")
        if actual.get("name") != expected_name:
            errors.append(
                f"{profile_id}: expected Brave name {expected_name!r}, "
                f"found {actual.get('name')!r}"
            )
    return errors


def build_brave_command(
    route: BrowserRoute, config: dict[str, Any], url: str | None = None
) -> list[str]:
    """Build a shell-free Brave launch command for the selected profile."""
    browser = config.get("browser", {})
    executable = str(browser.get("executable", "")).strip()
    if not executable:
        raise BrowserRoutingError("Brave executable is not configured")
    arguments = browser.get("launch_arguments", [])
    if not isinstance(arguments, list) or not all(isinstance(item, str) for item in arguments):
        raise BrowserRoutingError("browser.launch_arguments must be a string list")
    command = [
        executable,
        f"--profile-directory={route.profile_directory}",
        *arguments,
    ]
    if url is not None:
        command.append(url)
    return command
