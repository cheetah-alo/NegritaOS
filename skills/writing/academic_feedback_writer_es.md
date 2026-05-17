# Skill: Academic Feedback Writer (Español)

**Tipo:** Domain — Writing / Academic
**Agentes aplicables:** uvi_master_ia_agent

## Propósito
Produce feedback académico en español para TFMs del Máster en IA de la UVI.
Feedback constructivo, específico, accionable y proporcional al nivel del programa.

---

## Estructura de feedback

### Bloque positivo (siempre primero)
Identificar 2-3 fortalezas genuinas del trabajo. No fabricar elogios.
Fortalezas válidas: dataset bien seleccionado, metodología correctamente justificada,
resultados bien interpretados, estructura clara, limitaciones honestas.

```
PUNTOS FUERTES:
1. [Fortaleza 1 — con evidencia específica del documento]
2. [Fortaleza 2 — con evidencia específica]
```

### Bloque de mejoras (estructurado por dimensión)
Para cada debilidad: indicar exactamente qué es, por qué es un problema,
y qué cambio concreto lo resuelve.

```
ÁREAS DE MEJORA:

[DIMENSIÓN]: [Nombre de la dimensión evaluada]
Problema: [Qué específicamente no está bien]
Impacto: [Por qué afecta la calidad del trabajo]
Acción requerida: [Qué exactamente debe cambiar — específico y alcanzable]
```

### Bloque de nota y decisión
```
NOTA PROPUESTA: [X.X / 10]
DECISIÓN: [Apto / Apto con condiciones / No apto]
Condiciones (si aplica): [Lista de condiciones para aprobación]
```

---

## Calibración de feedback por nivel

| Nota | Indicadores reales |
|------|--------------------|
| 9-10 | Metodología sólida, resultados bien interpretados, limitaciones honestas, redacción clara |
| 7-8 | Trabajo completo y correcto, con 1-2 debilidades menores que no invalidan el trabajo |
| 5-6 | Trabajo aprobable pero con debilidades estructurales que deben mejorar en la versión final |
| < 5 | Error metodológico grave (leakage confirmado, objetivos no medibles, datos inaccesibles) |

---

## Frases a evitar

| Frase a evitar | Por qué | Alternativa |
|----------------|---------|-------------|
| "Trabajo interesante" | No aporta información | "El dataset seleccionado es adecuado porque..." |
| "Buen esfuerzo" | Condescendiente, sin criterio | "La estructura del documento es clara y bien organizada" |
| "Se podría mejorar" | Vago | "El objetivo 2 no es medible. Reescribirlo como: 'Lograr recall ≥ 0.80 en holdout'" |
| "No es suficientemente profundo" | Sin criterio | "El análisis de SHAP está presente pero no interpreta los 3 features principales en contexto de negocio" |
| "El tema es muy común" | No es criterio válido | Evaluar si el enfoque es diferenciado, no si el tema es popular |

---

## Protocolo para TFMs con errores graves

Si se detecta leakage confirmado, objetivos circulares o datos inaccesibles:
1. Describir el error con precisión técnica
2. Explicar por qué invalida los resultados o el trabajo
3. Proponer el camino de corrección de forma clara
4. No suspender sin explicar cómo se podría recuperar

```
ERROR CRÍTICO DETECTADO:
Tipo: [Leakage / Objetivo_no_medible / Dataset_inaccesible]
Descripción: [Exactamente qué y dónde]
Impacto: [Por qué invalida el trabajo o una parte de él]
Corrección requerida: [Qué debe hacer el estudiante]
```
