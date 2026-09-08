"""Install and audit checkout-local Git identity controls with reversible backups."""

from __future__ import annotations

import hashlib
import json
import os
import shlex
import shutil
import subprocess
from contextlib import ExitStack, contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .commit_identity import load_commit_identity_policies, resolve_policy
from .config import NEGRITAOS_ROOT, load_project, load_yaml
from .git_identity_core import effective_violations, git, normalize_email


STATE_NAME = "identity-guard.json"
HOOK_NAMES = ("pre-commit", "pre-push")
CONFIG_KEYS = ("user.email", "user.useConfigOnly", "core.hooksPath")


def digest(data: bytes) -> str:
    """Return a byte-level artifact fingerprint."""
    return hashlib.sha256(data).hexdigest()


def common_dir(repo: Path) -> Path:
    """Support normal repos and linked worktrees without assuming .git is a directory."""
    return Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir"))


def config_values(repo: Path, key: str, local: bool = True) -> list[str]:
    """Read only the configuration keys owned by this installer."""
    result = subprocess.run(
        ["git", "-C", str(repo), "config", *(["--local"] if local else []),
         "--get-all" if local else "--get", key],
        capture_output=True, text=True, check=False,
    )
    if result.returncode not in (0, 1):
        raise ValueError("Cannot inspect Git configuration")
    return result.stdout.splitlines()


def restore(repo: Path) -> dict:
    """Detach managed hooks and restore the original repo-local configuration."""
    state = read_state(repo)
    if state is None:
        raise ValueError("No managed identity installation to restore")
    current_hooks = config_values(repo, "core.hooksPath", False)
    if current_hooks != [str(common_dir(repo) / "identity-hooks")]:
        raise ValueError("Hooks configuration changed since installation; preserve it for review")
    for key, values in state["original_config"].items():
        if key not in CONFIG_KEYS:
            raise ValueError("Unowned configuration key in receipt")
        result = subprocess.run(["git", "-C", str(repo), "config", "--local", "--unset-all", key],
                                capture_output=True, check=False)
        if result.returncode not in (0, 5):
            raise ValueError("Cannot restore local Git configuration")
        for value in values:
            git(repo, "config", "--local", "--add", key, value)
    return {"status": "RESTORED", "root": str(repo), "retained_ci_files": True}


def project_identity(repo: Path, root: Path) -> tuple[str, dict] | None:
    """Resolve personal checkout identity separately from repository contributor policy."""
    if (repo / ".codex/project.yaml").is_file():
        project = load_project(repo, root).project
    else:
        project = None
        common = common_dir(repo)
        for path in (root / "projects").glob("*.yaml"):
            candidate = load_yaml(path).get("project", {})
            primary = candidate.get("local_paths", {}).get("primary")
            if not candidate.get("local_commit_identity") or not primary:
                continue
            primary_path = Path(primary).expanduser()
            if primary_path.exists() and common_dir(primary_path) == common:
                project = candidate
                break
        if project is None:
            raise ValueError("Checkout has no registered Git identity")
    document = load_commit_identity_policies(root)
    resolved = resolve_policy(project, document)
    if resolved is None:
        return None
    name = project.get("local_commit_identity")
    profile = document.get("identity_profiles", {}).get(name, {})
    emails = profile.get("allowed_emails", [])
    if len(emails) != 1:
        raise ValueError("Project requires one explicit local identity profile")
    return normalize_email(emails[0]), dict(resolved[1])


def ci_files(root: Path, policy: dict) -> dict[str, bytes]:
    """Produce neutral standalone CI files with no local paths or private branding."""
    public_policy = {
        "allowed_email_domains": policy["allowed_email_domains"],
        "allow_subdomains": policy["allow_subdomains"],
    }
    if "ci_allowed_emails" in policy:
        public_policy["allowed_emails"] = policy["ci_allowed_emails"]
    return {
        "scripts/check_git_identity.py": (root / "src/negrita_brain/git_identity_core.py").read_bytes(),
        ".github/commit-identity-policy.json": (json.dumps(public_policy, indent=2) + "\n").encode(),
        ".github/workflows/commit-identity.yml": (root / "templates/git_identity_ci.yml").read_bytes(),
    }


def runtime_files(root: Path) -> dict[str, bytes]:
    """Build the immutable private distribution from canonical sources."""
    return {"git_identity_hook.py": (root / "scripts/git_identity_hook.py").read_bytes(),
            "git_identity_core.py": (root / "src/negrita_brain/git_identity_core.py").read_bytes()}


