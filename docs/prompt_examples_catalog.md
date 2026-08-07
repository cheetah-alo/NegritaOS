# NegritaOS — Catálogo de Prompts por Caso de Uso

**Versión**: 1.0.0  
**Fecha**: Mayo 2026  
**Propósito**: Ejemplos de prompts optimizados para activar correctamente el sistema NegritaOS con sus agentes, skills, rules y quality gates.

---

## 🎯 Estructura Básica de Todo Prompt

```text
CARGA DEL SISTEMA:
Estoy en <project_id>. 
Carga .codex/project.yaml → lee registry NegritaOS/projects/<project_id>.yaml → 
activa agentes + skills + rules + templates → carga memoria ~/.negritaos/memory/projects/<project_id> → 
aplica execution_policy + metaagent_router.

DETECCIÓN AUTOMÁTICA:
- Si hay archivos .py, .sql, .ipynb → activa engineering_rules automáticamente
- Si router mode = CR → activa python_standards, logging, config, reproducibility

CLASIFICACIÓN:
Router mode: [LP / AE / TD / MR / CR / EP / DQ / RT]
Agente(s): [nombre_agente]

TAREA:
[Descripción específica con skills, rules, templates y quality gates]

OUTPUT:
[Formato esperado, idioma, quality warnings visibles]

METADATOS (Generados Automáticamente):
- Source: codex_claude | human | codex_claude_human_reviewed
- Version: 1.0.0 (semantic versioning)
- Generated: YYYY-MM-DD
- Agent: [agent_id]
- Mode: [router_mode]
- Project: [project_id]
- Quality Status: PASSED | PASSED_WITH_WARNINGS | FAILED
```

---

## 📋 Metadatos de Trazabilidad (Automático en Todos los Documentos)

**Todos los documentos generados incluyen metadatos obligatorios:**

```yaml
---
metadata:
  source: codex_claude  # codex_claude | human | codex_claude_human_reviewed | human_codex_enhanced
  document_version: "1.0.0"
  generated_date: "2026-05-19"
  last_modified_date: "2026-05-19"
  agent_id: "model_review_agent"
  router_mode: "MR"
  project_id: "proj_data_analytics"
  template_used: "templates/model_review_report_template.md"
  quality_gates_status: PASSED  # PASSED | PASSED_WITH_WARNINGS | FAILED
  quality_warnings: []
---
```

**En Notion, aparece como callout:**

> 📋 **Document Metadata**
> - **Source:** Codex Claude
> - **Version:** 1.0.0
> - **Generated:** 2026-05-19
> - **Agent:** model_review_agent (MR mode)
> - **Project:** proj_data_analytics
> - **Quality Status:** ✅ Passed

---

## 🐍 Reglas de Python (Activación Automática)

**Se activan AUTOMÁTICAMENTE cuando:**
- Router mode es CR (Code Review)
- Archivos con extensión: `.py`, `.sql`, `.ipynb`, `.yaml`, `.sh`
- Request contiene: "review code", "code review", "check my code"
- Agente es: code_review_agent, model_review_agent (con código)

**Estándares aplicados:**
- **PEP8**: Line length max 100, snake_case variables, PascalCase classes, imports organizados
- **Docstrings**: Obligatorios para funciones públicas (Google/NumPy style)
- **Type Hints**: Obligatorios en signatures (`def func(x: int) -> str:`)
- **File Length**: Max 500 líneas (flag P2 si excede)
- **Function Length**: Max 50 líneas (flag P2 si excede)
- **Max Parameters**: 5 por función (flag P2 si excede)
- **OOP**: Recomendar cuando hay state compartido en 3+ funciones
- **Logging**: Usar `logging`, no `print()` (P1 si falta)
- **Config**: No hardcodear paths/credentials (P0/P1)
- **Reproducibility**: Seeds fijos, dependencies pinned (P1 si falta)

**Severidad:**
- **P0 Critical**: Data leakage, credentials en código, fit en full dataset
- **P1 High**: No logging, hardcoded config, bare except, unpinned deps
- **P2 Medium**: Missing docstrings, type hints, file/function too long
- **P3 Low**: Style violations, whitespace

---

## 📊 Caso 1: Revisión de Modelo ML (Mode: MR)

### Prompt Completo

```text
CARGA DEL SISTEMA:
Estoy en ml_automl_autogluon.
Carga .codex/project.yaml → lee registry NegritaOS/projects/ml_automl_autogluon.yaml →
activa model_review_agent + skills ML + rules/ml/ml_rules.yaml →
carga memoria ~/.negritaos/memory/projects/ml_automl_autogluon.

ROUTER: MR (ML Review)
AGENTE: model_review_agent

TAREA:
Revisar modelo de churn prediction para Hot Telecom.

INPUT:
- Confusion matrix en outputs/churn_model_v2/confusion_matrix.png
- Feature importance en outputs/churn_model_v2/feature_importance.csv
- Classification report en outputs/churn_model_v2/metrics.json
- Dataset: Hot_customers_2026Q1.parquet (100K rows, 45 features)

SKILLS REQUERIDAS:
- skills/ml/model_review.md
- skills/ml/leakage_detection.md
- skills/ml/explainability_review.md
- skills/ml/operational_rule_extraction.md

RULES:
- no_metric_dumping_without_interpretation
- leakage_check_is_first_priority
- imbalance_must_be_addressed_before_metric_claims
- operational_rules_must_not_be_overclaimed

QUALITY GATES:
- target_definition_is_reviewed
- split_strategy_is_assessed
- leakage_risk_is_evaluated
- metrics_are_interpreted_in_business_context
- model_limitations_are_explicit

OUTPUT:
Template: templates/model_review_report_template.md
Formato: Notion-ready markdown
Idioma: Español (código/configs en inglés)
Incluir: Quality warnings si algún gate falla
```

