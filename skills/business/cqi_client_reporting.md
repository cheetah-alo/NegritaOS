# Skill: CQI Client Reporting

**Tipo:** Domain — Business
**Agentes aplicables:** hot_operations_agent, moneyflow_analyst_agent, presentation_agent

## Propósito
Garantiza que cualquier output destinado a cliente (Hot, HotMobile u otros)
sigue los estándares de marca CQISense, estructura correcta, y nivel de comunicación
apropiado para la audiencia del cliente.

---

## Estándares de entrega CQISense

### Identidad de marca
- **Empresa:** CQISense (cqisense.com)
- **Paleta primaria:** Azul `#0044ff`, carbón `#232324`, blanco `#ffffff`
- **Tipografía:** Arial (headings), Malgun Gothic (body)
- **Referencia completa:** `brands/cqi/brand_style/brand_style.md`

### Documentos formales (propuestas, informes, business plans)
- Usar plantillas en: `brands/cqi/plantillas/`
- Idioma: **español** para narrativa; inglés para código, SQL, métricas técnicas
- Versión del documento en el header: `v1.0`
- Footer o metadatos: Fecha + Autor + Estado (Borrador / En revisión / Aprobado)

### Presentaciones ejecutivas para cliente
- Seguir estructura top-down: TL;DR → Contexto → Hallazgos → Recomendaciones → Próximos pasos
- Audiencia ejecutiva de telecom: sin jerga de ML, traducir a KPIs de negocio
- Cada slide: un mensaje central + evidencia
- Usar colores CQI — no introducir paletas externas

---

## Protocolo de entrega por tipo de output

### Informe de análisis (Notion/Confluence/PDF)
```
Estructura requerida:
1. TL;DR (callout, máximo 4 líneas)
2. Contexto del análisis
3. Metodología resumida (para audiencia técnica) o omitida (ejecutiva)
4. Hallazgos principales (numerados, con evidencia)
5. Implicaciones de negocio
6. Recomendaciones (propietario + plazo)
7. Próximos pasos
```

### Propuesta técnica
- Usar: `brands/cqi/plantillas/template_propuesta_tecnica.md`
- Incluir siempre: problema → solución → impacto estimado → plazo → decisión requerida

### Business plan
- Usar: `brands/cqi/plantillas/template_business_plan.md`
- Secciones obligatorias: resumen ejecutivo, mercado, modelo de negocio, riesgos, métricas de éxito

### Decision document
- Usar: `brands/cqi/plantillas/template_decision_doc.md`
- Siempre incluir: opciones evaluadas, criterios de decisión, decisión tomada, supuestos

---

## Reglas de calidad para entrega a cliente

| Criterio | Requerimiento |
|----------|--------------|
| Idioma | Español para narrativa; inglés solo para código/configs |
| TL;DR | Obligatorio en todo documento > 1 página |
| Evidencia | Cada hallazgo debe ser reproducible o citado |
| Recomendaciones | Deben ser accionables con propietario identificable |
| Métricas | Contextualizadas en negocio, no solo reportadas |
| Brand | Colores, fuentes y estructura CQI en docs formales |
| Limitaciones | Siempre explícitas — no ocultar incertidumbre al cliente |

---

## Errores comunes al generar outputs de cliente

- **Usar jerga de ML sin traducción**: "AUC de 0.82" sin decir qué significa operacionalmente
- **TL;DR que describe el documento en lugar de resumir las conclusiones**
- **Recomendaciones sin propietario**: "Se debería analizar X" — ¿quién? ¿cuándo?
- **Mezclar Hot y HotMobile sin separación clara** en un mismo párrafo
- **No contextualizar el baseline**: "churn bajó 2%" — ¿respecto a qué?
