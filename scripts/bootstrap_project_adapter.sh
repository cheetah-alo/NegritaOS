#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bootstrap_project_adapter.sh \
    --project-id <id> \
    --repo <repo-path> \
    --archetypes <a,b> \
    --capabilities <a,b> \
    --agents <a,b>

Creates:
  ~/.negritaos/memory/projects/<id>/
  NegritaOS/projects/<id>.yaml
  <repo>/.codex/project.yaml
  <repo>/.codex/local-overrides.md

Safety:
  The script refuses to overwrite existing project registry or adapter files.
  It refuses to write into a repo whose .codex has tracked dirty changes.
EOF
}

PROJECT_ID=""
REPO_PATH=""
ARCHETYPES=""
CAPABILITIES=""
AGENTS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-id)
      PROJECT_ID="$2"
      shift 2
      ;;
    --repo)
      REPO_PATH="$2"
      shift 2
      ;;
    --archetypes)
      ARCHETYPES="$2"
      shift 2
      ;;
    --capabilities)
      CAPABILITIES="$2"
      shift 2
      ;;
    --agents)
      AGENTS="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$PROJECT_ID" || -z "$REPO_PATH" || -z "$ARCHETYPES" || -z "$CAPABILITIES" || -z "$AGENTS" ]]; then
  usage >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEGRITA_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REGISTRY_FILE="$NEGRITA_ROOT/projects/$PROJECT_ID.yaml"
MEMORY_HOME="$HOME/.negritaos/memory/projects/$PROJECT_ID"
ADAPTER_DIR="$REPO_PATH/.codex"
ADAPTER_FILE="$ADAPTER_DIR/project.yaml"
OVERRIDES_FILE="$ADAPTER_DIR/local-overrides.md"

if [[ ! -d "$REPO_PATH" ]]; then
  echo "Repo path does not exist: $REPO_PATH" >&2
  exit 1
fi

if [[ -e "$REGISTRY_FILE" ]]; then
  echo "Refusing to overwrite existing registry file: $REGISTRY_FILE" >&2
  exit 1
fi

if [[ -e "$ADAPTER_FILE" || -e "$OVERRIDES_FILE" ]]; then
  echo "Refusing to overwrite existing adapter files in: $ADAPTER_DIR" >&2
  exit 1
fi

if [[ -d "$REPO_PATH/.git" ]]; then
  dirty_codex="$(git -C "$REPO_PATH" status --short .codex 2>/dev/null || true)"
  tracked_dirty_codex="$(printf '%s\n' "$dirty_codex" | grep -E '^( M|M |D | D|A |R |C |UU|AA|DD) ' || true)"
  if [[ -n "$tracked_dirty_codex" ]]; then
    echo "Refusing to write adapter because .codex has tracked dirty changes:" >&2
    printf '%s\n' "$tracked_dirty_codex" >&2
    exit 1
  fi
fi

mkdir -p "$MEMORY_HOME/sessions" "$MEMORY_HOME/decisions" "$MEMORY_HOME/tasks" "$MEMORY_HOME/legacy_import"
mkdir -p "$ADAPTER_DIR"

cat > "$MEMORY_HOME/index.md" <<EOF
# Memory Index: $PROJECT_ID

## Current Focus

- Canonical memory initialized under \`~/.negritaos/memory/projects/$PROJECT_ID\`.

## Latest Session

- No session recorded yet.

## Retrieval Notes

- Start with this index.
- Search \`observations.jsonl\`, \`sessions/\`, \`decisions/\`, \`tasks/\`, and \`legacy_import/\` with \`rg\`.
EOF

: > "$MEMORY_HOME/observations.jsonl"
printf '# Sessions: %s\n' "$PROJECT_ID" > "$MEMORY_HOME/sessions/README.md"
printf '# Decisions: %s\n' "$PROJECT_ID" > "$MEMORY_HOME/decisions/README.md"
printf '# Tasks: %s\n' "$PROJECT_ID" > "$MEMORY_HOME/tasks/README.md"

cat > "$REGISTRY_FILE" <<EOF
project:
  id: $PROJECT_ID
  name: "$PROJECT_ID"
  version: "1.0.0"
  local_paths:
    primary: "$REPO_PATH"
  memory_home: "~/.negritaos/memory/projects/$PROJECT_ID"
  archetypes:
EOF

IFS=',' read -r -a archetype_items <<< "$ARCHETYPES"
for item in "${archetype_items[@]}"; do
  printf '    - %s\n' "$item" >> "$REGISTRY_FILE"
done

cat >> "$REGISTRY_FILE" <<'EOF'
  capabilities:
EOF

IFS=',' read -r -a capability_items <<< "$CAPABILITIES"
for item in "${capability_items[@]}"; do
  printf '    - %s\n' "$item" >> "$REGISTRY_FILE"
done

cat >> "$REGISTRY_FILE" <<'EOF'
  agents:
EOF

IFS=',' read -r -a agent_items <<< "$AGENTS"
for item in "${agent_items[@]}"; do
  printf '    - %s\n' "$item" >> "$REGISTRY_FILE"
done

cat >> "$REGISTRY_FILE" <<EOF
  preservation:
    backup_required_before_migration: true
    repo_codex_status: "adapter_local"
    canonical_memory_outside_repo: true
EOF

cat > "$ADAPTER_FILE" <<EOF
project_id: $PROJECT_ID
negrita_registry: $REGISTRY_FILE
memory_home: ~/.negritaos/memory/projects/$PROJECT_ID
repo_codex_role: adapter
repo_codex_status: adapter_local
canonical_memory_outside_repo: true
session_load_order:
  - negrita_project_registry
  - personal_memory
  - project_memory
  - repo_local_adapter
  - task_specific_profile
active_capabilities:
EOF

for item in "${capability_items[@]}"; do
  printf '  - %s\n' "$item" >> "$ADAPTER_FILE"
done

cat > "$OVERRIDES_FILE" <<EOF
# Local Codex Adapter: $PROJECT_ID

This .codex directory is a repo-local adapter. It is not the canonical memory store.

Canonical memory: ~/.negritaos/memory/projects/$PROJECT_ID
NegritaOS registry: $REGISTRY_FILE

Rules:
- Do not copy a full .codex from another project into this repo.
- Do not store durable private memory here as the canonical source.
- Update project memory under ~/.negritaos/memory/projects/$PROJECT_ID at session close.
- Preserve local repo rules and commands that are specific to this codebase.
EOF

echo "Created project adapter for $PROJECT_ID"
echo "Registry: $REGISTRY_FILE"
echo "Memory: $MEMORY_HOME"
echo "Adapter: $ADAPTER_FILE"
