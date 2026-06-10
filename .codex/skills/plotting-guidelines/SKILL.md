---
id: plotting-guidelines
name: plotting-guidelines
domain: ml-eda
metadata:
  scope: [plotting, eda, visualization, ml, analytics]
  auto_invoke:
    - when creating or modifying any matplotlib/seaborn/plotly chart
    - when generating EDA reports or dashboard outputs
    - when writing plot helper functions
version: 1.1.0
depends_on: [coding-standards, naming-guidelines, dev-python]
---

# Plotting & Visualization Skill

Full specification for business-quality plots in EDA and pre-model decision phases.
Emphasis on **labels readiness**, **visual hierarchy**, **legend placement**, and charts that answer real business questions without extra narrative.

---

## 0. Agile Plot QA Loop

For business-facing analytical plots, use a short two-pass loop instead of one large rewrite.

### Pass 1 — Evidence contract

Before changing visuals, state or infer the plot contract:

- Population and filters.
- Denominator: calls, accounts, rows, events, or pairs.
- Minimum support threshold.
- Outcome window and direction.
- Whether the metric is a rate, count, lift, difference in percentage points, score, or normalized index.
- Whether the category comes from binary flags, primary slot, all slots, latest slot, sequence, or account-level aggregation.

If any of these are unclear and cannot be discovered from source code or data, ask before implementing.

### Pass 2 — Visual contract

Then make the plot readable:

- Maximum two subplots per output. Split dense figures instead of shrinking labels.
- Labels must show both nominal support (`n`) and rate/percentage when both are needed for interpretation.
- Use overall/base reference lines or annotations for every KPI compared against a baseline.
- Use stable semantic colors across related plots. Avoid mixing visually competing warning colors unless the classes truly mean different risk states.
- Long taxonomy labels must be wrapped or split into grouped plots.
- Render or inspect the generated plot before presenting it as evidence.

### Required plot artifact metadata

For repeatable reporting runs, each generated plot should be traceable to:

- Source plotting function or runner.
- Input file/table.
- Output path.
- Base filter and denominator.
- KPI columns and windows.
- Support threshold.
- Grouping/split dimensions.
- Any excluded categories.

This can be a manifest row, registry JSON, CSV index, or logged artifact record.

---

## 1. Title & Subtitle Standard

Every figure MUST have:

### Title
- Describes **what** the chart shows, the **metric or KPI**, and the **scope**.
- Must embed `N` (sample size), key KPI name, or feature being visualized when relevant.
- Pattern: `<Metric> by <Dimension> — N={n:,} | <Period or Scope>`

```python
ax.set_title(f"Monthly Churn Rate by Contract Type — N={len(df):,} | Last 12 Months", fontsize=14, fontweight="bold", pad=14)
```

### Subtitle (mandatory when title alone is insufficient)
- Placed immediately below title using `ax.text(...)` or `fig.suptitle` + `ax.set_title` combo.
- Must state: calculation method, feature engineering context, or key KPI formula if non-obvious.
- Pattern: `<calculation note> | <feature derivation note>`

```python
# Subtitle via text annotation below title
ax.annotate(
    "Churn = cancelled within 30 days | tenure_months = subscription age at observation date",
    xy=(0.5, 1.02), xycoords="axes fraction",
    ha="center", va="bottom", fontsize=9, color="#555555",
)
```

### When to embed N, KPIs, and feature calculations in titles
| Chart type | What to embed |
|---|---|
| Distribution / histogram | `N=<n>`, feature formula if derived |
| Correlation heatmap | `N=<n>`, normalization method |
| Time series | date range, rolling window size |
| Segment comparison | `N=<n>` per segment if sizes differ significantly |
| Feature importance | model name, top-K count |
| Confusion matrix / ROC | model name, threshold, dataset split |

---

## 2. Labels Readiness

All plots must pass the following label-readiness checks before commit.

### 2.1 Mandatory label elements
- X-axis label: explicit, includes units (`minutes`, `EUR`, `count`, `%`)
- Y-axis label: explicit, includes units
- Title: present (see §1)
- Subtitle: present when calculation context is needed (see §1)

### 2.2 Axis tick formatting
- Use human-readable scale formatters; never raw scientific notation.
- Dates: `mdates.DateFormatter("%b %Y")` or `"%Y-%m"` depending on granularity.
- Large numbers: use `FuncFormatter` — `1_000_000 → "1M"`, `1_000 → "1K"`.

