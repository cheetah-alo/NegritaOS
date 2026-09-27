---
metadata:
  source: negritaos
  document_version: "1.2.0-ux-review"
  generated_date: "2026-09-27"
  last_modified_date: "2026-09-27"
  project_id: negritaos
  document_class: decision_documentation
  status: PROTOTYPE_FOR_USER_REVIEW
  baseline: docs/negritaos_360_dashboard_architecture_plan__updated_20260927_124000.md
  independent_reviewer: gpt-6-astra
  quality_gates_status: NOT_RELEASE_CERTIFIED
---

# Decision Memo — NegritaOS 360: look & feel y revisión del plan

> **TL;DR:** revisar primero una interfaz local y navegable; después construir el catálogo tipado y su read model. No empezar por un grafo gigante ni confundir configuración con uso.

## Context

Documento para el owner de NegritaOS y los futuros responsables de arquitectura, frontend, Brain y QA. Revisa el plan v1.1 antes de desarrollar el dashboard conectado. Es documentación de decisión junto al código, no un reporte de datos reales.

Fuentes: [plan v1.1](negritaos_360_dashboard_architecture_plan__updated_20260927_124000.md), revisión independiente de Astra en esta sesión y [fuentes del prototipo](../prototypes/negritaos360/README.md). Esta enmienda prevalece sobre las secciones OO, métricas y secuencia de entrega del plan anterior; conserva su catálogo de tareas CAT/FLOW/KNOW. No afirma haber revisado de nuevo los vídeos.

Situación actual: existe una maqueta modular HTML/CSS/JS con fixtures sintéticos. No hay backend, conexión Brain, API de dashboard, integración Git ni motor de grafo en producción. La revisión inicial de Astra fue **HOLD provisional del plan**, no una certificación de release. Señaló estados mezclados, relaciones incompletas y métricas sin población/ventana.

## Decision Required

Validar la dirección visual y la navegación antes de CAT-001. El usuario puede revisar una pantalla funcional sin autorizar lecturas de clientes, publicación pública ni acciones facturables. Aceptar este diseño no aprueba una ejecución o un commit de otro proyecto.

## Options

| Opción | Ventaja | Compromiso / riesgo |
|---|---|---|
| Observatorio modular local — recomendado | Probar jerarquía y navegación con coste técnico mínimo | Las cifras no representan el sistema real |
| Dashboard conectado desde el principio | Datos operativos antes | Mezclaría decisiones UX con permisos y adapters todavía no validados |
| Grafo como pantalla principal | Visión relacional inmediata | Peor lectura del inventario y demasiada densidad para tareas cotidianas |

## Recommendation

### 1. Dirección visual y lo que verá el usuario

Verde petróleo en navegación, fondo marfil, tarjetas claras y ámbar/terracota para atención. Títulos con tipografía serif local y tablas compactas con tipografía de sistema. Sin fuentes remotas, CDN ni analytics. La estética busca una mesa de trabajo personal, no un panel de alarmas permanente.

| Vista | Pregunta que responde | Interacciones de la maqueta |
|---|---|---|
| Panorama | ¿Qué tengo y dónde debería mirar? | Resumen, proyectos, señales sintéticas y mapa compacto |
| Proyectos | ¿Qué aplica a este espacio? | Selector de proyecto, capacidades y responsable |
| Capacidades | ¿Qué agents, skills y rules existen? | Tipo, búsqueda, ficha y relaciones |
| Conocimiento | ¿Cómo se relaciona lo definido y qué respalda una decisión? | Alternar capacidades/conocimiento, profundidad, zoom y lista navegable |
| Flujos | ¿Cuál es la secuencia y quién decide? | Pasos ilustrativos y avance simulado, sin ejecutar |
| Brain y Git | ¿Cómo conservar continuidad entre sesiones y ramas? | Referencias sintéticas; conexiones reales pendientes |

Cabecera permanente “datos simulados, sin conexión”; filtro de proyecto compartido; escenarios loading/empty/error/stale; ficha lateral de procedencia y ownership. La lista navegable es una alternativa al SVG. Las tablas y fichas son la ruta principal; el grafo es complementario.

La futura Project Lens añadirá analytics assets, runs, gates y riesgos cuando existan adapters autorizados. La Capability Matrix y el diagnóstico de utilización quedan pendientes, no representados como funciones ya completas. El prototipo no sustituye la visión 360 del plan.

### 2. Corregir estados antes de implementar

| Dimensión | Contrato futuro |
|---|---|
| Configuración | `defined`, `resolved`, `available`: cada comprobación `yes/no/unknown`, contexto de proyecto/proveedor y motivo |
| Evidencia | `verified/unverified/missing`, referencia, versión y alcance |
| Freshness | `fresh/stale/unknown`, observación temporal y umbral versionado |
| Uso | `observed/not_observed/unknown`, intervalo UTC semiabierto y cobertura de observación |
| Lectura | `loading/ready/partial/error/timeout/blocked`, fallo de acceso separado de resultado de comprobación |

