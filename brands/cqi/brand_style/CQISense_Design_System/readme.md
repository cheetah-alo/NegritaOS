# CQISense Design System

**CQISense** is the data-science product of CQI — a team that turns call-center transcripts into explainable, auditable customer-journey intelligence. The flagship POC is the **Hot Orange Journey Rules** engine, which scores every customer journey on two pressure axes (Repair / Risk) and assigns a final archetype (A–F, D2) used for churn-prioritization and operational routing.

> Source materials: `uploads/hot-orange-archetypes-mechanisms-v5_share.pptx` and `uploads/workflow explained jun24.pptx`. Raw text extractions at `research/hot-orange-text.md` and `research/workflow-text.md`. No external GitHub repo or Figma link was provided.

---

## Product context

| Product | What it does |
|---|---|
| **Hot Orange Journey Rules** | Tags call transcripts with PR/FR signals → fires 9 strict rules → builds Repair & Risk scores → derives Operational score (0–100) → assigns mechanism & archetype |
| **Shadow3 v0.6** | The SQL scoring pipeline that runs the model in production |
| **CDS Rule Detail Pages** | Business-readable rule specification (the upstream source) |

**Users:** Data scientists + business validators who review scoring logic, calibrate rules, and present findings to ops leadership.

---

## Content fundamentals

- **Language:** English (some slide footnotes in Spanish — bilingual team).
- **Tone:** Precise, grounded, calm. No hype. Every claim has a source or a sample size.
- **Casing:** Sentence case everywhere. No ALL-CAPS for content (only for eyebrows / monospaced overlines).
- **Numbers:** Always tabular mono (`font-family: var(--font-mono)`). Write 144,966 not 144966. Percentages to one decimal.
- **Qualifiers matter:** "validation-pending", "evidence-only", "not a churn probability" — always include these guardrails.
- **Brevity:** One idea per slide. One sentence per bullet. The boss has attention deficit — front-load the conclusion.
- **Emoji:** Never used.

---

## Visual foundations

### Colors
Cool gray surfaces dominate. CQI cobalt (`#1A43F5`) is the primary brand. Pink (`#FF8093`) is the secondary accent. "Hot Orange" is a semantic priority flag only — never a surface.

- **Surfaces:** `--surface-page` (gray-50), `--surface-card` (white), `--surface-sunken` (gray-100), `--surface-inverse` (blue-900 navy).
- **Text:** `--text-strong` (gray-800), `--text-body` (gray-800), `--text-muted` (gray-600).
- **Brand:** `--brand` (blue-500 / cobalt `#1A43F5`), used for interactive elements, dark headers, and the primary CTA.
- **Accent:** `--accent` (pink-300 / `#FF8093`) — section markers, highlights, secondary actions.
- **Score families:** `--repair` (teal-400) = Repair Pressure; `--risk` (pink-400) = Risk Pressure; `--operational` (green-600) = the 0-100 synthesis.
- **Archetype palette:** A (green) → B (khaki) → C (ochre) → D (pink/clay) → D2 (deep) → E (teal) → F (gray).
- **Categorical data:** 8-color cobalt-anchored palette (`--cat-1` … `--cat-8`) for charts.

### Typography
- **Display / headings:** Poppins (geometric sans) — headings, titles, slide headers. Loaded via Google Fonts CDN.
- **Body:** Noto Sans (universal sans) — UI, paragraphs, labels.
- **Mono / data:** IBM Plex Mono — all metrics, formulas, codes, tabular figures. Always use `font-variant-numeric: tabular-nums`.
- Heading weights: 600. Body: 400. Labels/overlines: 600 + `letter-spacing: 0.08em` + `text-transform: uppercase`.

### Layout & spacing
4 px base grid. `--space-*` tokens. Balanced density — generous padding on cards (20–28px), breathing room between sections. App sidebar width `--sidebar-w: 248px`.

### Cards
Default: flat hairline (`--shadow-sm: none`, `border: 1px solid var(--border-hair)`). Focal cards: `raised` (adds `--shadow-sm`). Dialogs: `floating`. Optional left accent rail (3px, score family color).

### Shadows
Cool navy-tinted (`rgb(0 20 80 / a)`) — never warm gray. Subtle: xs → lg.

### Borders
Hairline by default. `--border-hair` (10% ink), `--border-soft` (16%), `--border-strong` (30%).

### Motion
Calm, no bounce. `--ease-out`, durations 120–320ms. No infinite decorative loops.

### Hover / press
Buttons: `translateY(-1px)` on hover. Color one shade darker (`--brand-hover`). 200ms. No shrink.

### Backgrounds
Flat cool-gray surfaces. No gradients, no textures. Occasional full-bleed navy (`--blue-900`) panels for section breaks / title slides.

