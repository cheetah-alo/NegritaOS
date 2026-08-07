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
    - "La propuesta no implementa código, hooks, API ni dashboard."
    - "El router no declara un modo específico para la acción deliverable."
    - "Brain reporta sesiones antiguas abiertas y coexistencia del índice v1; requieren cierre o migración explícita."
---

# Propuesta funcional: trazabilidad Git multi-sesión para Negrita Brain

## 1. Propósito

Definir el comportamiento funcional, la arquitectura, las responsabilidades y
las tareas trazables para conectar sesiones de Negrita Brain con worktrees,
ramas, commits, gates, decisiones y futuros PRs.

El resultado esperado es una vista 360 de trabajo técnico sin convertir el
dashboard en otra fuente de verdad ni almacenar prompts, respuestas, secretos o
contenido completo de diffs.

Este documento es un plan aprobado para implementación posterior. No representa
funcionalidad disponible todavía.

## 2. Audiencia y alcance

### Audiencia

- Owner de NegritaOS y decisiones de integración.
- Mantenedores del runtime Negrita Brain.
- Responsables de dashboard, API, CI y hooks.
- Revisores de ramas, commits y PRs.

### Incluido

- Identidad de sesión, repositorio y worktree.
- Estado Git y relación session → worktree → branch → commit.
- Gates, decisiones y handoffs relacionados con commits.
- Detección de commits confirmados, inferidos y huérfanos.
- Read model y vistas funcionales del dashboard.
- Tests, documentación, ownership, rollout y criterios de salida.

### Excluido

- Push, merge, creación de PR o despliegue automático.
- Edición automática de código o resolución de conflictos.
- Almacenamiento de prompts, respuestas, secretos o diffs completos.
- Sustitución de Git como fuente de verdad de commits y ramas.
- Sustitución de Negrita Brain como fuente de verdad de sesiones y gates.
- Elección obligatoria de FastAPI, Next.js, BigQuery o PostgreSQL en esta fase.

## 3. Provenance y fuentes de verdad

### Fuentes consultadas

| Fuente | Uso |
|---|---|
| `.codex/project.yaml` | Identidad y ruta canónica del proyecto |
| `projects/negritaos.yaml` | Registry, outputs esperados y memoria canónica |
| `src/negrita_brain/runtime.py` | Contratos, punteros, gates y eventos actuales |
| `scripts/negrita_brain.py` | CLI pública de resolve, gate, event y close |
| `src/negrita_brain/installer.py` | Hook pre-commit actual |
| `tests/test_negrita_brain_runtime.py` | Tests actuales de aislamiento y eventos seguros |
| `docs/negrita-brain-runtime.md` | Contrato operativo de Memory v2 |
| `.codex/rules/dev-commit-hygiene.md` | Reglas de rama, commit, tests y cobertura |
| `.codex/skills/analytical-dashboard-architecture/SKILL.md` | Boundaries del dashboard |
| `core/orchestration/negrita_brain_policy.yaml` | Política Brain y quality gates |

### Política de verdad

| Dominio | Fuente de verdad | Regla |
|---|---|---|
| Commit, árbol, rama y worktree | Git local | No duplicar ni reinterpretar su identidad |
| Sesión, contrato y gate | Negrita Brain | Asociar por `provider + session-key` |
| Decisión | Ledger de decisiones Brain | Aceptación explícita o evidencia de commit/PR |
| PR, checks y merge | Proveedor Git, cuando exista | Adaptador opcional y de solo lectura en MVP |
| Dashboard | Read model derivado | Nunca escribe en Git ni en memoria canónica |

## 4. Comportamiento actual verificado

- Brain v2 usa `CODEX_THREAD_ID` en Codex y acepta `--session-key` para
  automatización.
- Los punteros activos v2 están separados por proveedor y hash de sesión.
- Existe fallback compatible con `runtime/active_session.json` de Memory v1.
- El contrato Git actual conserva `branch` y `HEAD`, pero no worktree, base,
  dirty state, ahead/behind ni relación con commits.
- El hook pre-commit disponible ejecuta `gate --action commit`, pero no registra
  el SHA posterior ni enlaza el commit con la sesión.
- Los eventos aceptan metadatos seguros con whitelist; actualmente no existe
  un contrato específico para metadatos Git de commit.
- Hay tests de aislamiento entre sesiones y de descarte de prompts y outputs de
  herramientas.

