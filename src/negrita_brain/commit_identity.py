"""Commit identity policy and deterministic PR-range inspection."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .config import NEGRITAOS_ROOT, load_yaml


POLICY_PATH = Path("core/orchestration/commit_identity_policies.yaml")
VALID_INSPECTION_ROLES = {"author", "committer"}
RECORD_SEPARATOR = b"\x1e"
FIELD_COUNT = 6


@dataclass(frozen=True)
class CommitIdentity:
    """Author and committer metadata for one commit."""

    sha: str
    subject: str
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str


@dataclass(frozen=True)
class IdentityViolation:
    """One noncompliant identity without exposing the email local part."""

    sha: str
    subject: str
    role: str
    redacted_email: str


def load_commit_identity_policies(
    root: Path = NEGRITAOS_ROOT,
) -> Mapping[str, Any]:
    """Load the canonical commit identity policy document."""
    document = load_yaml(root / POLICY_PATH)
    value = document.get("commit_identity_policies")
    if not isinstance(value, Mapping):
        raise ValueError("commit_identity_policies root is missing")
    errors = validate_policy_document(value)
    if not errors:
        errors.extend(validate_project_policy_references(root, value))
    if errors:
        raise ValueError(errors[0])
    return value


def validate_policy_document(document: Mapping[str, Any]) -> list[str]:
    """Validate all declared commit identity policies."""
    errors: list[str] = []
    if document.get("schema_version") != 1:
        errors.append("commit identity policy schema_version must be 1")
    policies = document.get("policies")
    if not isinstance(policies, Mapping) or not policies:
        errors.append("commit identity policies must be a non-empty mapping")
        return errors
    for policy_id, value in policies.items():
        if not isinstance(value, Mapping):
            errors.append(f"policy {policy_id}: must be a mapping")
            continue
        project_scope = value.get("project_scope")
        valid_scope = isinstance(project_scope, list)
        if valid_scope:
            valid_scope = bool(project_scope) and all(
                isinstance(item, str) and item.strip() for item in project_scope
            )
            valid_scope = valid_scope and len(project_scope) == len(set(project_scope))
        if not valid_scope:
            errors.append(f"policy {policy_id}: project_scope is invalid")
        if value.get("enforcement") != "strict":
            errors.append(f"policy {policy_id}: enforcement must be strict")
        domains = value.get("allowed_email_domains")
        if not isinstance(domains, list) or not domains or not all(
            isinstance(item, str) and item.strip() and "@" not in item
            for item in domains
        ):
            errors.append(f"policy {policy_id}: allowed_email_domains is invalid")
        if not isinstance(value.get("allow_subdomains"), bool):
            errors.append(f"policy {policy_id}: allow_subdomains must be boolean")
        inspect = value.get("inspect")
        valid_inspect = isinstance(inspect, list)
        if valid_inspect:
            valid_inspect = len(inspect) == len(VALID_INSPECTION_ROLES)
            valid_inspect = valid_inspect and set(inspect) == VALID_INSPECTION_ROLES
        if not valid_inspect:
            errors.append(f"policy {policy_id}: inspect must contain author and committer")
        if value.get("range") != "introduced_commits_only":
            errors.append(f"policy {policy_id}: range must be introduced_commits_only")
        if value.get("legacy_history") != "excluded":
            errors.append(f"policy {policy_id}: legacy_history must be excluded")
        if value.get("hard_stop") is not True:
            errors.append(f"policy {policy_id}: hard_stop must be true")
        remediation = value.get("remediation")
        if not isinstance(remediation, Mapping):
            errors.append(f"policy {policy_id}: remediation must be a mapping")
        else:
            if remediation.get("automatic_history_rewrite") is not False:
                errors.append(
                    f"policy {policy_id}: automatic_history_rewrite must be false"
                )
            if remediation.get("require_explicit_user_authorization") is not True:
                errors.append(
                    f"policy {policy_id}: explicit rewrite authorization is required"
                )
            if remediation.get("force_mode") != "force_with_lease_only":
                errors.append(f"policy {policy_id}: force_mode must be force_with_lease_only")
    return errors


def validate_project_policy_references(
    root: Path, document: Mapping[str, Any]
) -> list[str]:
    """Validate both sides of policy-to-project opt-in declarations."""
    errors: list[str] = []
    policies = document.get("policies", {})
    if not isinstance(policies, Mapping):
        return ["commit identity policies must be a mapping"]
    scoped_projects: dict[str, str] = {}
    for policy_id, policy in policies.items():
        if not isinstance(policy, Mapping):
            continue
        for project_id in policy.get("project_scope", []):
            previous = scoped_projects.get(project_id)
            if previous is not None and previous != policy_id:
                errors.append(
                    f"project {project_id}: scoped by both {previous} and {policy_id}"
                )
            scoped_projects[project_id] = str(policy_id)

    declared_projects: dict[str, str] = {}
    for registry_path in sorted((root / "projects").glob("*.yaml")):
        registry = load_yaml(registry_path)
        project = registry.get("project", {})
        if not isinstance(project, Mapping):
            continue
        project_id = project.get("id")
        policy_id = project.get("commit_identity_policy")
        if not isinstance(project_id, str) or policy_id is None:
            continue
        if not isinstance(policy_id, str) or not policy_id.strip():
            errors.append(
                f"project {project_id}: commit_identity_policy must be a non-empty string"
            )
            continue
        declared_projects[project_id] = policy_id
        if policy_id not in policies:
            errors.append(
                f"project {project_id}: unknown commit identity policy {policy_id}"
            )

    for project_id, policy_id in sorted(scoped_projects.items()):
        registry_path = root / "projects" / f"{project_id}.yaml"
        if not registry_path.is_file():
            errors.append(f"policy {policy_id}: missing scoped project {project_id}")
        elif declared_projects.get(project_id) != policy_id:
            errors.append(
                f"project {project_id}: policy scope requires {policy_id}, "
                f"found {declared_projects.get(project_id)!r}"
            )
    for project_id, policy_id in sorted(declared_projects.items()):
        if scoped_projects.get(project_id) != policy_id:
            errors.append(
                f"project {project_id}: declares {policy_id} but is absent from its scope"
            )
    return errors


def resolve_policy(
    project: Mapping[str, Any], document: Mapping[str, Any]
) -> tuple[str, Mapping[str, Any]] | None:
    """Resolve a project's optional commit identity policy."""
    policy_id = project.get("commit_identity_policy")
    if policy_id is None:
        return None
    if not isinstance(policy_id, str) or not policy_id.strip():
        raise ValueError("commit_identity_policy must be a non-empty string")
    policies = document.get("policies", {})
    policy = policies.get(policy_id) if isinstance(policies, Mapping) else None
    if not isinstance(policy, Mapping):
        raise ValueError(f"unknown commit identity policy: {policy_id}")
    return policy_id, policy


