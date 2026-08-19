# Executive Deck Outline — [Presentation Title]

**Audience:** [C-Suite / VP / Senior Management / Mixed]
**Decision required:** [State the single decision this deck must enable]
**Narrative pattern:** [SCR / Evidence-Insight-Recommendation / Options-Tradeoffs-Decision]
**Total length:** [10-80 slides, including appendix]
**Evidence refresh mode:** [reuse_only / targeted_refresh / full_refresh]
**Selected analysis run:** [run ID or manifest path]
**Reused artifacts:** [CSV / Parquet / JSON / plots / manifests / hashes]

---

## Slide Structure

### Slide 1: Title
- **Title:** [Presentation title]
- **Subtitle:** [Context — date, project, organization]
- **Speaker note:** [Opening hook — why this matters now]

---

### Slide 2: Agenda
- **Sections:** [List the narrative sections in presentation order]
- **Speaker note:** [Set expectations for the decision path]

---

### Slide 3: Executive Summary (TL;DR)
- **Message:** [The single most important thing the audience must take away]
- **Supporting points:** [2-3 bullets — findings or options]
- **Call to action:** [What we are asking the audience to decide or do]
- **Speaker note:** [Anticipate first objection and address it here]

---

### Slide 4: [Context / Situation]
- **Message:** [Why we are here — the situation statement]
- **Evidence:** [1 data point or fact that frames the context]
- **Speaker note:** [Connect to audience's prior knowledge or current pain point]

---

### Slide 5: [Problem / Complication]
- **Message:** [What has changed, failed, or is at risk]
- **Evidence:** [Chart or metric that demonstrates the problem]
- **Chart takeaway label:** [The headline of the chart — state the finding, not the chart type]
- **Speaker note:** [Quantify the impact if possible]

---

### Slide 6-N-2: [Core Findings / Analysis]
*(Repeat this block for each key finding. One slide = one message.)*

- **Message:** [The finding this slide communicates]
- **Evidence:** [Chart / table / example]
- **Chart takeaway label:** [Headline that states the finding]
- **Speaker note:** [Supporting context, limitations, or notes]

---

### Slide N-1: Recommendations and Next Actions
- **Message:** [What we recommend and why]
- **Recommendations:**
  - [Action 1] — [Owner] — [Timeline]
  - [Action 2] — [Owner] — [Timeline]
- **Risk of inaction:** [Optional — 1 sentence]
- **Speaker note:** [Address expected pushback on the recommendation]

---

### Slide N: Appendix Separator
*(Insert before appendix slides)*
- **Message:** "Additional Detail"
- **Speaker note:** [Indicate which appendix slides address which anticipated questions]

---

## Appendix Slides (as needed)

| Slide | Content | Triggers |
|-------|---------|---------|
| A1 | Methodology detail | "How was this computed?" |
| A2 | Raw data tables | "Can I see the numbers?" |
| A3 | Alternative scenarios | "What if...?" |
| A4 | Glossary | Jargon questions |

---

## Quality Checklist

- [ ] Deck contains 10-80 slides in total, including appendix
- [ ] Agenda appears immediately after the cover and matches the deck order
- [ ] Each slide has exactly one message sentence
- [ ] Every chart has a headline that states the finding (not the chart type)
- [ ] No methodology in main deck — appendix only
- [ ] Recommendation slide references findings by slide number
- [ ] Appendix is separated from main deck
- [ ] Audience type matches language level and detail depth
- [ ] Existing run artifacts were inventoried before any query was considered
- [ ] Deck-only corrections used `reuse_only` and executed no data queries
- [ ] `targeted_refresh` lists each refreshed metric and direct dependency
- [ ] `full_refresh` includes explicit authorization and bounded query preflight
- [ ] Reused artifacts and executed queries are recorded separately
