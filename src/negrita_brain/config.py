"""Canonical project and policy configuration loading."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import ConfigurationError


NEGRITAOS_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ProjectContext:
    """Resolved project adapter, registry, catalog, and policy."""

    work_root: Path
    negritaos_root: Path
    adapter_path: Path
    registry_path: Path
    adapter: dict[str, Any]
    project: dict[str, Any]
    catalog: dict[str, Any]
    policy: dict[str, Any]

    @property
    def project_id(self) -> str:
        """Return the canonical project identifier."""
        return str(self.project["id"])


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping with PyYAML and a Ruby Psych fallback."""
    try:
        import yaml  # type: ignore[import-not-found]

        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (ImportError, ModuleNotFoundError):
        ruby = (
            "require 'yaml'; require 'json'; "
            "puts JSON.generate(YAML.load_file(ARGV.fetch(0)))"
        )
        try:
            output = subprocess.check_output(
                ["ruby", "-e", ruby, str(path)], text=True
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            raise ConfigurationError(f"Cannot parse YAML {path}: {exc}") from exc
        value = json.loads(output)
    if not isinstance(value, dict):
        raise ConfigurationError(f"Expected a YAML mapping in {path}")
    return value


def _resolve_reference(raw: str, base: Path) -> Path:
    """Resolve an absolute, home-relative, or base-relative file reference."""
    candidate = Path(raw).expanduser()
    return candidate.resolve() if candidate.is_absolute() else (base / candidate).resolve()


def load_project(
    work_root: Path,
    negritaos_root: Path = NEGRITAOS_ROOT,
) -> ProjectContext:
    """Resolve one workspace through its adapter and canonical registry."""
    root = work_root.expanduser().resolve()
    canonical = negritaos_root.expanduser().resolve()
    adapter_path = root / ".codex" / "project.yaml"
    if not adapter_path.is_file():
        raise ConfigurationError(f"Missing NegritaOS adapter: {adapter_path}")
    adapter = load_yaml(adapter_path)
    project_id = adapter.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        raise ConfigurationError(f"project_id is missing in {adapter_path}")
    registry_raw = adapter.get("negrita_registry")
    if isinstance(registry_raw, str) and registry_raw.strip():
        registry_path = _resolve_reference(registry_raw, root)
    else:
        registry_path = canonical / "projects" / f"{project_id}.yaml"
    if not registry_path.is_file():
        raise ConfigurationError(f"Missing project registry: {registry_path}")
    registry = load_yaml(registry_path)
    project = registry.get("project")
    if not isinstance(project, dict) or project.get("id") != project_id:
        raise ConfigurationError(
            f"Registry project id does not match adapter {project_id!r}: {registry_path}"
        )
    catalog = load_yaml(canonical / "skills" / "catalog.yaml")
    policy = load_yaml(canonical / "core" / "orchestration" / "negrita_brain_policy.yaml")
    return ProjectContext(
        work_root=root,
        negritaos_root=canonical,
        adapter_path=adapter_path,
        registry_path=registry_path,
        adapter=adapter,
        project=project,
        catalog=catalog,
        policy=policy,
    )


def project_memory_home(
    context: ProjectContext,
    memory_base: Path | None = None,
) -> Path:
    """Return the canonical memory home for a resolved project."""
    if memory_base is not None:
        return memory_base.expanduser().resolve() / context.project_id
    raw = context.project.get("memory_home")
    if isinstance(raw, str) and raw.strip():
        return Path(raw).expanduser().resolve()
    return Path.home() / ".negritaos" / "memory" / "projects" / context.project_id


def adapter_memory_home(context: ProjectContext) -> Path | None:
    """Return the optional adapter mirror without making it authoritative."""
    raw = context.adapter.get("memory_home")
    if not isinstance(raw, str) or not raw.strip():
        return None
    return Path(raw).expanduser().resolve()


def workspace_kind(context: ProjectContext) -> str:
    """Classify a workspace for enforcement without reading evidence files."""
    root_text = str(context.work_root)
    if "/Library/CloudStorage/" in root_text:
        return "evidence"
    return "code" if (context.work_root / ".git").exists() else "workspace"
