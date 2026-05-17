# Análisis de Churn — Hot / HotMobile

> **TL;DR:** [Tasa de churn observada, segmento más afectado, revenue at risk, recomendación principal]

**Cliente:** Hot / HotMobile | **Fecha:** DD/MM/YYYY | **Versión:** v1.0
**Período de análisis:** [DD/MM/YYYY — DD/MM/YYYY]
**Preparado por:** CQISense

---

## 1. Definición de churn utilizada

> Crítico: sin definición explícita el análisis no es reproducible.

- **Evento de churn:** [portabilidad / cancelación de contrato / inactividad > N días / baja de servicio]
- **Ventana de predicción:** [churn en los próximos X días desde la fecha de scoring]
- **Aplicable a:** [Hot / HotMobile / Ambas — si ambas, resultados separados]

---

## 2. Overview de churn — Período analizado

| Métrica | Hot | HotMobile | Total |
|---------|-----|-----------|-------|
| Base de clientes (inicio período) | | | |
| Clientes que churnearon | | | |
| Churn rate | X% | X% | X% |
| Revenue perdido por churn | €X | €X | €X |
| ARPU de clientes churned | €X | €X | |

**Baseline churn histórico (12m previos):** X%
**Desviación vs. baseline:** ±X% → [Significativa / Normal / Por debajo de lo esperado]

---

## 3. Segmentación del churn

### Por valor de cliente (ARPU tier)
| Tier | Clientes churned | % del total churned | Revenue perdido | Churn rate del tier |
|------|-----------------|---------------------|----------------|---------------------|
| Alto ARPU (>€X) | | | €X | X% |
| Medio ARPU (€X-€X) | | | | |
| Bajo ARPU (<€X) | | | | |

### Por tipo de producto
| Producto | Churn rate | vs. Total | Revenue at risk residual |
|----------|-----------|-----------|--------------------------|
| Fibra / Broadband | | | |
| TV / Cable | | | |
| Móvil Postpago | | | |
| Móvil Prepago | | | |

### Por antigüedad
| Antigüedad | Churn rate | Observación |
|------------|-----------|-------------|
| < 6 meses | | |
| 6-24 meses | | |
| > 24 meses | | |

---

## 4. Performance del modelo de churn *(si aplica)*

- **Modelo:** [XGBoost / LightGBM / etc.]
- **Threshold utilizado:** [X] — Justificación: [...]
- **AUC-ROC en holdout:** X
- **Recall en top 10% scoring:** X% de churners reales capturados
- **Lift:** Xx vs. baseline aleatoria
- **Leakage detectado:** [Sí — detalle / No]

**Interpretación operacional:**
> [El modelo permite identificar N clientes de alto riesgo, concentrando el X% del revenue at risk en los primeros Y% del ranking. Una campaña sobre el top Z% costaría €X y protegería €Y en revenue.]

---

## 5. Drivers de churn identificados

| Driver | Magnitud | Tipo | Evidencia |
|--------|---------|------|-----------|
| [Precio / Competencia] | Alta | Externo | |
| [Calidad de red] | Media | Operacional | |
| [Fin de promoción] | Alta | Contractual | |
| [Tiempo de resolución de incidencias] | Media | CX | |

---

## 6. Revenue at risk

| Segmento | Clientes alto riesgo | ARPU | Revenue at risk mensual |
|----------|---------------------|------|------------------------|
| | | €X | €X |
| **Total** | | | **€X** |

---

## 7. Recomendaciones de retención

| # | Segmento objetivo | Acción | Revenue protegido estimado | Coste estimado | Prioridad |
|---|------------------|--------|--------------------------|----------------|-----------|
| 1 | | | €X | €X | Alta |
| 2 | | | | | |

---

## 8. Próximos pasos

1. [Acción — Responsable — Fecha]
2. [Acción — Responsable — Fecha]

---

*CQISense — NegritaOS / hot_operations_agent | v1.0*
