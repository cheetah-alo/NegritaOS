---
id: plotting-guidelines
domain: ml-eda
enforcement: advisory
depends_on:
  - coding-standards
  - naming-guidelines
  - ml-python
provides:
  - plot-standards
  - business-focused-visuals
  - premodel-evaluation-plots
description: >
  Standards for creating business-relevant and analytic plots during EDA and pre-model decision phases.
  Emphasis on clarity, interpretability, visual hierarchy, and visual design that looks professional and
  human-crafted (not “AI-ish”). Ensures labels, scales, and visual cues answer core business questions.
version: 1.0.0
applyTo: [plotting, eda, visualization]
priority: warning
---

# Plotting & Visualization Guidelines



# Visualization Rules — EDA & Pre-Model Decisions

## Purpose

Visualizations are not decorative; they must answer **business questions** and support **pre-model decisions** such as:

- identifying trends
- detecting anomalies or drift
- understanding distributions and outliers
- confirming correlations and relationships relevant to business KPIs
- assessing temporal behavior
- informing feature transformations

Plots should be clearly interpretable by a data scientist, analyst, or stakeholder without extra narrative.

---

## 1. Plot Types and When to Use Them

### a) Time Series & Trends
Plots that show evolution over time are critical when dealing with temporal data (e.g., churn rates, usage metrics, revenue).

👉 Use:
- line charts
- rolling averages
- seasonal decomposition

**What to show**
- clear date axis
- trend vs noise
- business-relevant thresholds

---

### b) Distributions & Summary Statistics
Understanding spread, skewness, and outliers informs transformations.

👉 Use:
- histograms
- boxplots
- violin plots
- ECDFs

**What to show**
- clear labels
- statistical annotations (mean, median, quartiles)

---

### c) Relationships & Correlations
These help determine feature relevance.

👉 Use:
- scatter plots
- heatmaps of correlation
- pairwise plots (small set)

**What to show**
- color encodings with legend
- regression line or trend indicator
- annotations for meaningful clusters

---

### d) Categorical Comparisons
Essential for segment analysis (e.g., churn by plan type).

👉 Use:
- bar charts
- stacked bars
- normalized percent bars

**What to show**
- clear group ordering
- relative versus absolute values

---

## 2. Labels, Legends, and Axis Design (Mandatory)

All plots must include:

### a) Axis Labels
- X-axis and Y-axis labels must be **explicit and descriptive**
- Include units where applicable
```

Date (YYYY-MM-DD)
Average Revenue per User (EUR)

````

### b) Title and Subtitle
Every figure must have:
- a **title** summarizing what the plot shows
- a **subtitle** (optional) that adds context such as “30-day rolling average of churn rate”

### c) Legends
- Legends must be placed where they do not obscure data
- Label categories and colors clearly
- Avoid abbreviations unless domain standard

---

## 3. Scales and Tick Formatting

- Use **human‐readable scales** (e.g., 1K, 100K, 1M as appropriate)
- Avoid scientific notation unless data magnitude requires it
- Date axes must be formatted by business relevance (e.g., weekly, monthly)
- Use fixed limits when comparing subplots

---

## 4. Color Choices & Accessibility

- Use a **consistent, professional palette** (avoid default random colors)
- Color choices should:
- respect contrast
- be color-blind friendly
- align with brand or domain expectations if present
- Never use decoration colors that distract from data

Good palettes:
- Matplotlib `viridis`, `cividis`
- Seaborn `colorblind`, `deep`
- Custom theme with > 60% contrast between classes

---

## 5. Answer Business Questions

Each plot **must be tied to at least one of the following objectives**:

| Plot Objective | Example Business Question |
|---------------|----------------------------|
| Trend identification | Are churn rates increasing month-over-month? |
| Anomaly detection | Are there dates with abnormal user activity? |
| Distribution understanding | Is revenue skewed by a small group of users? |
| Temporal segmentation | Does seasonality affect usage patterns? |
| Feature behavior | Do high-value customers have different retention behavior? |

Plots that don’t answer a clear question must be **justified or removed**.

---

## 6. Subplots & Layouts

When showing multiple facets:

- Arrange subplots logically (rows first, then columns)
- Align shared axes when comparing similar measures
- Provide a single legend if possible to reduce clutter
- Maintain consistent scales where comparison requires

---

## 7. Annotations & Highlights

- Annotate meaningful thresholds (e.g., churn benchmark)
- Use arrows or text to highlight key observations
- Avoid excessive annotations:
- no overlapping text
- no rainbow typography

---

## 8. Code Patterns (Best Practice)

Standardized patterns help readability and consistency.

### a) Wrapper function for plotting

```python
def plot_time_series(
  df: pd.DataFrame,
  x: str,
  y: str,
  title: str,
  ylabel: str,
  xlabel: str = "",
  *,
  rolling: Optional[int] = None,
  ax: Optional[plt.Axes] = None,
):
  ax = ax or plt.gca()
  df_sorted = df.sort_values(x)
  ax.plot(df_sorted[x], df_sorted[y], label=y, linewidth=2)
  if rolling is not None:
      df_sorted[f"{y}_roll"] = df_sorted[y].rolling(rolling).mean()
      ax.plot(df_sorted[x], df_sorted[f"{y}_roll"], label=f"{y} (rolling)", linestyle="--")
  ax.set_title(title)
  ax.set_ylabel(ylabel)
  ax.set_xlabel(xlabel)
  ax.legend(loc="best")
  return ax
````

### b) Consistent labeling pattern

```python
ax.set_title("Daily Active Users Over Time")
ax.set_ylabel("Active Users (count)")
ax.set_xlabel("Date (YYYY-MM-DD)")
```

---

## 9. Plot Review Checklist (for PRs)

Before merging any plot:

✔ Titles are present and explicit
✔ Labels include units if relevant
✔ Legends are readable and correctly placed
✔ Color palette is consistent and accessible
✔ Axes scales are appropriate and readable
✔ Plot answers a business or pre-model question
✔ No visual clutter (gridlines, tick density, overlapping labels)

---

## 10. Integration with EDA Workflows

Plots should be generated as part of:

* **Exploratory Notebooks**
  with narrative markdown emphasizing *why the plot matters*

* **Automated EDA Reports**
  with plots embedded alongside business questions and statistical summaries

* **Pre-Model Validation**
  where plots serve as checks for:

  * leakage
  * distribution shifts
  * feature behavioral differences across target segments

---

## 11. Forbidden Patterns

Never produce:

* plots with overlapping text
* default color cycles without intention
* hidden tick labels
* unlabeled axes
* plots with no business context

---

## 12. Example — Good Plot Title Pattern

```
Daily Active Users (DAU) — 30-Day Rolling Average — Last 180 Days
```

This provides:

* what
* how
* period

---

## Changelog

```
v1.0.0 — Initial plot guideline focusing on business questions, readability, and professional visualization standards.
```

---

## Summary

This rule makes sure that plots:

🔹 answer questions that matter for business and modeling
🔹 have clear titles, labels, and legends
🔹 use thoughtful scales and palettes
🔹 avoid looking generic or “AI-generated”
🔹 help humans make decisions confidently