### Prompt Corto (versión rápida)

```text
Estoy en ml_automl_autogluon. LOAD: system + memory.

[MR/model_review_agent] Revisa churn model v2:
- Inputs: confusion_matrix.png, feature_importance.csv, metrics.json
- Skills: model_review, leakage_detection, operational_rule_extraction
- Rules: no metric dumping, leakage first, imbalance awareness
- Template: model_review_report
- Gates: leakage check, metrics contextualized, limitations explicit

Output: Notion markdown, español, quality warnings visibles.
```

---

## 🎓 Caso 2: Evaluación de TFM (Mode: AE)

### Prompt Completo

```text
CARGA DEL SISTEMA:
Estoy en uvi_master_ia_workspace.
Carga .codex/project.yaml → lee registry NegritaOS/projects/uvi_master_ia.yaml →
activa uvi_master_ia_agent + tfm_evaluator_agent + skills académicas →
carga memoria ~/.negritaos/memory/projects/uvi_master_ia.

ROUTER: AE (Academic Evaluation)
AGENTE: uvi_master_ia_agent

TAREA:
Evaluar propuesta de TFM de estudiante UVI Máster IA.

INPUT:
- Documento: TFM_propuesta_juan_garcia.pdf
- Título: "Aplicación de Machine Learning para Detección de Fraude en Transacciones Bancarias"
- Fase: Propuesta inicial (pre-aprobación)

SKILLS REQUERIDAS:
- skills/academic/tfm_evaluation.md
- skills/academic/objective_alignment.md
- skills/academic/methodology_review.md
- skills/academic/dataset_validation.md

RULES:
- objectives_must_be_academic_not_method_names
- title_problem_objective_alignment_required
- dataset_feasibility_must_be_assessed
- conclusions_must_be_bounded_by_results

RUBRICS:
- rubrics/academic_tfm_rubric.yaml
- rubrics/uvi_master_rubric.yaml

QUALITY GATES:
- title_problem_objectives_are_aligned
- objectives_are_measurable
- dataset_is_feasible
- methodology_matches_research_question
- improvement_feedback_is_specific_and_actionable

OUTPUT:
Template: templates/uvi_tfm_evaluation_template.md
Formato: Evaluación dimensionada (OBJ, MET, DATA, RES, PRES)
Idioma: Español
Incluir: Nota propuesta (0-10), puntos fuertes, debilidades con acciones de mejora
Quality warnings: visible
```

### Prompt Corto

```text
Estoy en uvi_master_ia_workspace. LOAD: system + memory.

[AE/uvi_master_ia_agent] Evalúa propuesta TFM:
- Doc: TFM_propuesta_juan_garcia.pdf
- Título: "ML para Detección de Fraude Bancario"
- Skills: tfm_evaluation, objective_alignment, methodology_review, dataset_validation
- Rubrics: academic_tfm_rubric + uvi_master_rubric
- Gates: title-problem-objectives aligned, dataset feasible, feedback actionable

Output: Template uvi_tfm_evaluation, nota 0-10 + justificación, español.
```

---

## 📝 Caso 3: Documentación Técnica (Mode: TD)

### Prompt Completo

```text
CARGA DEL SISTEMA:
Estoy en proj_data_analytics.
Carga .codex/project.yaml → lee registry NegritaOS/projects/proj_data_analytics.yaml →
activa technical_writer_agent + skills writing + rules documentation →
carga memoria ~/.negritaos/memory/projects/proj_data_analytics.

ROUTER: TD (Technical Documentation)
AGENTE: technical_writer_agent

TAREA:
Documentar análisis EDA de Hot/Orange TSR (Technical Service Rate) / CSR (Customer Service Rate).

INPUT:
- Notebook: notebooks/eda_tsr_csr_hot_orange.ipynb
- Plots: outputs/eda_plots/*.png (15 figuras)
- Raw findings: session notes del 15-18 Mayo 2026

SKILLS REQUERIDAS:
- skills/transversal/structured_reasoning.md
- skills/transversal/evidence_framing.md
- skills/transversal/tldr_writer.md
- skills/ml/eda_review.md

RULES:
- no_orphan_plots (cada plot con takeaway)
- no_orphan_sections
- evidence_before_claims
- operational_relevance_first

TEMPLATE: Analytical report structure

OUTPUT SECTIONS:
1. TL;DR (max 150 palabras)
2. Context (problema de negocio Hot/Orange)
3. Objective (qué queríamos descubrir)
4. Methodology (cómo se hizo el EDA)
5. Evidence (plots + tablas interpretadas)
6. Findings (numerados, traceable)
7. Interpretation (qué significan los findings)
8. Risks and Notes (limitaciones de datos)
9. Recommendations (accionables, referenciando findings)
10. Next Actions (con owners o TBD)

QUALITY GATES:
- findings_are_numbered_and_traceable
- recommendations_reference_findings
- no_plot_without_operational_takeaway
- risks_have_severity_labels
- next_actions_have_owners_or_marked_tbd

OUTPUT:
Formato: Notion-ready markdown
Idioma: Español (código/SQL en inglés)
Quality warnings: visible
Destination: documents/ with document-control; persist only reusable findings through /brain remember or /brain handoff
```

