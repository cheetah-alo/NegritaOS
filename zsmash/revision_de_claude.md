Perfecto. Ahora tengo 95% de confianza. Te doy mi dictamen antes de tocar nada.

---

## Dictamen Arquitectónico

**No recomiendo integración. Recomiendo federación.**

La diferencia es crítica:

- **Integración** = fusionar ambos sistemas en uno → viola separación de concerns, genera bloat, rompe el principio de `no_orphan_content`. Un agente de evaluación académica no necesita saber nada de React 19.
- **Federación** = cada sistema mantiene su dominio, se comunican a través de interfaces definidas → limpio, portable, mantenible.

---

## Propuesta: Arquitectura Federada

```
NegritaOS/                          ← Cognitive OS (always active)
│
├── .codex/                         ← Engineering Execution Module (context-activated)
│   │
│   ├── core/                       ← Universal — always loads
│   │   ├── rules/                  ← ai-behavior, coding-standards, naming,
│   │   │                               logging, error-handling, data-contracts,
│   │   │                               data-validation, tests, notebooks
│   │   └── skills/                 ← python-core, create-unittest, eda-reports,
│   │                                   data-analytics, data-contracts, data-loading,
│   │                                   memory-protocol, rule-compliance-gate,
│   │                                   commit-hygiene, pr-review-deep
│   │
│   ├── stacks/                     ← Profile-activated, NOT always loaded
│   │   ├── web/                    ← react-19, nextjs-15, django-drf, playwright,
│   │   │                               tailwind-4, typescript, zod-4, zustand-5
│   │   ├── ml/                     ← data-analytics, eda-reports, data-contracts
│   │   └── backend/                ← api-design, backend-service, mcp-server
│   │
│   ├── profiles/                   ← Context switches (which stack activates)
│   │   ├── analysis-run.yaml       ← ML/data mode (existing)
│   │   ├── eda-pre-ml.yaml         ← EDA mode (existing)
│   │   ├── web-dev.yaml            ← Web stack (NEW — React/Django/Playwright)
│   │   ├── review.yaml             ← Code review (existing)
│   │   └── refactor.yaml           ← Refactor (existing)
│   │
│   ├── projects/                   ← One file per project/job (NEW)
│   │   ├── moneyflowlist.yaml      ← paths, active stack, trusted=true
│   │   └── [next-project].yaml     ← plug-and-play for any future job
│   │
│   ├── system.md                   ← MODIFIED: abstract paths, no hardcodes
│   └── config.toml                 ← MODIFIED: multi-project registry
```

---

## Interfaz entre sistemas

Los agentes de NegritaOS y `.codex` no se mezclan. La comunicación es unidireccional:

```
NegritaOS Router (metaagent_router.yaml)
    │
    ├── Modo CR / MR / DQ  →  activa .codex/core/ + stack según proyecto activo
    │
    ├── Modo AE / RT / EP / LP / TD  →  NegritaOS skills únicamente, .codex inactivo
    │
    └── Stack detection:
            proyecto tiene web-dev.yaml → carga stacks/web/
            proyecto tiene analysis-run.yaml → carga stacks/ml/
```

---

## Qué cambia (cambios mínimos y seguros)

| Archivo | Acción | Riesgo |
|---|---|---|
| `.codex/system.md` | Abstraer paths hardcodeados → `{{PROJECT_ROOT}}` | Bajo |
| `.codex/config.toml` | Convertir en registry multi-proyecto | Bajo |
| `.codex/skills/` | Reorganizar en `core/` y `stacks/` | Medio — no se borra nada |
| `core/orchestration/metaagent_router.yaml` | Añadir regla de activación de `.codex` por modo | Bajo |
| `projects/` (nuevo) | Crear directorio con un yaml por proyecto | Cero — solo addición |

**Nada se elimina. Nada se rompe. Solo se reorganiza y se añade.**

---

## Lo que NO hago

No toco los agentes de NegritaOS (academic-layer, intelligence-layer, strategic-layer). No mergeo skills de `.codex` con los de NegritaOS. No creo abstracciones nuevas sin operación real detrás.