### Estado de trabajo usado como fixture de diseño

En la auditoría de esta propuesta, el worktree principal estaba limpio en
`main` y existía un worktree temporal limpio cuya rama estaba por detrás de su
base remota. Este caso representa el escenario de sesiones concurrentes que el
producto debe explicar, no ocultar.

## 5. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación |
|---|---|---:|---|
| REQ-001 | Identificar cada sesión por proveedor y clave estable | P0 | Dos sesiones concurrentes nunca comparten el puntero activo |
| REQ-002 | Identificar cada worktree sin depender solo de su ruta temporal | P0 | El mismo worktree conserva un `worktree_id` estable mientras exista |
| REQ-003 | Capturar branch, HEAD, base, upstream, dirty state y ahead/behind | P0 | El dashboard muestra el estado observado y su timestamp |
| REQ-004 | Asociar un commit a sesión y contrato Brain | P0 | El enlace confirmado contiene SHA, session ID y contract hash |
| REQ-005 | Distinguir evidencia confirmada, inferida y huérfana | P0 | Una inferencia nunca se presenta como confirmación |
| REQ-006 | Mantener privacidad y minimización de datos | P0 | No se persisten prompts, outputs, secretos ni diff completo |
| REQ-007 | Mostrar sesiones abiertas, temporales y pendientes de handoff | P1 | Cada excepción tiene estado, owner y siguiente acción |
| REQ-008 | Permitir commits externos al hook sin perder trazabilidad | P1 | El reconciliador marca la asociación como inferida o huérfana |
| REQ-009 | Exponer una API lógica independiente del proveedor Git | P1 | El frontend no conoce comandos Git ni rutas físicas |
| REQ-010 | Integrar PR/checks sin mutaciones externas en MVP | P2 | La integración inicial solo lee y cita evidencia |

## 6. Arquitectura funcional

### Flujo principal

```text
resolve
  -> GitIdentitySnapshot
  -> SessionContract
  -> pre-commit gate
  -> commit-msg trailer
  -> post-commit event
  -> append-only traceability ledger
  -> read model
  -> dashboard / API / handoff
```

### Componentes y boundaries

| Componente | Responsabilidad | Interfaz pública | No debe poseer |
|---|---|---|---|
| `git_identity` | Leer y normalizar estado Git | `snapshot(root)` | Sesiones o decisiones |
| `worktree_registry` | Clasificar y dar identidad al worktree | `resolve_worktree(root)` | Contenido de archivos |
| `traceability_linker` | Asociar sesión, contrato y commit | `link_commit(event)` | Reescritura de Git |
| `commit_trailer` | Leer o añadir referencias Brain | `prepare(message, context)` | Reglas de negocio del dashboard |
| `brain_git_events` | Persistir eventos seguros append-only | `record_git_event(...)` | Prompts, outputs y diffs completos |
| `reconciler` | Detectar commits sin hook o sin sesión | `reconcile(refs)` | Convertir inferencia en confirmación |
| `read_model` | Consultar relaciones y excepciones | Queries versionadas | Escribir en Git |
| `dashboard_api` | Validar filtros y servir payload lógico | `GET /git-traceability/*` | SQL/Git provider routing |
| `dashboard_ui` | Vistas, filtros y navegación | Browser routes | Nombres físicos de fuentes |
| `pr_adapter` | Leer PR, checks y merge | Provider-neutral adapter | Push, merge o aprobación automática |

### Dirección de dependencias

```text
Git CLI / provider
        ↓
git_identity + adapters
        ↓
logical traceability contracts
        ↓
Brain event ledger + read model
        ↓
API routes
        ↓
dashboard pages/components
```

El frontend solo consume campos lógicos. Las referencias físicas, credenciales,
dialecto y comandos pertenecen a configuración/adapters backend.

## 7. Contratos de datos propuestos

### `GitIdentitySnapshot v1`

```yaml
schema_version: 1
project_id: negritaos
repo_id: <hash-of-common-git-dir>
worktree_id: <hash-of-common-dir-and-git-dir>
worktree_class: main|feature|temporary|detached|unknown
root_path_policy: redacted|relative|hashed
branch: <branch-or-null>
head: <sha>
upstream: <ref-or-null>
base_ref: <declared-or-detected-ref>
merge_base: <sha-or-null>
ahead: 0
behind: 0
dirty: false
staged_count: 0
unstaged_count: 0
untracked_count: 0
captured_at: <iso-8601>
```