### Prompt Corto

```text
Estoy en proj_data_analytics. LOAD: system + memory.

[TD/technical_writer_agent] Documenta EDA TSR/CSR Hot/Orange:
- Inputs: notebook eda_tsr_csr, 15 plots, session notes
- Skills: structured_reasoning, evidence_framing, tldr_writer, eda_review
- Rules: no orphan plots/sections, evidence first, operational relevance
- Template: analytical_report (10 sections: TL;DR → Next Actions)
- Gates: findings numbered, recommendations trace findings, plots interpreted

Output: Notion markdown, español, routed by document-control. Use /brain handoff only for continuation memory.
```

---

## 🎤 Caso 4: Presentación Ejecutiva (Mode: EP)

### Prompt Completo

```text
CARGA DEL SISTEMA:
Estoy en proj_data_analytics.
Carga .codex/project.yaml → lee registry NegritaOS/projects/proj_data_analytics.yaml →
activa presentation_agent + skills executive + rules presentation →
carga memoria ~/.negritaos/memory/projects/proj_data_analytics.

ROUTER: EP (Executive Presentation)
AGENTE: presentation_agent

TAREA:
Crear slide deck ejecutivo sobre resultados churn model Hot para stakeholders C-level.

INPUT:
- Source: Model review report (memory/sessions/2026-05-15_churn_model_review.md)
- Audience: VP Operations, CFO, CTO Hot Telecom
- Duration: 15 min presentación + 10 min Q&A
- Max slides: 10 main + appendix

SKILLS REQUERIDAS:
- skills/executive/executive_summary.md
- skills/executive/presentation_storyline.md
- skills/transversal/tldr_writer.md

RULES:
- top_down_storytelling_required
- one_message_per_slide_enforced
- every_chart_must_have_labeled_takeaway
- appendix_separates_methodology_from_main_story
- audience_must_be_defined_before_structure

RUBRICS:
- rubrics/presentation_quality_rubric.yaml

QUALITY GATES:
- audience_is_defined
- narrative_arc_is_top_down
- each_slide_has_one_core_message
- each_chart_has_takeaway
- recommendation_is_decision_oriented
- appendix_separates_methodology

OUTPUT:
Template: templates/executive_deck_outline_template.md
Estructura:
  1. TL;DR slide (situación + recomendación)
  2-4. Key findings (3 slides, 1 finding/slide)
  5-6. Business impact (cuantificado)
  7-8. Recommendations (decision-ready)
  9. Next steps (owners + timeline)
  10. Q&A
  Appendix: Metodología técnica, métricas completas

Idioma: Español (gráficos bilingües si es necesario)
Formato: Outline para PPT + speaker notes
Quality warnings: visible
```

### Prompt Corto

```text
Estoy en proj_data_analytics. LOAD: system + memory.

[EP/presentation_agent] Crea deck ejecutivo churn model Hot:
- Source: Model review report (sessions/2026-05-15)
- Audience: C-level (VP Ops, CFO, CTO)
- Slides: 10 main + appendix
- Skills: executive_summary, presentation_storyline, tldr_writer
- Rules: top-down, one message/slide, charts con takeaway, appendix separa metodología
- Gates: narrative top-down, cada slide 1 mensaje, recommendation decision-ready

Output: Template executive_deck_outline + speaker notes, español.
```

---

## 🔧 Caso 5: Code Review (Mode: CR)

### Prompt Completo

