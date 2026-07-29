# Skill: TFM Academic Reviewer

**Type:** Domain — Academic
**Applicable agent:** `tfm_evaluator_agent`
**Activation wrapper:** `.codex/skills/tfm-academic-reviewer/SKILL.md`

## Purpose

Performs standardized, reproducible final reviews of Master's Thesis documents
in Artificial Intelligence. The uploaded thesis is always the primary object
of analysis. The benchmark PDFs calibrate severity and tone only.

## Authoritative References

- Operational scoring contract: `rubrics/academic_tfm_reviewer_rubric.yaml`
- Benchmark resolution and calibration: `skills/academic/tfm_benchmark_registry.md`
- Existing proposal and milestone gates: `rubrics/academic_tfm_rubric.yaml`
- Applied UVI context: `rubrics/uvi_master_rubric.yaml`
- External textual rubric when available through the project registry:
  `project.local_paths.tools/TFM_Modelos/rubric_v1_light.md`

Do not state that `rubric_v1_2025_full.md` was loaded unless that exact file is
present and readable.

## When To Use

Use this skill for a complete TFM PDF review, final draft review, academic
tribunal preparation, or a publication-readiness assessment. Use the existing
proposal or milestone skills for early-stage feasibility checks unless the user
explicitly requests the full reviewer output.

## Review Protocol

1. Identify the thesis language, document stage, title, author, program, and
   available page count. Respond in the thesis language unless the user asks for
   another language.
2. Inspect the uploaded thesis before opening benchmarks. Confirm whether text
   extraction is reliable; if pages are image-only, mark OCR-dependent findings
   as uncertain.
3. Load the operational rubric and benchmark registry. Keep uploaded-thesis
   evidence, benchmark calibration, and evaluator inference as separate layers.
4. Build an evidence map for problem, justification, delimitation, hypothesis,
   variables, objectives, data, methodology, model development, validation,
   metrics, results, discussion, conclusions, limitations, future work, and
   references. Record page numbers for material findings.
5. Score the four required table criteria from 0 to 4: Literature Review,
   Research Design, Technical Quality, and Academic Writing. Explain each score
   with thesis evidence. Use `N/D` for Benchmark Avg. unless numeric calibration
   records are explicitly available.
6. Convert the weighted 0–4 score into the final 1–10 grade using the formula in
   the operational rubric. Apply critical-failure constraints and never raise a
   score merely to match a benchmark label.
7. Review model metrics according to task type. Check baselines, split strategy,
   leakage, class imbalance, calibration, stability, drift, uncertainty,
   reproducibility, and application/business impact when relevant. Accuracy,
   precision, recall, and F1 are not universal metrics.
8. Compare five concrete results with the state of the art. Require a named
   source, result or metric, direction of comparison, and implication. If the
   thesis lacks the evidence, say so.
9. List exactly five high-value issues with page references when page evidence
   exists. Include the impact and a concrete correction.
10. Identify formulaic language only as linguistic indicators. Never present
    them as proof of AI authorship. Give an authentic academic rewrite.
11. Write five reflective and five technical mastery questions with concise,
    evidence-grounded model answers. Do not imply that the student supplied the
    answers.
12. End with the mandatory `Final Academic Review` section and its summary table.

## Required Output Structure

Use these headings in this order:

1. `Scoring Table (0–4 Scale)`
2. `Section-by-Section Feedback`
3. `Five Key Issues`
4. `AI-Generated Text Indicators`
5. `Discussion vs. State of the Art`
6. `Reflective Questions`
7. `Technical Mastery Questions`
8. `Model Metrics Summary`
9. `Recommendations`
10. `Final Academic Review`

The final section must include: Academic & Methodological Summary, Discussion
vs. State of the Art, Reflective & Mastery Questions, Research Structure &
Conclusions, Recommendations, Final Grade (1–10), and the final summary table
defined in the operational rubric.

## Evidence And Style Rules

- Use formal, impersonal, analytically rigorous language.
- Distinguish observation, evidence, inference, and recommendation.
- Explain every numeric score.
- Flag missing, outdated, inconsistent, or uncited references.
- Check that figures, tables, and annexes are referenced and interpreted.
- Check conclusions against objectives, variables, results, and limitations.
- Include the academic and technical value of business segmentation when the
  thesis contains segmentation or business-risk claims; otherwise mark it N/A.
- Keep the output concise, but do not omit required sections merely to satisfy a
  fixed character limit.
