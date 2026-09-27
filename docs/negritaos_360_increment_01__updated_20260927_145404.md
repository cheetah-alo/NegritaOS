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

# NegritaOS 360 — incremento 01: contratos y catálogo de proyectos

## Propósito y alcance

Implementar la primera parte de `CAT-001`, `TRK-001` y `TRK-002` del [plan aceptado](negritaos_360_design_decision__updated_20260927_143145.md). El destinatario es el equipo que construirá el read model y la activación de planes. Este incremento define datos y validaciones puras; no conecta aún la interfaz ni modifica un proyecto real.

## Fuentes y contrato actual

- [Contratos tipados](../src/negrita_brain/dashboard_contracts.py): referencias de cliente/proyecto, goal, diseño, funcionalidades, criterios, revisión de plan, activación, observación de outcome y evidencia. Las definiciones son dataclasses inmutables con enums y IDs tipados.
- [Adapter de registry](../src/negrita_brain/dashboard_registry.py): lee exclusivamente un conjunto de archivos pasado por el llamador. `project.id`, `project.name` y `project.metadata.client_id` son los campos permitidos para el catálogo. El rótulo heredado `project.client` no se convierte en identidad estable.
- Cliente: `known` sólo con `metadata.client_id` explícito; `internal` con ID `internal`; sin ID, `unknown`. El `ProjectRef` puede conservar un cliente desconocido para lectura. La activación de un plan exige cliente explícito.
- `validate_activation_preflight(plan)` verifica owner, alcance/exclusiones con texto real, goal medible y fuente, diseño funcional versionado con SHA-256 y contenido real, criterios, referencias a la versión correcta, IDs únicos, dependencias y ciclos. `target=0` es válido; desconocido, booleano, infinito o NaN no lo son. Cliente `None`, clasificación inconsistente, IDs o revisiones vacías, e identidad/hash de diseño desconocidos bloquean activación.
- `ActivationRecord` y `GoalObservation` son contratos separados de `PlanRevision`. Un porcentaje de funcionalidades entregadas no se interpreta como logro del goal.

Los DTOs del adapter no son una API pública ni una comprobación de autorización. El llamador debe limitar la visibilidad por cliente y proyecto antes de presentar nombres. Ninguna ruta local, secreto o contenido anidado del registry se incorpora al DTO.

## Verificación local

```sh
PYTHONPATH=src /Users/jackyb-cqi/repos/NegritaOS/.venv-pr-quality/bin/python -m unittest discover -s tests -p 'test_negrita_brain_dashboard_*.py'
```

Resultado tras las correcciones del revisor: **28/28 pruebas Python**. La maqueta mantuvo **19/19 pruebas Node** con `node --test prototypes/negritaos360/state.test.mjs prototypes/negritaos360/tracking.test.mjs`. `git diff --check` limpio. Ruff no estaba instalado en la venv y no se ejecutó; no se atribuye un lint PASS.

Las pruebas son sintéticas. No hay test de permisos, concurrencia, persistencia, API, métricas reales ni navegador conectado. El prototipo sigue local y no se incluye en el commit de estos contratos. La validación de PR/release y los controles de distribución de fuentes permanecen pendientes.

## Ownership, riesgos y siguiente tarea

Arquitectura NegritaOS mantiene los contratos; el backend del dashboard mantiene el adapter y el futuro read model; QA verifica aislamiento y versionado. El siguiente incremento `CAT-005` deberá construir un snapshot/DTO autorizado a partir de estas clases, con pruebas de scoping, campos minimizados y estados de lectura. `TRK-003` añadirá transiciones con permisos, compare-and-swap e idempotencia antes de permitir activar planes reales.

Actualizar este documento mediante una versión nueva cuando cambie la semántica de cliente, la prevalidación o la fuente autorizada. No inferir cliente desde ruta, nombre, organización o identidad Git.