def runtime_directory(root: Path, common: Path) -> Path:
    """Address the installed runtime by source hash so branch switching is harmless."""
    content = b"".join(name.encode() + b"\0" + data for name, data in sorted(runtime_files(root).items()))
    return common / "identity-runtime" / digest(content)


def hook_text(root: Path, name: str, common: Path) -> bytes:
    """Build a thin launcher for the hash-bound canonical runtime distribution."""
    interpreter = "/usr/bin/python3" if Path("/usr/bin/python3").is_file() else shutil.which("python3")
    if not interpreter:
        raise ValueError("A stable Python 3.9+ interpreter is required")
    command = " ".join(shlex.quote(part) for part in (
        interpreter, str(runtime_directory(root, common) / "git_identity_hook.py"), name,
    ))
    return ("#!/bin/sh\nexec " + command + ' "$@"\n').encode()


def read_state(repo: Path) -> dict | None:
    """Read an existing installation receipt without guessing authority."""
    path = common_dir(repo) / STATE_NAME
    if not path.exists():
        return None
    state = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(state, dict) or state.get("schema_version") != 1:
        raise ValueError("Invalid identity installation receipt")
    return state


def audit(repo: Path, root: Path = NEGRITAOS_ROOT, with_ci: bool = True) -> dict:
    """Check effective email, dispatcher, retained hooks and generated CI byte identity."""
    resolved = project_identity(repo, root)
    if resolved is None:
        return {"status": "NOT_APPLICABLE", "issues": []}
    expected, policy = resolved
    issues = []
    common = common_dir(repo)
    directory = common / "identity-hooks"
    state = read_state(repo)
    if config_values(repo, "user.email") != [expected]:
        issues.append("local_email_mismatch")
    if config_values(repo, "user.useConfigOnly", False) != ["true"]:
        issues.append("user_use_config_only_missing")
    if config_values(repo, "core.hooksPath", False) != [str(directory)]:
        issues.append("hooks_path_mismatch")
    if effective_violations(repo, expected):
        issues.append("effective_identity_mismatch")
    if state is None:
        issues.append("installation_missing")
    else:
        if state.get("canonical_root") != str(root.resolve()):
            issues.append("canonical_root_mismatch")
        for name in HOOK_NAMES:
            path = directory / name
            if not path.is_file() or path.read_bytes() != hook_text(root, name, common) or not os.access(path, os.X_OK):
                issues.append("hook_drift:" + name)
        if state.get("expected_email") != expected or state.get("contributor_policy") != policy:
            issues.append("installed_policy_drift")
        for name, content in runtime_files(root).items():
            path = runtime_directory(root, common) / name
            if not path.is_file() or path.read_bytes() != content:
                issues.append("runtime_drift:" + name)
        for name, target in state.get("passthrough", {}).items():
            path = directory / name
            if not path.is_symlink() or path.resolve() != Path(target).resolve():
                issues.append("retained_hook_drift:" + name)
    ci_issues = []
    if with_ci:
        for relative, content in ci_files(root, policy).items():
            path = repo / relative
            if not path.is_file() or path.read_bytes() != content:
                ci_issues.append("ci_drift:" + relative)
    return {"status": "FAIL" if issues or ci_issues else "PASS", "issues": issues,
            "ci_issues": ci_issues, "remote_ci": "NOT_VERIFIED"}