```python
from matplotlib.ticker import FuncFormatter

def human_format(value, _):
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value/1_000:.0f}K"
    return f"{value:.0f}"

ax.yaxis.set_major_formatter(FuncFormatter(human_format))
```

### 2.3 No label overlap rules
- Rotate x-axis tick labels when > 6 categories: `ax.tick_params(axis="x", rotation=45)`.
- Use `ha="right"` with rotation for long category names.
- Y-axis labels must NEVER be cut off: always call `fig.tight_layout()` or set `left` margin explicitly.
- Avoid overlapping annotations: use `adjustText` library when annotating scatter points.

```python
fig.subplots_adjust(left=0.15)   # prevent y-axis label clipping
fig.tight_layout()
```

---

## 3. Legend Placement

### 3.1 Default position: top-center below subtitle
Place legend inside axes, horizontally centered, below the subtitle line.

```python
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 1.0),   # 1.0 = top of axes; adjust if subtitle present
    ncols=1,
    frameon=False,
    fontsize=9,
)
```

When a subtitle annotation is present, shift legend down to avoid overlap:
```python
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 0.97),  # slightly inside axes
    ncols=1,
    frameon=False,
    fontsize=9,
)
```

### 3.2 Long legends: multi-column layout
When legend has > 4 entries, switch to 2 or 3 columns placed **below the chart** (outside axes), centered.

```python
n_items = len(ax.get_legend_handles_labels()[0])
ncols = 3 if n_items > 6 else 2

ax.legend(
    loc="lower center",
    bbox_to_anchor=(0.5, -0.18),  # below axes, centered
    ncols=ncols,
    frameon=False,
    fontsize=9,
    columnspacing=1.2,
    handlelength=1.5,
)
fig.subplots_adjust(bottom=0.22)  # reserve space for legend below axes
```

### 3.3 No-overlap rules for legends
- Legend MUST NOT overlap the Y-axis label or ticks — always test with `fig.tight_layout()`.
- Legend MUST NOT overlap data in the primary data region.
- When in doubt, place outside: `bbox_to_anchor=(0.5, -0.18)` with `subplots_adjust(bottom=...)`.
- Never use `loc="best"` when the chart has dense data near edges — always specify explicit `loc`.

### 3.4 Legend title
- Add `legend.set_title(...)` only when the grouping variable name adds interpretive value.
- Keep legend title font smaller than body text: `prop={"size": 8}`.

---

## 4. Plot Types & Business Context

### Time series & trends
- Line charts, rolling averages, seasonal decomposition.
- Always show: clear date axis, trend vs noise, business thresholds.

### Distributions & summary statistics
- Histograms, boxplots, violin plots, ECDFs.
- Always annotate: mean, median, or quartile lines with text labels.

### Relationships & correlations
- Scatter plots, correlation heatmaps, pairwise plots (small N only).
- Color encoding with legend; regression line when relevant.

### Categorical comparisons
- Bar charts, stacked bars, normalized percent bars.
- Clear group ordering; show absolute vs relative scales explicitly.

---

## 5. Color Standards

- Use consistent, professional palettes — never default random `matplotlib` color cycle.
- Color-blind friendly: `seaborn` `colorblind` or `cividis` / `viridis`.
- Contrast ratio between classes > 60%.
- Never use decoration colors that distract from data signal.
- When plots compare outcomes, use stable outcome semantics across a deck/report:
  recall/contact pressure, escalation/complaint pressure, churn/exit validation, recovery/resolution.
- When plots compare signal families, use stable family semantics. Do not let a color encode different business meanings across adjacent plots.

## 5.1 Outcome And Window Semantics

Any plot using future-looking labels must state the direction.

- `leads_to_*`: the current row/event is followed by at least one future event within the window; it is temporal association, not causality.
- `current_call_is_*`: the current row is itself a recall/current-window event.
- `*_30d`, `*_7d`, `*_72h`, `*_24h`: state whether the denominator is calls, accounts, source events, or target events.
- For sequence plots, state whether the match is the first future target, any future target, same-call pair, prior-window pair, or account-level presence.

Do not present temporal association as causal impact unless the analysis design supports causal inference.

