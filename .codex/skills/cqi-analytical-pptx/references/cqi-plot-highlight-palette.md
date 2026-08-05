# CQI Plot and Highlight Palette

## Purpose

Define how CQI analytical decks use color in charts, tables, KPI cards,
callouts, and visual highlights. Color is not decoration: every non-neutral
color must have an explicit analytical role.

## Color Roles

Every visible non-neutral color must serve one of these roles:

| Role | Use |
|---|---|
| `status_color` | Governance, readiness, approval, risk, or blocked state. |
| `category_color` | Stable category, source, family, segment, or layer across slides. |
| `emphasis_color` | The current slide's key analytical finding or selected focus. |
| `magnitude_color` | Numeric intensity, concentration, rank, or heatmap value. |
| `comparison_color` | Baseline vs candidate, before vs after, observed vs expected. |
| `alert_color` | Exception, outlier, anomaly, or decision point. |

If none applies, use neutral styling.

## Base Palette

| Token | Hex | Use |
|---|---:|---|
| `navy` | `#001450` | Cover, section dividers, decision bands, table headers. |
| `cobalt` | `#2347FF` | Primary analytical emphasis, left rail, selected bars. |
| `bright_blue` | `#1A43F5` | Alternate blue emphasis and chart accents. |
| `white` | `#FFFFFF` | Main slide canvas. |
| `off_white` | `#F4F6FB` | Card background, table alternate rows, subtle panels. |
| `ink` | `#111827` | Primary text. |
| `muted` | `#5E687A` | Secondary text, subtitles, metadata. |
| `grid` | `#D7DCE3` | Borders, dividers, chart grid lines. |
| `slate` | `#8791A4` | Residual, unknown, disabled, or no-observable values. |

## Analytical Accent Palette

| Token | Hex | Primary use |
|---|---:|---|
| `teal` | `#3CAD8C` | Confirmed coverage, valid association, usable signal. |
| `deep_teal` | `#327C7E` | Strong teal emphasis or secondary confirmed series. |
| `violet` | `#7B61FF` | Candidate, alternate segment, secondary analytical layer. |
| `gold` | `#C99A2E` | Ranking, benchmark, middle tier, review emphasis. |
| `amber` | `#F2A93B` | Pending decision, review gate, warning without failure. |
| `rose` | `#A9364F` | Severe risk, blocked condition, critical exception. |
| `coral` | `#F27A8A` | HOLD, fail, negative exception, high-risk highlight. |
| `cyan` | `#36BFEF` | Low-severity candidate, exploratory or support signal. |

## Status Mapping

| State | Color guidance |
|---|---|
| `OBSERVED` | cobalt or teal |
| `CONFIRMED` | teal |
| `CANDIDATE` | violet |
| `REVIEW` | amber or gold |
| `HOLD` / `FAIL` | rose or coral |
| `UNKNOWN` / `N/D` | slate |
| `NOT_OBSERVABLE` | slate |
| `NOT_MATERIALIZED` | muted gray |

Do not use coral/red only because a value is large. Use coral/red when the value
represents risk, failure, blocker, severity, or negative exception.

## Bar Chart Rules

- Default single-series bars use muted blue or slate-blue.
- The finding bar or selected Top-N uses cobalt.
- Secondary comparison series uses violet or teal.
- Review or pending-decision bars use amber.
- Risk, blocked, or severe exception bars use coral or rose.
- `Other`, `Unknown`, residual, or no-observable values use slate.
- Prefer direct labels at bar ends over legends when space allows.
- If category colors are used, keep the mapping stable across all slides in the
  deck.

## Heatmap Rules

- Sequential magnitude heatmaps use one hue from light to dark.
- Diverging palettes are only allowed when a meaningful zero, target, or
  benchmark exists.
- Missing, null, suppressed, or not-observable cells use gray.
- Focus cells should use border/stroke first, not only fill.
- Governance states should appear as badges or annotations, not mixed into the
  numeric heatmap scale.

## KPI Card Rules

- Primary KPI: cobalt.
- Confirmed or valid KPI: teal.
- Review or pending KPI: amber/gold.
- Hold, fail, severe, or risk KPI: coral/rose.
- Residual, unknown, or no-observable KPI: slate.
- Supporting context KPI: neutral/off-white.

## Table Rules

- Header: navy background with white text.
- Alternating rows: off-white and white.
- Metric, code, and ID columns: IBM Plex Mono.
- Critical cells may use fill, left stripe, or badge, but readability must stay
  above the CQI minimum font thresholds.
- Do not color every table cell unless the table is explicitly a heatmap.
