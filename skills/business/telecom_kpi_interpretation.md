# Skill: Telecom KPI Interpretation

**Tipo:** Domain — Business
**Agentes aplicables:** hot_operations_agent, moneyflow_analyst_agent

## Propósito
Garantiza que los KPIs de telecomunicaciones se interpretan en contexto de negocio,
no solo se reportan como cifras. Cada métrica debe ir acompañada de su implicación operativa.

---

## Glosario de KPIs críticos y cómo interpretarlos

### Churn Rate
**Definición:** Porcentaje de clientes que abandonan en un período dado.
**Cómo reportar:**
```
Churn mensual: X% → equivale a N clientes → impacto en revenue: €M al mes
Comparar contra: baseline histórico, benchmark industria (telecom EU: ~1-2% mensual)
```
**Error común:** Reportar churn rate sin definir el evento de churn. ¿Es portabilidad, inactividad, cancelación?

### ARPU (Average Revenue Per User)
**Definición:** Ingresos promedio por usuario activo por mes.
**Cómo reportar:**
```
ARPU: €X (total) → desagregar por segmento: prepago vs. postpago, Hot vs. HotMobile
Tendencia: compara ARPU actual vs. ARPU hace 6m, 12m
Driver: cambios en plan mix, upsell, downgrade forzado
```
**Error común:** ARPU agregado sin desagregación pierde información de mix shift.

### NPS (Net Promoter Score)
**Definición:** % Promotores − % Detractores (escala −100 a +100).
**Cómo reportar:**
```
NPS: +X → posicionar en contexto: telecom EU media ~20-30
Segmentar por: servicio (móvil, fibra, TV), motivo de contacto, tiempo como cliente
Acción: ¿qué hace que los detractores sean detractores? Cruzar con tickets de soporte.
```
**Error común:** Reportar NPS agregado sin identificar drivers de detractores.

### Churn Revenue Impact vs. Churn Rate
**Distinción crítica:**
```
Churn rate = % de clientes que se van (volumen)
Churn revenue impact = cuánto revenue se pierde (valor)
Clientes de alto ARPU con bajo churn rate pueden tener MAYOR impacto en revenue que
muchos clientes de bajo ARPU con alto churn rate.
```
Siempre reportar ambos cuando el análisis es de retención.

### Lift (en modelos de propensión)
**Definición:** Cuántas veces mejor que aleatorio es el modelo en detectar el evento.
**Cómo reportar:**
```
Top 10% de scoring captura X% de churners reales
Lift = X (ej. 3.5x) → el modelo detecta 3.5 veces más churners que selección aleatoria
Comparar con: política actual del cliente (¿hay alguna? ¿Es solo aleatorio?)
```

### Plan Mix
**Definición:** Distribución de clientes por tipo de plan.
**Por qué importa:** Cambios en plan mix explican movimientos de ARPU sin cambio en base de clientes.
```
Si plan mix se desplaza hacia planes más baratos → ARPU baja aunque clientes crezcan
Ojo con: migraciones forzadas (end-of-life de planes), promociones agresivas
```

### Revenue at Risk
**Definición:** Revenue mensual proveniente de clientes clasificados como alto riesgo de churn.
**Cómo calcular:**
```
Revenue at risk = ARPU_segmento × Clientes_high_risk
Priorizar intervención por revenue at risk, no solo por churn rate
```

---

## Protocolo de interpretación para análisis de monitoreo

Para cualquier KPI que se reporte en un dashboard de monitoreo:
1. Valor actual vs. baseline (histórico o target)
2. Tendencia (últimas 4–8 semanas si disponible)
3. Segmentación relevante (Hot/HotMobile, prepago/postpago, etc.)
4. Driver identificado o hipótesis si hay desviación
5. Acción recomendada si hay desviación significativa (>10% del baseline)
