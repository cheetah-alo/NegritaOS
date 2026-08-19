# Technical Deck Outline — [Presentation Title]

**Audience:** Technical team  
**Decision or discussion required:** [Question to resolve]  
**Total length:** [10-80 slides, including appendix]
**Evidence refresh mode:** [reuse_only / targeted_refresh / full_refresh]
**Selected analysis run:** [run ID or manifest path]
**Reused artifacts:** [CSV / Parquet / JSON / plots / manifests / hashes]

## Slide Structure
1. Title and scope
2. Agenda
3. TL;DR
4. Data and assumptions
5. Methodology
6. Core findings
7. Validation and notes
8. Recommendations
9. Appendix

## Rules
- Keep the complete deck between 10 and 80 slides, including the appendix.
- Do not impose per-section slide caps.
- Inventory reusable run-scoped evidence before considering queries.
- Use `reuse_only` for titles, agenda, notes, layout, readability,
  interpretation, plot emphasis, or styling corrections.
- Use `targeted_refresh` only for named missing or stale evidence.
- Use `full_refresh` only with explicit authorization and bounded query
  preflight.
- Keep methodology in the main deck only when the audience is technical.
- Every chart must state the finding in the headline.
- Every recommendation must cite a prior finding.