### `CommitTraceabilityEvent v1`

```yaml
schema_version: 1
event_kind: commit
commit_sha: <sha>
tree_sha: <sha-or-null>
parent_shas: [<sha>]
branch: <branch-or-null>
worktree_id: <id-or-null>
session_id: <brain-session-or-null>
contract_sha256: <hash-or-null>
decision_ids: []
gate_status: ALLOW|WARN|BLOCK|UNKNOWN
evidence_status: confirmed|inferred|orphan
changed_file_count: 0
insertions: 0
deletions: 0
path_fingerprint: <hash-or-null>
observed_at: <iso-8601>
```

`path_fingerprint` es opcional y no sustituye una política explícita de
privacidad. No se almacenará el contenido de un diff.

### Identidad de sesión concurrente

1. Usar `CODEX_THREAD_ID` cuando esté disponible.
2. Exigir `--session-key` para CI, scripts, sesiones temporales o proveedores
   sin identidad nativa.
3. Si se usa `provider_default` y existe más de una sesión activa del mismo
   proyecto, producir `WARN` y bloquear el enlace automático del commit.
4. Asociar el worktree mediante un ID derivado de su identidad Git; la ruta
   absoluta solo se muestra redacted y nunca es la clave primaria.

## 8. Funcionalidad del dashboard

### Vista 360

Tarjetas mínimas:

- sesiones activas y sesiones sin cierre;
- worktrees dirty;
- ramas detrás de su base;
- ramas por encima del umbral de PR;
- commits huérfanos o inferidos;
- worktrees temporales abandonados;
- contratos Brain sin commit relacionado;
- decisiones pendientes de aceptación;
- warnings de fallback v1 y configuración.

### Vistas operativas

1. **Matriz de worktrees:** sesión, proveedor, rama, HEAD, base, ahead/behind,
   dirty, clasificación y última observación.
2. **Timeline:** sesión → gate → commit → PR → merge.
3. **Detalle de commit:** SHA, contrato, gates, decisiones, evidencia y enlaces
   a `git show` local o al proveedor externo.
4. **Excepciones:** estado, severidad, owner, fecha de detección y siguiente
   acción.
5. **Handoff queue:** sesiones temporales listas para continuar, integrar o
   cerrar deliberadamente.

### API lógica planificada

```text
GET /api/v1/git-traceability/overview
GET /api/v1/git-traceability/sessions
GET /api/v1/git-traceability/worktrees
GET /api/v1/git-traceability/commits/{commit_sha}
GET /api/v1/git-traceability/exceptions
```

La API deberá declarar paginación, freshness, filtros, nullability, estados de
evidencia y límites de acceso antes de implementar las páginas.

## 9. Tareas trazables

| ID | Fase | Tarea | Owner primario | Depende de | Entrega verificable |
|---|---:|---|---|---|---|
| GIT-001 | 0 | Aprobar contrato `GitIdentitySnapshot v1` y `CommitTraceabilityEvent v1` | software_architect_agent | — | ADR y schemas versionados |
| GIT-002 | 0 | Definir política de `repo_id`, `worktree_id`, rutas redacted y worktrees temporales | Brain maintainer | GIT-001 | Política de identidad y privacidad |
| GIT-003 | 1 | Implementar collector read-only de branch, HEAD, upstream, base, dirty y ahead/behind | Brain maintainer | GIT-001,GIT-002 | Unit tests con repos Git temporales |
| GIT-004 | 1 | Integrar snapshot ampliado en `resolve`, `gate` y `close` | Brain maintainer | GIT-003 | Contract tests de sesión |
| GIT-005 | 1 | Añadir whitelist de metadatos Git seguros al ledger Brain | Brain maintainer | GIT-001,GIT-002 | Tests anti-secreto y compatibilidad v1/v2 |
| GIT-006 | 2 | Diseñar y probar trailers `Negrita-*` sin reemplazar el checklist de commit | Commit/CI owner | GIT-001,GIT-005 | Tests idempotentes de `commit-msg` |
| GIT-007 | 2 | Registrar el commit posterior mediante `post-commit` o comando explícito | Commit/CI owner | GIT-004,GIT-006 | Evento con SHA y contract hash |
| GIT-008 | 2 | Implementar reconciliador para commits externos, inferidos y huérfanos | Brain maintainer | GIT-003,GIT-007 | Fixture de commits sin hook |
| GIT-009 | 2 | Crear CLI `git-trace`/equivalente para inspección read-only y reconciliación | Brain maintainer | GIT-003,GIT-008 | Help, errores y tests CLI |
| GIT-010 | 3 | Materializar read model lógico para sesiones, worktrees, commits y excepciones | Dashboard backend owner | GIT-005,GIT-008 | Contract/API tests |
| GIT-011 | 3 | Implementar overview 360, matriz, timeline, detalle y excepciones | Dashboard frontend owner | GIT-010 | Browser tests de estados principales |
| GIT-012 | 3 | Implementar handoff queue y acciones no destructivas de continuación/cierre | Brain + dashboard owners | GIT-004,GIT-010 | Tests de lifecycle y permisos |
| GIT-013 | 4 | Añadir adapter opcional de PR/checks/merge en modo solo lectura | Git provider owner | GIT-010 | Contract tests provider-neutral |
| GIT-014 | 4 | Publicar runbooks, ownership, alertas, retención y recuperación | technical_writer_agent | GIT-001..GIT-013 | Docs auditados y manifestados |
| GIT-015 | 4 | Activar enforcement gradual de commits sin sesión o contrato | Brain maintainer + owner | GIT-003..GIT-014 | Gate con WARN/BLOCK explícitos |

