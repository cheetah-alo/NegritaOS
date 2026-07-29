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
9. The active project's canonical memory home exists under
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
S9. Declared `memory_home` exists on disk.
S10. The canonical project -> registry -> agent/profile asset resolution passes.

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
import re
import subprocess
from pathlib import Path
from typing import Callable, Iterable

try:
    from .validate_config_resolution import validate_resolution
except ImportError:
    from validate_config_resolution import validate_resolution

REPO_ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()
PROJECTS_DIR = REPO_ROOT / "projects"
META_PROJECT_ID = "negritaos"
CANONICAL_RULES_DIR = (REPO_ROOT / ".codex" / "rules").resolve()


def _ok(msg: str) -> tuple[bool, str]:
    return True, f"[OK]   {msg}"


def _fail(msg: str) -> tuple[bool, str]:
    return False, f"[FAIL] {msg}"


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
    project_yaml = REPO_ROOT / ".codex" / "project.yaml"
    if not project_yaml.exists():
        return _fail("cannot resolve memory_home: .codex/project.yaml missing")
    text = project_yaml.read_text(encoding="utf-8")
    match = re.search(r"memory_home:\s*(\S+)", text)
    if match is None:
        return _fail(".codex/project.yaml does not declare memory_home")
    raw = match.group(1).strip()
    expanded = Path(raw.replace("~", str(HOME)))
    if expanded.exists():
        return _ok(f"memory_home present: {expanded}")
    return _fail(f"memory_home missing on disk: {expanded}")


CHECKS = (
    check_claude_alignment,
    check_project_yaml,
    check_config_resolution,
    check_local_overrides,
    check_manifest_router,
    check_canonical_router_rule,
    check_adapter_router_stub,
    check_router_skill,
    check_no_orphan_sessions,
    check_memory_home,
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
    py_text = project_yaml.read_text(encoding="utf-8")
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
    elif "negritaos-router" in manifest.read_text(encoding="utf-8"):
        results.append(_ok_s(project_id, "manifest registers negritaos-router"))
    else:
        results.append(
            _fail_s(project_id, "manifest does not mention negritaos-router")
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

    # S9 — memory_home exists
    memory_home_str = _scalar(py_text, "memory_home")
    if memory_home_str is None:
        results.append(_fail_s(project_id, "memory_home not declared"))
    else:
        memory_home = _expand(memory_home_str)
        if memory_home.exists():
            results.append(_ok_s(project_id, f"memory_home present: {memory_home}"))
        else:
            results.append(
                _fail_s(project_id, f"memory_home missing on disk: {memory_home}")
            )

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

    stub = rules_dir / "negritaos-router.md"
    if stub.exists():
        out.append(_ok_s(project_id, "rules/negritaos-router.md reachable"))
    else:
        out.append(_fail_s(project_id, "rules/negritaos-router.md missing"))

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
