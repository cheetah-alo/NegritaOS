"""Validate NegritaOS / .codex / .claude alignment.

Meta-repo checks (NegritaOS itself):

1. `.claude` is either a symlink to `.codex` or its directory tree matches
   `.codex` byte-for-byte (sync fallback).
2. `.codex/project.yaml` exists and resolves to `projects/<project_id>.yaml`.
3. `.codex/local-overrides.md` exists.
4. `.codex/instruction-manifest.yaml` lists the `negritaos-router` rule.
5. `rules/global/negritaos_router_rule.md` exists (canonical router rule).
6. `.codex/rules/negritaos-router.md` adapter stub exists.
7. `.codex/skills/negritaos-mode-router/SKILL.md` exists.
8. `.codex/memory/sessions/` does not contain a moneyflowlist-style orphan
   referencing `frontend/src/` (a heuristic from the Jun-1 cleanup).
9. `.codex/agents/<mode>.md` contains Claude-native aliases for every
   NegritaOS router mode.
10. Project-declared `.codex/agents/*.toml` custom agents resolve canonically.
11. The active project's canonical memory home exists under
   `~/.negritaos/memory/projects/<project_id>/`.

Sibling-repo checks (when --siblings is on, the default):

For every registry under `projects/*.yaml` that declares
`local_paths.primary` and is NOT the NegritaOS meta-repo itself, verify:

S1. The primary path exists on disk.
S2. `.codex/project.yaml` exists and `project_id` matches the registry filename.
S3. `negrita_registry` points back to the NegritaOS canonical registry file.
S4. `.claude` is a symlink to `.codex` (or tree-matches).
S5. `.codex/instruction-manifest.yaml` is reachable and mentions `negritaos-router`.
S6. `.codex/rules/negritaos-router.md` reachable; symlinks (if any) dereference
    into the NegritaOS canonical `.codex/rules/` tree.
S7. `.codex/skills/negritaos-mode-router/SKILL.md` reachable.
S8. `.codex/commands/` reachable (file or symlink dir).
S9. Registry `project.memory_home` exists; an adapter value is only a matching mirror.
S10. The canonical project -> registry -> agent/profile asset resolution passes.
S11. `.codex/agents/<mode>.md` exposes NegritaOS modes as Claude-native aliases.
S12. Project-declared Codex custom agent TOMLs resolve to canonical files.

Exit codes:
    0 — all checks pass.
    1 — at least one check failed (details printed to stdout).

CLI:
    python scripts/validate_alignment.py                # meta + siblings
    python scripts/validate_alignment.py --only-meta    # legacy behaviour
    python scripts/validate_alignment.py --sibling PATH # one sibling only
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable, Iterable

try:
    from .validate_config_resolution import validate_resolution
    from .validate_claude_agent_aliases import validate_repo as validate_claude_aliases
    from .validate_codex_custom_agents import (
        validate_registry_declarations as validate_codex_agent_registry,
        validate_repo as validate_codex_agents,
    )
    from .validate_browser_profile_routing import validate_all as validate_browser_routing
    from .validate_model_escalation_policy import validate_all as validate_model_policy
except ImportError:
    from validate_config_resolution import validate_resolution
    from validate_claude_agent_aliases import validate_repo as validate_claude_aliases
    from validate_codex_custom_agents import (
        validate_registry_declarations as validate_codex_agent_registry,
        validate_repo as validate_codex_agents,
    )
    from validate_browser_profile_routing import validate_all as validate_browser_routing
    from validate_model_escalation_policy import validate_all as validate_model_policy

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from negrita_brain.config import (  # noqa: E402
    adapter_memory_home,
    load_project,
    project_memory_home,
)
from negrita_brain.codex_config import codex_config_status  # noqa: E402
from negrita_brain.memory import index_is_runtime_owned  # noqa: E402
from negrita_brain.profiles import resolve_project_profiles  # noqa: E402
from negrita_brain.commit_identity import (  # noqa: E402
    load_commit_identity_policies,
    validate_project_policy_references,
)
HOME = Path.home()
PROJECTS_DIR = REPO_ROOT / "projects"
META_PROJECT_ID = "negritaos"
CANONICAL_RULES_DIR = (REPO_ROOT / ".codex" / "rules").resolve()
MANAGED_START = "<!-- NEGRITA_BRAIN:START -->"
BRAIN_HOOK_EVENTS = {
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "Stop",
    "SessionEnd",
}


def _ok(msg: str) -> tuple[bool, str]:
    return True, f"[OK]   {msg}"


def _fail(msg: str) -> tuple[bool, str]:
    return False, f"[FAIL] {msg}"


def _warn(msg: str) -> tuple[bool, str]:
    return True, f"[WARN] {msg}"


def check_claude_alignment() -> tuple[bool, str]:
    claude = REPO_ROOT / ".claude"
    codex = REPO_ROOT / ".codex"
    if not claude.exists():
        return _fail(".claude/ is missing")
    if claude.is_symlink():
        target = claude.resolve()
        if target == codex.resolve():
            return _ok(".claude -> .codex symlink in place")
        return _fail(f".claude is a symlink but points to {target}, not .codex")
    diff = subprocess.run(
        ["diff", "-rq", str(claude), str(codex)],
        capture_output=True,
        text=True,
        check=False,
    )
    if diff.returncode == 0:
        return _ok(".claude/ and .codex/ trees match (sync fallback)")
    differing = diff.stdout.strip().splitlines()
    head = "; ".join(differing[:3])
    return _fail(f".claude/ drifts from .codex/ ({len(differing)} diffs): {head}")


def check_project_yaml() -> tuple[bool, str]:
    project_yaml = REPO_ROOT / ".codex" / "project.yaml"
    if not project_yaml.exists():
        return _fail(".codex/project.yaml missing")
    text = project_yaml.read_text(encoding="utf-8")
    match = re.search(r"project_id:\s*(\S+)", text)
    if match is None:
        return _fail(".codex/project.yaml does not declare project_id")
    project_id = match.group(1).strip()
    registry = REPO_ROOT / "projects" / f"{project_id}.yaml"
    if not registry.exists():
        return _fail(f".codex/project.yaml -> missing registry {registry}")
    return _ok(f".codex/project.yaml -> projects/{project_id}.yaml")


def check_config_resolution() -> tuple[bool, str]:
    """Ensure the active project can resolve all declared agent assets."""
    errors, warnings, project_id = validate_resolution(REPO_ROOT)
    if errors:
        first_error = errors[0]
        return _fail(f"config resolution for {project_id}: {first_error}")
    suffix = f" ({len(warnings)} warning(s))" if warnings else ""
    return _ok(f"config resolution complete for {project_id}{suffix}")


def check_local_overrides() -> tuple[bool, str]:
    target = REPO_ROOT / ".codex" / "local-overrides.md"
    if target.exists():
        return _ok(".codex/local-overrides.md present")
    return _fail(".codex/local-overrides.md missing")


def check_manifest_router() -> tuple[bool, str]:
    manifest = REPO_ROOT / ".codex" / "instruction-manifest.yaml"
    if not manifest.exists():
        return _fail(".codex/instruction-manifest.yaml missing")
    if "negritaos-router" in manifest.read_text(encoding="utf-8"):
        return _ok("negritaos-router registered in instruction-manifest.yaml")
    return _fail("negritaos-router not registered in instruction-manifest.yaml")


def check_canonical_router_rule() -> tuple[bool, str]:
    target = REPO_ROOT / "rules" / "global" / "negritaos_router_rule.md"
    if target.exists():
        return _ok("rules/global/negritaos_router_rule.md present")
    return _fail("rules/global/negritaos_router_rule.md missing")


def check_external_app_financial_control() -> tuple[bool, str]:
    """Ensure the mandatory no-spend-without-approval rule is globally loaded."""
    required_markers = {
        REPO_ROOT / "rules" / "global" / "global_rules.yaml": (
            "external_app_financial_control:",
            "BLOCKED_FINANCIAL_AUTHORIZATION",
            "explicit_user_authorization_required: true",
        ),
        REPO_ROOT / "core" / "orchestration" / "negrita_brain_policy.yaml": (
            "external_app_financial_control:",
            "default_decision: BLOCK",
            "authorization_scope: one_specific_operation",
        ),
        REPO_ROOT / "rules" / "global" / "negritaos_router_rule.md": (
            "External App Financial Authority",
            "BLOCKED_FINANCIAL_AUTHORIZATION",
            "Authorization is never inferred",
        ),
        REPO_ROOT / ".codex" / "skills" / "negritaos-mode-router" / "SKILL.md": (
            "External app financial gate",
            "BLOCKED_FINANCIAL_AUTHORIZATION",
            "Previous approval does not carry forward",
        ),
        REPO_ROOT / "rules" / "writing" / "writing_rules.yaml": (
            "preserve_governance_states:",
            "BLOCKED_FINANCIAL_AUTHORIZATION",
        ),
    }
    for path, markers in required_markers.items():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            return _fail(f"external app financial control unreadable: {path}: {exc}")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            return _fail(
                f"external app financial control incomplete in {path}: {missing[0]}"
            )
    return _ok("external app financial control is globally enforced")


def check_browser_profile_routing() -> tuple[bool, str]:
    """Ensure every project has a deterministic, fail-closed browser context."""
    try:
        errors, checked = validate_browser_routing(REPO_ROOT)
    except Exception as exc:
        return _fail(f"browser profile routing could not be validated: {exc}")
    if errors:
        return _fail(f"browser profile routing: {errors[0]}")
    return _ok(f"browser profile routing covers {checked} projects")


def check_browser_rule_registration() -> tuple[bool, str]:
    """Ensure the browser rule is registered and exposed by the meta adapter."""
    manifest = REPO_ROOT / ".codex" / "instruction-manifest.yaml"
    stub = REPO_ROOT / ".codex" / "rules" / "browser-profile-routing.md"
    canonical = REPO_ROOT / "rules" / "global" / "browser_profile_routing_rule.md"
    if not manifest.is_file() or "browser-profile-routing" not in manifest.read_text(
        encoding="utf-8", errors="ignore"
    ):
        return _fail("browser-profile-routing is absent from instruction-manifest.yaml")
    if not stub.is_file() or not canonical.is_file():
        return _fail("browser profile routing rule or adapter stub is missing")
    return _ok("browser profile routing rule is registered and reachable")


def check_model_escalation_policy() -> tuple[bool, str]:
    """Ensure model routing is global, valid, and backed by canonical agents."""
    try:
        errors, count = validate_model_policy(REPO_ROOT)
    except Exception as exc:
        return _fail(f"model escalation policy could not be validated: {exc}")
    if errors:
        return _fail(f"model escalation policy: {errors[0]}")
    manifest = REPO_ROOT / ".codex" / "instruction-manifest.yaml"
    stub = REPO_ROOT / ".codex" / "rules" / "model-escalation.md"
    canonical = REPO_ROOT / "rules" / "global" / "model_escalation_rule.md"
    if not manifest.is_file() or "model-escalation" not in manifest.read_text(
        encoding="utf-8", errors="ignore"
    ):
        return _fail("model-escalation is absent from instruction-manifest.yaml")
    if not stub.is_file() or not canonical.is_file():
        return _fail("model escalation rule or adapter stub is missing")
    return _ok(f"model escalation routes {count} global Codex agents")


def check_commit_identity_policies() -> tuple[bool, str]:
    """Ensure scoped corporate identity policies and project opt-ins agree."""
    try:
        document = load_commit_identity_policies(REPO_ROOT)
        errors = validate_project_policy_references(REPO_ROOT, document)
    except Exception as exc:
        return _fail(f"commit identity policies could not be validated: {exc}")
    if errors:
        return _fail(f"commit identity policies: {errors[0]}")
    from negrita_brain.git_identity_install import audit, registered_checkouts
    drift = []
    try:
        for repo in registered_checkouts(REPO_ROOT):
            report = audit(repo, REPO_ROOT)
            if report["status"] != "PASS":
                drift.append(str(repo))
    except (OSError, ValueError, RuntimeError) as exc:
        return _warn(f"commit identity installation audit unavailable: {exc}")
    if drift:
        return _warn("commit identity installation or CI drift: " + ", ".join(drift))
    policies = document.get("policies", {})
    scoped = sum(
        len(policy.get("project_scope", []))
        for policy in policies.values()
        if isinstance(policy, dict)
    )
    return _ok(
        f"commit identity policies cover {scoped} scoped projects"
    )


def check_adapter_router_stub() -> tuple[bool, str]:
    target = REPO_ROOT / ".codex" / "rules" / "negritaos-router.md"
    if target.exists():
        return _ok(".codex/rules/negritaos-router.md adapter stub present")
    return _fail(".codex/rules/negritaos-router.md adapter stub missing")


def check_router_skill() -> tuple[bool, str]:
    target = REPO_ROOT / ".codex" / "skills" / "negritaos-mode-router" / "SKILL.md"
    if target.exists():
        return _ok(".codex/skills/negritaos-mode-router/SKILL.md present")
    return _fail(".codex/skills/negritaos-mode-router/SKILL.md missing")


def check_claude_agent_aliases() -> tuple[bool, str]:
    """Ensure NegritaOS router modes are invocable as Claude native agents."""
    errors = validate_claude_aliases(REPO_ROOT, REPO_ROOT)
    if errors:
        return _fail(f"Claude agent aliases invalid: {errors[0]}")
    return _ok(".codex/agents exposes every router mode as a Claude alias")


def check_codex_custom_agents() -> tuple[bool, str]:
    """Ensure project-scoped Codex TOML agents resolve canonically."""
    errors = validate_codex_agent_registry(REPO_ROOT)
    if errors:
        return _fail(f"Codex custom agents invalid: {errors[0]}")
    return _ok("project-declared Codex custom agents resolve canonically")


def check_no_orphan_sessions() -> tuple[bool, str]:
    sessions = REPO_ROOT / ".codex" / "memory" / "sessions"
    if not sessions.exists():
        return _ok(".codex/memory/sessions/ absent (acceptable for meta-repo)")
    suspicious: list[str] = []
    for path in sessions.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "frontend/src/" in text or "moneyflowlist" in text.lower():
            suspicious.append(path.name)
    if suspicious:
        joined = ", ".join(suspicious)
        return _fail(f"orphan sessions in .codex/memory/sessions/: {joined}")
    return _ok(".codex/memory/sessions/ contains no orphan sibling-repo sessions")


def check_memory_home() -> tuple[bool, str]:
    try:
        context = load_project(REPO_ROOT, REPO_ROOT)
    except Exception as exc:
        return _fail(f"cannot resolve registry memory_home: {exc}")
    canonical = project_memory_home(context)
    mirror = adapter_memory_home(context)
    if mirror is not None and mirror != canonical:
        return _fail(f"adapter memory_home {mirror} != registry {canonical}")
    if canonical.exists():
        return _ok(f"registry memory_home present: {canonical}")
    return _fail(f"registry memory_home missing on disk: {canonical}")


def check_memory_policy() -> tuple[bool, str]:
    """Verify Memory v2 ownership is explicit in runtime policy."""
    policy = REPO_ROOT / "core" / "orchestration" / "negrita_brain_policy.yaml"
    text = policy.read_text(encoding="utf-8") if policy.is_file() else ""
    required = (
        "schema_version: 2",
        "owner: negrita_brain",
        "persistence: relevant",
        "active_pointer_strategy: provider_session",
    )
    missing = [value for value in required if value not in text]
    if missing:
        return _fail(f"Memory v2 policy fields missing: {', '.join(missing)}")
    return _ok("Memory v2 policy ownership and pointer strategy declared")


def check_codex_memory_permission() -> tuple[bool, str]:
    """Detect whether new Codex tasks can write canonical project memory."""
    try:
        status = codex_config_status()
    except Exception as exc:
        return _fail(f"cannot validate Codex memory permission: {exc}")
    if status["configured"]:
        return _ok("Codex workspace-write includes canonical memory")
    return _fail(
        "Codex workspace-write excludes canonical memory; run configure codex --apply"
    )


def check_orphan_memory_homes() -> tuple[bool, str]:
    """Report memory homes without deleting or reassigning them."""
    root = HOME / ".negritaos" / "memory" / "projects"
    if not root.is_dir():
        return _warn(f"project memory root is absent: {root}")
    registered = {path.stem for path in PROJECTS_DIR.glob("*.yaml")}
    orphans = sorted(
        path.name for path in root.iterdir() if path.is_dir() and path.name not in registered
    )
    if not orphans:
        return _ok("no orphan project memory homes detected")
    return _warn(f"orphan project memory homes preserved: {', '.join(orphans)}")


CHECKS = (
    check_claude_alignment,
    check_project_yaml,
    check_config_resolution,
    check_local_overrides,
    check_manifest_router,
    check_canonical_router_rule,
    check_external_app_financial_control,
    check_browser_profile_routing,
    check_browser_rule_registration,
    check_model_escalation_policy,
    check_commit_identity_policies,
    check_adapter_router_stub,
    check_router_skill,
    check_claude_agent_aliases,
    check_codex_custom_agents,
    check_no_orphan_sessions,
    check_memory_home,
    check_memory_policy,
    check_codex_memory_permission,
    check_orphan_memory_homes,
)


# ---------------------------------------------------------------------------
# Sibling-repo discovery and checks
# ---------------------------------------------------------------------------


def _scalar(text: str, key: str) -> str | None:
    """Extract the first `key: <scalar>` value from a yaml-ish text.

    Intra-line whitespace only — never crosses newlines, so block-style keys
    like ``primary:\\n  - item`` are correctly treated as having no scalar value.
    """
    pattern = rf"^[ \t]*{re.escape(key)}[ \t]*:[ \t]*(\S[^\n]*?)[ \t]*$"
    match = re.search(pattern, text, re.MULTILINE)
    if match is None:
        return None
    value = match.group(1).strip().strip('"').strip("'")
    if not value or value.startswith(("-", "|", ">", "#")):
        return None
    return value


def _expand(path_str: str) -> Path:
    return Path(path_str.replace("~", str(HOME)))


def discover_siblings() -> list[tuple[str, Path, Path]]:
    """Return (project_id, primary_repo_path, registry_path) for each sibling.

    The NegritaOS meta-repo is excluded. Entries without a resolvable
    `local_paths.primary` are skipped silently (those are pure registry stubs).
    """
    siblings: list[tuple[str, Path, Path]] = []
    for registry in sorted(PROJECTS_DIR.glob("*.yaml")):
        text = registry.read_text(encoding="utf-8")
        project_id = _scalar(text, "id") or registry.stem
        if project_id == META_PROJECT_ID:
            continue
        primary = _scalar(text, "primary")
        if primary is None:
            continue
        siblings.append((project_id, _expand(primary), registry))
    return siblings


def _ok_s(project_id: str, msg: str) -> tuple[bool, str]:
    return True, f"[OK]   [{project_id}] {msg}"


def _fail_s(project_id: str, msg: str) -> tuple[bool, str]:
    return False, f"[FAIL] [{project_id}] {msg}"


def _warn_s(project_id: str, msg: str) -> tuple[bool, str]:
    return True, f"[WARN] [{project_id}] {msg}"


def check_sibling(
    project_id: str, repo: Path, registry: Path
) -> list[tuple[bool, str]]:
    """Run all per-sibling checks; return one tuple per assertion."""
    results: list[tuple[bool, str]] = []

    # S1 — primary path exists
    if not repo.exists():
        results.append(_fail_s(project_id, f"primary path missing: {repo}"))
        return results
    results.append(_ok_s(project_id, f"primary path present: {repo}"))

    codex = repo / ".codex"
    claude = repo / ".claude"
    project_yaml = codex / "project.yaml"

    # S2 — .codex/project.yaml present + project_id matches
    if not project_yaml.exists():
        results.append(_fail_s(project_id, ".codex/project.yaml missing"))
        return results
    try:
        py_text = project_yaml.read_text(encoding="utf-8")
    except OSError as exc:
        results.append(
            _fail_s(project_id, f".codex/project.yaml unreadable: {exc}")
        )
        return results
    declared = _scalar(py_text, "project_id")
    if declared != project_id:
        results.append(
            _fail_s(
                project_id,
                f".codex/project.yaml declares project_id={declared!r}, "
                f"expected {project_id!r}",
            )
        )
    else:
        results.append(_ok_s(project_id, ".codex/project.yaml project_id matches"))

    # S3 — registry pointer is the canonical NegritaOS file
    pointer = _scalar(py_text, "negrita_registry")
    if pointer is None:
        results.append(_fail_s(project_id, "negrita_registry not declared"))
    else:
        if Path(pointer).resolve() == registry.resolve():
            results.append(_ok_s(project_id, "negrita_registry -> canonical"))
        else:
            results.append(
                _fail_s(
                    project_id,
                    f"negrita_registry={pointer} != canonical {registry}",
                )
            )

    # S4 — .claude alignment
    results.append(_check_sibling_claude(project_id, claude, codex))

    # S5 — manifest reachable + mentions router
    manifest = codex / "instruction-manifest.yaml"
    if not manifest.exists():
        results.append(_fail_s(project_id, ".codex/instruction-manifest.yaml missing"))
    elif all(
        marker in manifest.read_text(encoding="utf-8", errors="ignore")
        for marker in ("negritaos-router", "browser-profile-routing", "model-escalation")
    ):
        results.append(
            _ok_s(project_id, "manifest registers router and browser profile rule")
        )
    else:
        results.append(
            _fail_s(
                project_id,
                "manifest does not register router and browser profile rule",
            )
        )

    # S6 — router stub reachable + symlinks (if any) point into canonical rules
    results.extend(_check_sibling_rules(project_id, codex))

    # S7 — router skill reachable
    skill = codex / "skills" / "negritaos-mode-router" / "SKILL.md"
    if skill.exists():
        results.append(_ok_s(project_id, "router skill reachable"))
    else:
        results.append(_fail_s(project_id, "router skill missing"))

    # S8 — commands dir reachable
    commands = codex / "commands"
    if commands.exists() and commands.is_dir():
        results.append(_ok_s(project_id, ".codex/commands/ reachable"))
    else:
        results.append(_fail_s(project_id, ".codex/commands/ missing"))

    # S9 — registry memory_home is authoritative; adapter value is a mirror only.
    try:
        memory_context = load_project(repo, REPO_ROOT)
        memory_home = project_memory_home(memory_context)
        mirror = adapter_memory_home(memory_context)
        if mirror is not None and mirror != memory_home:
            results.append(
                _fail_s(
                    project_id,
                    f"adapter memory_home {mirror} != registry {memory_home}",
                )
            )
        elif memory_home.exists():
            results.append(
                _ok_s(project_id, f"registry memory_home present: {memory_home}")
            )
        else:
            results.append(
                _fail_s(project_id, f"registry memory_home missing: {memory_home}")
            )
    except Exception as exc:
        results.append(_fail_s(project_id, f"memory_home resolution failed: {exc}"))

    # S10 — full canonical resolution, using the sibling adapter as the entrypoint
    errors, warnings, resolved_id = validate_resolution(
        REPO_ROOT, project_yaml.resolve()
    )
    if errors:
        results.append(
            _fail_s(
                project_id,
                f"canonical config resolution failed for {resolved_id}: {errors[0]}",
            )
        )
    else:
        suffix = f" ({len(warnings)} warning(s))" if warnings else ""
        results.append(_ok_s(project_id, f"canonical config resolution passed{suffix}"))

    # S11 — Claude-native aliases for all NegritaOS router modes
    alias_errors = validate_claude_aliases(repo, REPO_ROOT)
    if alias_errors:
        results.append(
            _fail_s(project_id, f"Claude agent aliases invalid: {alias_errors[0]}")
        )
    else:
        results.append(
            _ok_s(project_id, "Claude agent aliases expose every router mode")
        )

    # S12 — project-scoped Codex custom agent TOMLs.
    codex_agent_errors = validate_codex_agents(repo, REPO_ROOT)
    if codex_agent_errors:
        results.append(
            _fail_s(project_id, f"Codex custom agents invalid: {codex_agent_errors[0]}")
        )
    else:
        results.append(_ok_s(project_id, "Codex custom agents resolve canonically"))

    # S13-S17 — executable Negrita Brain enforcement surfaces.
    results.extend(_check_brain_runtime(project_id, repo))

    return results


def _check_brain_runtime(project_id: str, repo: Path) -> list[tuple[bool, str]]:
    """Check entrypoints, hooks, profile closure, document routing, and memory."""
    results: list[tuple[bool, str]] = []
    agents = repo / "AGENTS.md"
    claude = repo / "CLAUDE.md"
    agents_readable = True
    try:
        agents_text = (
            agents.read_text(encoding="utf-8", errors="ignore")
            if agents.is_file()
            else ""
        )
    except OSError as exc:
        agents_readable = False
        results.append(_fail_s(project_id, f"AGENTS.md unreadable: {exc}"))
        agents_text = ""
    if not agents_readable:
        pass
    elif MANAGED_START in agents_text:
        results.append(_ok_s(project_id, "managed AGENTS.md entrypoint present"))
    else:
        results.append(_fail_s(project_id, "managed AGENTS.md entrypoint missing"))
    if not agents_readable:
        pass
    elif "memory remember|handoff" in agents_text and "--provider codex" in agents_text:
        results.append(_ok_s(project_id, "AGENTS.md routes project-memory writes through Brain"))
    else:
        results.append(
            _fail_s(
                project_id,
                "AGENTS.md still permits or omits Brain-only memory writes",
            )
        )
    if claude.is_file():
        claude_readable = True
        try:
            claude_text = claude.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            claude_readable = False
            results.append(_fail_s(project_id, f"CLAUDE.md unreadable: {exc}"))
            claude_text = ""
        if not claude_readable:
            pass
        elif MANAGED_START in claude_text and "@AGENTS.md" in claude_text:
            results.append(_ok_s(project_id, "CLAUDE.md imports managed AGENTS.md"))
        else:
            results.append(_fail_s(project_id, "CLAUDE.md managed import missing"))
    else:
        results.append(_fail_s(project_id, "CLAUDE.md missing"))
    settings_path = repo / ".codex" / "settings.json"
    settings_readable = True
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        hooks = settings.get("hooks", {}) if isinstance(settings, dict) else {}
        missing_hooks = sorted(BRAIN_HOOK_EVENTS - set(hooks))
    except OSError as exc:
        settings_readable = False
        results.append(_fail_s(project_id, f".codex/settings.json unreadable: {exc}"))
        missing_hooks = []
    except (json.JSONDecodeError, TypeError) as exc:
        settings_readable = False
        results.append(_fail_s(project_id, f".codex/settings.json invalid: {exc}"))
        missing_hooks = []
    if missing_hooks:
        results.append(
            _fail_s(
                project_id,
                f"Negrita Brain hooks missing: {', '.join(missing_hooks)}",
            )
        )
    elif settings_readable:
        results.append(_ok_s(project_id, "all Negrita Brain hooks present"))
    try:
        context = load_project(repo, REPO_ROOT)
        closure = resolve_project_profiles(context.catalog, context.project)
        missing_skills = [
            skill_id
            for skill_id in closure.skills
            if not (repo / ".codex" / "skills" / skill_id / "SKILL.md").is_file()
        ]
        if missing_skills:
            results.append(
                _fail_s(
                    project_id,
                    "profile closure not materialized: "
                    f"{', '.join(missing_skills[:5])}",
                )
            )
        else:
            results.append(
                _ok_s(
                    project_id,
                    f"profile closure materialized ({len(closure.skills)} skills)",
                )
            )
        if "document-control" in closure.skills:
            results.append(
                _ok_s(
                    project_id,
                    "document-control present in resolved profile closure",
                )
            )
        else:
            results.append(
                _fail_s(
                    project_id,
                    "document-control missing from resolved profile closure",
                )
            )
        memory_home = project_memory_home(context)
        required_memory = [
            memory_home / "catalog",
            memory_home / "decisions",
            memory_home / "runtime" / "active",
            memory_home / "runtime" / "sessions",
            memory_home / "sessions",
            memory_home / "tasks",
        ]
        missing_memory = [str(path) for path in required_memory if not path.is_dir()]
        if missing_memory:
            results.append(
                _fail_s(
                    project_id,
                    f"runtime memory structure missing: {', '.join(missing_memory)}",
                )
            )
        else:
            results.append(_ok_s(project_id, "Memory v2 durable and runtime structure present"))
        protocol = repo / ".codex" / "skills" / "local-memory-protocol" / "SKILL.md"
        handoff_command = repo / ".codex" / "commands" / "session-handoff.md"
        protocol_text = (
            protocol.read_text(encoding="utf-8", errors="ignore")
            if protocol.is_file()
            else ""
        )
        handoff_text = (
            handoff_command.read_text(encoding="utf-8", errors="ignore")
            if handoff_command.is_file()
            else ""
        )
        if (
            "Negrita Brain is the only project-memory writer" in protocol_text
            and "memory handoff" in handoff_text
            and "write one at <memory_home>" not in handoff_text
        ):
            results.append(_ok_s(project_id, "no duplicate command or skill memory writer"))
        else:
            results.append(_fail_s(project_id, "duplicate or legacy direct memory writer detected"))
        if index_is_runtime_owned(memory_home / "index.md"):
            results.append(
                _warn_s(
                    project_id,
                    "INDEX_RUNTIME_OWNED preserved until explicit safe rebuild",
                )
            )
        else:
            results.append(_ok_s(project_id, "durable index is not runtime-owned"))
        local_memory = repo / ".codex" / "memory"
        if local_memory.is_dir() and any(local_memory.rglob("*")):
            results.append(
                _warn_s(
                    project_id,
                    f"legacy repo-local memory preserved as non-authoritative: {local_memory}",
                )
            )
    except Exception as exc:
        results.append(_fail_s(project_id, f"Negrita Brain resolution failed: {exc}"))
    return results


def _check_sibling_claude(
    project_id: str, claude: Path, codex: Path
) -> tuple[bool, str]:
    if not claude.exists() and not claude.is_symlink():
        return _fail_s(project_id, ".claude/ missing")
    if claude.is_symlink():
        if claude.resolve() == codex.resolve():
            return _ok_s(project_id, ".claude -> .codex symlink")
        return _fail_s(
            project_id, f".claude symlink points to {claude.resolve()}, not .codex"
        )
    diff = subprocess.run(
        ["diff", "-rq", str(claude), str(codex)],
        capture_output=True,
        text=True,
        check=False,
    )
    if diff.returncode == 0:
        return _ok_s(project_id, ".claude/ tree-matches .codex/")
    differing = diff.stdout.strip().splitlines()
    return _fail_s(
        project_id, f".claude/ drifts from .codex/ ({len(differing)} diffs)"
    )


def _check_sibling_rules(project_id: str, codex: Path) -> list[tuple[bool, str]]:
    out: list[tuple[bool, str]] = []
    rules_dir = codex / "rules"
    if not rules_dir.exists():
        out.append(_fail_s(project_id, ".codex/rules/ missing"))
        return out

    for required_stub in (
        "negritaos-router.md",
        "browser-profile-routing.md",
        "model-escalation.md",
    ):
        stub = rules_dir / required_stub
        if stub.exists():
            out.append(_ok_s(project_id, f"rules/{required_stub} reachable"))
        else:
            out.append(_fail_s(project_id, f"rules/{required_stub} missing"))

    # Any rule file that is a symlink must resolve into NegritaOS canonical
    # .codex/rules/ — otherwise it is drift.
    broken: list[str] = []
    foreign: list[str] = []
    for entry in rules_dir.iterdir():
        if not entry.is_symlink():
            continue
        try:
            target = entry.resolve(strict=True)
        except FileNotFoundError:
            broken.append(entry.name)
            continue
        try:
            target.relative_to(CANONICAL_RULES_DIR)
        except ValueError:
            foreign.append(f"{entry.name} -> {target}")
    if broken:
        out.append(
            _fail_s(project_id, f"broken rule symlinks: {', '.join(broken)}")
        )
    if foreign:
        out.append(
            _fail_s(
                project_id,
                "rule symlinks point outside NegritaOS canonical: "
                + "; ".join(foreign[:3]),
            )
        )
    if not broken and not foreign:
        out.append(
            _ok_s(project_id, "rule symlinks resolve into NegritaOS canonical")
        )
    return out


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _run_meta_checks(checks: Iterable[Callable[[], tuple[bool, str]]]) -> list[
    tuple[bool, str]
]:
    return [check() for check in checks]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--only-meta",
        action="store_true",
        help="Skip sibling-repo checks (legacy behaviour).",
    )
    parser.add_argument(
        "--sibling",
        metavar="PATH",
        help="Validate only the sibling repo at PATH; skip meta + other siblings.",
    )
    return parser.parse_args()


def main() -> int:
    """Run alignment checks for the meta-repo and (by default) all siblings."""
    args = _parse_args()
    results: list[tuple[bool, str]] = []

    if args.sibling:
        repo = Path(args.sibling).expanduser().resolve()
        # Locate the matching registry by primary path.
        match: tuple[str, Path, Path] | None = None
        for sibling in discover_siblings():
            if sibling[1].resolve() == repo:
                match = sibling
                break
        if match is None:
            print(f"[FAIL] no projects/*.yaml registry points to {repo}")
            return 1
        results.extend(check_sibling(*match))
    else:
        results.extend(_run_meta_checks(CHECKS))
        results.extend(_check_brain_runtime(META_PROJECT_ID, REPO_ROOT))
        if not args.only_meta:
            siblings = discover_siblings()
            if not siblings:
                print("[OK]   no sibling repos registered")
            for sibling in siblings:
                results.extend(check_sibling(*sibling))

    for _, message in results:
        print(message)
    failed = sum(1 for ok, _ in results if not ok)
    print(f"\n{len(results) - failed}/{len(results)} checks passed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
