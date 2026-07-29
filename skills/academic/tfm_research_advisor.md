# TFM Research Advisor

**Type:** Domain - Academic / Research Design
**Applicable agents:** ai_trend_radar_agent, paper_review_agent

## Purpose

Investigates and proposes new Master's Thesis (TFM) titles that are academically
strong, executable in three to six months, empirically testable, and suitable
for publication or further doctoral work. This skill specializes the existing
`tfm_opportunity_mapping`, `paper_synthesizer`, `research_quality_review`, and
`dataset_validation` skills; it does not replace them.

The output is a ranked shortlist of differentiated research opportunities, not
a list of attractive keywords. A title is only recommended when its research
question, evidence base, data access, evaluation design, and scope are aligned.

## Activation Contract

Activate when the user asks to:

- investigate or propose new TFM titles or research topics;
- identify research gaps with academic and industrial relevance;
- compare possible TFM topics for publication potential;
- find a public dataset and papers for a proposed TFM;
- turn AI, ML, XAI, NLP, LLM, survival, causal, GNN, federated, blockchain,
  telecom, finance, insurance, airline, health, energy, or cybersecurity signals
  into a defensible research proposal.

The request must provide, or the agent must establish before ranking:

- target language and academic programme;
- domain, decision problem, or research area;
- expected duration, number of students, and available compute;
- legal or ethics constraints;
- a readable corpus of previous proposals when non-duplication is required.

If the previous-proposal corpus is not configured or supplied, state:
`Differentiation against the local proposal corpus was not verified.` Do not
present an unverified originality claim as fact.

## Evidence Policy

### Literature

- Use at least five supporting papers per shortlisted title.
- Prefer peer-reviewed or formally published work from the last three years
  relative to the review date. A seminal paper up to five years old is allowed
  only when its role is explained.
- Prioritize Nature, Science, IEEE, ACM, Springer, Elsevier, AAAI, NeurIPS,
  ICML, ICLR, KDD, WWW, ACL, EMNLP, Financial Cryptography, and comparable
  peer-reviewed venues.
- Prefer the publisher, DOI, proceedings, or official repository link. Use an
  arXiv version only when no published version is available, and label it.
- Never invent a DOI, venue, publication year, result, or citation. If a paper
  is available only as an abstract, mark the synthesis as abstract-only.
- A paper citation supports a research claim; it does not prove that its
  dataset is currently accessible or legally reusable.

### Existing proposals and differentiation

- Inspect the configured proposal corpus in read-only mode before making a
  duplication or novelty claim. Accept PDFs, Markdown, DOCX, and tabular
  inventories when the project declares how they are read.
- Extract metadata, problem, domain, data, method, target, and contribution
  angle. Do not copy titles, abstracts, grades, or distinctive wording.
- Build a differentiation matrix: prior proposal, overlap, unresolved gap,
  proposed differentiator, and evidence still required.
- Distinguish `unseen in the inspected corpus` from `novel in the literature`.
  The latter requires current literature verification and remains a bounded
  differentiation hypothesis until confirmed.
- Do not use the five TFM benchmark PDFs as a source of topic novelty. They are
  reviewer calibration artifacts and may only calibrate tone and score severity
  under the reviewer skill.

### Dataset and access

Every candidate must name a concrete data source and verify, where possible:

1. owner or official publisher;
2. canonical URL or official API endpoint;
3. public availability and actual download/API access;
4. license, terms of use, privacy restrictions, and academic reuse status;
5. documentation, schema, time coverage, sample scale, and relevant variables;
6. target or outcome definition and a reproducible target-engineering plan;
7. known missingness, bias, representativeness, and temporal limitations;
8. access reproducibility as of the review date.

Use these evidence states: `verified`, `partially_verified`, `unverified`, or
`rejected`. A paper that mentions a dataset is never sufficient evidence of
current access or legality.

Reject or hold a candidate when the data is private, inaccessible, legally
unclear, undocumented, too small for the proposed claim, or dependent on
unavailable infrastructure. A realistic access plan may be listed as a
contingency, but it cannot be presented as a validated public-data route.

## Research Design Gates

For each candidate, check all of the following before recommending it:

- The title names the object, problem, population or domain, and method or
  contribution without claiming more than the evidence supports.
- The problem identifies a concrete scientific or operational gap.
- The research question is measurable and answerable with the proposed data.
- The hypothesis predicts an observable relationship or comparative result.
- General and specific objectives are non-overlapping and testable.
- The baseline, proposed method, ablation or comparison, and validation split
  are defined before implementation.
- The target, unit of analysis, observation window, prediction horizon, and
  leakage exclusions are explicit.
- The scope is executable by one or two students in three to six months.
- The method has publication potential because it tests a gap, limitation,
  transfer, robustness question, causal assumption, or meaningful application;
  direct replication without differentiation is not enough.
- Compute, software, ethics approval, and data access are realistic.