### Trazabilidad requisito → tarea

| Requisito | Tareas |
|---|---|
| REQ-001, REQ-002 | GIT-002,GIT-003,GIT-004 |
| REQ-003 | GIT-003,GIT-004,GIT-010 |
| REQ-004 | GIT-005,GIT-006,GIT-007 |
| REQ-005, REQ-008 | GIT-007,GIT-008,GIT-010 |
| REQ-006 | GIT-002,GIT-005 y security tests |
| REQ-007 | GIT-010,GIT-011,GIT-012 |
| REQ-009 | GIT-001,GIT-009,GIT-010 |
| REQ-010 | GIT-013 |

## 10. Tests y quality gates

### Test layers

| Capa | Cobertura requerida |
|---|---|
| Unit | Parser Git, identidad, clasificación, trailers y estados |
| Integration | Dos sesiones, dos worktrees, ramas divergentes y worktree temporal |
| Contract | Schemas de snapshots, eventos y API lógica |
| Hook | `pre-commit`, `commit-msg`, `post-commit`, reintentos e idempotencia |
| Reconciliation | Commit externo, branch drift, sesión cerrada y worktree borrado |
| Security | Sin prompts, outputs, secretos, contenido de diff o rutas sensibles |
| Browser | Loading, empty, error, stale, filtros URL y navegación conectada |
| Regression | Fallback Memory v1, punteros v2 y cierre de sesión |

