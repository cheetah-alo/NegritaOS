---
id: team-panel
mode_hint: LP
loads:
  - rules/global/negritaos_router_rule.md
  - integrator.yaml
---

# Team Panel — HOT/Orange Analysis Team

Lanza el panel completo de 5 agentes en paralelo sobre una pregunta de análisis,
diseño de modelo, definición de scope, o decisión de requerimiento.

## Equipo

| Agente | Rol |
|--------|-----|
| **Max** | CEO / Client Vision — visión ejecutiva y presión de negocio |
| **Lea** | Business Owner — contexto operativo del call center |
| **Brene** | Data Scientist — evidencia analítica, features, modelos |
| **Dan** | AI Engineer — prompts, extracción y taxonomías |
| **Blue** | Product Governance — trazabilidad y Decision Records |

## Cuándo usar

- Decisiones de target: ¿recall_24h, risk_discreq o churn_7d?
- Selección de features: ¿qué variables usar sin leakage?
- Definición de scope: ¿qué entra y qué queda fuera de v1?
- Revisión de taxonomías: ¿qué significa `resolved`, `friction`, `promise`?
- Priorización de análisis: ¿qué construir primero para el cliente?

## Procedimiento

### Paso 1 — Genera las cinco perspectivas

Para la pregunta recibida del usuario, produce las 5 perspectivas desde el mismo
contexto NegritaOS. Si el cliente dispone de una herramienta multi-agente, puede
usarse; si no, sintetiza las perspectivas secuencialmente sin depender de
archivos de agente externos.

```
Pregunta del panel: <pregunta del usuario>

Responde desde tu perspectiva como <nombre_agente> en el equipo HOT/Orange.
Sé conciso (3-5 puntos). En español. Incluye tu postura y las preguntas que
harías al resto del equipo.
```

### Paso 2 — Agrega las respuestas

Presenta las 5 respuestas en este orden:
1. Max (presión ejecutiva)
2. Lea (validez operativa)
3. Brene (rigor analítico)
4. Dan (consistencia semántica)
5. Blue (trazabilidad y scope)

### Paso 3 — Genera el Decision Record (Blue)

Después de presentar las 5 perspectivas, Blue produce el Decision Record obligatorio:

```
Decision Record — <fecha ISO> — <tema>

1. Business question:
2. Target:
3. Prediction window:
4. Operational action:
5. Required variables:
6. Risk of ambiguity:
7. Validation criteria:
8. Open questions:
```

### Paso 4 — Guarda en memoria (opcional)

Si se tomó una decisión definitiva, invita al usuario a confirmarla y guárdala
en la memoria canónica del proyecto (`~/.negritaos/memory/projects/<project_id>/decisions/`).

## Notas

- Si el usuario quiere solo uno o dos roles, puede llamarlos directamente por nombre.
- Para decisiones de leakage, Brene lidera. Para scope drift, Blue lidera.
- Max puede cambiar de postura entre turnos — eso es comportamiento esperado.
- El Decision Record es **obligatorio** cuando se define un target o se aprueba un scope.
