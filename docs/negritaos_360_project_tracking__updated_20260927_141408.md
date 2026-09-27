---
metadata:
  source: negritaos
  document_version: "1.3.0-design-proposal"
  generated_date: "2026-09-27"
  last_modified_date: "2026-09-27"
  project_id: negritaos
  document_class: decision_documentation
  status: PROTOTYPE_FOR_USER_REVIEW
  baseline: docs/negritaos_360_ux_plan_review__updated_20260927_134112.md
  quality_gates_status: NOT_RELEASE_CERTIFIED
---

# Decision Memo — clientes, planes activables y diseño Tepulume

> **TL;DR:** el seguimiento propuesto une cliente → proyecto → goal → versión del plan → funcionalidades → evidencia. La versión activa no cambia cuando se propone otra. Entrega validada y logro del objetivo son métricas distintas.

## Context

Audiencia: owner de NegritaOS, diseño, arquitectura, backend y QA. El usuario pidió probar el sistema visual de Tepulume, añadir seguimiento activable por proyecto, definir goal/diseño/funcionalidades y versionar los cambios. Después pidió añadir cliente a cada proyecto.

Ámbito actual: maqueta local, sintética y volátil. No modifica los registries, proyectos reales, Brain, Git ni Tepulume. No crea un goal ejecutable en Codex ni programa automatizaciones. Extiende el [plan UX previo](negritaos_360_ux_plan_review__updated_20260927_134112.md), que sigue vigente para CAT/FLOW/KNOW. Este memo prevalece para el diseño visual alternativo y el nuevo seguimiento propuesto, no como aprobación de arquitectura de producción.

### Fuentes de diseño verificadas

- Repositorio de referencia: `/Users/jackyb-cqi/repos/backup_repos/tepulume` (sólo lectura).
- `tepulume-landing/app/brand-tokens.css`: azul petróleo `#0d6684`, magenta `#c81f68`, fondo cálido `#f7f6f5`, superficies blancas, radios 2–4 px y espacios 4/8/12/16/24/32.
- `tepulume-landing/app/brand.css`: tipografía recta, sin cursivas, bordes discretos, controles sobrios y sin sombras decorativas.
- `tepulume-landing/app/layout.tsx`: Montserrat para títulos e Instrument Sans para texto.
- `tepulume-landing/app/enterprise.css`: jerarquía legible, densidad sobria y variante web pública más blanca.
- `JBNegritaOS.zip`: inspección de inventario, theme y ejemplo de cards. Su tema Broadsheet usa otro par tipográfico; para esta variante se eligió la implementación vigente de la landing, no ese tema archivado.

Huellas de las dos fuentes principales al inspeccionar:

```text
brand-tokens.css 390b6f5ce01f56ea984b639ca33274b1ea31e312e8fb08a74b712a289e8591e9
brand.css        6d0cc822bda78df09e24cde399da3956f9b9a292a8beddaf240dd309e1ae7573
```

Las fuentes tipográficas existentes se copiaron localmente desde `documents/lubricantes_venezuela/reproducibilidad/` dentro del repositorio de referencia. Sólo los dos TTF, ningún documento, imagen de persona o contenido comercial. Los TTF están ignorados en Git; revisar licencias/distribución antes de promoverlos. La demo no solicita fuentes a Google ni a un CDN. La marca visible sigue siendo NegritaOS.

## Decision Required

Aceptar o ajustar: variante Tepulume, jerarquía por cliente/proyecto y flujo de activación/versionado. Esta revisión no autoriza ingestión de clientes, persistencia real, despliegue ni automatización. Los nombres Cliente demo A/B, Atlas/Brisa/Faro son ficticios.

## Options

| Opción | Ventaja | Riesgo / decisión |
|---|---|---|
| Plan versionado y medición por evidencia — recomendada | Historial explicable y alcance estable | Requiere contratos, aceptación y trazabilidad explícitos |
| Checklist editable sin versiones | Inicio rápido | Pierde la línea base y permite mover la meta sin rastro |
| Progreso inferido desde commits | Automatismo aparente | Un commit no demuestra aceptación ni resultado; descartado |