```text
CARGA DEL SISTEMA:
Estoy en ml_automl_autogluon.
Carga .codex/project.yaml → lee registry NegritaOS/projects/ml_automl_autogluon.yaml →
activa code_review_agent + skills engineering + rules/engineering →
carga memoria ~/.negritaos/memory/projects/ml_automl_autogluon.

DETECCIÓN AUTOMÁTICA:
Archivos .py detectados → ACTIVA AUTOMÁTICAMENTE:
- rules/engineering/engineering_rules.yaml (version 2.0.0)
  - python_standards (PEP8, docstrings, type hints, file/function length)
  - logging_standards (logging module, levels, structured logging)
  - configuration_management (no hardcoding, config validation)
  - reproducibility (seeds, pinned dependencies, data versioning)
  - ml_pipeline_standards (train/test split, feature engineering, serialization)

ROUTER: CR (Code Review)
AGENTE: code_review_agent

TAREA:
Revisar pipeline de training para production readiness.

INPUT:
- File: src/pipelines/train_churn_model.py (250 líneas)
- File: src/config/model_config.yaml
- File: src/utils/bigquery_loader.py
- Context: Pipeline se ejecutará en Cloud Run cada semana

SKILLS REQUERIDAS:
- skills/engineering/python_quality_review.md
- skills/engineering/sql_bigquery_review.md
- skills/engineering/reproducibility_review.md
- skills/engineering/logging_config_review.md

RULES (AUTO-ACTIVATED):
- python_standards:
  - Line length max 100 (tolerance 120)
  - Docstrings mandatory for public functions
  - Type hints mandatory in signatures
  - Max file length: 500 lines
  - Max function length: 50 lines
  - Max parameters: 5
- logging_standards: logging module (not print), structured logging
- configuration_management: no hardcoded paths/credentials
- reproducibility: random seeds fixed, dependencies pinned
- ml_pipeline_standards: time-based split, no leakage, versioned models

SEVERITY TRIAGE (AUTOMATIC):
- P0: Critical (data leakage, credentials in code, fit on full dataset) → blocker
- P1: High (no logging, hardcoded configs, non-reproducible, unpinned deps) → must fix before merge
- P2: Medium (missing docstrings, type hints, file/function too long) → fix next sprint
- P3: Low (style, minor refactor, whitespace) → backlog

QUALITY GATES:
- P0_and_P1_issues_are_explicitly_flagged
- reproducibility_is_assessed
- logging_coverage_is_reviewed
- data_leakage_paths_are_checked
- configuration_management_is_evaluated
- test_coverage_or_absence_is_noted
- python_standards_compliance_score_included

OUTPUT:
Template: templates/code_review_report_template.md
Formato: 
  - Executive summary (P0/P1 count)
  - Python Standards Compliance Score (0-100)
  - Issues por severity (P0 → P3) con file:line, risk, fix
  - Reproducibility verdict
  - Logging coverage assessment
  - Configuration management assessment
  - Recommended refactors
Idioma: Español (código y nombres técnicos en inglés)
Quality warnings: visible

METADATOS (Generados Automáticamente):
---
metadata:
  source: codex_claude
  document_version: "1.0.0"
  generated_date: "2026-05-19"
  agent_id: code_review_agent
  router_mode: CR
  project_id: ml_automl_autogluon
  template_used: templates/code_review_report_template.md
  quality_gates_status: TBD
  python_standards_applied: true
  engineering_rules_version: "2.0.0"
---
```

### Prompt Corto

```text
Estoy en ml_automl_autogluon. LOAD: system + memory.

[CR/code_review_agent] Revisa training pipeline:
- Files: train_churn_model.py, model_config.yaml, bigquery_loader.py
- Context: Production en Cloud Run, weekly execution

AUTO-ACTIVATED (archivos .py detectados):
- Python standards (PEP8, docstrings, type hints, max lengths)
- Logging standards (logging module, no print)
- Config management (no hardcoding)
- Reproducibility (seeds, pinned deps)
- ML pipeline standards (no leakage, time splits)

Triage: P0-P3 severity
Output: Code review report + Python compliance score + metadatos, español.
```

---

## 🚨 Caso 6: Data Quality Incident (Mode: DQ)

### Prompt Completo

```text
CARGA DEL SISTEMA:
Estoy en proj_data_analytics.
Carga .codex/project.yaml → lee registry NegritaOS/projects/proj_data_analytics.yaml →
activa data_quality_sentinel_agent + skills governance + rules/governance →
carga memoria ~/.negritaos/memory/projects/proj_data_analytics.

ROUTER: DQ (Data Quality / Escalation)
AGENTE: data_quality_sentinel_agent

TAREA:
Documentar y escalar incidente de data quality detectado en pipeline Hot.

INPUT:
- Descripción: NPS scores muestran 0 para segmento HotMobile premium en semana 2026-W20
- Affected table: `hot_analytics.nps_weekly_aggregates`
- Time period: 2026-05-12 to 2026-05-18
- Downstream impact: Dashboard ejecutivo mostrando datos incorrectos
- Evidence: Query reproducible en notebooks/dq_investigation_2026_05_19.ipynb

SKILLS REQUERIDAS:
- skills/governance/risk_framing.md
- skills/transversal/evidence_framing.md
- skills/transversal/structured_reasoning.md

RULES:
- reproducible_evidence_required_before_escalation
- affected_scope_must_be_quantified
- business_impact_must_be_stated
- resolution_criteria_required
- severity_classification_required

SEVERITY SLA:
¿Clasificación correcta?
- P1 Critical: Production KPIs corrupted, models outputting wrong → escalate 1h
- P2 High: Significant gaps, analysis may be invalid → escalate 4h
- P3 Medium: Partial issues, analysis degraded but usable → remediate current sprint
- P4 Low: Minor inconsistencies, no immediate impact → backlog

→ Propongo: P2 (dashboard ejecutivo afectado, pero modelos no impactados aún)

QUALITY GATES:
- affected_tables_and_fields_are_named
- affected_time_period_is_bounded
- severity_is_assigned_with_justification
- evidence_is_reproducible_via_query_or_reference
- business_impact_is_quantified_or_estimated
- resolution_criteria_are_measurable
- escalation_path_is_defined

OUTPUT:
Template: templates/data_quality_incident_template.md
Formato:
  - Incident ID: DQ-2026-05-19-001
  - Severity: P2
  - Affected scope: hot_analytics.nps_weekly_aggregates, HotMobile premium segment
  - Time window: 2026-W20
  - Evidence: Reproducible query
  - Business impact: Dashboard ejecutivo incorrecto → decisiones comerciales en riesgo
  - Resolution criteria: NPS > 0 para todos los segmentos, validación histórica 4 semanas
  - Escalation: Data Engineering team + Hot Business Owner (within 4h)
Idioma: Español
Quality warnings: visible
```