Select models according to the task. Always include a simple, reproducible
baseline and explain why any advanced model is needed. Possible families include
classical ML, deep learning, survival/time-to-event, causal or uplift, NLP/LLM,
GNN, federated, anomaly detection, clustering, or forecasting. Do not select a
model merely because it is fashionable.

Select metrics by problem type. Examples:

- classification: balanced accuracy, precision/recall, F1, PR-AUC, ROC-AUC,
  calibration, and threshold utility as appropriate;
- regression: MAE, RMSE, MAPE or sMAPE when valid, R2, residual analysis, and
  interval coverage when uncertainty is claimed;
- survival: concordance index, time-dependent AUC, integrated Brier score,
  calibration, and censoring assumptions;
- causal/uplift: treatment balance, policy value, uplift/Qini, effect error, and
  sensitivity to confounding assumptions;
- NLP/LLM: task metrics plus human or expert evaluation, reliability, bias,
  and leakage checks;
- clustering/GNN/anomaly/forecasting: task-appropriate external or structural
  metrics, temporal validation, stability, and operational usefulness.

Do not force accuracy, F1, or ROC-AUC on regression, clustering, anomaly, or
survival work. Metrics must state the denominator, split strategy, prediction
horizon, and decision context.

## Required Output

Unless the user asks for another format, produce three to five ranked candidate
cards and a final recommendation. Write in the language of the TFM or request:
Spanish input produces Spanish output and English input produces English output.

### 1. Decision summary

State the recommended title, decision (`recommend`, `recommend_with_gates`, or
`reject`), the decisive evidence, and the blocking uncertainty.

### 2. Candidate card

Use this structure for every title:

```text
TFM RESEARCH OPPORTUNITY
Title:
Decision:
Differentiation status: verified / partially_verified / unverified

Context and impact:
State the scientific and economic or operational relevance.

State of the art and limitation:
Summarize what the supporting papers establish and the specific limitation or gap.

Research question:
Hypothesis:
General objective:
Specific objectives:

Dataset and legal access:
- Owner and official URL/API:
- License and academic reuse:
- Access check and date:
- Records, variables, time coverage, and target:
- Target engineering and foreseeable exclusions:
- Dataset evidence state:

Variable taxonomy and leakage controls:
- Inputs available at prediction time:
- Target and observation/prediction windows:
- Excluded post-outcome or proxy variables:
- Missingness, bias, privacy, and representativeness risks:

Method and evaluation:
- Baseline:
- Proposed method and justification:
- Comparators, ablations, or robustness checks:
- Split and validation design:
- Metrics and decision interpretation:

Roadmap and milestones:
Give a three-to-six-month sequence with concrete gates.

Risks and mitigations:
Difficulty: Medium / High / Very High
Team size: one student / two students
Scientific potential: TFM / paper / doctoral extension / industrial application

Supporting papers:
List at least five papers with year, venue, DOI or official link, and exact relevance.

Internal score (1-10):
- Originality:
- Feasibility:
- Dataset quality:
- Technical complexity:
- Scientific value:
- Industrial applicability:
- Publication potential:
- Methodological quality:
- Mean score:
```

### 3. Comparison and recommendation

Include a compact comparison table with title, dataset evidence, proposal-corpus
overlap, literature strength, feasibility, publication potential, mean score,
and decision. Explain trade-offs rather than choosing solely by score.

## Scoring and Failure Rules

Score each dimension from 1 to 10 and justify it with evidence. The mean is a
prioritization aid, not a substitute for the gates. Apply these labels:

- `Medium`: achievable with a well-scoped dataset and established methods;
- `High`: substantial integration, validation, or methodological risk;
- `Very High`: only acceptable with two students, exceptional supervision, or
  a reduced scope.

Hard failures:

- fewer than five usable supporting papers without an explicit user-approved
  exception;
- no legally credible, documented, public or reproducibly accessible dataset;
- title duplicates an inspected proposal without a meaningful differentiator;
- question, target, data, method, and metrics do not align;
- required infrastructure, compute, or permissions are not realistically
  available;
- a result, dataset, license, DOI, or novelty claim is fabricated or unverifiable.

When a hard failure is present, use `reject` or `recommend_with_gates` and state
the minimum evidence needed to reopen it. Never fill missing evidence with
assumptions.

## Reproducibility and Safety

- Use public research sources and official dataset pages when browsing is
  needed. Record access dates and URLs in the output.
- Keep local proposal and benchmark directories read-only. Do not copy or alter
  student work, grades, personal data, secrets, or downloaded artifacts.
- Do not download data merely to make a recommendation unless the user asked
  for it and the license/access rules permit it.
- Do not claim ethics approval, legal clearance, or institutional endorsement.
  Flag them as decisions for the student and supervisor.
- Separate verified evidence, interpretation, assumptions, and open questions.
- Existing skills remain authoritative for paper synthesis, research quality,
  dataset validation, objective alignment, and methodology review; link their
  outputs into this card rather than silently rewriting their rules.
