---
metadata:
  source: negritaos
  document_version: "1.0.0"
  generated_date: "2026-09-27"
  last_modified_date: "2026-09-27"
  project_id: negritaos
  document_class: decision_documentation
  status: ACCEPTED
  accepted_by: user
  supersedes:
    - docs/negritaos_360_ux_plan_review__updated_20260927_134112.md
    - docs/negritaos_360_project_tracking__updated_20260927_141408.md
  quality_gates_status: PASSED_WITH_WARNINGS
---

# Decision Memo — diseño elegido para NegritaOS 360

> **Decisión aceptada:** desarrollar NegritaOS 360 con la última variante visual Tepulume del prototipo local. El usuario la eligió explícitamente el 27 de septiembre de 2026.

## Contexto y alcance

Esta decisión fija la dirección de diseño antes del desarrollo conectado. La referencia navegable está en `prototypes/negritaos360/`, especialmente `tepulume-theme.css` y la vista `#tracking`. Los documentos anteriores registran el razonamiento y las alternativas; conservan su valor histórico, pero sus frases «pendiente de aceptación visual» ya no describen el estado actual.

La elección visual no valida los datos ficticios ni autoriza publicar, desplegar, conectar clientes o activar workflows reales. El código del prototipo sigue siendo una simulación local.

## Contrato visual aceptado

- Identidad visible: **NegritaOS**. Se adoptan los tokens de la implementación actual de Tepulume como sistema de diseño, sin presentar el dashboard como producto Tepulume.
- Azul petróleo `#0d6684`, magenta `#c81f68`, blanco cálido `#f7f6f5`, superficies blancas, bordes sobrios y radios pequeños.
- Montserrat para títulos, Instrument Sans para texto, tipografía recta y sin cursivas. Antes de distribuir los TTF de la maqueta se revisarán sus derechos de redistribución; no forman parte de este commit.
- Navegación por **Panorama, Proyectos, Planes y avance, Capacidades, Conocimiento, Flujos, Brain y Git**. La UI muestra fuentes, estados desconocidos y procedencia junto a cada resultado relevante.
- Cliente por proyecto y filtro cliente → proyecto. El catálogo, los grafos y el seguimiento respetarán el mismo ámbito. La aplicación conectada impondrá ese ámbito en backend.

## Funcionalidad de seguimiento acordada para desarrollar

Cada proyecto podrá vincular un cliente, objetivos y planes. Un plan define funcionalidades, criterios verificables, diseño versionado y responsable. La activación exige revisión explícita de una versión exacta. Los cambios posteriores generan otra revisión con motivo y diff; la línea base y las mediciones históricas se conservan.

El avance de entrega se calcula con funcionalidades aceptadas y evidencia aplicable a la versión activa. El logro del objetivo se mide por su propia métrica y ventana. Un commit, una sesión o una tarea en curso no constituyen aceptación. Sin observación suficiente, la UI mostrará `unknown` o `sin medir`.

El [plan de seguimiento](negritaos_360_project_tracking__updated_20260927_141408.md) desarrolla contratos, clases, límites de acceso, pruebas y tareas `TRK-001` a `TRK-007`. El [plan de arquitectura](negritaos_360_dashboard_architecture_plan__updated_20260927_124000.md) conserva `CAT`, `FLOW` y `KNOW`.

## Secuencia de implementación

1. **CAT-001 / TRK-002:** contratos tipados de cliente, proyecto, goal, plan, diseño, funcionalidad, versión, evidencia y estados; tests de invariantes.
2. **TRK-001 / CAT-002:** adapter de registries, IDs estables y pertenencia cliente/proyecto. Lo no declarado seguirá `unknown`, sin inferir clientes de rutas o nombres.
3. **CAT-005:** snapshot y DTO de lectura autorizados para catálogo y seguimiento; UI consume el contrato.
4. **TRK-003/004:** activación/versiones y progreso con permisos, concurrencia, idempotencia y evidencia. En este punto se revisa el nuevo límite de escritura frente al dashboard originalmente read-only.
5. **CAT-007/008 + TRK-005/007:** integrar la variante Tepulume, pruebas de filtros/estados/accesibilidad y rollout por proyecto opt-in.

Cada tarea tendrá un cambio pequeño y evidencia de pruebas. La rama actual es `feature/negritaos-360-capability-graph`; los prototipos y fuentes anteriores no se confunden con backend conectado. El primer tramo delegará contratos y adaptación de registries con ownership de archivos separado.

## Verificación, owner y disparadores de actualización

Owner de diseño: usuario. Owner del contrato: arquitectura NegritaOS. QA independiente revisará los cambios de alto impacto antes de integrarlos. La documentación deberá actualizarse si cambia la marca elegida, la jerarquía cliente/proyecto, la fórmula de avance o el proceso de activación.

Estado al registrar la decisión: prototipo local comprobado en navegador; 19/19 pruebas unitarias de la maqueta en el turno anterior. No hay integración real con Brain/Git, autorización por cliente, persistencia ni validación de producción. Esta aceptación permite iniciar el desarrollo; no equivale a un PASS de release.