### Prompt Corto

```text
Estoy en proj_data_analytics. LOAD: system + memory.

[DQ/data_quality_sentinel_agent] Documenta incident NPS zeros HotMobile:
- Scope: hot_analytics.nps_weekly_aggregates, segment premium, 2026-W20
- Impact: Dashboard ejecutivo incorrecto
- Evidence: Query reproducible (notebooks/dq_investigation)
- Skills: risk_framing, evidence_framing, structured_reasoning
- Severity: P2 (dashboard afectado, modelos aún no)
- Gates: scope quantified, evidence reproducible, resolution criteria measurable

Output: Template dq_incident, incident ID, escalation path, español.
```

---

## 👔 Caso 7: Decision Support (Mode: LP)

### Prompt Completo

```text
CARGA DEL SISTEMA:
Estoy en proj_data_analytics.
Carga .codex/project.yaml → lee registry NegritaOS/projects/proj_data_analytics.yaml →
activa decision_support_agent + skills governance/executive →
carga memoria ~/.negritaos/memory/projects/proj_data_analytics.

ROUTER: LP (Leadership Planning)
AGENTE: decision_support_agent

TAREA:
Estructurar decisión sobre estrategia de deployment para churn model.

INPUT:
- Contexto: Modelo de churn está listo (AUC 0.82, recall@20% = 0.65)
- Opciones consideradas:
  1. Deploy completo a toda base Hot (2M clientes)
  2. Pilot en segmento alto valor (200K clientes)
  3. Shadow mode (sin acciones, solo tracking) 1 mes
- Stakeholders: VP Operations, Data Science Lead, Engineering Manager
- Decision deadline: 2026-05-30

SKILLS REQUERIDAS:
- skills/transversal/structured_reasoning.md
- skills/executive/executive_summary.md
- skills/governance/risk_framing.md
- skills/transversal/evidence_framing.md

RULES:
- present_options_not_just_recommendations
- trade_offs_must_be_explicit
- risks_must_be_quantified_or_bounded
- assumptions_behind_recommendation_must_be_stated
- decision_criteria_must_be_defined_before_options

QUALITY GATES:
- at_least_two_options_presented
- decision_criteria_defined
- trade_offs_are_explicit
- recommendation_references_criteria
- risks_of_recommended_option_are_stated
- assumptions_are_listed

OUTPUT:
Template: templates/decision_memo_template.md
Formato:
  1. TL;DR (decisión requerida + recomendación en 1 párrafo)
  2. Decision criteria (business impact, risk, speed, learning)
  3. Options analysis:
     - Option 1: Full deploy
     - Option 2: Pilot
     - Option 3: Shadow mode
  4. Trade-off matrix (criteria vs options)
  5. Recommendation (con justificación basada en criteria)
  6. Risks of recommended option
  7. Assumptions
  8. Open questions for decision makers
Idioma: Español
Quality warnings: visible
```

### Prompt Corto

```text
Estoy en proj_data_analytics. LOAD: system + memory.

[LP/decision_support_agent] Estructura decisión deployment churn model:
- Opciones: Full deploy / Pilot / Shadow mode
- Skills: structured_reasoning, risk_framing, evidence_framing, executive_summary
- Rules: present options not just recommendation, trade-offs explicit, risks quantified
- Gates: ≥2 options, criteria defined, trade-offs explicit, assumptions listed

Output: Template decision_memo, español.
```

---

## 🔬 Caso 8: Research Paper Synthesis (Mode: RT)

### Prompt Completo

