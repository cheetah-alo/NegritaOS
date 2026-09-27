"""Pure, fail-closed CAT-005 project catalog read model.

This module consumes already validated registry entries and a trusted caller
scope grant.  The grant expresses visibility; it is not authentication and
does not establish caller identity.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Iterable

from .dashboard_registry import ClientClassification, ProjectCatalogEntry


_ID = re.compile(r"^[a-z][a-z0-9_-]*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class CatalogReadModelError(ValueError):
    """Raised when snapshot metadata, entries, or scope grants are invalid."""


class CatalogReadState(str, Enum):
    """State of the authorized catalog result, independent of source health."""

    READY = "READY"
    EMPTY = "EMPTY"


@dataclass(frozen=True, slots=True)
class CatalogProvenance:
    """Trusted input provenance; its global digest is never returned to viewers."""

    snapshot_id: str
    sha256: str
    captured_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot_id, str) or not self.snapshot_id.strip():
            raise CatalogReadModelError("snapshot_id must be a non-empty opaque string")
        if "/" in self.snapshot_id or "\\" in self.snapshot_id:
            raise CatalogReadModelError("snapshot_id must not be a path")
        if not isinstance(self.sha256, str) or _SHA256.fullmatch(self.sha256) is None:
            raise CatalogReadModelError("sha256 must be a 64-character lowercase digest")
        if not isinstance(self.captured_at, datetime) or self.captured_at.tzinfo is None:
            raise CatalogReadModelError("captured_at must be timezone-aware")
        if self.captured_at.utcoffset() is None:
            raise CatalogReadModelError("captured_at must have a resolvable timezone offset")


@dataclass(frozen=True, slots=True)
class CatalogScopeGrant:
    """Trusted visibility scope, not an authentication or identity check.

    Known and internal projects require an explicit ``(project_id, client_id)``
    pair.  Unknown-client projects require both an explicit project grant and
    an explicit entry in ``unknown_client_projects``.
    """

    project_client_grants: frozenset[tuple[str, str]] = frozenset()
    project_grants: frozenset[str] = frozenset()
    unknown_client_projects: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        pairs = frozenset(self.project_client_grants)
        projects = frozenset(self.project_grants)
        unknown = frozenset(self.unknown_client_projects)
        if any(not isinstance(project_id, str) or not _ID.fullmatch(project_id) for project_id in projects):
            raise CatalogReadModelError("project_grants contain malformed IDs")
        for pair in pairs:
            if (
                not isinstance(pair, tuple)
                or len(pair) != 2
                or not isinstance(pair[0], str)
                or not _ID.fullmatch(pair[0])
                or not isinstance(pair[1], str)
                or not _ID.fullmatch(pair[1])
            ):
                raise CatalogReadModelError("project_client_grants contain malformed IDs")
        if any(not isinstance(project_id, str) or not _ID.fullmatch(project_id) for project_id in unknown):
            raise CatalogReadModelError("unknown_client_projects contain malformed IDs")
        object.__setattr__(self, "project_client_grants", pairs)
        object.__setattr__(self, "project_grants", projects)
        object.__setattr__(self, "unknown_client_projects", unknown)


@dataclass(frozen=True, slots=True)
class ProjectCatalogDTO:
    """Allowlisted project fields safe for an authorized catalog response."""

    project_id: str
    name: str
    client_id: str | None
    client_classification: ClientClassification


@dataclass(frozen=True, slots=True)
class CatalogViewProvenance:
    """A digest derived only from fields visible in one authorized view."""

    snapshot_id: str
    view_sha256: str


@dataclass(frozen=True, slots=True)
class ProjectCatalogReadModel:
    """Immutable scoped catalog response with explicit READY/EMPTY state."""

    state: CatalogReadState
    projects: tuple[ProjectCatalogDTO, ...]
    provenance: CatalogViewProvenance

    def to_dict(self) -> dict[str, object]:
        """Serialize only the DTO contract and caller-supplied provenance."""
        return {
            "state": self.state.value,
            "projects": [_project_to_dict(project) for project in self.projects],
            "provenance": {
                "snapshot_id": self.provenance.snapshot_id,
                "view_sha256": self.provenance.view_sha256,
            },
        }


def build_project_catalog_read_model(
    entries: Iterable[ProjectCatalogEntry],
    provenance: CatalogProvenance,
    scope: CatalogScopeGrant,
    *,
    requested_project_id: str | None = None,
    requested_client_id: str | None = None,
) -> ProjectCatalogReadModel:
    """Build a deterministic catalog after authorization and then filtering.

    Authorization is evaluated against the complete validated snapshot before
    either optional request filter is applied.  Consequently, counts and names
    from projects outside the grant can never influence the response.
    """
    if not isinstance(provenance, CatalogProvenance) or not isinstance(scope, CatalogScopeGrant):
        raise CatalogReadModelError("provenance and scope must use CAT-005 types")
    validated = _validate_entries(tuple(entries))
    visible = tuple(entry for entry in validated if _is_authorized(entry, scope))
    if requested_project_id is not None and not _valid_optional_id(requested_project_id):
        raise CatalogReadModelError("requested_project_id must be a stable identifier")
    if requested_client_id is not None and not _valid_optional_id(requested_client_id):
        raise CatalogReadModelError("requested_client_id must be a stable identifier")
    filtered = tuple(
        entry
        for entry in visible
        if (requested_project_id is None or entry.project_id == requested_project_id)
        and (requested_client_id is None or entry.client_id == requested_client_id)
    )
    projects = tuple(
        ProjectCatalogDTO(
            project_id=entry.project_id,
            name=entry.name,
            client_id=entry.client_id,
            client_classification=entry.client_classification,
        )
        for entry in filtered
    )
    state = CatalogReadState.READY if projects else CatalogReadState.EMPTY
    return ProjectCatalogReadModel(
        state=state, projects=projects, provenance=_scoped_provenance(projects)
    )


def _project_to_dict(project: ProjectCatalogDTO) -> dict[str, str | None]:
    return {
        "project_id": project.project_id,
        "name": project.name,
        "client_id": project.client_id,
        "client_classification": project.client_classification.value,
    }


def _scoped_provenance(projects: tuple[ProjectCatalogDTO, ...]) -> CatalogViewProvenance:
    payload = [_project_to_dict(project) for project in projects]
    digest = hashlib.sha256(
        json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return CatalogViewProvenance(
        snapshot_id=f"view-{digest[:20]}", view_sha256=digest
    )


def _validate_entries(entries: tuple[ProjectCatalogEntry, ...]) -> tuple[ProjectCatalogEntry, ...]:
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, ProjectCatalogEntry):
            raise CatalogReadModelError("catalog entries must be ProjectCatalogEntry values")
        if not isinstance(entry.project_id, str) or not _ID.fullmatch(entry.project_id):
            raise CatalogReadModelError("project entry has a malformed project_id")
        if not isinstance(entry.name, str) or not entry.name.strip():
            raise CatalogReadModelError("project entry has a malformed name")
        if not isinstance(entry.client_classification, ClientClassification):
            raise CatalogReadModelError("project entry has an invalid classification")
        if entry.project_id in seen:
            raise CatalogReadModelError(f"Duplicate project id: {entry.project_id}")
        seen.add(entry.project_id)
        if entry.client_classification is ClientClassification.UNKNOWN and entry.client_id is not None:
            raise CatalogReadModelError("unknown classification requires no client_id")
        if entry.client_classification is ClientClassification.KNOWN and (
            not isinstance(entry.client_id, str) or not _ID.fullmatch(entry.client_id)
            or entry.client_id == "internal"
        ):
            raise CatalogReadModelError("known classification requires a non-internal client_id")
        if entry.client_classification is ClientClassification.INTERNAL and entry.client_id != "internal":
            raise CatalogReadModelError("internal classification requires client_id internal")
    return tuple(sorted(entries, key=lambda entry: entry.project_id))


def _is_authorized(entry: ProjectCatalogEntry, scope: CatalogScopeGrant) -> bool:
    if entry.client_classification is ClientClassification.UNKNOWN:
        return entry.project_id in scope.project_grants and entry.project_id in scope.unknown_client_projects
    return (entry.project_id, entry.client_id) in scope.project_client_grants


def _valid_optional_id(value: str) -> bool:
    return isinstance(value, str) and bool(_ID.fullmatch(value))
