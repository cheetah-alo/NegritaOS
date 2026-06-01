# 50 — Per-repo bootstrap checklist

Run these steps when onboarding a new repo to NegritaOS. A future
`scripts/bootstrap_negritaos_repo.sh` will automate steps 1–7.

## 0. Prerequisites
- NegritaOS cloned at `~/repos/NegritaOS` (or wherever).
- Optional: global router rule symlinked into `~/.negritaos/rules/global/`.

## 1. Copy `.codex/` skeleton
```bash
cd <new-repo>
mkdir -p .codex/{rules,skills}
cp -R ~/repos/NegritaOS/.codex/rules/*       .codex/rules/
cp -R ~/repos/NegritaOS/.codex/skills/*      .codex/skills/
cp    ~/repos/NegritaOS/.codex/system.md     .codex/
cp    ~/repos/NegritaOS/.codex/instruction-manifest.yaml .codex/
```

## 2. Author repo identity
```bash
cp ~/repos/NegritaOS/repos_structure/20_codex_project.yaml.template .codex/project.yaml
$EDITOR .codex/project.yaml          # set project_id, project_name, archetype, brand
```

## 3. Author local overrides
```bash
cp ~/repos/NegritaOS/repos_structure/21_codex_local-overrides.md.template \
   .codex/local-overrides.md
$EDITOR .codex/local-overrides.md    # repo-specific paths + lexicon
```

## 4. Symlink Claude → Codex
```bash
ln -s .codex .claude
```

## 5. Create entry-point file
```bash
cp ~/repos/NegritaOS/repos_structure/10_AGENTS.md.template AGENTS.md
$EDITOR AGENTS.md                    # replace <PROJECT_NAME>, etc.
```

## 6. Seed canonical memory home
```bash
PROJECT_ID=$(grep '^project_id:' .codex/project.yaml | awk '{print $2}')
mkdir -p ~/.negritaos/memory/projects/$PROJECT_ID/sessions
cat > ~/.negritaos/memory/projects/$PROJECT_ID/index.md <<EOF
# $PROJECT_ID — memory index

## Latest session
_(none yet)_

## Open threads
_(none)_
EOF
```

## 7. Install the validator
```bash
mkdir -p scripts
cp ~/repos/NegritaOS/scripts/validate_alignment.py scripts/
python3 scripts/validate_alignment.py   # expect 9/9
```

## 8. Gitignore additions
Add these lines to `.gitignore`:
```
.codex/memory/
.codex/.DS_Store
.claude/.DS_Store
```

## 9. Commit
```bash
git add AGENTS.md .codex .claude scripts/validate_alignment.py .gitignore
git commit -m "chore: bootstrap NegritaOS scaffolding"
```

## 10. (Optional) Verify in each client
- Open the repo in Claude Code: it should auto-discover `AGENTS.md`.
- Open in Codex CLI: same.
- Open in VS Code Copilot: the instructions list should include all
  `.claude/rules/*.md` files (already verified per session prelude).