## 5.2 Processed Versus Missing Signal

When an extraction or AI-processing layer exists:

- Separate `processed but no signal` from `not processed`.
- Do not label `not processed` as `no signal`.
- Do not let coverage tokens appear as business reason/category labels.
- If an unprocessed bucket has high outcome rates, frame it as a coverage/data-quality audit queue, not as a validated taxonomy finding.

---

## 6. Helper Function Template

```python
from __future__ import annotations
from typing import Optional
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import pandas as pd


def _human_format(value: float, _: int) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.0f}K"
    return f"{value:.0f}"


def plot_time_series(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    ylabel: str,
    xlabel: str = "Date",
    subtitle: Optional[str] = None,
    rolling: Optional[int] = None,
    hue_col: Optional[str] = None,
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """Plot a time series with standard label readiness and legend placement.

    Args:
        df: Source DataFrame.
        x: Column name for the x-axis (date/time).
        y: Column name for the y-axis (metric).
        title: Chart title. Embed N and KPI where appropriate.
        ylabel: Y-axis label with units.
        xlabel: X-axis label. Defaults to "Date".
        subtitle: Optional subtitle for calculation context.
        rolling: Window size for rolling average overlay.
        hue_col: Optional column for color grouping.
        ax: Existing Axes to draw on; creates new figure if None.

    Returns:
        Configured Axes object.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 5))

    df_sorted = df.sort_values(x)

    if hue_col:
        groups = df_sorted[hue_col].unique()
        for group in groups:
            mask = df_sorted[hue_col] == group
            ax.plot(df_sorted.loc[mask, x], df_sorted.loc[mask, y], label=str(group), linewidth=2)
        n_items = len(groups)
        ncols = 3 if n_items > 6 else (2 if n_items > 4 else 1)
        ax.legend(
            loc="lower center",
            bbox_to_anchor=(0.5, -0.18),
            ncols=ncols,
            frameon=False,
            fontsize=9,
            columnspacing=1.2,
        )
        plt.subplots_adjust(bottom=0.22)
    else:
        ax.plot(df_sorted[x], df_sorted[y], label=y, linewidth=2)
        if rolling is not None:
            df_sorted[f"{y}_roll"] = df_sorted[y].rolling(rolling).mean()
            ax.plot(df_sorted[x], df_sorted[f"{y}_roll"], label=f"{rolling}-period avg", linestyle="--", linewidth=1.5)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0.97), frameon=False, fontsize=9)

    # Title & subtitle
    ax.set_title(title, fontsize=14, fontweight="bold", pad=16 if subtitle else 10)
    if subtitle:
        ax.annotate(
            subtitle,
            xy=(0.5, 1.01),
            xycoords="axes fraction",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#555555",
        )

    # Axis labels
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xlabel(xlabel, fontsize=11)

    # Formatters
    ax.yaxis.set_major_formatter(FuncFormatter(_human_format))
    if pd.api.types.is_datetime64_any_dtype(df_sorted[x]):
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    plt.tight_layout()
    return ax
```

---

## 7. PR Review Checklist

Before merging any chart code:

- [ ] Title present, embeds N and/or KPI when relevant
- [ ] Subtitle present when calculation context is non-obvious
- [ ] X and Y axis labels with units
- [ ] Axis tick labels readable — no overlap, human-readable scale
- [ ] Legend: top-center below subtitle OR bottom-center multi-column for > 4 items
- [ ] Legend does NOT overlap Y-axis labels or ticks
- [ ] Color palette is consistent and color-blind friendly
- [ ] `fig.tight_layout()` or explicit margin called
- [ ] Plot answers a named business or pre-model question

---

## 8. Forbidden Patterns

- `loc="best"` on dense charts
- Overlapping text labels or tick marks
- Y-axis label clipped by figure boundary
- Legend covering data in the primary data region
- Unlabeled axes
- Default matplotlib color cycle without explicit palette
- Titles that do not state what the chart shows

---

## 9. Changelog

```
v1.1.0 — Promoted to skill. Added §1 title/subtitle with N & KPI embedding,
         §2 labels readiness checklist, §3 legend placement rules (top-center,
         multi-column, no Y-axis overlap), §6 full helper template.
v1.0.0 — Initial rule-file version.
```