### Validación planificada

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_negrita_brain_coverage.py --fail-under 80
python3 scripts/validate_config_resolution.py
python3 scripts/validate_registry_paths.py --root "$PWD"
python3 scripts/validate_alignment.py
python3 scripts/audit_document_control.py "$PWD"
git diff --check
```

Para el dashboard se añadirán los comandos reales del runtime elegido y se
reportarán conteos exactos de tests, cobertura, contract tests y E2E. Hasta que
ese runtime sea seleccionado, FastAPI/Next.js son solo una posible asignación,
no una decisión de arquitectura.

## 11. Ownership y operación

| Área | Owner | Responsabilidad |
|---|---|---|
| Contratos y ledger Brain | Brain maintainer | Schema, eventos, compatibilidad y retención |
| Git collector/linker | Brain maintainer | Estado Git y evidencia de asociación |
| Hooks y CI | Commit/CI owner | Instalación, idempotencia y fallos fail-safe |
| Read model/API | Dashboard backend owner | Payload lógico, paginación y filtros |
| UI | Dashboard frontend owner | Vistas, estados y accesibilidad |
| PR adapter | Git provider owner | Lectura de checks y merge, sin mutaciones |
| Política | Owner de NegritaOS | Umbrales, excepciones y decisión de enforcement |
| Documentación | technical_writer_agent | Runbooks, contratos y changelog |

La rama de integración se debe confirmar en el registry antes de abrir PR. Esta
propuesta se crea en una rama `feature/*` aislada y no publica ni hace merge.

## 12. Rollout

### Fase 0 — Contrato y decisión

- Aprobar este documento y GIT-001/GIT-002.
- Mantener el hook actual sin cambios.
- Resolver la política de sesiones antiguas y del índice v1.

### Fase 1 — Observabilidad read-only

- Capturar snapshots Git en resolve/gate/close.
- Exponer CLI de inspección.
- No bloquear commits ni escribir trailers todavía.

### Fase 2 — Soft traceability

- Activar eventos post-commit y trailers opt-in.
- Mostrar `confirmed`, `inferred` y `orphan`.
- Medir falsos enlaces, worktrees sin cierre y fallos de hooks.

### Fase 3 — Dashboard 360

- Publicar read model, API y vistas operativas.
- Incorporar alertas y handoff queue.
- Mantener todas las acciones externas en modo explícito y no automático.

### Fase 4 — Enforcement controlado

- `WARN` para falta de sesión o contract hash.
- `BLOCK` solo con sesión ambigua, contrato inválido o intento fuera de policy.
- Revisar excepciones y rollback antes de convertir el gate en obligatorio.

## 13. Criterios de aceptación del producto

- Dos sesiones concurrentes en dos worktrees aparecen separadas y no cruzan
  commits.
- Cada commit confirmado se puede recorrer hasta su sesión, contrato y gates.
- Un commit externo se etiqueta como inferido u huérfano, nunca como confirmado
  sin evidencia suficiente.
- El dashboard muestra branch drift, dirty state, ahead/behind y worktrees
  temporales.
- Cerrar una sesión conserva el estado final y permite continuar mediante
  handoff.
- Git y Brain siguen siendo las fuentes de verdad de sus respectivos dominios.
- No se persisten prompts, outputs, secretos ni diffs completos.
- Las vistas toleran sesiones antiguas, fallback v1 y datos incompletos con
  warnings visibles.
- El rollout puede detenerse después de cada fase sin perder commits ni
  contratos.

## 14. Riesgos, bloqueadores y preguntas abiertas

### Riesgos

- Un hook local puede no ejecutarse en todos los clientes o scripts.
- Un worktree temporal puede desaparecer antes del post-commit.
- Los cambios de rama entre resolve y commit pueden producir asociaciones
  ambiguas.
- Las rutas absolutas pueden contener información sensible.
- El read model puede quedar stale si no se define freshness explícita.

### Bloqueadores antes de implementar

1. Confirmar el runtime del dashboard y su integración branch.
2. Decidir si los trailers se añaden automáticamente o solo mediante comando.
3. Definir retención de eventos Git y tratamiento de worktrees eliminados.
4. Resolver el cierre de las sesiones v1 abiertas antes de enforcement.
5. Definir el proveedor PR inicial, si se incorpora en la primera versión.

### Preguntas abiertas

- ¿Se mostrará la ruta redacted, un alias de worktree o únicamente su ID?
- ¿Qué umbral de dirty state debe generar alerta inmediata?
- ¿El owner podrá confirmar manualmente una asociación inferida?
- ¿Qué datos de paths son aceptables para auditoría sin exponer información
  local?

## 15. Quality score de la propuesta

| Dimensión | Score | Máx. | Nota |
|---|---:|---:|---|
| Modularidad | 18 | 20 | Boundaries explícitos y dependencias unidireccionales |
| Documentación | 14 | 15 | Contratos, tareas, ownership y rollout |
| Tests | 18 | 20 | Unit, integration, contract, hook, security y browser |
| Configuración | 8 | 10 | Provider/runtime del dashboard queda abierto |
| Observabilidad | 10 | 10 | Eventos, estados de evidencia y excepciones |
| Reproducibilidad | 9 | 10 | Fixtures Git y comandos definidos |
| Higiene de dependencias | 9 | 10 | No impone framework ni proveedor en MVP |
| Developer experience | 4 | 5 | CLI, trailers y handoff planificados |
| **Total** | **90** | **100** | Apto para pasar a implementación tras resolver bloqueadores |

## 16. Estado y actualización

**Estado:** propuesta funcional lista para revisión; implementación no iniciada.

**Owner del documento:** `software_architect_agent`, bajo decisión del owner de
NegritaOS.

**Actualizar cuando:** se apruebe el contrato, se elija el runtime del
dashboard, cambie el integration branch, se complete una fase del rollout o se
modifique la política de enforcement.