```text
CARGA DEL SISTEMA:
Estoy en research_workspace.
Carga .codex/project.yaml → lee registry NegritaOS/projects/research_workspace.yaml →
activa paper_review_agent + ai_trend_radar_agent →
carga memoria ~/.negritaos/memory/projects/research_workspace.

ROUTER: RT (Research / TFM Generation)
AGENTE: paper_review_agent

TAREA:
Sintetizar paper de Arxiv sobre federated learning para telecom.

INPUT:
- Paper: "Federated Learning for Network Anomaly Detection in 5G" (Arxiv 2026)
- URL: https://arxiv.org/abs/2026.xxxxx
- Propósito: Evaluar aplicabilidad a Hot network quality monitoring

SKILLS REQUERIDAS:
- skills/academic/paper_synthesizer.md
- skills/academic/research_quality_review.md
- skills/academic/citation_extraction.md
- skills/academic/methodology_deconstruction.md
- skills/academic/tfm_opportunity_mapping.md

RULES:
- no_hallucinated_citations
- evidence_vs_interpretation_separation
- limitations_required
- reproducibility_required

QUALITY GATES:
- objective_is_identified
- dataset_is_identified
- methodology_is_explained
- limitations_are_explicit
- relevance_to_user_domains_is_mapped
- no_hallucinated_citation_included

OUTPUT:
Template: templates/paper_summary_template.md
Formato:
  1. Paper metadata (autores, fecha, venue)
  2. TL;DR (100 palabras)
  3. Research objective
  4. Dataset used
  5. Methodology (step-by-step)
  6. Key findings
  7. Limitations (stated by authors + identified by review)
  8. Reproducibility assessment
  9. Relevance to Hot/CQI domains
  10. Potential TFM topics inspired by this work
Idioma: Español (términos técnicos en inglés)
Quality warnings: visible
```

### Prompt Corto

```text
Estoy en research_workspace. LOAD: system + memory.

[RT/paper_review_agent] Sintetiza paper federated learning 5G:
- Input: Arxiv 2026.xxxxx "Federated Learning for Network Anomaly Detection"
- Purpose: Aplicabilidad a Hot network monitoring
- Skills: paper_synthesizer, methodology_deconstruction, tfm_opportunity_mapping
- Rules: no hallucinated citations, limitations required, reproducibility assessed
- Gates: objective identified, methodology explained, relevance mapped

Output: Template paper_summary, español.
```

---

## 📋 Caso 9: Multi-Agent Pipeline (Mixed Mode: TD + EP)

### Prompt Completo para Pipeline

```text
CARGA DEL SISTEMA:
Estoy en proj_data_analytics.
Carga .codex/project.yaml → lee registry NegritaOS/projects/proj_data_analytics.yaml →
activa multi-agent pipeline (technical_writer_agent → presentation_agent) →
carga memoria ~/.negritaos/memory/projects/proj_data_analytics.

ROUTER: Mixed-mode TD + EP
PIPELINE: technical_writer_agent → presentation_agent

TAREA MULTI-AGENT:
A partir del análisis EDA Hot TSR/CSR:
1. [TD] Crear documentación técnica completa (Notion)
2. [EP] Generar slide deck ejecutivo para stakeholders

INPUT:
- Notebook: notebooks/eda_tsr_csr_hot.ipynb
- Plots: outputs/eda_plots/ (15 figuras)
- Session notes: sessions/2026-05-15_to_2026-05-18.md
- Target audiences:
  - Technical doc: Data Science team
  - Presentation: VP Operations Hot

STEP 1: [TD/technical_writer_agent]
Skills: structured_reasoning, evidence_framing, tldr_writer, eda_review
Rules: no orphan plots/sections, evidence first, operational relevance
Template: analytical_report
Output: Notion-ready markdown
Gates: findings numbered, plots interpreted, next actions with owners

STEP 2: [EP/presentation_agent]
Input: Output from Step 1
Skills: executive_summary, presentation_storyline, tldr_writer
Rules: top-down storytelling, one message/slide, charts with takeaway
Template: executive_deck_outline
Output: Slide outline + speaker notes
Gates: narrative top-down, each slide 1 message, recommendation decision-ready

HANDOFF:
technical_writer_agent pasa a presentation_agent:
- key_findings
- recommendations
- critical_plots
- business_context

OUTPUT FINAL:
1. Notion doc técnico (sessions/2026-05-19_eda_tsr_csr_doc.md)
2. PPT outline (sessions/2026-05-19_eda_tsr_csr_deck.md)
Idioma: Español
Quality warnings: visible para ambos outputs
```

### Prompt Corto para Pipeline

```text
Estoy en proj_data_analytics. LOAD: system + memory.

PIPELINE: TD → EP

[TD/technical_writer_agent] Documenta EDA TSR/CSR →
[EP/presentation_agent] Crea deck ejecutivo.

Input: notebook + 15 plots + session notes
Audiences: DS team (doc) + VP Ops (deck)

Step 1 [TD]: analytical_report, español, Gates: findings numbered
Step 2 [EP]: executive_deck_outline, español, Gates: top-down narrative

Handoff: findings + recommendations + plots → presentation_agent

Output: 2 files (Notion doc + PPT outline), quality warnings visibles.
```

---

## 🎯 Caso 10: Sprint Planning (Mode: LP)

### Prompt Completo

