# Drop-in NegritaOS scaffold

Copy the **contents** of this folder into the root of a new repo:

```bash
# from inside the new repo (empty or existing)
cp -R /Users/jackyb-cqi/repos/NegritaOS/repos_structure/template/. .

# the symlink may not copy with -R on some macOS settings; recreate it:
[ -L .claude ] || ln -s .codex .claude
```

> The trailing `/.` copies hidden files (`.codex`, `.claude`, `.gitignore`) too.

## Then edit 3 files

1. `AGENTS.md` — replace `<PROJECT_NAME>`, `<PROJECT_ID>`, archetype, brand, modes.
2. `.codex/project.yaml` — set `project_id`, `project_name`, `archetype`, `brand`, `memory_home`.
3. `.codex/local-overrides.md` — list this repo's actual top-level folders and lexicon.

## Optionally pull the craft rules

The template intentionally ships **only** the router + manifest + skill so the
scaffold stays small. If this repo will use engineering modes (MR / CR / DQ),
copy the adapter rules you need from NegritaOS:

```bash
cp -R /Users/jackyb-cqi/repos/NegritaOS/.codex/rules/dev-*.md .codex/rules/
cp -R /Users/jackyb-cqi/repos/NegritaOS/.codex/rules/ai-behavior.md .codex/rules/
# data/ml/notebooks/plotting as needed per archetype
```

Then keep `instruction-manifest.yaml` in sync with what you actually copied.

## Seed canonical memory home

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

## Validate

```bash
python3 scripts/validate_alignment.py    # expect 9/9
```

## Commit

```bash
git add AGENTS.md .codex .claude scripts/validate_alignment.py .gitignore
git commit -m "chore: bootstrap NegritaOS scaffolding"
```

## One-shot alternative

Run `./bootstrap.sh <project_id> <archetype>` inside the target repo after
copying the folder — it does all of the above except the manual edits to
`AGENTS.md` / `local-overrides.md`.
