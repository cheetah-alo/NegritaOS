---
metadata:
  source: codex_claude
  document_version: "1.0.0"
  generated_date: "2026-08-07"
  last_modified_date: "2026-08-07"
  agent_id: software_architect_agent
  router_mode: CR
  project_id: negritaos
  template_used: templates/repo_architecture_blueprint_template.md
  quality_gates_status: PASSED_WITH_WARNINGS
  quality_warnings:
    - "La implementación actual cubre el snapshot Git y la CLI read-only; hooks, ledger de commits y dashboard siguen pendientes."
    - "El upstream de la rama de trabajo no está configurado; el snapshot usa origin/main como base disponible."
---

# Actualización de implementación MVP: Git Traceability

## Propósito

Registrar qué parte de la propuesta funcional de trazabilidad Git ya está
implementada y qué queda pendiente, manteniendo una separación verificable entre
Git, Negrita Brain y el futuro dashboard.

## Audiencia y alcance

Documento dirigido al owner de NegritaOS y a los mantenedores de Brain. Cubre el
primer corte técnico de `GIT-003`, `GIT-004` y `GIT-009`. No cubre hooks,
persistencia de commits, reconciliación ni UI.

## Fuente de verdad y commit base

- Propuesta funcional: `documents/git_traceability_functional_proposal__updated_20260807_185348.md`.
- Commit de la propuesta: `4ae0a47`.
- Contrato Brain y runtime: `src/negrita_brain/runtime.py`.
- Collector Git: `src/negrita_brain/git_traceability.py`.
- CLI: `scripts/negrita_brain.py`.
- Tests: `tests/test_negrita_brain_git_traceability.py`,
  `tests/test_negrita_brain_runtime.py` y `tests/test_negrita_brain_cli.py`.

Git sigue siendo la fuente de verdad de branch, HEAD, base y estado del
worktree. Brain solo captura un snapshot seguro dentro del contrato de sesión.

## Funcionalidad implementada

### Snapshot Git v1

`src/negrita_brain/git_traceability.py` incorpora una lectura sin mutaciones que
calcula:

- branch y HEAD;
- upstream y base disponible;
- merge-base;
- commits `ahead` y `behind`;
- dirty state, staged, unstaged y untracked counts;
- clasificación `main`, `feature`, `temporary`, `detached` o `unknown`;
- `repo_id` y `worktree_id` mediante SHA-256, sin persistir rutas locales;
- `git_valid`, política de ruta y timestamp de captura.

### Integración Brain

`resolve` ahora incorpora el snapshot completo en `contract["git"]`. Esto
mantiene la identidad de sesión existente por `CODEX_THREAD_ID` o
`--session-key` y añade contexto de worktree sin cambiar los punteros Memory v2.

### CLI read-only

```bash
python3 scripts/negrita_brain.py git-trace --root "$PWD"
```

El comando devuelve JSON y no crea commits, no cambia ramas, no escribe el ledger
y no expone el path absoluto del worktree.

## Tareas y estado

| ID | Estado | Evidencia |
|---|---|---|
| GIT-003 | COMPLETADA | Collector, parser de status y tests con subprocess mockeado |
| GIT-004 | COMPLETADA | `resolve` persiste el snapshot en el contrato |
| GIT-009 | COMPLETADA | Comando `git-trace` y test de gramática CLI |
| GIT-001 | PARCIAL | Campos v1 implementados; ADR y schema formal siguen pendientes |
| GIT-002 | PARCIAL | IDs hasheados y clasificación temporal implementados; política formal pendiente |
| GIT-005 | PENDIENTE | Ampliar whitelist del ledger para eventos Git |
| GIT-006 | PENDIENTE | Trailers `Negrita-*` |
| GIT-007 | PENDIENTE | Registro post-commit |
| GIT-008 | PENDIENTE | Reconciliación de commits externos |
| GIT-010..GIT-015 | PENDIENTE | Read model, dashboard, PR adapter, runbooks y enforcement |

## Validación ejecutada

```bash
python3 -m unittest tests.test_negrita_brain_git_traceability \
  tests.test_negrita_brain_cli tests.test_negrita_brain_runtime
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_negrita_brain_coverage.py --fail-under 80
python3 scripts/validate_config_resolution.py
python3 scripts/validate_registry_paths.py --root "$PWD"
python3 scripts/validate_alignment.py --only-meta
python3 -m compileall -q src scripts tests
git diff --check
```

La suite focal y la suite completa terminaron correctamente. La auditoría de
configuración, registry y alignment también terminó sin errores bloqueantes.

Ejemplo observado en la rama actual:

```json
{
  "branch": "feature/git-traceability-functional-proposal",
  "base_ref": "origin/main",
  "ahead": 1,
  "behind": 0,
  "dirty": true,
  "root_path_policy": "hashed",
  "worktree_class": "feature"
}
```

Los identificadores completos y el timestamp se generan en runtime; el ejemplo
no pretende ser una copia persistida del estado actual.

## Limitaciones conocidas

- La rama aún no tiene upstream; el collector usa `origin/main` si existe.
- El snapshot todavía no se añade al ledger como evento `commit`.
- No hay trailers automáticos ni reconciliador de commits sin hook.
- El worktree puede estar dirty durante la implementación; eso es esperado y
  debe quedar visible antes del commit de código.
- No se han creado hooks, API, read model ni dashboard.

## Siguiente corte recomendado

1. Crear tests de contrato para los campos `GitIdentitySnapshot v1`.
2. Añadir whitelist segura para `commit_sha`, `worktree_id`, `gate_status` y
   `evidence_status`.
3. Implementar registro post-commit opt-in y mantener `WARN` para commits sin
   contrato hasta completar la reconciliación.

## Ownership y actualización

Owner técnico: `software_architect_agent` junto con el mantenedor de Brain.

Actualizar este documento cuando se complete otra tarea `GIT-*`, cambie el
contrato snapshot, se elija el runtime del dashboard o se active enforcement.