## Recommendation

### 1. Jerarquía y pertenencia

```text
ClientId
└── ProjectId (canónico, estable)
    └── GoalId + GoalRevision
        └── PlanId + PlanRevision
            ├── DesignRevision
            ├── FeatureId + AcceptanceRevision
            │   └── TaskId → Git/session refs → tests → EvidenceReceipt
            └── ActivationRecord + ChangeRequest + ProgressSnapshot
```

Cada proyecto pertenece a **un cliente primario** en el MVP. Un cliente agrupa muchos proyectos. Trabajos internos usan una entidad explícita `internal`, no un cliente inventado. La asociación real cliente/proyecto se resuelve desde un registry autorizado, nunca del nombre de una carpeta. Cambiar esa asociación exige auditoría; no renombra el ID del proyecto ni mueve su historia.

La demo muestra cliente en inventario, fichas y seguimiento. Cambiar el filtro cliente reinicia el proyecto seleccionado y restringe catálogo, grafos y seguimiento. Esto demuestra navegación, **no autorización multi-tenant**. El backend futuro debe aplicar permisos antes de entregar cualquier DTO. Clientes, owners y rutas corporativas no deben filtrarse a Git público; los fixtures del código siguen siendo sintéticos.

### 2. Definición mínima para activar

| Objeto | Campos obligatorios del contrato futuro |
|---|---|
| Goal revision | ID, propósito, métrica, unidad, dirección, target, ventana, baseline o `unknown`, owner y fuente de medición |
| Plan revision | ID estable del plan, revision ID, parent revision, project/client scope, goal revision, alcance, exclusiones, dependencias, riesgos y owner |
| Design revision | Referencia versionada/hash, pantallas/estados, interacciones, accesibilidad, decisiones, límites y criterios funcionales |
| Feature specification | ID estable, goal mapping, descripción funcional, inputs/outputs, acceptance criteria versionados, design ref, owner, dependencias y tareas |
| Acceptance criterion | Condición verificable, prueba/observación requerida y versión del criterio |
| Activation record | Versión exacta aprobada, hash, actor autorizado, fecha UTC, motivo y permisos comprobados |

No activar si faltan objetivo medible, diseño, alcance, owner, funcionalidades o criterios. Tampoco si hay IDs duplicados, referencias rotas, dependencias cíclicas, proyecto incompatible o falta de permisos. El diseño puede estar aprobado antes de implementar; activar un plan **no** afirma que sus funcionalidades ya estén aceptadas.

La maqueta incluye un caso activo, otro activable y otro bloqueado por falta de diseño. Los escenarios son ejemplos, no decisiones del usuario sobre proyectos reales.

### 3. Lifecycle y cambios de alcance

Flujo propuesto: borrador → revisión → aprobado → activo → completado / pausado / cancelado. Un plan tiene como máximo una revisión activa; un proyecto puede tener varios planes con objetivos distintos. La demo sólo muestra un plan por proyecto.

Al activar, se congela la definición completa. El avance operacional vive en registros separados. Un cambio de goal, criterio, diseño o alcance crea una revisión nueva con autor, motivo, diff, impacto y parent revision. La candidata no sustituye automáticamente la activa. El owner revisa y acepta el cambio exacto antes de activarlo.

- **Añadir alcance:** conserva evidencia compatible y cambia el denominador sólo al activar. Ejemplo: 2/5 = 40 % pasa a 2/6 = 33 %. Es cambio de alcance, no pérdida del trabajo.
- **Cambiar criterio:** invalida la aplicabilidad de su evidencia anterior; ésta no se borra. La maqueta cambia F-02: 2/5 pasa a 1/5 en la nueva versión hasta revalidar.
- **Cambiar diseño o goal:** revisar qué criterios y evidencias dejan de ser aplicables. No heredar automáticamente una aprobación entre contratos distintos.
- **Retirar/cancelar funcionalidades:** cambio explícito con motivo y diff; no borrar el trabajo pendiente para subir el porcentaje.
- **Corrección editorial:** nueva revisión identificable, sin alterar acceptance keys si el contrato no cambia. El criterio de compatibilidad se valida en backend.
- **Rollback:** nueva activación autorizada con snapshot y motivo, no sobrescritura ni borrado. La demo no permite reactivar versiones históricas; este flujo queda pendiente.

