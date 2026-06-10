#!/usr/bin/env bash
# Migrate a sibling repo to consume NegritaOS canonical .codex governance via symlinks.
#
# Idempotent. Safe to re-run. Always backs up before destructive moves.
#
# Usage:
#   scripts/migrate_sibling_to_canonical.sh <absolute-path-to-sibling-repo>
#
# Pre-conditions:
#   - <repo>/.codex/project.yaml exists (carries project_id + negrita_registry).
#   - NegritaOS canonical lives at /Users/jackyb-cqi/repos/NegritaOS.
#
# Post-conditions:
#   - <repo>/.codex/rules/*.md          -> symlinks into NegritaOS canonical (22 files)
#   - <repo>/.codex/commands            -> symlink to NegritaOS canonical dir
#   - <repo>/.codex/instruction-manifest.yaml -> symlink to canonical
#   - <repo>/.codex/skills/AGENTS.md    -> symlink to canonical
#   - <repo>/.codex/skills/negritaos-mode-router/ -> symlink to canonical
#   - <repo>/.claude                    -> symlink to .codex
#   - <repo>/.claude.bak.<ts>/          backup of pre-existing real .claude/
#   - <repo>/.codex/<file>.preCanonical.<ts>  per-file backups when symlinking over real files

set -euo pipefail

readonly NEGRITAOS_ROOT="/Users/jackyb-cqi/repos/NegritaOS"
readonly CANONICAL_CODEX="${NEGRITAOS_ROOT}/.codex"
readonly TS="$(date +%Y%m%d-%H%M%S)"

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <sibling-repo-absolute-path>" >&2
  exit 2
fi

readonly REPO="$1"
if [[ ! -d "${REPO}" ]]; then
  echo "ERROR: repo path not found: ${REPO}" >&2
  exit 2
fi
if [[ ! -f "${REPO}/.codex/project.yaml" ]]; then
  echo "ERROR: missing ${REPO}/.codex/project.yaml — bootstrap project.yaml first" >&2
  exit 2
fi

cd "${REPO}"

echo "==> migrating ${REPO}"

# Step 1 — Back up real .claude/ if present (skip if symlink or absent).
if [[ -e .claude || -L .claude ]]; then
  if [[ -L .claude ]]; then
    echo "  [skip] .claude is already a symlink: $(readlink .claude)"
  elif [[ -d .claude ]]; then
    backup=".claude.bak.${TS}"
    echo "  [backup] mv .claude -> ${backup}"
    mv .claude "${backup}"
  fi
fi

# Step 2 — Symlink instruction-manifest.yaml to canonical (back up if real file).
manifest=".codex/instruction-manifest.yaml"
if [[ -L "${manifest}" ]]; then
  echo "  [skip] ${manifest} already a symlink"
elif [[ -f "${manifest}" ]]; then
  echo "  [backup] ${manifest} -> ${manifest}.preCanonical.${TS}"
  mv "${manifest}" "${manifest}.preCanonical.${TS}"
fi
if [[ ! -L "${manifest}" ]]; then
  ln -s "${CANONICAL_CODEX}/instruction-manifest.yaml" "${manifest}"
  echo "  [link] ${manifest} -> canonical"
fi

# Step 3 — Replace .codex/rules/*.md with per-file symlinks into canonical.
mkdir -p .codex/rules
for src in "${CANONICAL_CODEX}/rules"/*.md; do
  name="$(basename "${src}")"
  dst=".codex/rules/${name}"
  if [[ -L "${dst}" ]]; then
    if [[ "$(readlink "${dst}")" == "${src}" ]]; then
      continue   # already canonical
    fi
    rm "${dst}"
  elif [[ -f "${dst}" ]]; then
    mv "${dst}" "${dst}.preCanonical.${TS}"
  fi
  ln -s "${src}" "${dst}"
done
echo "  [link] .codex/rules/*.md -> canonical (22 files)"

# Step 4 — Symlink .codex/commands -> canonical dir.
if [[ -L .codex/commands ]]; then
  if [[ "$(readlink .codex/commands)" != "${CANONICAL_CODEX}/commands" ]]; then
    rm .codex/commands
  fi
fi
if [[ -d .codex/commands && ! -L .codex/commands ]]; then
  mv .codex/commands ".codex/commands.preCanonical.${TS}"
fi
if [[ ! -e .codex/commands ]]; then
  ln -s "${CANONICAL_CODEX}/commands" .codex/commands
  echo "  [link] .codex/commands -> canonical"
fi

# Step 5 — Symlink router skill + AGENTS.md inside .codex/skills/ (preserve sibling skills).
mkdir -p .codex/skills
for entry in AGENTS.md negritaos-mode-router; do
  src="${CANONICAL_CODEX}/skills/${entry}"
  dst=".codex/skills/${entry}"
  if [[ ! -e "${src}" ]]; then
    echo "  [warn] canonical skill missing: ${src}"
    continue
  fi
  if [[ -L "${dst}" ]]; then
    if [[ "$(readlink "${dst}")" == "${src}" ]]; then continue; fi
    rm "${dst}"
  elif [[ -e "${dst}" ]]; then
    mv "${dst}" "${dst}.preCanonical.${TS}"
  fi
  ln -s "${src}" "${dst}"
done
echo "  [link] .codex/skills/{AGENTS.md,negritaos-mode-router} -> canonical"

# Step 6 — .claude -> .codex symlink.
if [[ -L .claude ]]; then
  if [[ "$(readlink .claude)" != ".codex" ]]; then
    rm .claude
    ln -s .codex .claude
  fi
else
  ln -s .codex .claude
fi
echo "  [link] .claude -> .codex"

# Step 7 — Ensure memory_home dir exists (read from project.yaml).
memhome="$(grep -E '^memory_home:' .codex/project.yaml | head -1 | sed -E 's/^memory_home:[ \t]*//; s/^"//; s/"$//')"
if [[ -n "${memhome}" ]]; then
  expanded="${memhome/#~/${HOME}}"
  mkdir -p "${expanded}"
  echo "  [mkdir] memory_home: ${expanded}"
fi

# Step 8 — Append backup pattern to .gitignore if present.
if [[ -f .gitignore ]] && ! grep -q '^\.claude\.bak\.' .gitignore; then
  printf '\n# NegritaOS adapter migration backups\n.claude.bak.*/\n.codex/**/*.preCanonical.*\n' >> .gitignore
  echo "  [gitignore] appended backup patterns"
fi

echo "==> done: ${REPO}"
