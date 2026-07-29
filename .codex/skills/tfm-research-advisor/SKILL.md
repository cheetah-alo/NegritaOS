---
name: tfm-research-advisor
description: >
  Investigates and proposes academically strong, publishable Master's Thesis
  titles using recent literature, a read-only previous-proposal corpus, and
  legally validated public datasets. Trigger: new TFM titles, research gaps,
  topic scouting, dataset-backed thesis ideas, or publication-oriented TFM
  proposals.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Investigating or proposing new TFM titles"
    - "Finding research gaps supported by recent papers"
    - "Validating public datasets for a thesis topic"
    - "Comparing TFM ideas for feasibility and publication potential"
---

# TFM Research Advisor

Read `skills/academic/tfm_research_advisor.md` before proposing or ranking any
TFM topic. Reuse the existing academic skills instead of copying their rules:

- `skills/academic/tfm_opportunity_mapping.md`
- `skills/academic/paper_synthesizer.md`
- `skills/academic/research_quality_review.md`
- `skills/academic/dataset_validation.md`
- `skills/academic/objective_alignment.md`
- `skills/academic/methodology_review.md`

## Non-negotiable activation rules

- Produce three to five ranked candidate cards unless the user requests one.
- Require at least five recent, traceable supporting papers per candidate.
- Verify the dataset from an official source, its license or terms, documentation,
  actual access route, schema, target, and legal/reproducible use.
- Inspect a configured previous-proposal corpus in read-only mode before claiming
  non-duplication. Without it, label differentiation as unverified.
- Treat originality as a bounded differentiation hypothesis, never as a fact
  inferred from a few search results.
- Match the language of the TFM or user request.
- Include the eight 1-10 dimensions, the mean, the evidence state, gates,
  roadmap, risks, model choice, leakage controls, and task-appropriate metrics.
- Do not use the five reviewer benchmark PDFs as a source of topics, content,
  grades, or novelty. They are only reviewer calibration material.
- Do not modify proposal PDFs, benchmark PDFs, datasets, or external repositories.

## Invocation inputs

Accept a project-provided `proposal_corpus` path or inventory when available.
Also record domain, language, duration, student count, compute, ethics limits,
and preferred scientific areas. If any of these materially affect feasibility,
ask for them or state the assumption before ranking.

## Quality gate

The answer is incomplete when any candidate lacks:

1. a measurable research question and hypothesis;
2. a concrete dataset with legal-access evidence;
3. five paper references with official links or DOI;
4. a leakage-aware evaluation design;
5. a scoped roadmap and explicit risks;
6. a differentiation status based on the available proposal corpus.