El historial guarda denominadores, numeradores y versión correspondientes a cada evento/snapshot. No recalcular el pasado usando el alcance actual. El goal tiene mediciones propias y no se marca conseguido por completar tareas.

### 4. Medición de avance

MVP: **avance de entrega = funcionalidades aceptadas con evidencia vigente / funcionalidades de la revisión activa**. Peso igual por funcionalidad; desglose de tareas informativo. Un commit, una sesión abierta o una tarea en curso no suman aceptación. Sin plan activo: `not_active`; sin alcance: `not_applicable`; evidencia inaccesible/desactualizada: `unknown` o `stale`, no 0 ni aceptación automática.

Evidencia vinculada a `(project_id, feature_id, criterion_revision, design_revision, source_hash)`. Para migrar evidencia entre revisiones debe probarse compatibilidad; registrar la decisión. En la demo sólo se usa una `acceptanceKey` sintética para mostrar el comportamiento: **no es hash de seguridad ni receipt Brain**.

Tres lecturas distintas:

1. Entrega: pendiente/en curso/bloqueada/en revisión/aceptada, con versión y snapshot.
2. Resultado: métrica observada del goal frente a target, ventana y baseline.
3. Confianza: vigencia y cobertura de la evidencia, separadas del resultado.

No se mostrará un porcentaje agregado de clientes sumando planes heterogéneos. Portfolio: conteos de planes por estado, bloqueos y fechas explícitas. Pesos o hitos futuros requerirán contratos versionados y aprobación, no cambios ad hoc.

### 5. Diseño OO y boundaries futuros

Seguir `dataclass(frozen=True, slots=True)`, `Enum` y IDs tipados para definiciones. No construir una clase “ProjectManager” que mezcle todo. Adapters mediante `Protocol`; composición en vez de herencia extensa.

| Clase / componente propuesto | Responsabilidad | No debe hacer |
|---|---|---|
| `ClientRef`, `ProjectRef` | Identidad, pertenencia y clasificación | Cargar contenidos privados |
| `GoalSpec`, `DesignSpec`, `FeatureSpec`, `PlanRevision` | Definiciones inmutables/versionadas | Acumular estado mutable de ejecución |
| `ChangeRequest`, `ActivationRecord` | Diff, decisión y transición exacta | Aprobarse por existir un commit |
| `EvidenceReceipt`, `ProgressSnapshot`, `GoalObservation` | Evidencia y mediciones por versión/tiempo | Mezclar entrega con outcome |
| `PlanRepository` (Protocol) | Persistencia autorizada | Interpretar UI o calcular KPIs |
| `PlanActivationService` | Validaciones, permisos, compare-and-swap, idempotencia | Desplegar, ejecutar agentes o modificar Git |
| `ProgressCalculator` | Fórmula pura sobre snapshot autorizado | Inventar evidencia o consultar proveedores |
| `TrackingReadModel` | DTO de lectura minimizado | Exponer rutas, tokens, prompts o diffs |
| UI de seguimiento | Filtros, formularios y representación | Autoridad final de activación o aceptación |

Futuro flujo: `registro autorizado → validación de spec → repositorio de versiones → servicio de activación → proyección read-only → UI`. Las escrituras de plan se introducen como un nuevo servicio acotado; no convierten el dashboard entero en un editor de Brain/Git. El dashboard anterior era read-only: este cambio de alcance requiere revisión de permisos antes de una implementación conectada.

Futuro API deberá exigir `expected_active_revision`, `idempotency_key`, permisos por proyecto/cliente y transacción para cerrar carreras entre sesiones. El cambio de plan no activa automáticamente ningún worker. Git aporta refs opacas verificadas; Brain sigue siendo autoridad de sus sesiones/gates. Nunca sincronizar contenido de clientes a NegritaOS para alimentar el tracker.

