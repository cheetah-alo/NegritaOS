# Plan Revisado: Implementar NegritaOS Sin Perder Información Ni Cambios Git

## Resumen

NegritaOS queda separado en tres responsabilidades:

- **NegritaOS**: sistema central versionado con agentes cognitivos, reglas de calidad, templates, marcas, arquetipos y registry de proyectos.
- **`~/.negritaos/memory`**: memoria privada local, persistente y fuera de ramas/worktrees. Esta es la fuente canónica de memoria.
- **`.codex` por repo**: adaptador técnico local del repo. Puede activar EDA, ML, AutoML, frontend, backend, BigQuery, APIs o archivos locales, pero no debe ser la memoria canónica.

La implementación empieza siempre con preservación. Ningún archivo se debe mover, borrar, reemplazar o normalizar antes de tener respaldo verificable.

## Estado Implementado

### Fase 0 — Preservación

Completado.

Backup local creado en:

```text
~/.negritaos/backups/2026-05-17_150934/
```

Incluye, por proyecto:

- branch, HEAD, remotes y upstream.
- `git status --short --branch --ignored`.
- diff staged y unstaged.
- lista de untracked.
- lista de ignored relevantes para `.codex`, `.claude`, `.cursor`, `.gemini`.
- tarballs de carpetas locales de agentes cuando existen.
- bundle de commits locales para `proj_data_analytics`, que estaba ahead `6`.

Estado observado:

- `proj_data_analytics`: branch `feature/updating_analysis_with_fr_pr`, ahead `6`; `.codex` y `.claude` ignorados.
- `moneyflowlist`: branch `dev`; `.codex`, `.claude`, `.cursor` ignorados.
- `ml_automl_autogluon`: branch `feature/ai_ml_development_as_software_dev`; `.codex` trackeado con cambios pendientes. No se modificó.
- `composer-local-dev`: branch `main`, behind `16`; `.codex` untracked y respaldado.

### Fase 1 — Memoria Local Canónica

Completado.

Estructura creada:

```text
~/.negritaos/memory/
  README.md
  personal/
    voice.md
    working_style.md
    team_lead_operating_model.md
    presentation_style.md
  projects/
    negritaos/
    proj_data_analytics/
    ml_automl_autogluon/
    moneyflowlist/
    composer_local_dev/
```

Cada proyecto tiene:

```text
index.md
observations.jsonl
sessions/
decisions/
tasks/
legacy_import/
```

### Fase 2 — Importación Copy-only De Memoria Existente

Completado.

Importación realizada con ID:

```text
2026-05-17_151111
```

Reglas aplicadas:

- Se copiaron memorias existentes a `legacy_import/`.
- No se borró ni modificó la memoria original en los repos.
- Se extrajeron líneas candidatas de MoneyFlow desde la memoria legacy de `proj_data_analytics`.
- Se extrajeron líneas candidatas de Analytics/Hot/EDA para `proj_data_analytics`.
- `ml_automl_autogluon` y `composer_local_dev` registran explícitamente que no tenían `.codex/memory` al momento de la importación.

### Fase 3 — Registry Central De NegritaOS

Completado.

Nuevas carpetas:

```text
archetypes/
projects/
```

Arquetipos creados:

- `eda-analytics.yaml`
- `ml-automl.yaml`
- `product-app.yaml`
- `data-platform.yaml`

Registros de proyecto creados:

- `projects/proj_data_analytics.yaml`
- `projects/ml_automl_autogluon.yaml`
- `projects/moneyflowlist.yaml`
- `projects/composer_local_dev.yaml`
- `projects/negritaos.yaml`

### Fase 4 — Adaptadores `.codex` Por Repo

Parcialmente completado.

Adaptadores escritos de forma segura en repos con `.codex` ignorado o untracked:

- `/Users/jackyb-cqi/repos/proj_data_analytics/.codex/project.yaml`
- `/Users/jackyb-cqi/repos/proj_data_analytics/.codex/local-overrides.md`
- `/Users/jackyb-cqi/repos/backup_repos/moneyflowlist/.codex/project.yaml`
- `/Users/jackyb-cqi/repos/backup_repos/moneyflowlist/.codex/local-overrides.md`
- `/Users/jackyb-cqi/repos/composer-local-dev/.codex/project.yaml`
- `/Users/jackyb-cqi/repos/composer-local-dev/.codex/local-overrides.md`

No se tocó `ml_automl_autogluon/.codex` porque tiene cambios trackeados pendientes. Se dejó tarea diferida en:

```text
~/.negritaos/memory/projects/ml_automl_autogluon/tasks/deferred_codex_adapter.md
```

## Flujo Operativo De Sesión

Al empezar una sesión:

1. Detectar repo actual.
2. Leer `NegritaOS/projects/<project>.yaml`.
3. Leer memoria personal mínima desde `~/.negritaos/memory/personal`.
4. Leer memoria del proyecto desde `~/.negritaos/memory/projects/<project>`.
5. Leer `.codex/project.yaml` del repo si existe.
6. Activar agentes y perfiles según la tarea.

Durante la sesión:

- Decisiones durables van a `decisions/`.
- Aprendizajes van a `observations.jsonl`.
- Cierres de trabajo van a `sessions/`.
- Próximos pasos van a `tasks/`.

Al cerrar:

- Actualizar `index.md`.
- Escribir resumen de sesión.
- Registrar riesgos, decisiones y próximos pasos.

## Reglas De Seguridad

- No usar `rm`, `git reset`, `git checkout --`, `git restore` ni operaciones destructivas.
- No convertir `.codex` trackeado a local/ignorado sin revisión explícita.
- No sobrescribir memoria existente.
- Primero copiar, luego comparar, luego apuntar al nuevo sistema.
- La limpieza se hace en una fase posterior, nunca durante la migración inicial.

## Validación Pendiente

- Curar manualmente las líneas MoneyFlow importadas desde `proj_data_analytics`.
- Clasificar los cambios `.codex` trackeados en `ml_automl_autogluon`.
- Decidir si el registry de NegritaOS se debe commitear como sistema central.
- Decidir si los adaptadores `.codex` locales quedan ignorados permanentemente o si cada repo necesita un adapter mínimo versionado.