```text
CARGA DEL SISTEMA:
Estoy en proj_data_analytics.
Carga .codex/project.yaml → lee registry NegritaOS/projects/proj_data_analytics.yaml →
activa team_lead_ds_agent + skills governance →
carga memoria ~/.negritaos/memory/projects/proj_data_analytics.

ROUTER: LP (Leadership Planning)
AGENTE: team_lead_ds_agent

TAREA:
Convertir meeting notes de sprint planning en Jira epics + stories estructuradas.

INPUT:
- Meeting: Sprint Planning 2026-S21 (20 Mayo)
- Attendees: DS Lead, 2 Data Scientists, Engineering Manager
- Raw notes:
  """
  - Terminar modelo churn Hot v2
  - Empezar análisis NPS HotMobile por segmento
  - Revisar pipeline BigQuery porque está costando mucho
  - Preparar presentación para VP Operations sobre TSR/CSR
  - Investigar paper de federated learning que mencionó Juan
  - Bug en dashboard: métricas de Orange aparecen mezcladas con Hot
  """
- Sprint duration: 2 semanas (2026-05-20 to 2026-05-31)

SKILLS REQUERIDAS:
- skills/transversal/structured_reasoning.md
- skills/transversal/tldr_writer.md
- skills/governance/risk_framing.md

RULES:
- actionability_required
- owner_dependency_risk_required_in_task_output
- escalation_visibility_required
- no_tasks_without_acceptance_criteria

QUALITY GATES:
- tasks_have_acceptance_criteria
- blockers_are_explicit
- owners_are_identified_or_marked_TBD
- timeline_is_realistic
- risks_are_actionable_not_vague
- no_task_without_defined_output

OUTPUT:
Template: templates/jira_epic_template.md + jira_story_template.md
Formato:
  - Epic 1: Churn Model Hot v2 Completion
    - Story 1.1: Finalizar hyperparameter tuning
    - Story 1.2: Validar en holdout Q1-2026
    - Story 1.3: Code review + reproducibility check
  - Epic 2: NPS HotMobile Segmentation Analysis
  - Epic 3: BigQuery Cost Optimization
  - Epic 4: Executive Presentation TSR/CSR
  - Epic 5: Research Review Federated Learning
  - Bug: Dashboard Orange/Hot Metric Mixing

Cada task con:
- Acceptance criteria
- Owner (o TBD)
- Dependencies
- Risks
- Estimated effort
- Definition of Done

Idioma: Español (código/configs en inglés)
Quality warnings: visible
```

### Prompt Corto

```text
Estoy en proj_data_analytics. LOAD: system + memory.

[LP/team_lead_ds_agent] Convierte sprint planning notes → Jira structure:
- Input: Meeting notes (6 items ambiguos)
- Sprint: 2026-S21 (2 weeks)
- Skills: structured_reasoning, risk_framing, tldr_writer
- Rules: actionability required, owners explicit, acceptance criteria mandatory
- Gates: tasks with AC, blockers explicit, timeline realistic

Output: Epics + stories, cada task con owner/dependencies/risks/DoD, español.
```

---

## 🧩 Plantilla Genérica Adaptable

```text
CARGA DEL SISTEMA:
Estoy en <project_id>.
Carga .codex/project.yaml → lee registry NegritaOS/projects/<project_id>.yaml →
activa <agente(s)> + skills + rules + templates →
carga memoria ~/.negritaos/memory/projects/<project_id>.

ROUTER: <mode_id>
AGENTE: <agent_name>

TAREA:
<descripción clara y específica>

INPUT:
<archivos, contexto, datos necesarios>

SKILLS REQUERIDAS:
- skills/<domain>/<skill_name>.md

RULES:
- <rule_constraint_1>
- <rule_constraint_2>

RUBRICS (opcional):
- rubrics/<rubric_name>.yaml

QUALITY GATES:
- <gate_1>
- <gate_2>

OUTPUT:
Template: templates/<template_name>.md
Formato: <estructura esperada>
Idioma: <español/inglés/mixto>
Quality warnings: visible
```

---

## 📚 Referencia Rápida: Modes y Agentes

| Mode | ID | Agente Principal | Uso Típico |
|------|----|--------------------|------------|
| Leadership Planning | LP | team_lead_ds_agent, decision_support_agent | Roadmaps, tasks, decisions, escalations |
| Academic Evaluation | AE | tfm_evaluator_agent, paper_review_agent, uvi_master_ia_agent | TFM eval, paper synthesis, academic review |
| Technical Documentation | TD | technical_writer_agent | Notion/Confluence docs, memos |
| ML Review | MR | model_review_agent, eda_reviewer_agent | Model review, EDA, explainability |
| Code Review | CR | code_review_agent | Python, SQL, pipeline review |
| Executive Presentation | EP | presentation_agent | Slide decks, executive briefs |
| Data Quality | DQ | data_quality_sentinel_agent | DQ incidents, escalations |
| Research/TFM | RT | ai_trend_radar_agent, research_radar_agent, blockchain_ai_watcher_agent | Paper synthesis, trend tracking |

---

## 🎓 Tips para Prompts Efectivos

### ✅ DO:
- **Siempre carga el sistema completo** al inicio (adapter → registry → memory)
- **Especifica el router mode** para activar el agente correcto
- **Lista las skills específicas** que necesitas
- **Menciona rules y quality gates** para asegurar calidad
- **Define el template de output** esperado
- **Declara idioma** (español/inglés/mixto)
- **Pide quality warnings visibles** al final

### ❌ DON'T:
- No digas solo "sigue con el proyecto" sin cargar contexto
- No omitas el router mode cuando hay ambigüedad
- No pidas outputs sin especificar template o estructura
- No ignores los quality gates (son tu garantía de calidad)
- No mezcles idiomas sin declararlo explícitamente
- No asumas que el agente recuerda contexto de sesiones anteriores sin cargar memoria
- **No especifiques manualmente engineering_rules cuando trabajas con código** — se activan automáticamente

