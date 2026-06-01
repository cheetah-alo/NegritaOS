"""Validate NegritaOS / .codex / .claude alignment.

Checks performed:

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

Exit codes:
    0 — all checks pass.
    1 — at least one check failed (details printed to stdout).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()


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
    check_local_overrides,
    check_manifest_router,
    check_canonical_router_rule,
    check_adapter_router_stub,
    check_router_skill,
    check_no_orphan_sessions,
    check_memory_home,
)


def main() -> int:
    """Run every alignment check and report a pass/fail summary."""
    results = [check() for check in CHECKS]
    for _, message in results:
        print(message)
    failed = sum(1 for ok, _ in results if not ok)
    print(f"\n{len(results) - failed}/{len(results)} checks passed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