Una capacidad puede estar resuelta, tener evidencia antigua y uso desconocido simultáneamente. `configured_not_observed` exige cobertura suficiente durante la ventana. Los estados abreviados de los fixtures son etiquetas ilustrativas, **no** el contrato del backend. Todos los fixtures son `synthetic` por procedencia, sin equivalencia con validación real.

### 3. Contrato OO y extensibilidad

Mantener dataclasses inmutables, adapters `Protocol` y funciones puras. El ejemplo siguiente es diseño propuesto, no código instalado. Amplía el ejemplo de v1.1; sustituye `GraphEdge.relation: str` y prohíbe un único `CapabilityNode.status` que mezcle dimensiones.

```python
from dataclasses import dataclass
from enum import Enum
from typing import NewType, Protocol

NodeId = NewType("NodeId", str)

class Relation(str, Enum):
    DECLARES = "declares"
    MAPS = "maps"
    ROUTES_TO = "routes_to"
    ACTIVATES = "activates"
    USES = "uses"
    GOVERNED_BY = "governed_by"
    DEPENDS_ON = "depends_on"
    ENFORCES = "enforces"
    PRODUCES = "produces"
    OBSERVED_IN = "observed_in"

@dataclass(frozen=True, slots=True)
class Provenance:
    source_id: str                 # Opaque authorized reference, not a file path.
    source_sha256: str
    synthetic: bool = False

@dataclass(frozen=True, slots=True)
class GraphEdge:
    source_id: NodeId
    target_id: NodeId
    relation: Relation
    provenance: Provenance

class EdgeValidator(Protocol):
    def validate(self, edge: GraphEdge) -> tuple[str, ...]: ...
```

Añadir `Gate`, `Evidence` y `Run` a los tipos correspondientes. `Coverage` será una métrica derivada, no un nodo; se elimina `Evidence → updates → Coverage` del grafo conceptual anterior. `updates` no es una relación válida. Execution y Knowledge tienen vocabularios separados y versionados; no se permite extenderlos con strings arbitrarios.

| Origen → destino | Relación / multiplicidad saliente | Regla |
|---|---|---|
| Project → Profile | declares / 0..N | Referencia explícita |
| Project → Mode | maps / 0..N | No inferir de nombres |
| Mode → Agent | routes_to / 0..N | Más de un destino exige contexto de routing |
| Profile → Skill | activates / 0..N | Perfil efectivo, no sólo declarado |
| Agent → Skill o Template | uses / 0..N | Declaración no demuestra uso observado |
| Agent → Rule | governed_by / 0..N | Regla resuelta y versionada |
| Skill → Skill | depends_on / 0..N | Ciclos se reportan, no se ocultan |
| Rule → Gate | enforces / 0..N | Gate concreto |
| Gate → Evidence | produces / 0..N | Receipt con procedencia |
| Agent o Skill → Run | observed_in / 0..N | Evento verificable, no inferencia desde configuración |

CAT-001 debe validar IDs, pareja de tipos, dirección, pertenencia al ámbito autorizado, duplicados y provenance al ingresar datos. Las dataclasses no hacen esa validación por sí solas. Referencias rotas generan diagnóstico `unresolved`, no nodos falsamente disponibles. Extensiones futuras requieren un schema versionado y adapter registrado. Añadir una skill ordinaria sólo cambia metadata y regeneración; nunca un `if skill_name` en la UI.

### 4. Métricas con población definida

Cada métrica llevará `snapshot_id`, población autorizada, versión del contrato, unidad, numerador, denominador, ventana y cobertura. Deduplicar capabilities por ID estable y eventos por ID de evento. Denominador cero significa `not_applicable`, no 0 %.

- Resolución, ownership y dependencias: mismo snapshot y proyecto, sin combinar versiones. Los datos desconocidos se muestran aparte.
- Uso: ventana UTC `[start, end)` y población disponible **durante esa ventana**; no dividir uso histórico entre disponibilidad actual. Si no se puede reconstruir esa población o la observación es insuficiente: `unknown`.
- Freshness: edad desde la última comprobación válida de esa versión, no desde el último render.
- Fiabilidad de workflows: unidad run, terminales y reintentos definidos antes del KPI; los runs en curso no son fallos.
- Costes: desconocidos sin fuente autorizada y unidad explícita. No convertir créditos Codex en USD ni atribuir horas a partir de commits.

### 5. Boundaries, ownership y privacidad

`Registry adapters → domain validation → authorized snapshot → DTO → UI`.

- Arquitectura: schemas, estados, tipos/relaciones y contratos de métricas.
- Brain maintainer: lectura acotada de sesiones/receipts, sin copiar contenido de memoria.
- Backend owner: compiler, caché y redacción/minimización antes del DTO.
- Frontend owner: estado de interacción y representación; no interpretación de policies.
- QA independiente: falsificación, aislamiento por proyecto, freshness y error semantics.
- Owner humano: aceptación visual, acceso a fuentes y cambios de alcance.