---

## 🚨 IMPORTANTE: Activación Automática de Reglas

### ¿Cuándo se activan automáticamente las reglas de Python/Code?

**TRIGGERS AUTOMÁTICOS (No necesitas pedirlo):**

1. **Por Router Mode:**
   - Router classifica como CR (Code Review) → engineering_rules.yaml se cargan

2. **Por File Extension:**
   - Archivos .py, .sql, .ipynb, .yaml, .sh detectados → python_standards activadas

3. **Por Keywords en Request:**
   - "review code", "code review", "check my code", "review pipeline" → auto-activa

4. **Por Agente:**
   - code_review_agent invocado → engineering_rules cargadas
   - model_review_agent + código → engineering_rules cargadas

**Lo que se activa AUTOMÁTICAMENTE:**
- ✅ PEP8 compliance (line length, naming, imports, whitespace)
- ✅ Docstrings obligatorios (Google/NumPy style)
- ✅ Type hints obligatorios
- ✅ File/function length limits (500/50 lines)
- ✅ OOP recommendations
- ✅ Logging standards (logging module, no print)
- ✅ Configuration management (no hardcoding)
- ✅ Reproducibility (seeds, pinned deps)
- ✅ ML pipeline standards (splits, leakage, serialization)
- ✅ SQL BigQuery cost-awareness

**Lo que NO necesitas especificar manualmente:**
- ❌ "aplica PEP8"
- ❌ "revisa docstrings"
- ❌ "chequea line length"
- ❌ "valida reproducibilidad"

**Esto ya está en el execution_policy y se ejecuta automáticamente.**

---

## 📋 IMPORTANTE: Metadatos Automáticos

### Todos los documentos incluyen metadatos sin pedirlos

**Se generan AUTOMÁTICAMENTE:**

```yaml
---
metadata:
  source: codex_claude  # Siempre presente
  document_version: "1.0.0"  # Semantic versioning
  generated_date: "2026-05-19"
  last_modified_date: "2026-05-19"
  agent_id: "agent_name"  # Del agent contract
  router_mode: "MODE_ID"  # Del metaagent_router
  project_id: "project_name"  # Del .codex/project.yaml
  template_used: "templates/template_name.md"
  quality_gates_status: PASSED | PASSED_WITH_WARNINGS | FAILED
  quality_warnings: []
---
```

**En Notion aparece como:**

> 📋 **Document Metadata**
> - **Source:** Codex Claude
> - **Version:** 1.0.0
> - **Generated:** 2026-05-19
> - **Agent:** model_review_agent (MR mode)
> - **Project:** proj_data_analytics
> - **Quality Status:** ✅ Passed

**Valores posibles de `source`:**
- `codex_claude` — Generado por AI (default)
- `human` — Escrito por humano
- `codex_claude_human_reviewed` — Generado por AI, revisado por humano
- `human_codex_enhanced` — Escrito por humano, mejorado por AI

**NO necesitas especificar metadatos en el prompt** — se inyectan automáticamente por execution_policy.

---

## 🔗 Enlaces Útiles

### Core System
- **Core Principles**: `/Users/jackyb-cqi/repos/NegritaOS/core/core-principles.md`
- **Metaagent Router**: `/Users/jackyb-cqi/repos/NegritaOS/core/orchestration/metaagent_router.yaml`
- **Execution Policy v2.0**: `/Users/jackyb-cqi/repos/NegritaOS/core/orchestration/execution_policy.yaml`
- **Agent Registry**: `/Users/jackyb-cqi/repos/NegritaOS/agents/README.md`

### Standards
- **Document Metadata Standards**: `/Users/jackyb-cqi/repos/NegritaOS/core/standards/document_metadata_standards.yaml`
- **Output Standards**: `/Users/jackyb-cqi/repos/NegritaOS/core/standards/output_standards.yaml`
- **Naming Conventions**: `/Users/jackyb-cqi/repos/NegritaOS/core/standards/naming_conventions.md`

### Rules
- **Global Rules**: `/Users/jackyb-cqi/repos/NegritaOS/rules/global/global_rules.yaml`
- **Engineering Rules v2.0**: `/Users/jackyb-cqi/repos/NegritaOS/rules/engineering/engineering_rules.yaml` ⚠️ **Auto-activa con código**
- **ML Rules**: `/Users/jackyb-cqi/repos/NegritaOS/rules/ml/`
- **Academic Rules**: `/Users/jackyb-cqi/repos/NegritaOS/rules/academic/`

### Agents
- **All Agents**: `/Users/jackyb-cqi/repos/NegritaOS/<layer>/<agent-name>/agent.yaml`

---

**Última actualización**: 19 Mayo 2026  
**Versión del sistema**: NegritaOS 2.0.0  
**Execution Policy**: v2.0 (metadatos automáticos + engineering rules auto-activation)  
**Engineering Rules**: v2.0 (Python standards completos + auto-triggers)