### 6. UX actual y límites

Selector visual **Tepulume / Observatorio**, cliente/proyecto compartidos, pestañas Plan y objetivo / Funcionalidades / Versiones y cambios, ficha de criterio, propuesta de revisión y confirmación explícita de activación. El banner marca datos sintéticos. Las operaciones sólo afectan memoria de la página y se reinician al recargar; no se usa localStorage ni una API.

Se mantiene código modular: fixtures, lógica de simulación, vistas, controladores, estilos y pruebas separados. El prototipo no es un contrato backend completo, ni implementa permisos, dates/hashes auditables, edición libre del goal/diseño, varios planes por proyecto, persistencia o concurrencia real. No reutilizarlo como servicio productivo sin las tareas siguientes.

## Next Actions

| ID | Entrega / owner | Dependencia | Criterio de salida |
|---|---|---|---|
| UX-003 | Variante Tepulume / frontend | UX-001 | Comparación local disponible; aceptación visual pendiente |
| TRK-001 | Cliente ↔ proyecto / arquitectura | Registry y CAT-001 | IDs y cardinalidad; internos y no asignados explícitos; sin exposición corporativa |
| TRK-002 | Contratos tipados / arquitectura | TRK-001 | Dataclasses + schemas, lifecycle, compatibilidad y test de refs/ciclos |
| TRK-003 | Versiones/activación / backend | TRK-002 | Estado persistente, permisos, idempotencia y concurrencia; test sin sobrescritura |
| TRK-004 | Evidence y progreso / Brain + backend | TRK-003, CAT-006 | Snapshot/version binding; unknown/stale, invalidación y denominador congelado |
| TRK-005 | Tracking conectado / frontend | TRK-003/004 | UI desde DTO; no KPIs locales ni autorizaciones en cliente |
| TRK-006 | Goal outcomes / analytics owner | Fuente autorizada | Métrica/ventana/baseline/target, distinta de entrega |
| TRK-007 | QA y rollout / revisor + owner | TRK-005/006 | Separación cliente/proyecto, intentos de carrera y evidencia revocada |

Rollout: aceptar diseño → contratos probados → fixtures persistentes en entorno local → NegritaOS opt-in → proyecto autorizado. Una PR corta por responsabilidad. Flags separados para lectura y activación; rollback apaga comandos de escritura y conserva versiones/eventos. Ningún despliegue ni acceso facturable autorizado aquí.

## Validation, ownership and update trigger

Owner visual: usuario. Especificación: arquitectura; persistencia/medición: backend y Brain según tabla. Actualizar el memo cuando cambien jerarquía de clientes, criterio de aceptación, lifecycle o modelo de medición. Validar esta propuesta antes de implementar el backend.

Comando: `node --test --experimental-test-coverage prototypes/negritaos360/state.test.mjs prototypes/negritaos360/tracking.test.mjs`. Resultado inicial: 19/19 tests; lógica de tracking 100 % líneas y 86.42 % ramas. La cobertura global del conjunto cargado no incluye el controlador DOM ni demuestra integración real.

Checks locales del navegador: propuesta v1.1 sin tocar v1.0; confirmación de activación; historial 40 % → 33 % conservado; filtro Cliente demo B restringe proyectos, catálogo y grafo a Faro; activación de Faro deshabilitada por diseño faltante; cambio de tema sin perder selección. No hay certificación de release, revisión independiente nueva ni auditoría WCAG completa.

Regresión adicional: cambio de criterio F-02 reduce evidencia compatible a 1/5 (20 %); su validación simulada restaura 2/5 (40 %), sin medir el goal. F-04 bloqueada no permite validar. Ancho móvil efectivo 390×844, documento 390 sin overflow global en plan/tabla; Escape cierra ficha y el salto por teclado preserva `#tracking`. Escritorio efectivo 1280×900. Sin errores de consola observados en esta sesión. Las capturas del navegador tienen una diferencia de escala respecto al viewport declarado; las dimensiones indicadas son las comprobadas en el DOM, no una certificación pixel-perfect.
