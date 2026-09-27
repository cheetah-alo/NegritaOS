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

# NegritaOS 360 — incremento 02: catálogo de lectura acotado

## Propósito, audiencia y alcance

Este incremento implementa la primera parte de `CAT-005`: una proyección inmutable del catálogo de proyectos para consumidores autorizados. Lo usarán el backend y QA del dashboard. Sigue el [incremento 01](negritaos_360_increment_01__updated_20260927_145404.md) y el [diseño aceptado](negritaos_360_design_decision__updated_20260927_143145.md). No crea endpoint HTTP, proveedor de identidad ni acceso a proyectos reales.

## Fuente de verdad y contrato actual

- `src/negrita_brain/dashboard_registry.py` produce entradas validadas sólo desde registries explícitos. No infiere el cliente desde rutas, nombre, organización o `project.client` heredado.
- `src/negrita_brain/dashboard_read_model.py` recibe esas entradas, `CatalogScopeGrant` de un llamador confiable y `CatalogProvenance`. Es una función pura: no lee archivos, memoria, Git ni red.
- Cliente conocido o interno: visibilidad sólo con el par exacto `(project_id, client_id)` en el grant. Cliente desconocido: requiere el ID de proyecto y una autorización explícita adicional para mostrarlo. Sin grants, la vista queda vacía.
- Filtros solicitados por proyecto o cliente se aplican después del control de ámbito. Un ID oculto consultado no revela si el proyecto existe; `EMPTY` significa «sin resultados visibles» y no prueba que no haya datos globales.
- La lista se ordena por ID estable y sólo contiene `project_id`, `name`, `client_id` y `client_classification`. El estado visible es `READY` o `EMPTY`; fallos de fuente o permisos reales todavía pertenecen a una futura capa de servicio.

`CatalogProvenance` de entrada contiene un ID, hash SHA-256 y fecha consciente de zona horaria aportados por el llamador. Sus metadatos globales quedan internos. El DTO muestra un `view_sha256` e ID de vista derivados exclusivamente de campos visibles; un cambio de proyecto oculto no altera la respuesta. La fecha de la fuente no se expone al consumidor porque revelaría cuándo cambió contenido fuera de su ámbito. Esta vista tampoco afirma la frescura de cada proyecto ni el logro de un goal.

El valor de retorno de `to_dict()` es serializable en JSON. Es un contrato de lectura, no una API pública: el backend aún debe autenticar al actor, obtener permisos desde su fuente de verdad y crear el grant sin datos del cliente. Crear un `CatalogScopeGrant` manualmente no concede autoridad fuera de ese proceso.

## Verificación

```sh
PYTHONPATH=src /Users/jackyb-cqi/repos/NegritaOS/.venv-pr-quality/bin/python -m unittest discover -s tests -p 'test_negrita_brain_dashboard_*.py'
```

Resultado tras la corrección de privacidad: 37/37 pruebas del módulo y sus contratos previos. Casos cubiertos: pares cliente/proyecto, interno, cliente desconocido, ausencia de grants, filtros tras ámbito, duplicados, clasificación contradictoria, metadatos inválidos, JSON y respuesta idéntica si sólo cambian contenido y metadatos de fuente ocultos. Son fixtures sintéticos, no una auditoría de permisos reales. La suite completa, revisión independiente y publicación en rama son gates de integración.

## Ownership, límites y siguiente paso

Backend mantiene el adapter y la proyección; el proveedor de permisos y QA deberán revisar el acceso por proyecto antes de conectarla a UI. Arquitectura conserva los estados y límites de contrato. `CAT-005B` deberá añadir el servicio que obtiene grants autorizados y snapshots desde fuentes canónicas, con estado explícito de error/timeout, tests de aislamiento y una ruta de lectura si se elige runtime HTTP. La Capability Matrix, Project Lens completo, Knowledge Graph y métricas de uso no son parte de este incremento.

Actualizar mediante otra versión si cambia la regla de visibilidad, los campos del DTO o la semántica de provenance. El prototipo Tepulume sigue local y usa datos ficticios; aún no consume este módulo.