def _configure(repo: Path, root: Path = NEGRITAOS_ROOT, *, apply: bool = False, with_ci: bool = False) -> dict:
    """Install only owned keys/files; retain originals and refuse unmanaged collisions."""
    repo, root = repo.resolve(), root.resolve()
    resolved = project_identity(repo, root)
    if resolved is None:
        return {"status": "NOT_APPLICABLE", "root": str(repo)}
    email, policy = resolved
    common = common_dir(repo)
    directory, state_path = common / "identity-hooks", common / STATE_NAME
    state = read_state(repo)
    report = audit(repo, root, with_ci)
    if report["status"] == "PASS":
        return {**report, "root": str(repo), "changed": False}
    if state is None and directory.exists():
        raise ValueError("Unmanaged identity-hooks directory exists; inspect it before adoption")
    bundle = ci_files(root, policy) if with_ci else {}
    for relative, content in bundle.items():
        path = repo / relative
        if not path.resolve().is_relative_to(repo):
            raise ValueError("CI target escapes checkout: " + relative)
        receipt = state or {}
        previous = receipt.get("ci_hashes_by_checkout", {}).get(
            str(repo), receipt.get("ci_hashes", {})
        ).get(relative)
        if path.is_symlink():
            raise ValueError("CI target must not be a symlink: " + relative)
        if path.exists() and path.read_bytes() != content:
            if previous is None or digest(path.read_bytes()) != previous:
                raise ValueError("Preserved locally modified/unmanaged CI file: " + relative)
    for name in HOOK_NAMES:
        if (directory / name).is_symlink():
            raise ValueError("Managed dispatcher was replaced with a symlink")
    if not apply:
        return {**report, "status": "DRY_RUN", "root": str(repo), "changed": True,
                "ci_files": list(bundle), "config_keys": list(CONFIG_KEYS)}

    backup = common / "identity-guard-backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup.mkdir(parents=True, exist_ok=False)
    original_config = {key: config_values(repo, key) for key in CONFIG_KEYS}
    (backup / "config.json").write_text(json.dumps(original_config), encoding="utf-8")
    if state_path.exists():
        shutil.copy2(state_path, backup / STATE_NAME)
    previous_hooks = git(repo, "rev-parse", "--path-format=absolute", "--git-path", "hooks")
    if state is None:
        state = {"schema_version": 1, "previous_hooks": previous_hooks,
                 "original_config": original_config, "passthrough": {}, "ci_hashes": {}}
    else:
        if directory.exists():
            shutil.copytree(directory, backup / "hooks", symlinks=True)
    previous_dir = Path(state["previous_hooks"])
    if previous_dir.resolve() == directory.resolve():
        raise ValueError("Recursive hook chain")
    directory.mkdir(exist_ok=True)
    runtime = runtime_directory(root, common)
    runtime.mkdir(parents=True, exist_ok=True)
    for name, content in runtime_files(root).items():
        target = runtime / name
        if target.exists():
            if target.read_bytes() != content:
                raise ValueError("Immutable identity runtime was modified")
        else:
            target.write_bytes(content)
    for path in previous_dir.iterdir() if previous_dir.is_dir() else []:
        if path.name.endswith(".sample") or not path.is_file():
            continue
        shutil.copy2(path, backup / ("previous-" + path.name))
        if path.name not in HOOK_NAMES:
            destination = directory / path.name
            if not destination.exists() and not destination.is_symlink():
                destination.symlink_to(path)
            state["passthrough"][path.name] = str(path)
    for name in HOOK_NAMES:
        path = directory / name
        if path.is_symlink():
            raise ValueError("Managed dispatcher was replaced with a symlink")
        temporary_hook = backup / name
        temporary_hook.write_bytes(hook_text(root, name, common))
        temporary_hook.chmod(0o755)
        os.replace(temporary_hook, path)
    for relative, content in bundle.items():
        path = repo / relative
        if path.exists():
            saved = backup / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        state.setdefault("ci_hashes_by_checkout", {}).setdefault(str(repo), {})[relative] = digest(content)
    state.update({"canonical_root": str(root), "backup": str(backup), "expected_email": email,
                  "contributor_policy": policy,
                  "installed_at": datetime.now(timezone.utc).isoformat()})
    temporary_state = backup / "next-state.json"
    temporary_state.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary_state, state_path)
    for key, value in (("user.email", email), ("user.useConfigOnly", "true"), ("core.hooksPath", str(directory))):
        git(repo, "config", "--local", "--replace-all", key, value)
    return {**audit(repo, root, with_ci), "root": str(repo), "changed": True, "backup": str(backup)}


