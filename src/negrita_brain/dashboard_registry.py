"""Read-only project catalog adapter; callers must authorize its display scope."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
import re
from typing import Any, Mapping, Sequence

from .config import load_yaml
from .dashboard_contracts import ClientId, ProjectId, ProjectRef, UNKNOWN


STABLE_ID = re.compile(r"^[a-z][a-z0-9_-]*$")


class RegistryAdapterError(ValueError):
    """Raised when a registry does not satisfy the dashboard adapter contract."""


class ClientClassification(str, Enum):
    """Explicit client classification exposed by the catalog."""

    KNOWN = "known"
    UNKNOWN = "unknown"
    INTERNAL = "internal"


@dataclass(frozen=True, slots=True)
class ProjectCatalogEntry:
    """Minimal project DTO derived from one project registry mapping."""

    project_id: str
    name: str
    client_id: str | None
    client_classification: ClientClassification

    def to_display_dict(self) -> dict[str, str | None]:
        """Return allowlisted fields after the caller enforces project access."""
        value = asdict(self)
        value["client_classification"] = self.client_classification.value
        return value


def parse_project_registry(registry: Mapping[str, Any]) -> ProjectCatalogEntry:
    """Map one registry document to a safe project catalog entry.

    Only ``project.id``, ``project.name``, and ``project.metadata.client_id``
    are allowlisted. Client identity is never inferred from names, paths,
    repository metadata, organization fields, or the current user identity.
    """
    project = registry.get("project")
    if not isinstance(project, Mapping):
        raise RegistryAdapterError("Registry must contain a project mapping")

    project_id = _required_text(project, "id", "project.id")
    if not STABLE_ID.fullmatch(project_id):
        raise RegistryAdapterError("project.id must be a stable lowercase identifier")
    name = _required_text(project, "name", "project.name")
    metadata = project.get("metadata", {})
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, Mapping):
        raise RegistryAdapterError("project.metadata must be a mapping")

    client_id = metadata.get("client_id")
    if client_id is not None:
        client_id = _validate_client_id(client_id)

    classification = _classify_client(client_id)
    return ProjectCatalogEntry(
        project_id=project_id,
        name=name,
        client_id=client_id,
        client_classification=classification,
    )


def parse_project_registries(
    registries: Sequence[Mapping[str, Any]],
) -> tuple[ProjectCatalogEntry, ...]:
    """Map registry mappings deterministically and reject duplicate project IDs."""
    entries = tuple(parse_project_registry(registry) for registry in registries)
    seen: set[str] = set()
    for entry in entries:
        if entry.project_id in seen:
            raise RegistryAdapterError(f"Duplicate project id: {entry.project_id}")
        seen.add(entry.project_id)
    return tuple(sorted(entries, key=lambda entry: entry.project_id))


def to_project_ref(entry: ProjectCatalogEntry) -> ProjectRef:
    """Map a catalog entry to domain scope without inventing a missing client."""
    client_id = ClientId(entry.client_id) if entry.client_id is not None else UNKNOWN
    return ProjectRef(project_id=ProjectId(entry.project_id), client_id=client_id)


def load_project_catalog(paths: Sequence[Path]) -> tuple[ProjectCatalogEntry, ...]:
    """Load YAML registries and return their public project catalog."""
    registries = tuple(load_yaml(path) for path in paths)
    return parse_project_registries(registries)


def _required_text(value: Mapping[str, Any], key: str, label: str) -> str:
    candidate = value.get(key)
    if not isinstance(candidate, str) or not candidate.strip():
        raise RegistryAdapterError(f"{label} must be a non-empty string")
    return candidate.strip()


def _validate_client_id(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RegistryAdapterError("project.metadata.client_id must be a non-empty string")
    client_id = value.strip()
    if client_id.casefold() == "unknown":
        raise RegistryAdapterError(
            "Use an omitted client_id for unknown client classification"
        )
    if "/" in client_id or "\\" in client_id:
        raise RegistryAdapterError("Client id must not contain path separators")
    if not STABLE_ID.fullmatch(client_id):
        raise RegistryAdapterError("Client id must be a stable lowercase identifier")
    return client_id


def _classify_client(client_id: str | None) -> ClientClassification:
    if client_id is None:
        return ClientClassification.UNKNOWN
    if client_id.casefold() == "internal":
        return ClientClassification.INTERNAL
    return ClientClassification.KNOWN