def policy_contract(
    project: Mapping[str, Any], document: Mapping[str, Any]
) -> dict[str, Any]:
    """Return the non-secret policy fields needed by runtime reviewers."""
    resolved = resolve_policy(project, document)
    if resolved is None:
        return {"policy": None, "status": "not_applicable"}
    policy_id, policy = resolved
    return {
        "policy": policy_id,
        "status": "required",
        "enforcement": policy["enforcement"],
        "allowed_email_domains": list(policy["allowed_email_domains"]),
        "allow_subdomains": policy["allow_subdomains"],
        "inspect": list(policy["inspect"]),
        "range": policy["range"],
        "hard_stop": policy["hard_stop"],
    }


def email_domain(email: str) -> str | None:
    """Return a normalized domain or None for malformed email metadata."""
    normalized = email.strip().lower()
    if "@" not in normalized:
        return None
    local, domain = normalized.rsplit("@", maxsplit=1)
    return domain if local and domain else None


def email_is_allowed(
    email: str,
    allowed_domains: Iterable[str],
    allow_subdomains: bool,
) -> bool:
    """Return whether an email belongs to an allowed corporate domain."""
    domain = email_domain(email)
    if domain is None:
        return False
    for raw_allowed in allowed_domains:
        allowed = raw_allowed.strip().lower()
        if domain == allowed:
            return True
        if allow_subdomains and domain.endswith(f".{allowed}"):
            return True
    return False


def redact_email(email: str) -> str:
    """Mask the local part while retaining the policy-relevant domain."""
    domain = email_domain(email)
    return f"***@{domain}" if domain is not None else "<invalid-email>"


def identity_violations(
    commits: Iterable[CommitIdentity], policy: Mapping[str, Any]
) -> tuple[IdentityViolation, ...]:
    """Return violations for every configured author/committer identity."""
    domains = tuple(str(item) for item in policy["allowed_email_domains"])
    allow_subdomains = bool(policy["allow_subdomains"])
    inspect = set(str(item) for item in policy["inspect"])
    violations: list[IdentityViolation] = []
    for commit in commits:
        values = {
            "author": commit.author_email,
            "committer": commit.committer_email,
        }
        for role in ("author", "committer"):
            email = values[role]
            if role in inspect and not email_is_allowed(
                email, domains, allow_subdomains
            ):
                violations.append(
                    IdentityViolation(
                        sha=commit.sha,
                        subject=commit.subject,
                        role=role,
                        redacted_email=redact_email(email),
                    )
                )
    return tuple(violations)


def parse_git_log(raw_log: bytes) -> tuple[CommitIdentity, ...]:
    """Parse record-separated Git identity output."""
    commits: list[CommitIdentity] = []
    records = raw_log.split(RECORD_SEPARATOR) if RECORD_SEPARATOR in raw_log else (raw_log,)
    for record in records:
        normalized = record.strip(b"\n")
        if not normalized:
            continue
        fields = normalized.split(b"\0")
        if len(fields) != FIELD_COUNT:
            raise ValueError("git log returned an incomplete commit identity record")
        commits.append(
            CommitIdentity(
                *(field.decode("utf-8", errors="replace") for field in fields)
            )
        )
    return tuple(commits)


def commit_identities(
    repo: Path,
    base: str,
    head: str,
    exclude_reachable: Iterable[str] = (),
) -> tuple[CommitIdentity, ...]:
    """Read identities from commits introduced between base and head."""
    command = [
        "git",
        "-C",
        str(repo),
        "log",
        "--format=%H%x00%s%x00%an%x00%ae%x00%cn%x00%ce%x1e",
        f"{base}..{head}",
    ]
    for excluded_ref in exclude_reachable:
        command.append(f"^{excluded_ref}")
    result = subprocess.run(command, check=True, capture_output=True)
    return parse_git_log(result.stdout)
