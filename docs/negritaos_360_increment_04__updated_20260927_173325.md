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

# NegritaOS 360 — incremento 04: interfaz conectada al catálogo local

## Propósito, alcance y fuente de verdad

Conectar la interfaz visual aceptada con el [servicio local de lectura](negritaos_360_increment_03__updated_20260927_161157.md), respetando la [decisión de uso local](negritaos_360_local_only_decision__updated_20260927_160308.md). Dirigido al owner, frontend, backend y QA. Este incremento conecta únicamente el catálogo de proyectos; Brain, Git, skills, grafos, goals y activación de planes siguen sin fuente real.

Fuente física: `projects/<id>.yaml` sólo para los IDs de la política JSON local. El backend `LocalCatalogService` valida esa política y la identidad del cliente; `ProjectCatalogReadModel` define el DTO visible. El frontend consume `GET /api/v1/catalog` por el mismo origen y no lee registries, rutas, archivos de política ni contenido privado.

## Comportamiento actual

- `src/negrita_brain/dashboard_local_server.py` abre exclusivamente `127.0.0.1` y sirve la ruta versionada `/api/v1/catalog` y los archivos estáticos del directorio `prototypes/negritaos360/`. No acepta host externo, origen externo, rutas con traversal, dotfiles o symlinks; no añade CORS abierto. Envía CSP local, `no-store`, `nosniff` y `no-referrer`.
- El endpoint recibe a lo sumo un `project_id` y un `client_id`. Rechaza entradas inesperadas o URL malformada con JSON `400`; métodos no admitidos devuelven JSON `405` (HEAD sin cuerpo). Fallos de política/fuente devuelven JSON `503` con código `UNAVAILABLE`, sin nombres ni rutas. La UI no presenta ese fallo como catálogo vacío.
- En `prototypes/negritaos360/`, el selector **Fuente: Demo / Local** deja clara la procedencia. Demo mantiene los fixtures sintéticos anteriores. Local consulta el DTO, muestra Panorama/Proyectos, filtros y búsqueda sólo sobre proyectos autorizados. Las demás secciones indican que su fuente local aún no está conectada.
- La API no publica la hora ni hash del snapshot global. El identificador y hash de la vista se derivan sólo de datos visibles. La interfaz no calcula salud, uso ni progreso a partir del número de proyectos.
- La política local `.local/dashboard-access.json` está ignorada por Git y tiene modo `0600`. En este worktree opta únicamente por `negritaos` con cliente no clasificado; no lee proyectos CQI. Si el archivo falta, el servidor funciona con una vista `EMPTY` y no abre YAML de proyectos.

## Arranque y verificación

Desde el worktree, con la venv local configurada:

```sh
PYTHONPATH=src /Users/jackyb-cqi/repos/NegritaOS/.venv-pr-quality/bin/python -m negrita_brain.dashboard_local_server --port 8791 --access-file .local/dashboard-access.json
```

Abrir `http://127.0.0.1:8791/?source=local#projects`. El servidor no ofrece opción para cambiar el host. El antiguo `http.server` en `8790` puede seguir mostrando Demo, pero no posee la API local.

Comprobaciones automatizadas: `PYTHONPATH=src /Users/jackyb-cqi/repos/NegritaOS/.venv-pr-quality/bin/python -m unittest discover -s tests -p 'test_negrita_brain_dashboard_*.py'` y `node --test prototypes/negritaos360/*.test.mjs`. Los tests Python de red usan un socket en memoria en el sandbox; la prueba funcional del servidor real se hizo en loopback tras abrir `127.0.0.1:8791`.

En el navegador local se verificó la lista de un solo proyecto `NegritaOS`, cliente `unknown`, búsqueda sin coincidencias y limpieza de filtros, cambio a Demo y vuelta a Local, vista honesta para Capacidades, diseño móvil sin desbordamiento global y consola sin errores observados. La escucha real se confirmó sólo en `127.0.0.1:8791`. Además, peticiones locales reales comprobaron POST → JSON `405` y URL malformada → JSON `400`. Son evidencias locales, no validación de un despliegue o de permisos multiusuario.

## Ownership, límites y siguiente tarea

Backend mantiene el puente HTTP, política y DTO; frontend mantiene fuente, estados y representación; QA revisa aislamiento por proyecto/cliente y el tráfico del navegador. El siguiente tramo conectará capacidades/Brain/Git mediante adapters de lectura propios, sin inferir uso desde configuración. La UI de planes continúa como simulación Demo hasta implementar `TRK-003/004` con versiones, permisos y evidencia reales.

Los TTF del estilo Tepulume siguen como assets locales ignorados por Git hasta verificar su distribución. En otra instalación se usarán fuentes de sistema de respaldo. Actualizar este documento cuando se añada una fuente, cambie el contrato JSON, se abra otro listener o se decida publicar la app fuera de loopback.
