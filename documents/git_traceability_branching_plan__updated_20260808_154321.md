---
metadata:
  source: codex_claude
  document_version: "1.0.0"
  generated_date: "2026-08-08"
  last_modified_date: "2026-08-08"
  agent_id: software_architect_agent
  router_mode: CR
  project_id: negritaos
  template_used: templates/repo_architecture_blueprint_template.md
  quality_gates_status: PASSED_WITH_WARNINGS
  quality_warnings:
    - "La rama de tarea debe validarse y mezclarse por fast-forward en la rama padre antes del PR final."
    - "No se ha publicado ninguna rama remota ni se ha creado PR."
---

# Plan de ramas cortas: Git Traceability

## Propósito

Documentar la estrategia para implementar Git Traceability en tareas pequeñas,
aisladas y mezclables, manteniendo una única rama padre como candidato al PR.

## Alcance y fuentes de verdad

- Base de integración actual: `main` / `origin/main`.
- Rama padre del PR: `feature/git-traceability-functional-proposal`.
- Rama de tarea actual: `feature/git-traceability-git-events`.
- Propuesta funcional: `documents/git_traceability_functional_proposal__updated_20260807_185348.md`.
- Estado MVP: `documents/git_traceability_mvp_implementation_update__updated_20260807_190952.md`.

Git es la fuente de verdad de ramas, commits y merges. Brain es la fuente de
verdad de sesiones, contratos y gates. Este plan solo organiza la integración;
no sustituye ninguna de las dos fuentes.

## Topología aprobada

```text
main
  └── feature/git-traceability-functional-proposal  [PR parent]
        ├── feature/git-traceability-git-events     [current task]
        ├── feature/git-traceability-trailers       [next task]
        └── feature/git-traceability-reconciler     [future task]
```

Cada rama de tarea nace del último commit de la rama padre. La rama de tarea
contiene una sola unidad lógica, sus tests y la documentación necesaria.

## Workflow por tarea

1. Verificar que la rama padre esté limpia y registrar `git log
   origin/main..HEAD`.
2. Crear `feature/git-traceability-<task>` desde la rama padre.
3. Ejecutar Brain `resolve` y `gate --action write` antes de editar.
4. Aplicar código, tests y documentación de la tarea.
5. Ejecutar tests focales, suite completa, coverage y `git diff --check`.
6. Crear un commit atómico en la rama de tarea.
7. Mezclar la tarea en la rama padre con fast-forward cuando la validación pase.
8. Mantener el PR dirigido a `main`; no mezclar ramas de tarea directamente en
   `main`.

## Estado de tareas

| Tarea | Rama | Estado | Siguiente acción |
|---|---|---|---|
| GIT-003/004/009 | `feature/git-traceability-functional-proposal` | COMPLETADA | Incluida en commits `4ae0a47` y `ee90c4d` |
| GIT-005 | `feature/git-traceability-git-events` | EN IMPLEMENTACIÓN | Validar y fast-forward a rama padre |
| GIT-006 | `feature/git-traceability-trailers` | PLANIFICADA | Crear desde rama padre actualizada |
| GIT-007 | `feature/git-traceability-post-commit` | PLANIFICADA | Depende de GIT-005 y GIT-006 |
| GIT-008 | `feature/git-traceability-reconciler` | PLANIFICADA | Depende de eventos confirmados |

## Criterios de mezcla

Una tarea puede mezclarse en la rama padre solo si:

- el worktree está limpio salvo cambios intencionados antes del commit;
- no incluye coverage, tmp, outputs, secretos ni artefactos locales;
- tests focales y suite completa pasan;
- coverage mantiene el umbral Brain de 80%;
- la documentación y el manifest quedan alineados;
- `git diff --check` pasa;
- la tarea mantiene un único objetivo lógico.

## Riesgos y rollback

- Si la tarea falla, se conserva la rama de tarea y no se toca la rama padre.
- Si el fast-forward no es posible, se detiene la mezcla y se revisa divergencia;
  no se fuerza ni se reescribe historia.
- Un PR parcial se mantiene en la rama padre; hooks, dashboard y PR adapter no
  se mezclan hasta tener sus gates propios.

## Ownership y actualización

Owner técnico: `software_architect_agent` y mantenedor de Negrita Brain.

Actualizar este plan al crear, validar, mezclar o descartar cada rama `GIT-*`.
