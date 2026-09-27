"""Local-only CAT-005B project catalog service."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from . import config
from .dashboard_local_access import LocalPolicyError, load_local_catalog_scope
from .dashboard_read_model import (
    CatalogProvenance,
    CatalogReadModelError,
    CatalogReadState,
    ProjectCatalogReadModel,
    CatalogScopeGrant,
    build_project_catalog_read_model,
)
from .dashboard_registry import ClientClassification, ProjectCatalogEntry, parse_project_registry


class LocalCatalogError(ValueError):
    """Raised when a local catalog source cannot satisfy CAT-005B."""


class LocalCatalogService:
    """Read an explicitly allowlisted local project catalog without discovery."""

    def __init__(
        self,
        work_root: Path,
        access_path: Path,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        if not isinstance(work_root, Path) or not isinstance(access_path, Path):
            raise LocalCatalogError("work_root and access_path must be pathlib.Path values")
        self._work_root = work_root
        self._access_path = access_path
        self._now = now or (lambda: datetime.now(timezone.utc))

    def read_catalog(
        self,
        requested_project_id: str | None = None,
        requested_client_id: str | None = None,
    ) -> ProjectCatalogReadModel:
        """Load only policy-granted registry files and return the scoped DTO."""
        try:
            scope = load_local_catalog_scope(self._access_path)
        except LocalPolicyError as exc:
            raise LocalCatalogError("local catalog policy is unavailable") from exc

        project_ids = {project_id for project_id, _ in scope.project_client_grants}
        project_ids.update(scope.unknown_client_projects)
        if not project_ids:
            return self._build((), scope, requested_project_id, requested_client_id)

        expected = _policy_entries(scope)
        entries = tuple(
            self._load_allowlisted_entry(project_id, expected[project_id])
            for project_id in sorted(project_ids)
        )
        return self._build(entries, scope, requested_project_id, requested_client_id)

    def _load_allowlisted_entry(
        self,
        project_id: str,
        expected: tuple[str | None, ClientClassification],
    ) -> ProjectCatalogEntry:
        projects_dir = self._work_root / "projects"
        try:
            directory_stat = os.lstat(projects_dir)
        except OSError as exc:
            raise LocalCatalogError("local catalog source is unreadable") from exc
        if stat.S_ISLNK(directory_stat.st_mode) or not stat.S_ISDIR(directory_stat.st_mode):
            raise LocalCatalogError("local catalog source is unreadable")

        candidate = projects_dir / f"{project_id}.yaml"
        try:
            candidate_stat = os.lstat(candidate)
        except OSError as exc:
            raise LocalCatalogError("local catalog source is unreadable") from exc
        if stat.S_ISLNK(candidate_stat.st_mode) or not stat.S_ISREG(candidate_stat.st_mode):
            raise LocalCatalogError("local catalog source is unreadable")
        try:
            registry = config.load_yaml(candidate)
            entry = parse_project_registry(registry)
        except Exception as exc:
            raise LocalCatalogError("local catalog source is unreadable") from exc
        if entry.project_id != project_id:
            raise LocalCatalogError("local catalog source does not match policy")
        if (entry.client_id, entry.client_classification) != expected:
            raise LocalCatalogError("local catalog source does not match policy")
        return entry

    def _build(
        self,
        entries: tuple[ProjectCatalogEntry, ...],
        scope: CatalogScopeGrant,
        requested_project_id: str | None,
        requested_client_id: str | None,
    ) -> ProjectCatalogReadModel:
        try:
            captured_at = self._now()
            if not isinstance(captured_at, datetime) or captured_at.tzinfo is None or captured_at.utcoffset() is None:
                raise LocalCatalogError("catalog timestamp must be timezone-aware")
            captured_at = captured_at.astimezone(timezone.utc)
            source_digest = hashlib.sha256(
                json.dumps(
                    [entry.to_display_dict() for entry in entries],
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=True,
                ).encode("utf-8")
            ).hexdigest()
            provenance = CatalogProvenance("local-catalog", source_digest, captured_at)
            return build_project_catalog_read_model(
                entries,
                provenance,
                scope,
                requested_project_id=requested_project_id,
                requested_client_id=requested_client_id,
            )
        except (CatalogReadModelError, TypeError, ValueError) as exc:
            if isinstance(exc, LocalCatalogError):
                raise
            raise LocalCatalogError("local catalog request is invalid") from exc


def _policy_entries(scope: CatalogScopeGrant) -> dict[str, tuple[str | None, ClientClassification]]:
    expected: dict[str, tuple[str | None, ClientClassification]] = {
        project_id: (
            client_id,
            ClientClassification.INTERNAL if client_id == "internal" else ClientClassification.KNOWN,
        )
        for project_id, client_id in scope.project_client_grants
    }
    expected.update(
        {
            project_id: (None, ClientClassification.UNKNOWN)
            for project_id in scope.unknown_client_projects
        }
    )
    return expected
