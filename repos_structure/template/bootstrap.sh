#!/usr/bin/env bash
# bootstrap.sh — apply the NegritaOS template to the CURRENT repo.
#
# Usage:
#   ./bootstrap.sh <project_id> <archetype> [brand]
#
# Idempotent. Run from the target repo root AFTER copying the template/
# contents into it (or after running it from inside the template/ folder
# checked into a new repo).

set -euo pipefail

PROJECT_ID="${1:-}"
ARCHETYPE="${2:-}"
BRAND="${3:-none}"

if [[ -z "$PROJECT_ID" || -z "$ARCHETYPE" ]]; then
  echo "Usage: $0 <project_id> <archetype> [brand]"
  echo "Archetypes: data-platform, eda-analytics, ml-automl, product-app"
  exit 1
fi

# 1. Ensure .claude symlink
if [[ ! -L .claude ]]; then
  rm -rf .claude 2>/dev/null || true
  ln -s .codex .claude
  echo "[OK] .claude -> .codex symlink created"
else
  echo "[skip] .claude symlink already present"
fi

# 2. Patch project.yaml in place (very simple sed; only top-level keys)
if [[ -f .codex/project.yaml ]]; then
  sed -i.bak -E \
    -e "s|^project_id:.*|project_id: ${PROJECT_ID}|" \
    -e "s|^archetype:.*|archetype: ${ARCHETYPE}|" \
    -e "s|^brand:.*|brand: ${BRAND}|" \
    -e "s|^memory_home:.*|memory_home: ~/.negritaos/memory/projects/${PROJECT_ID}|" \
    .codex/project.yaml
  rm -f .codex/project.yaml.bak
  echo "[OK] .codex/project.yaml patched"
fi

# 3. Seed canonical memory home
MEM_HOME="${HOME}/.negritaos/memory/projects/${PROJECT_ID}"
mkdir -p "${MEM_HOME}/sessions"
if [[ ! -f "${MEM_HOME}/index.md" ]]; then
  cat > "${MEM_HOME}/index.md" <<EOF
# ${PROJECT_ID} — memory index

## Latest session
_(none yet)_

## Open threads
_(none)_
EOF
  echo "[OK] seeded ${MEM_HOME}/index.md"
else
  echo "[skip] ${MEM_HOME}/index.md already exists"
fi

# 4. Validate
if [[ -x scripts/validate_alignment.py || -f scripts/validate_alignment.py ]]; then
  echo "--- running validate_alignment.py ---"
  python3 scripts/validate_alignment.py || true
fi

cat <<EOF

Next steps (manual):
  1. Edit AGENTS.md      — replace <PROJECT_NAME> placeholders.
  2. Edit .codex/local-overrides.md — list this repo's actual paths + lexicon.
  3. (Optional) Copy craft rules from NegritaOS .codex/rules/ as needed
     and update .codex/instruction-manifest.yaml accordingly.
  4. git add AGENTS.md .codex .claude scripts/ .gitignore && git commit
EOF
