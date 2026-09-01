#!/usr/bin/env python3
"""Validate canonical Luna/Terra/Sol routing and global agent coverage."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from negrita_brain.model_routing import (  # noqa: E402
    load_model_escalation_policy,
    validate_model_escalation_policy,
)


def validate_all(root: Path = ROOT) -> tuple[list[str], int]:
    """Return policy errors and the number of globally routed agents."""
    try:
        policy = load_model_escalation_policy(root)
    except (OSError, ValueError) as exc:
        return [str(exc)], 0
    errors = validate_model_escalation_policy(policy)
    agents = policy.get("global_codex_custom_agents", [])
    count = len(agents) if isinstance(agents, list) else 0
    for name in agents if isinstance(agents, list) else []:
        path = root / ".codex" / "agents" / f"{name}.toml"
        if not path.is_file():
            errors.append(f"missing global Codex custom agent: {path}")
    return errors, count


def main() -> int:
    """Validate the canonical policy and its global Codex agent declarations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors, count = validate_all(args.root.expanduser().resolve())
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print(f"[OK] model escalation policy: {count} global Codex agents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
