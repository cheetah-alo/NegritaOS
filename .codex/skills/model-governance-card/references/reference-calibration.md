# Reference Calibration

Read-only source:

`/Users/jackyb-cqi/Library/CloudStorage/OneDrive-Personal/CQI Documents/Projects/00_TeamDataScientist/documents/CDS-Model Results and Governance on Production - Hotmobile hourly-040926-135128.pdf`

SHA-256:

`89f75bb394782ef3e4567d19c35376cfa27278764d4bbcfa4d7e5fca53f73151`

The seven-page PDF is calibration for a compact model follow-up record. It
organizes model summary, lineage, data quality, EDA, target/label policy,
design, training, experimentation, evaluation, explainability, operational
evaluation, monitoring, and governance.

Retain:

- compact section hierarchy;
- tables for stable facts, metrics, owners, statuses, and monitoring;
- explicit parent/derived model relationship;
- lineage and artifact references;
- train/test comparison;
- explainability and governance as first-class sections.

Do not copy as truth:

- `[add value]`, blank metrics, or incomplete sentences;
- a readiness summary when a quality check is `Unknown`;
- production status inherited from a parent model;
- unexplained population differences such as 11.7M versus 1.2M rows;
- monitoring limits without baseline, owner, response action, and evidence;
- status icons without evidence references;
- train/test exclusion asymmetry without leakage review;
- overlapping temporal windows without entity/time split validation;
- SHAP importance as causal explanation;
- generic owners where accountability is unresolved.

The reference is not a factual source for any other model and must not be
quoted or copied beyond structural calibration.
