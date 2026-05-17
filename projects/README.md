# NegritaOS Project Registry

This directory maps local projects to NegritaOS memory, agents, archetypes,
and technical adapter profiles.

Rules:

- Canonical durable memory lives under `~/.negritaos/memory/projects/<project_id>`.
- Repository `.codex` directories are adapters, not canonical memory stores.
- Preservation backup must exist before any repo adapter migration.
- Dirty or tracked `.codex` folders are never rewritten until their changes are classified.

Load order for a session:

1. Detect the current repository.
2. Load the matching file in this directory.
3. Read personal memory from `~/.negritaos/memory/personal`.
4. Read project memory from the configured `memory_home`.
5. Read the repo-local `.codex/project.yaml` if present.
6. Activate agents and profiles according to the task.
