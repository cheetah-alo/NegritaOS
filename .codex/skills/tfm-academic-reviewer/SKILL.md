---
name: tfm-academic-reviewer
description: >
  Standardized final reviewer for Master's Thesis PDFs in Artificial
  Intelligence. Trigger: TFM review, thesis evaluation, tribunal report,
  academic scoring, benchmark calibration, or publication-readiness review.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Reviewing a Master's Thesis or TFM PDF"
    - "Preparing an academic tribunal report"
    - "Scoring a thesis against the operational academic rubric"
    - "Calibrating a TFM review against local benchmark PDFs"
---

# TFM Academic Reviewer

Read `skills/academic/tfm_academic_reviewer.md` before performing the review.
It is the canonical NegritaOS procedure and references the operational rubric
and read-only benchmark registry.

## Activation Contract

- Analyze the uploaded thesis first.
- Match the thesis language: Spanish input produces Spanish output; English
  input produces English output unless the user explicitly overrides it.
- Score the four required criteria on a 0–4 scale and provide a final grade on
  a 1–10 scale using the rubric formula.
- Use the five benchmark PDFs only for calibration of tone and severity.
- Do not copy benchmark content or treat benchmark labels as truth.
- Report missing evidence instead of filling gaps with assumptions.
- Treat AI-text findings as linguistic indicators, never proof of authorship.
- Do not modify, copy, rename, or move PDFs or other OneDrive artifacts.

## Required Final Sections

The response must include the scoring table, section feedback, five page-aware
issues, AI-text indicators, five state-of-the-art comparisons, five reflective
questions with grounded model answers, five technical mastery questions with
grounded model answers, a task-appropriate metrics table, recommendations, and
the mandatory `Final Academic Review` block.
