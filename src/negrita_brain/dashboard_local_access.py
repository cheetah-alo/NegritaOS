"""Load the local-only CAT-005B dashboard access policy."""

from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path
from typing import Any

from .dashboard_read_model import CatalogScopeGrant


_ID = re.compile(r"^[a-z][a-z0-9_-]*$")
_EXPECTED_KEYS = {"schema_version", "project_client_grants", "unknown_client_projects"}
_PAIR_KEYS = {"project_id", "client_id"}


class LocalPolicyError(ValueError):
    """Raised when a local CAT-005B policy is unsafe or malformed."""


def load_local_catalog_scope(config_path: Path) -> CatalogScopeGrant:
    """Load a local CAT-005B policy, defaulting to deny when it is absent.

    Existing policy files must be regular, non-symlink files owned by the
    current operating-system user and readable/writable only by that user.
    The loader performs no network access, client lookup, or logging.

    Args:
        config_path: Path to the local JSON policy file.

    Returns:
        The validated catalog scope grant.

    Raises:
        LocalPolicyError: If the policy path, JSON, schema, or entries are
            invalid.
    """
    if not isinstance(config_path, Path):
        raise LocalPolicyError("config_path must be a pathlib.Path")
    try:
        descriptor = os.open(config_path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    except FileNotFoundError:
        return CatalogScopeGrant()
    except OSError as exc:
        raise LocalPolicyError("unable to inspect local policy file") from exc
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise LocalPolicyError("local policy must be a regular non-symlink file")
        if file_stat.st_uid != os.getuid():
            raise LocalPolicyError("local policy must be owned by the current user")
        if file_stat.st_mode & 0o077:
            raise LocalPolicyError("local policy permissions must be user-only")
        if file_stat.st_size > 65536:
            raise LocalPolicyError("local policy exceeds the size limit")
        with os.fdopen(descriptor, "r", encoding="utf-8") as policy_file:
            descriptor = -1
            payload = json.load(policy_file)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LocalPolicyError("local policy is not valid JSON") from exc
    finally:
        if descriptor != -1:
            os.close(descriptor)

    return _scope_from_payload(payload)


def _scope_from_payload(payload: Any) -> CatalogScopeGrant:
    if not isinstance(payload, dict):
        raise LocalPolicyError("local policy must be a JSON object")
    if set(payload) != _EXPECTED_KEYS:
        raise LocalPolicyError("local policy contains unknown or missing keys")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise LocalPolicyError("local policy schema_version must be 1")

    pairs_payload = payload["project_client_grants"]
    unknown_payload = payload["unknown_client_projects"]
    if not isinstance(pairs_payload, list) or not isinstance(unknown_payload, list):
        raise LocalPolicyError("local policy grant fields must be lists")

    pairs: list[tuple[str, str]] = []
    client_by_project: dict[str, str] = {}
    for pair_payload in pairs_payload:
        if not isinstance(pair_payload, dict) or set(pair_payload) != _PAIR_KEYS:
            raise LocalPolicyError("project client grants must contain project_id and client_id")
        project_id = pair_payload["project_id"]
        client_id = pair_payload["client_id"]
        if not _valid_id(project_id) or not _valid_id(client_id):
            raise LocalPolicyError("project client grants contain malformed IDs")
        pair = (project_id, client_id)
        if pair in pairs:
            raise LocalPolicyError("project client grants contain duplicates")
        if project_id in client_by_project and client_by_project[project_id] != client_id:
            raise LocalPolicyError("one project cannot be granted to multiple clients")
        pairs.append(pair)
        client_by_project[project_id] = client_id

    unknown_ids: list[str] = []
    for project_id in unknown_payload:
        if not _valid_id(project_id):
            raise LocalPolicyError("unknown client projects contain malformed IDs")
        if project_id in unknown_ids:
            raise LocalPolicyError("unknown client projects contain duplicates")
        unknown_ids.append(project_id)

    unknown_set = set(unknown_ids)
    if any(project_id in unknown_set for project_id, _ in pairs):
        raise LocalPolicyError("unknown client projects overlap project client grants")

    return CatalogScopeGrant(
        project_client_grants=frozenset(pairs),
        project_grants=frozenset(unknown_ids),
        unknown_client_projects=frozenset(unknown_ids),
    )


def _valid_id(value: Any) -> bool:
    return isinstance(value, str) and len(value) <= 128 and _ID.fullmatch(value) is not None