@contextmanager
def rollback_guard(repo: Path, root: Path, with_ci: bool):
    """Restore all managed paths and local config when any activation step fails."""
    resolved = project_identity(repo, root)
    if resolved is None:
        yield
        return
    common = common_dir(repo)
    paths = [common / "identity-hooks", common / STATE_NAME, common / "identity-runtime"]
    original_config = {key: config_values(repo, key) for key in CONFIG_KEYS}
    if with_ci:
        paths.extend(repo / relative for relative in ci_files(root, resolved[1]))
    backup = common / "identity-guard-backups" / datetime.now(timezone.utc).strftime("transaction_%Y%m%dT%H%M%S%fZ")
    backup.mkdir(parents=True, exist_ok=False)
    snapshots = []
    for index, path in enumerate(paths):
        saved = backup / str(index)
        kind = "absent"
        if path.is_symlink():
            kind = "symlink"
            saved.symlink_to(path.readlink())
        elif path.is_dir():
            kind = "directory"
            shutil.copytree(path, saved, symlinks=True)
        elif path.exists():
            kind = "file"
            shutil.copy2(path, saved)
        snapshots.append((path, saved, kind))
    try:
        yield
    except BaseException:
        for key, values in original_config.items():
            subprocess.run(["git", "-C", str(repo), "config", "--local", "--unset-all", key],
                           capture_output=True, check=False)
            for value in values:
                subprocess.run(["git", "-C", str(repo), "config", "--local", "--add", key, value],
                               capture_output=True, check=True)
        for path, saved, kind in reversed(snapshots):
            if path.is_symlink() or path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
            if kind == "symlink":
                path.symlink_to(saved.readlink())
            elif kind == "directory":
                shutil.copytree(saved, path, symlinks=True)
            elif kind == "file":
                shutil.copy2(saved, path)
        raise


def configure(repo: Path, root: Path = NEGRITAOS_ROOT, *, apply: bool = False, with_ci: bool = False) -> dict:
    """Preflight before writes, then atomically activate or roll back owned state."""
    repo = repo.resolve()
    # Per-worktree overrides must never be silently hidden by shared config writes.
    if config_values(repo, "extensions.worktreeConfig", False) == ["true"]:
        raw = git(repo, "worktree", "list", "--porcelain", "-z")
        for record in raw.split("\0\0"):
            fields = record.split("\0")
            if any(field.startswith("prunable") for field in fields):
                continue
            for field in fields:
                if not field.startswith("worktree "):
                    continue
                sibling = field[9:]
                for key in CONFIG_KEYS:
                    result = subprocess.run(["git", "-C", sibling, "config", "--worktree", "--get", key],
                                            capture_output=True, check=False)
                    if result.returncode == 0:
                        raise ValueError(
                            "Existing worktree-specific " + key + "; reconcile that override before installation"
                        )
                    if result.returncode != 1:
                        raise ValueError("Cannot inspect sibling worktree configuration")
    plan = _configure(repo, root, apply=False, with_ci=with_ci)
    if not apply or not plan.get("changed"):
        return plan
    with rollback_guard(repo, root, with_ci):
        result = _configure(repo, root, apply=True, with_ci=with_ci)
        if result["status"] != "PASS":
            raise ValueError("Post-install audit failed; previous configuration restored")
        return result


def registered_checkouts(root: Path) -> list[Path]:
    """Enumerate registered scoped Git repos and their existing linked worktrees."""
    result = set()
    for path in sorted((root / "projects").glob("*.yaml")):
        project = load_yaml(path).get("project", {})
        if not project.get("local_commit_identity"):
            continue
        repo = Path(project["local_paths"]["primary"]).expanduser()
        raw = git(repo, "worktree", "list", "--porcelain", "-z")
        for record in raw.split("\0\0"):
            fields = record.split("\0")
            if any(field.startswith("prunable") for field in fields):
                continue
            for field in fields:
                if field.startswith("worktree "):
                    result.add(Path(field[9:]))
    return sorted(result)


def run_configuration(args) -> tuple[dict, int]:
    """Handle configure git-identity without changing global Git state."""
    root = args.negritaos_root
    repos = registered_checkouts(root) if args.all else [args.root]
    if args.apply:
        try:
            # Complete preflight across all checkouts before modifying the first one.
            for repo in repos:
                configure(repo, root, with_ci=args.with_ci)
            with ExitStack() as transaction:
                for repo in repos:
                    transaction.enter_context(rollback_guard(repo, root, args.with_ci))
                results = [configure(repo, root, apply=True, with_ci=args.with_ci) for repo in repos]
            return {"status": "PASS", "checkouts": results}, 0
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            return {"status": "BLOCKED", "reason": str(exc), "rolled_back": True}, 1
    results = []
    for repo in repos:
        try:
            if args.restore:
                result = restore(repo)
            elif args.check:
                result = {**audit(repo, root, args.with_ci), "root": str(repo)}
            else:
                result = configure(repo, root, apply=args.apply, with_ci=args.with_ci)
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            result = {"root": str(repo), "status": "BLOCKED", "reason": str(exc)}
        results.append(result)
    failed = any(item["status"] in {"FAIL", "BLOCKED"} for item in results)
    return {"status": "FAIL" if failed else "PASS", "checkouts": results}, int(failed)