### Corner radii
`--radius-xs` (4px) → `--radius-2xl` (28px). Default card: `--radius-md` (10px). Controls: `--radius-sm` (6px). Tags/chips: `--radius-full` (999px).

### Imagery / charts
The source decks embed matplotlib heatmap tables in navy/slate. The design system provides a calm earthy chart data palette (`--cat-1`–`--cat-8`). Charts should use these colors. The heatmap blue-navy is intentionally NOT in the design system — it belongs to the old Office theme.

---

## Iconography

No icon set was found in the source materials — the decks are text-only tables and matplotlib charts. **No icon font or SVG sprite is bundled.**

For consuming projects: use [Lucide Icons](https://lucide.dev) from CDN (`<script src="https://unpkg.com/lucide@latest"></script>`) — thin stroke, neutral geometric, aligns with Noto Sans's clean weight. Use 20×20 or 24×24 at 1.5px stroke. Do not use filled icons.

Unicode math characters are used in formulas (`÷`, `×`, `≥`, `→`) — this is intentional and canonical.

---

## Brand assets

| File | Description |
|---|---|
| `assets/cqi-logo.png` | Official CQI wordmark — extracted from brand PPT |
| `assets/cqisense-logo.svg` | AI-generated lockup (fallback only) |
| `assets/cqisense-mark.svg` | AI-generated mark (fallback only) |

The ensō (incomplete circle) was designed to reflect: continuous improvement (CQI), the "open loop" of an ongoing customer journey.

> **Logo:** `assets/cqi-logo.png` is the official CQI wordmark extracted from the brand PPT. Use this for all presentations, docs and UI.

---

## Files & index

```
styles.css                     ← consumer entry point (import this only)
tokens/
  fonts.css                    ← Google Fonts import + @font-face declarations
  colors.css                   ← base + semantic color tokens (152 tokens)
  typography.css               ← font families, scale, weights, spacing
  spacing.css                  ← 4px grid, container widths, control heights
  elevation.css                ← shadows, radii, borders, motion tokens
  domain.css                   ← CQISense model semantics (Repair/Risk, archetypes)
  base.css                     ← base element styles, scrollbars, utilities
components/
  core/
    Button.jsx + .d.ts + .prompt.md
    Badge.jsx + .d.ts + .prompt.md
    Card.jsx + .d.ts + .prompt.md      ← includes CardHeader
    Stat.jsx + .d.ts + .prompt.md
    core.card.html                     ← @dsCard "Components"
  domain/
    ArchetypeBadge.jsx + .d.ts + .prompt.md
    MechanismTag.jsx + .d.ts + .prompt.md
    PointsPill.jsx + .d.ts + .prompt.md   ← includes ChannelSplit
    ScoreMeter.jsx + .d.ts + .prompt.md
    RuleCard.jsx + .d.ts + .prompt.md
    domain.card.html                   ← @dsCard "Components"
guidelines/
  color-sand.html / color-ink.html / color-green.html   ← @dsCard "Colors"
  color-scores.html / color-archetypes.html              ← @dsCard "Colors"
  color-status.html / color-data.html                    ← @dsCard "Colors"
  type-display.html / type-body.html / type-mono.html    ← @dsCard "Type"
  type-scale.html                                        ← @dsCard "Type"
  spacing.html / radius-elevation.html                   ← @dsCard "Spacing"
  brand-wordmark.html / brand-reading-rule.html          ← @dsCard "Brand"
slides/
  TitleSlide.html / BigNumberSlide.html / ArchetypeMapSlide.html  ← @dsCard "Slides"
templates/
  hot-orange-deck/
    HotOrangeDeck.dc.html              ← ← ← THE DECK (10 slides, presentable now)
    deck-stage.js
    ds-base.js
assets/
  cqisense-mark.svg
  cqisense-logo.svg
research/
  hot-orange-text.md / workflow-text.md   ← raw slide-text extraction
  img/                                    ← extracted slide images (source reference)
```

---

## The domain model at a glance

```
EVIDENCE (PR/FR signals, call reason)
  ↓
RULES R1–R9  ×  support gate (n≥100, share≥1%, channel n≥30)
  ↓
BASE SCORES: Repair (÷206×100)  +  Risk (÷97×100)
  +  Journey overlays (strain / relief)
  ↓
OPERATIONAL SCORE = (0.55·Repair + 0.35·Risk + overlays) / 145 × 100  [0–100]
  ↓
MECHANISM (why)   →   ARCHETYPE (which state)
  ↓
ROOT CAUSE  +  RECOMMENDATION
```

**Reading rule:** Brand/UI = cobalt (`--brand`) · Repair = teal (`--repair`) · Risk = pink (`--risk`) · Operational = green (`--operational`) · Heat/Orange = priority flag only.

**Not a churn probability.** Operational Score is a prioritization index. Churn30 and DiscReq are validation-only.
