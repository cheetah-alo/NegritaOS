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
  supersedes: null
  quality_gates_status: PASSED_WITH_WARNINGS
---

# Decision Memo — NegritaOS 360 se usa sólo en local

> **Decisión aceptada:** la aplicación NegritaOS 360 se ejecutará únicamente en el equipo del usuario mientras madura. El usuario lo confirmó el 27 de septiembre de 2026.

## Contexto y alcance

Esta decisión rige el runtime, las fuentes de datos y la incorporación gradual de proyectos. Complementa el [diseño visual aceptado](negritaos_360_design_decision__updated_20260927_143145.md) y el [modelo de lectura acotado](negritaos_360_increment_02__updated_20260927_154047.md). Audiencia: desarrolladores del servicio local, frontend y QA. No cambia la rama Git ya autorizada para guardar código.

Situación actual: el prototipo estático puede servirse en `127.0.0.1`; usa datos sintéticos. Los contratos Python y la proyección de proyectos existen, pero aún no hay una aplicación conectada, listener API, servicio de permisos de cuenta ni clientes reales en la UI.

## Decisión y opciones

| Opción | Resultado | Decisión |
|---|---|---|
| Servicio local sin listener inicial | Lectura explícita y verificable de archivos permitidos | Adoptada para `CAT-005B` |
| UI local con API en loopback | Conveniente cuando haya un contrato estable | Evaluar después; si se crea, escuchar sólo en `127.0.0.1` |
| Hosting remoto o endpoint de red | Acceso desde otros dispositivos | Fuera del rollout actual |

No se configurará hosting web, túnel, URL pública, base de datos cloud, telemetría externa ni conexión automática de cuentas. Un commit o push del **código** a la rama Git autorizada no pone en línea la **aplicación**. Cualquier cambio de ese límite requiere una decisión nueva del usuario.

## Contrato local de fuentes y acceso

1. El arranque local recibe una ruta de política JSON elegida explícitamente fuera de Git. Ausencia de archivo significa lista de acceso vacía. El archivo existente debe pertenecer al usuario del proceso, ser regular, no ser symlink y no permitir lectura/escritura a grupo u otros.
2. La política declara pares exactos `(project_id, client_id)` o IDs de proyectos cuyo cliente todavía es `unknown`. No se usa `project.client` heredado como ID ni se infiere cliente del nombre de carpeta, Git o email.
3. El servicio lee únicamente `projects/<id>.yaml` para IDs listados. No recorre todos los proyectos. Rechaza rutas que salen del directorio, symlinks, referencias no declaradas y discrepancias entre política y registry.
4. Tras esa lectura, el modelo existente aplica el grant de ámbito y devuelve sólo los campos permitidos. Datos y metadatos de una fuente oculta no entran en el DTO de otra vista.
5. Ante un archivo autorizado ausente, inválido o inconsistente se devuelve un fallo explícito y redactado; no se presenta `EMPTY` como si fuera una lectura válida. El cliente no ve rutas locales, contenido de políticas ni secretos.

Este archivo local controla el acceso de **esta herramienta** en un proceso confiable de un solo usuario. No autentica procesos del sistema ni sustituye una política multiusuario. Antes de exponer una ruta HTTP local, deberán revisarse el origen de peticiones, la denegación por defecto y la ausencia de CORS abierto. No iniciar un servidor sobre `0.0.0.0` ni una IP de red.

## Ownership, pruebas y rollout

Backend NegritaOS mantiene el loader de política y el servicio de registries; frontend usa el DTO lógico; QA revisa que sólo se leen archivos allowlistados y que no hay llamadas o listeners externos. Tests con archivos temporales sintéticos cubren ausencia de política, permisos del archivo, IDs/clientes discrepantes, symlinks, fuentes faltantes y filtros de ámbito. Ninguna prueba debe leer datos de clientes reales por defecto.

Secuencia: `CAT-005B` servicio local sin HTTP → contrato de error y forma de arranque local → un proyecto interno opt-in → otros proyectos sólo con política explícita → UI conectada. La activación de planes (`TRK-003`) permanece separada de la lectura y requerirá sus propios permisos y evidencia. El prototipo Tepulume conserva sus fixtures hasta que esta ruta de lectura esté lista.

Actualizar esta decisión si se propone un listener, persistencia, lectura automática de registries, publicación remota o colaboración multiusuario. A fecha de creación, los cambios de `CAT-005B` estaban en implementación; este documento fija el límite, no certifica que el servicio ya esté completo.
