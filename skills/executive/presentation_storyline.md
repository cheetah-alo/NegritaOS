# Skill: Presentation Storyline

**Type:** Domain — Executive
**Applicable agents:** presentation_agent

## Purpose
Constructs the narrative arc for a slide deck before any content is written.
A presentation without a defined storyline produces slides that inform but do not persuade or decide.

## Storyline Architecture

### Step 1: Define the Audience and Decision
Before any slide is outlined, answer:
- Who is in the room? (technical / non-technical / mixed)
- What is the single decision they need to make, or action they need to take?
- What is their prior belief or assumption about this topic?

### Step 2: Select the Narrative Pattern

**Pattern A — Situation-Complication-Resolution (SCR)**
Use when: audience is unaware of the problem or its severity.
```
Situation: [What is the current state?]
Complication: [What changed, went wrong, or is at risk?]
Resolution: [What should be done?]
```

**Pattern B — Evidence-Insight-Recommendation**
Use when: audience is technical and skeptical; needs to see the reasoning.
```
Data: [What do we observe?]
Insight: [What does this mean?]
Recommendation: [What action follows?]
```

**Pattern C — Options-Tradeoffs-Decision**
Use when: presenting a choice between alternatives.
```
Context: [Why are we choosing?]
Option A / B / C: [Brief description + trade-offs]
Recommendation: [Preferred option with rationale]
```

### Step 3: Build the Slide Skeleton

For each slide position:
```
Slide N:
  Message: [The one sentence this slide must communicate]
  Evidence: [The data point, chart, or example that proves it]
  Transition: [How this slide connects to the next]
```

### Step 4: Validate the Arc

Before writing slide content:
- Read the message sentence from each slide in sequence
- The sequence must tell a coherent story
- Any slide whose message could be removed without breaking the narrative — remove it

## Deck Structure Template

```
Slide 1: Title + Agenda (optional)
Slide 2: TL;DR / Executive Summary (always)
Slide 3–N-2: Main story (SCR / Evidence / Options)
Slide N-1: Recommendation and next actions
Slide N: Appendix separator (if appendix follows)
Appendix Slides: Methodology, raw data, additional analysis
```

## Rules
- Appendix is never part of the main story
- Every chart slide has a headline that states the takeaway, not the chart type
  - Bad headline: "Feature Importance Chart"
  - Good headline: "Tenure and Contract Type Drive 68% of Churn Risk"
