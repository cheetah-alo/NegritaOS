---
metadata:
  source: codex_claude
  document_version: "1.1.0"
  generated_date: "2026-08-08"
  last_modified_date: "2026-08-08"
  agent_id: software_architect_agent
  router_mode: CR
  project_id: negritaos
  template_used: templates/repo_architecture_blueprint_template.md
  quality_gates_status: PASSED_WITH_WARNINGS
  quality_warnings:
    - "La rama padre no tiene upstream remoto ni PR publicado."
    - "El hook post-commit, reconciliador, read model y dashboard siguen pendientes."
---

# Actualización de implementación MVP: Git Traceability

## Propósito

Registrar el estado verificable de la propuesta de trazabilidad Git después de
completar `GIT-005` y `GIT-006`. Git continúa siendo la fuente de verdad de los
commits y Brain añade contexto seguro de sesión, contrato y worktree.

## Fuente de verdad y commit de implementación

- Propuesta funcional: `documents/git_traceability_functional_proposal__updated_20260807_185348.md`.
- Plan de ramas: `documents/git_traceability_branching_plan__updated_20260808_160407.md`.
- Commit de implementación GIT-006: `724d779`.
- Contrato y runtime: `src/negrita_brain/runtime.py`.
- Snapshot Git: `src/negrita_brain/git_traceability.py`.
- Trailers: `src/negrita_brain/git_trailers.py`.
- CLI: `scripts/negrita_brain.py`.

## Funcionalidad implementada

### Eventos Git seguros

`record_event` mantiene una whitelist explícita para eventos `commit`,
`git_snapshot` y `git_reconciled`. Los valores Git se validan por tipo, tamaño y
forma; el evento recibe el hash del contrato y defaults de branch, base, merge
base y worktree desde el contrato activo.

### Trailers Negrita v1

`src/negrita_brain/git_trailers.py` incorpora:

- `parse_trailers(message)`, limitado a claves `Negrita-*` soportadas;
- `append_trailers(message, trailers)`, que solo añade claves ausentes, no
  reemplaza valores existentes y es idempotente;
- `build_brain_trailers(contract, gates, decision_ids)`, que deriva contrato,
  sesión, worktree, gates y decisiones sin consultar ni mutar Git.

Las claves soportadas son `Negrita-Contract`, `Negrita-Session`,
`Negrita-Worktree`, `Negrita-Gates` y `Negrita-Decision`. El comando read-only
para inspeccionar los valores derivados es:

```bash
python3 scripts/negrita_brain.py git-trailers --root "$PWD" \
  --provider codex --gate write --gate commit --decision-id GIT-006
```

GIT-006 no activa todavía un hook obligatorio. El commit de implementación sí
incluye trailers reales parseables por Git como evidencia del contrato, sesión,
worktree, gates y decisión usados.

## Tareas y estado

| ID | Estado | Evidencia |
|---|---|---|
| GIT-003 | COMPLETADA | Collector, parser de status y tests con subprocess mockeado |
| GIT-004 | COMPLETADA | `resolve` persiste el snapshot en el contrato |
| GIT-009 | COMPLETADA | Comando `git-trace` y test de gramática CLI |
| GIT-005 | COMPLETADA | Whitelist y defaults seguros para eventos Git en `runtime.py` |
| GIT-006 | COMPLETADA | Parser/builder idempotente, CLI `git-trailers`, tests y commit con trailers |
| GIT-001 | PARCIAL | Campos v1 implementados; ADR y schema formal siguen pendientes |
| GIT-002 | PARCIAL | IDs hasheados y clasificación temporal implementados; política formal pendiente |
| GIT-007 | PLANIFICADA | Registro post-commit opt-in y evidencia de árbol |
| GIT-008 | PLANIFICADA | Reconciliación de commits externos o sin sesión |
| GIT-010..GIT-015 | PLANIFICADA | Read model, dashboard, PR adapter, runbooks y enforcement |

## Validación ejecutada

```text
python3 -m unittest discover -s tests -p 'test_*.py'  # 98/98 OK
python3 scripts/check_negrita_brain_coverage.py --fail-under 80  # 81.20%
python3 scripts/audit_document_control.py "$PWD"  # 4/4 válidos antes de esta versión
python3 -m compileall -q src scripts tests  # OK
git diff --check  # OK
```

También se verificó la salida del CLI `git-trailers` y que `git` reconoce los
cinco trailers del commit `724d779`.

## Limitaciones conocidas

- La rama aún no tiene upstream y no se ha creado PR ni push remoto.
- El builder es read-only; el hook automático queda para `GIT-007`.
- El reconciliador de eventos externos queda para `GIT-008`.
- No hay todavía read model, API ni dashboard 360 sobre estos eventos.

## Ownership y siguiente paso

Owner técnico: `software_architect_agent` junto con el mantenedor de Brain.

Siguiente corte recomendado: crear `feature/git-traceability-post-commit` para
registrar el commit confirmado de forma opt-in, usando este builder y la
whitelist de eventos ya existente.
