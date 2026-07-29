# TFM Benchmark Registry

## Purpose

The benchmark files calibrate the severity, tone, and relative interpretation
of the `tfm-academic-reviewer` skill. They are reference evidence only. They
are never the document under evaluation and their grades are not ground truth.

## Source Resolution

Resolve the benchmark root in this order:

1. Read `projects/ds_onedrive_workspace.yaml`.
2. Prefer `project.local_paths.tfm_models`; otherwise resolve
   `project.local_paths.tools` and append `TFM_Modelos`.
3. In the current local workspace the resolved path is:
   `/Users/jackyb-cqi/Library/CloudStorage/OneDrive-Personal/ds/Tools/TFM_Modelos`.
4. Treat all files as read-only local evidence. Do not copy, move, rename, or
   rewrite OneDrive artifacts.

## Registered References

The current benchmark set is:

| Calibration band | Logical ID | File hint |
|---|---|---|
| Excellent | `tfm_olivares_group4` | `TFM_Olivares_Grupo4.pdf` |
| Excellent | `tfm_viu_javier_presmanes` | `TFM___VIU___Javier_Presmanes_Cardama.pdf` |
| Excellent | `tfm_final_delange` | `TFM_FINAL-DELANGEMUNOZ_DAVID.pdf` |
| Lower quality | `tfm_sergi_puigmal` | `2604226259 - Sergi Puigmal Miranda - *.pdf` |
| Lower quality | `tfm_javier_cobas` | `2516363723 - Javier Cobas Silvestre - *.pdf` |

The local directory also contains `rubric_v1_light.md` v1.1 (October 2025).
The requested `rubric_v1_2025_full.md` was not present when this registry was
created. The evaluator must report that limitation rather than inventing a
missing source.

## Calibration Protocol

- Read the uploaded thesis first and keep its evidence separate.
- Use benchmark documents to calibrate relative language such as excellent,
  satisfactory, needs revision, or insufficient.
- Do not copy text, arguments, citations, grades, or conclusions from a model.
- Do not calculate `Benchmark Avg.` from labels alone. Use `N/D` when numeric
  benchmark records are unavailable.
- If a benchmark file is missing or unreadable, report the missing evidence and
  continue without silently substituting another thesis.
