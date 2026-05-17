# Skill: TFM Evaluation

**Type:** Domain — Academic
**Applicable agents:** tfm_evaluator_agent, proposal_validator_agent

## Purpose
Provides the protocol for evaluating a Trabajo Fin de Máster (master's thesis).
Covers proposal stage, milestone reviews, and final defense evaluation.
Ensures objective, structured, evidence-based academic feedback.

## Evaluation Dimensions

### 1. Title — Problem — Objective Alignment
The title must reflect the problem. The problem must drive the objectives.
The objectives must be measurable and achievable within the thesis scope.

**Pass criteria:**
- Title contains: domain + problem type + scope indicator
- Problem statement is specific and contextualized
- Each objective maps to a deliverable or measurable outcome
- No circular definitions: objective ≠ method name

**Failure patterns:**
- "Apply machine learning to predict X" — method as objective
- "Study the relationship between X and Y" — vague, not measurable
- Title that describes the dataset, not the problem

### 2. Methodology Appropriateness
The method must match the research question, the data type, and the available resources.

**Pass criteria:**
- Method is justified: why this method for this problem?
- Alternatives were considered and dismissed with rationale
- Validation strategy is appropriate (time-based split if temporal data)
- Evaluation metrics match the problem type (classification, regression, clustering)

### 3. Dataset Feasibility
The dataset must be accessible, sufficient, and appropriate for the stated problem.

**Pass criteria:**
- Dataset is named and its origin is stated
- Access is confirmed or a realistic acquisition plan exists
- Size is sufficient for the methodology (especially for deep learning)
- Temporal coverage is appropriate for the prediction window

### 4. Results and Conclusions Alignment
Conclusions must be bounded by what the results actually show.

**Pass criteria:**
- Each conclusion maps to a specific result or metric
- Limitations of the results are acknowledged
- No overclaiming: "the model works" requires a production-context benchmark

### 5. Academic Rigor
- Citations are relevant and correctly formatted
- Related work section positions the thesis in the existing literature
- Reproducibility: code, data access, or methodology description sufficient to replicate

## Scoring Guide (per dimension)

| Score | Label | Description |
|---|---|---|
| 4 | Excellent | Exceeds expectations. No revisions needed. |
| 3 | Satisfactory | Meets requirements with minor clarifications. |
| 2 | Needs Revision | Structural issues. Specific revisions required before approval. |
| 1 | Insufficient | Fundamental defect. Major rework required. |

## Feedback Format

For each dimension:
```
[DIMENSION NAME]: [Score 1–4] — [One-sentence verdict]
Evidence: [specific text or section from the thesis that supports the score]
Required action: [specific, actionable improvement if score < 4]
```
