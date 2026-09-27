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

# NegritaOS 360 — incremento 03: lectura local con política explícita

## Propósito, audiencia y alcance

Este incremento implementa `CAT-005B` como servicio Python de sólo lectura para un proceso local de NegritaOS 360. Lo usarán backend y QA antes de conectar la interfaz. Sigue la [decisión de uso local](negritaos_360_local_only_decision__updated_20260927_160308.md) y el [DTO acotado](negritaos_360_increment_02__updated_20260927_154047.md). No crea listener, CLI, endpoint, acceso cloud ni sincronización con clientes.

## Fuente de verdad y contrato actual

- `dashboard_local_access.py` lee un JSON seleccionado por el llamador. Ausencia de archivo ⇒ `CatalogScopeGrant` vacío. Si existe, debe ser regular, no symlink, propiedad del usuario del proceso y sin permisos para grupo u otros. Se abre con `O_NOFOLLOW` y se valida el descriptor abierto. El archivo tiene un límite de 64 KiB.
- Schema v1: `schema_version: 1`, `project_client_grants: [{project_id, client_id}]` y `unknown_client_projects: [project_id]`. No admite claves desconocidas, IDs mal formados, duplicados, proyectos asignados a dos clientes o solapamiento entre cliente conocido y desconocido. Se conserva fuera de Git y no se registra su contenido.
- `dashboard_local_service.py` carga primero la política y deriva la lista exacta de IDs. Sin grants retorna `EMPTY` sin abrir ningún YAML. Para cada ID permitido intenta leer `projects/<id>.yaml`; rechaza directorio o archivo symlink/no regular, fuente ausente y discrepancia entre ID/cliente de política y registry. No usa glob ni recorre todo `projects/`.
- La salida es el `ProjectCatalogReadModel` del incremento anterior, con filtros aplicados tras el ámbito. El hash de fuente interno se calcula únicamente sobre entradas ya permitidas; el DTO público conserva sólo su huella de vista. La captura temporal se mantiene interna y no se presenta como frescura del proyecto.

Errores de política y fuente tienen clases distintas (`LocalPolicyError`, `LocalCatalogError`) y mensaje genérico sin ruta o nombre de cliente. Una fuente autorizada ausente o inválida no se representa como `EMPTY` exitoso. Este código presupone un proceso local confiable del propio usuario; la política de archivo no autentica procesos del sistema ni constituye todavía un control multiusuario.

Ejemplo sintético del JSON local, con acceso vacío por defecto:

```json
{"schema_version":1,"project_client_grants":[],"unknown_client_projects":[]}
```

El usuario escogerá la ruta real fuera del repositorio cuando se habilite el arranque local; este incremento no crea archivos personales ni declara clientes de los proyectos existentes.

## Verificación y límites

```sh
PYTHONPATH=src /Users/jackyb-cqi/repos/NegritaOS/.venv-pr-quality/bin/python -m unittest discover -s tests -p 'test_negrita_brain_dashboard_*.py'
```

Resultado local inicial: 55/55 pruebas enfocadas. Casos de política ausente, permisos, symlink, cambio de symlink antes de abrir, IDs y clientes duplicados, fuente faltante, mismatch y lectura allowlistada. Son fixtures temporales, sin leer proyectos reales. La suite completa y la revisión independiente son gates antes de commit.

La comprobación de symlinks del YAML ocurre antes de que el loader existente abra la ruta; esta fase no es una defensa contra un proceso hostil que pueda modificar el mismo archivo simultáneamente con el mismo UID. Para una futura interfaz local con datos sensibles, cerrar esa carrera usando una lectura por descriptor, revisar el origen HTTP y evitar CORS abierto. La aplicación actual no escucha en ningún puerto por este código. El prototipo anterior sigue sirviéndose sólo en loopback y usa fixtures.

## Ownership y siguiente paso

Backend mantiene política y lectura; frontend recibirá únicamente el DTO lógico; QA verifica archivos realmente abiertos y estados de error. El próximo tramo definirá el arranque local que selecciona política y checkout, presenta errores sin rutas y, cuando la UI esté lista, se une a un listener fijado a `127.0.0.1`. Activar planes requiere contratos de escritura, permisos e idempotencia separados (`TRK-003`).

Actualizar mediante otra versión si cambia el schema local, la fuente de permisos, el comportamiento ante fuente ausente o la forma de abrir YAML. Ningún commit o push de este incremento pone la aplicación en línea.