En esta fase: cero lecturas de proyectos CQI, cero diffs, cero rutas privadas en fixtures, cero llamadas externas. Los filtros UI **no son** un control de autorización: el adapter/read model futuro debe aplicar el ámbito antes de entregar datos. NegritaOS conserva identidad personal; no se propaga metadata interna a Git corporativo. No se asume incorporado el trabajo de otra rama.

### 6. Tecnología y rollout

La maqueta usa SVG local y JS modular para probar interacciones, sin instalar librerías. Para producción, Cytoscape.js sigue como candidato para exploración visual y NetworkX como herramienta backend si las métricas lo necesitan. No se introducen Neo4j, búsqueda semántica ni orquestación continua en el MVP. La selección final requiere presupuesto de nodos/aristas, rendimiento y accesibilidad medidos, no sólo gusto visual.

## Next Actions

| ID / enlace previo | Tarea corta | Owner | Criterio de salida / estado |
|---|---|---|---|
| UX-001 | Prototipo modular local | Frontend | Seis vistas, filtros, ficha y escenarios; disponible para revisión |
| UX-002 | Validar dirección visual | Owner humano | Aceptar o ajustar densidad, tipografía y navegación; pendiente |
| CAT-001A / CAT-001 | Estados, tipos y relaciones | Arquitectura | Schemas + unittest de unknown, invalid edges, ciclos y namespaces; pendiente |
| CAT-001B / CAT-004 | Contratos de métricas | Arquitectura + QA | Ventanas, población histórica, duplicados y denominador cero; pendiente |
| CAT-002A / CAT-002 | Compiler y snapshot autorizado | Backend | Determinismo, referencias rotas y pruebas de aislamiento; pendiente |
| CAT-005A / CAT-005 | DTO de catálogo | Backend | Contrato versionado, procedencia y estados independientes; pendiente |
| CAT-007A / CAT-007 | Catálogo conectado + ficha | Frontend | Sin lógica de negocio en UI; empty/error/stale/blocked; pendiente |
| CAT-003A / CAT-003 | Capability Graph acotado | Frontend + backend | Mismos IDs y filtros que catálogo, 1–3 saltos, alternativa tabular; pendiente |
| CAT-006A / CAT-006 | Uso observado | Brain maintainer | No inferir uso; tests de ventanas/cobertura y privacidad; pendiente |
| FLOW-001 / KNOW-001 | Grafos específicos | Arquitectura | Contratos propios y provenance, primero lectura; pendiente |
| CAT-008 | QA y rollout progresivo | QA + owner | Proyecto sintético → NegritaOS autorizado → un proyecto opt-in; pendiente |

Una PR corta por contrato o entrega verificable; no mezclar UI con cambios de hooks/identidad. Rollback: deshabilitar la vista conectada o volver al último snapshot autorizado compatible, visible como antiguo; nunca modificar las fuentes desde el dashboard. Datos reales bloqueados hasta validar redacción y control de acceso. La aprobación visual es un gate, no autorización para publicar.

## Validation and limitations

Pruebas del prototipo: `node --test prototypes/negritaos360/state.test.mjs`. Se comprueban filtros, uso desconocido frente a cero, referencias sintéticas y recorrido acotado con ciclos. La comprobación en navegador cubre flujos de interacción de la maqueta; no demuestra integración, seguridad del backend ni rendimiento con un inventario real.

La revisión independiente inicial de Astra encontró gaps que motivan esta enmienda. Su registro Brain informó `BLOCKED/doctor FAIL` y no confirmó un cierre formal; no se etiqueta como PASS firmado. No se ha autorizado deployment, merge ni acceso a datos CQI. La aceptación visual del usuario sigue pendiente.

Revisión final de fuentes por Astra: detectó que el enlace «Saltar al contenido» cambiaba de vista. Se corrigió con enfoque de `main` sin navegación y regresión de ruta; Astra volvió a comprobar el delta y ejecutó **7/7 tests**, sin bloqueos pendientes de ese delta. Su revisión no fue visual ni certificación de release.

Verificación del builder en navegador local: filtro Skills + Atlas + búsqueda; apertura/cierre de ficha y Escape; estados loading/empty/error/stale y retry; filtro de proyecto también aplicado a señales; simulación de flujo; profundidad del grafo (6 nodos a un salto, 11 a tres), zoom; Brain/Git ficticios. Desktop revisado y viewport móvil 390×844 sin overflow global tras corregir una etiqueta accesible (ancho del documento 390). El salto por teclado conserva `#catalog` y enfoca `main`. Consola sin errores observados. No se ejecutaron auditoría WCAG completa, pruebas de carga ni integración con datos reales. Fuentes nuevas locales, sin commit ni publicación en este turno.

Actualizar esta decisión cuando el owner revise el prototipo, se congele el schema, se elija motor de grafo o se conecte una fuente. Mantener UX-001/002 separados de los hitos de producto CAT/FLOW/KNOW.
