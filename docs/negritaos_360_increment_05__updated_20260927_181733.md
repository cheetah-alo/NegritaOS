---
metadata:
  source: negritaos
  document_version: "1.0.0"
  generated_date: "2026-09-27"
  last_modified_date: "2026-09-27"
  project_id: negritaos
  document_class: source_documentation
  status: LOCAL_IMPLEMENTATION
  quality_gates_status: PASSED_WITH_WARNINGS
---

# NegritaOS 360 — incremento 05: proyectos y capacidades en modo Local

## Propósito, audiencia y alcance

Corregir el inventario local que inicialmente mostraba un solo proyecto y conectar la sección de agents, skills y rules priorizada por el usuario. Audiencia: owner, backend, frontend y QA. Continúa el [puente local](negritaos_360_increment_04__updated_20260927_173325.md) con las mismas restricciones de `127.0.0.1` y política Git-ignorada. No conecta sesiones Brain, actividad Git, mediciones de uso, outcomes de goals ni ejecución de agentes.

## Fuentes de verdad y comportamiento actual

- El directorio `projects/` contiene 25 YAML: 22 registros de proyecto con schema `project`, uno con schema heredado `project_registry` (`hot_frictions`) y dos índices de artefactos EL AL. Los índices no son proyectos y quedan fuera del catálogo. `dashboard_registry.parse_project_registry` admite los dos schemas de proyecto de forma explícita; nunca convierte `owner.client` heredado en un ID estable.
- La política local `.local/dashboard-access.json`, propiedad del usuario y modo `0600`, enumera los 23 IDs de proyecto. Está ignorada por Git y no se publica. Todos permanecen con cliente `unknown` porque sus registries no declaran `metadata.client_id`. El servidor lee sólo los IDs permitidos, no repositorios de clientes ni carpetas OneDrive externas.
- `dashboard_capability_catalog.py` compone la vista desde esos registries, `skills/catalog.yaml` y `integrator.yaml`. Expone sólo ID, nombre, proyecto, tipo y estado de configuración. Agentes canónicos presentes en `integrator` son `REGISTERED`; skills de la clausura de perfiles son `RESOLVED`; reglas globales y declaraciones heredadas son `DECLARED`. Un agente declarado en un proyecto pero ausente de `integrator` no se marca registrado.
- Reglas con referencias de archivo reciben un ID opaco derivado de hash y un nombre corto. No se envían rutas locales completas, prompts, contenido de reglas o secretos. El `view_sha256` se deriva sólo de los elementos visibles, sin hash ni fecha de fuente global.
- El servidor añade `GET /api/v1/capabilities` con filtros opcionales `project_id` y `kind=agent|skill|rule`; errores JSON genéricos. El frontend valida la respuesta, filtra dentro del ámbito autorizado y muestra conteos por tipo. Su selector de proyecto se comparte con el catálogo; el filtro de cliente usa únicamente los proyectos que ya recibió del endpoint autorizado.

En la comprobación local se mostraron **23 proyectos** y **630 relaciones proyecto-capacidad**: 228 agentes, 301 skills y 101 reglas. Son filas por proyecto, no 630 capacidades únicas ni evidencia de uso. Al elegir `NegritaOS`, la vista mostró 21 agentes, 11 skills y 4 reglas. Un estado `REGISTERED`, `RESOLVED` o `DECLARED` describe configuración; no afirma que se haya ejecutado, usado o validado la capacidad.

## Verificación

```sh
PYTHONPATH=src /Users/jackyb-cqi/repos/NegritaOS/.venv-pr-quality/bin/python -m unittest discover -s tests -p 'test_negrita_brain_dashboard_*.py'
node --test prototypes/negritaos360/*.test.mjs
```

Pruebas sintéticas cubren proyecto denegado, schema legado, perfil resuelto, agente no registrado, deduplicación, ID de regla opaco, hash estable si cambia una fuente oculta, filtros de endpoint y escape HTML. En navegador local se comprobó que la tabla de proyectos contiene 23 y Capacidades 630 relaciones, además del filtro a NegritaOS. Estas cifras se derivan de configuración local en el worktree actual y cambiarán si se modifica la política o las fuentes.

## Ownership, límites y siguiente tarea

Backend mantiene el adapter y el endpoint; frontend mantiene la presentación y el estado de filtros; QA comprueba autorización, procedencia y que no se confunda configuración con uso. Los clientes aún no tienen una tabla/ID canónico en todos los registries: la columna muestra `Sin clasificar`, no nombres inferidos. Para completarla, el owner debe definir las asociaciones cliente/proyecto de forma explícita y versionada.

Las otras secciones Local siguen pendientes: Knowledge Graph, Brain/sesiones/Git, planes versionados y goals. La siguiente entrega puede añadir el read model de Brain/Git con referencias mínimas o el contrato de cliente. Actualizar este documento cuando se añadan fuentes de capacidades, cambie la semántica de estados o se configure un cliente real. La aplicación continúa sólo en loopback.
