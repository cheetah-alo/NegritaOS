---
name: pptx
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill."
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md) |
| Create from scratch | Read [pptxgenjs.md](pptxgenjs.md) |

---

## CQI Design System for Presentations

**Always load and apply this system before building any slide.** Every design decision — colors,
layout, hierarchy, image handling — must follow these rules unless the user explicitly overrides them.

Brand feel: **clean · analytical · high-trust · modern enterprise**.  
Avoid decorative, playful, or overly creative styling. When in doubt: more whitespace, less color.

---

### 1. Sandwich Structure (non-negotiable)

The deck uses a strict **light-dark sandwich**:

| Slide type | Background | Text |
|---|---|---|
| Cover slide | Dark `#232324` | White `#FFFFFF` |
| Section dividers | Dark `#232324` | White `#FFFFFF` |
| All content slides | Light `#FFFFFF` | Dark `#343A40` |
| Closing / end card | Dark `#232324` | White `#FFFFFF` |

**Never use a dark background on a content slide.**  
**Never use a light background on a cover or section divider.**

---

### 2. CQI Color Palette — Presentation Roles

```
PRIMARY BLUE       #0044FF   Lead accent: section labels, key stat, primary borders
DARK BG            #232324   Cover / divider backgrounds, dark panels
DARK TEXT          #343A40   All body text on light slides
WHITE              #FFFFFF   Text on dark slides, content slide background
SECONDARY BLUE     #668FFF   Second stat accent, hover/support, chart series 2
MUTED GRAY         #AFAFAF   Captions, footer text, secondary labels, metadata
TEAL               #36A782   Positive/informational accent, success highlights
SUCCESS GREEN      #6BC95D   Positive KPIs, upward signals
WARNING ORANGE     #FFA620   Caution, moderate signals, third stat accent
HIGHLIGHT YELLOW   #FFD21D   Attention badges, featured numbers (dark bg ONLY)
DANGER RED         #FF563F   Critical / error states, negative signals
```

**Color discipline rules:**
- `#0044FF` is always the lead accent. Use first in every multi-accent context.
- Assign each stat in a stat row its own accent: `#0044FF` → `#668FFF` → `#36A782` → `#FFA620`
- `#FFD21D` (yellow) is **only on dark backgrounds** — contrast is insufficient on white.
- Status colors (`#FF563F`, `#FFA620`, `#6BC95D`) must be semantically justified. Never decorative.
- Never introduce colors outside this palette unless explicitly requested.

#### Extended DS Technical Deck — Multi-Accent Stat Sequence

For DS analysis decks with 4–5 stats in a row, the reference deck's vivid accent pattern (teal / orange / blue / pink) maps directly to CQI brand anchors. **Use these in order, top to bottom of priority:**

| Position | CQI Accent | Hex | Visual role in reference deck |
|---|---|---|---|
| Stat 1 | Primary Blue | `#0044FF` | Lead metric — main model result |
| Stat 2 | Teal | `#36A782` | Informational-positive — coverage, overlap |
| Stat 3 | Warning Orange | `#FFA620` | Caution or magnitude — event rate, gap |
| Stat 4 | Secondary Blue | `#668FFF` | Supporting metric — secondary benchmark |
| Stat 5 | Success Green | `#6BC95D` | Positive signal — improvement, precision |

**When a 5th or 6th accent is needed in a single slide**, the reference deck's exact vivid colors `#4FC3F7` (cyan) and `#FF6B9D` (pink) are approved for use in DS technical presentations as an extended accent-only palette — they must not replace or override the CQI brand anchors above, and must not appear in brand-facing or external-stakeholder materials.

```python
# Extended DS accent sequence (python-pptx)
BLUE    = RGBColor(0x00, 0x44, 0xFF)  # stat 1
TEAL    = RGBColor(0x36, 0xA7, 0x82)  # stat 2
ORANGE  = RGBColor(0xFF, 0xA6, 0x20)  # stat 3
BLUE2   = RGBColor(0x66, 0x8F, 0xFF)  # stat 4
GREEN   = RGBColor(0x6B, 0xC9, 0x5D)  # stat 5
# Extended-only (DS decks, internal):
CYAN    = RGBColor(0x4F, 0xC3, 0xF7)  # 6th accent if needed
PINK    = RGBColor(0xFF, 0x6B, 0x9D)  # 6th/7th accent if needed
```

---

### 3. Typography

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Slide title | Arial | 28–36pt | Bold | `#232324` light / `#FFFFFF` dark |
| Section label (above title) | Arial | 8–9pt | Bold | `#0044FF` light / `#668FFF` dark · ALL CAPS · letter-spaced |
| Subtitle / framing line | Malgun Gothic | 13–15pt | Regular | `#343A40` light / `#AFAFAF` dark |
| Body / bullet text | Malgun Gothic | 11–13pt | Regular | `#343A40` |
| Big stat number | Arial | 48–72pt | Bold | Accent color per stat |
| Stat label (below number) | Malgun Gothic | 9–10pt | Regular | `#AFAFAF` |
| Card title | Arial | 10–11pt | Bold | Same color as card border |
| Card body | Malgun Gothic | 9–10pt | Regular | `#343A40` |
| Footer | Malgun Gothic | 8pt | Regular | `#AFAFAF` |

---

### 4. Slide Anatomy — Content Slide (white bg)

```
┌──────────────────────────────────────────────────────────────────┐
│ ████████████████ thin blue stripe, 4–6px, #0044FF, full width ██ │ ← top
├──────────────────────────────────────────────────────────────────┤
│  SECTION LABEL    (8–9pt, Arial Bold, #0044FF, uppercase)        │ y ≈ 0.18"
│  Slide Title      (28–36pt, Arial Bold, #232324)                 │ y ≈ 0.30"
│  Subtitle line    (13–15pt, Malgun Gothic, #343A40)              │ y ≈ 0.72"
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CONTENT ZONE   (plots, stats, cards, text blocks)             │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Project name · context detail       (8pt, #AFAFAF, left)       │ ← bottom
└──────────────────────────────────────────────────────────────────┘
```

**Thin top stripe:** full-width rectangle, height `0.06"`, color `#0044FF`. The ONLY chrome element on content slides. No bottom bar.

**Section label:** uppercase text tag directly above the title — not a bar, not a box. Just text.

**Footer:** always present, always same format: `"Project name · sub-context detail"`.

---

### 5. Slide Anatomy — Section Divider (dark bg)

```
┌──────────────────────────────────────────────────────────────────┐
│ ████████████████ thin teal stripe, 4–6px, #36A782, full width ██ │ ← top
│                                                                  │
│                                                                  │
│                 SECTION 3 — EBM MODEL                            │ label, centered, 9pt, #36A782
│                                                                  │
│         Big Section Title (40–48pt, Arial Bold, white)           │ centered
│         ─────────────────────────────────────────                │ thin line, #36A782, ~5" centered
│         Supporting subtitle  (14pt, Malgun Gothic, #AFAFAF)      │ centered
│                                                                  │
│                                                                  │
│  Project name · context                  (8pt, #AFAFAF, left)   │ ← bottom
└──────────────────────────────────────────────────────────────────┘
```

**Accent line under the divider title is required** — it is a section separator, not a decorative
element. Width ~50% of slide, centered, color `#36A782`, height 1pt.

**Do NOT use accent lines under titles on content slides.** The rule applies only to dividers.

---

### 6. Big Stat Callouts

For 2–6 key numbers in a horizontal row. These are the highest-value elements in a slide.

**Rules:**
- Number: Arial, 48–72pt, bold, distinct accent color per stat
- Label: Malgun Gothic, 9–10pt, regular, `#AFAFAF`, directly below number
- **No background box or shape** — numbers sit directly on the slide background
- Each stat gets its own color from the accent sequence: `#0044FF` → `#668FFF` → `#36A782` → `#FFA620` → `#FF563F`
- Minimum 1.5" horizontal gap between stats
- Maximum 5 stats per row

```javascript
// pptxgenjs — stat row helper
const stats = [
  { val: "0.81",   label: "XGBoost AUC",       color: "0044FF" },
  { val: "21.9×",  label: "top 1% uplift",      color: "668FFF" },
  { val: "21.9%",  label: "recall in top 1%",   color: "36A782" },
  { val: "686",    label: "positives in 3.2M",  color: "FFA620" },
];
const colW = 10 / stats.length;
stats.forEach((s, i) => {
  const x = i * colW + 0.3;
  slide.addText(s.val,   { x, y: 3.0, w: colW - 0.3, h: 0.9, fontSize: 56, bold: true,
                            color: s.color, fontFace: "Arial" });
  slide.addText(s.label, { x, y: 3.95, w: colW - 0.3, h: 0.4, fontSize: 9,
                            color: "AFAFAF", fontFace: "Malgun Gothic" });
});
```

---

### 7. Cards — Bordered, No Fill

Use for categorization, option comparison, or multi-concept grids.

**Rules:**
- Background: `#FFFFFF` — same as slide. No gray fill.
- Border: 1.5–2pt, colored — each card gets its own CQI accent color
- Card title: Arial, 10–11pt, bold, same color as border
- Card body: Malgun Gothic, 9–10pt, regular, `#343A40`
- Minimum card size: 2.5" wide × 1.2" tall

```javascript
// pptxgenjs — bordered card helper
const cards = [
  { label: "user reboot",       body: "human troubleshooting\nsubjective quality perception", color: "FFA620" },
  { label: "non-user reboot",   body: "scheduled / ACS / firmware\nnetwork-driven processes",  color: "0044FF" },
  { label: "unexpected reboot", body: "watchdog / crash-like\noperational instability",         color: "36A782" },
];
const cW = 2.8, cH = 1.6, gap = 0.3, x0 = 0.5, y0 = 1.5;
cards.forEach((c, i) => {
  const x = x0 + i * (cW + gap);
  slide.addShape(pres.shapes.RECTANGLE, { x, y: y0, w: cW, h: cH,
    fill: { color: "FFFFFF" }, line: { color: c.color, width: 1.5 } });
  slide.addText(c.label, { x: x + 0.15, y: y0 + 0.12, w: cW - 0.3, h: 0.35,
    fontSize: 11, bold: true, color: c.color, fontFace: "Arial" });
  slide.addText(c.body,  { x: x + 0.15, y: y0 + 0.52, w: cW - 0.3, h: 0.9,
    fontSize: 9, color: "343A40", fontFace: "Malgun Gothic" });
});
```

---

### 8. Insight / Takeaway Box

One per slide maximum. Placed at the bottom of the content zone as the operative conclusion.

**Rules:**
- Border: `#0044FF`, 1.5pt
- Background: `#FFFFFF` (border creates emphasis, no fill needed)
- Text: Arial, 10–11pt, bold, `#232324`
- Width: 80–95% of slide, centered or left-aligned with content margin

```javascript
// pptxgenjs — insight box
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 4.6, w: 9.2, h: 0.65,
  fill: { color: "FFFFFF" }, line: { color: "0044FF", width: 1.5 }
});
slide.addText("For rare events, the key question is not only AUC: can we concentrate events in the top-risk tail?", {
  x: 0.55, y: 4.62, w: 9.0, h: 0.62, fontSize: 10, bold: true, color: "232324",
  fontFace: "Arial", valign: "middle"
});
```

---

### 9. Plot / Image Integration — CRITICAL RULES

When the user provides plots from their analysis runs, these rules are mandatory.

**Rule 1 — Preserve the plot exactly as provided.**
Never alter, re-style, or recreate a plot. Insert it with `addImage` / `add_picture` at original quality.
Never resize to non-proportional dimensions.

**Rule 2 — Measure before placing.**
```bash
python3 -c "from PIL import Image; img = Image.open('plot.png'); print(img.size)"
```
Compute display width/height preserving aspect ratio. If max height is 3.5" and original is 1400×700px:
```
display_w = 3.5 * (1400 / 700) = 7.0"
```

**Rule 3 — Annotation cards must match what the image shows.**
- Use the same colors as the lines/bars in the plot when adding legend or stat cards next to it
- Position the annotation spatially near the relevant part (e.g., stats go beside the plot, not below text)
- Label exact values visible in the plot — not generic descriptions
- If the plot shows "XGBoost AUC = 0.81" in its legend, the stat callout must say `0.81`, not `~0.8`

**Rule 4 — Every plot must have at minimum ONE of:**
- A caption below it (Malgun Gothic italic, `#AFAFAF`, 8–9pt)
- A stat callout derived from what the plot shows
- An insight box interpreting the main finding

**Rule 5 — Image does the quantitative work. Text frames the interpretation.**
Do NOT describe what is already visible (e.g., "the blue line goes up"). Write what it means:
why it matters, what action it implies, what the DS conclusion is.

**Rule 6 — Standard layout patterns for plot slides:**

*Single plot + annotations (left/right split):*
```
┌──────────────────────────┬─────────────────────┐
│                          │  [big stat]          │
│     [plot image]         │  [big stat]          │
│     55–60% of width      │  [bullet interpret]  │
│                          │  [insight box]       │
└──────────────────────────┴─────────────────────┘
```

*Two plots side by side:*
```
┌──────────────────┬──────────────────┐
│  [plot 1]        │  [plot 2]        │
│  equal split     │  equal split     │
├──────────────────┴──────────────────┤
│  [shared insight box, full width]   │
└─────────────────────────────────────┘
```

*Plot + stats below (when plot is wide):*
```
┌────────────────────────────────────────────────────────────────┐
│  [wide plot, full width or 90%]                                │
├────────────────────────────────────────────────────────────────┤
│  [stat 1]   [stat 2]   [stat 3]   [interpretation text]       │
└────────────────────────────────────────────────────────────────┘
```

---

### 10. Layout Patterns by Content Type

**Stats-only slide:**
3-layer header → 4–5 big stat callouts in one row → insight box at bottom.

**Plot + interpretation slide:**
3-layer header → left 55–60% plot → right 40–45% stacked: stat + bullets + insight box.

**Two plots side by side:**
3-layer header → equal-split plots → shared insight box full width.

**3-card comparison:**
3-layer header → 3 bordered cards in a row → optional arrow element → insight box.

**Numbered next steps:**
3-layer header → 5–6 rows: large bold number left (`#0044FF`, 20pt) + title bold + description body. No boxes.

**Text + data side-by-side:**
3-layer header → left column: bold-led body text → right column: big stat + bordered detail card.

---

### 11. What to Avoid

| ❌ Avoid | ✅ Instead |
|---|---|
| Dark background on content slides | White `#FFFFFF` always |
| Light background on cover / dividers | Dark `#232324` always |
| Gray fill on cards | White fill + colored border |
| Accent line under content slide title | Use whitespace; accent lines only on section dividers |
| Yellow `#FFD21D` on white background | Yellow only on dark bg slides |
| Plot without any caption or annotation | Always add caption, stat, or insight box |
| Annotation text that re-describes the plot | Write interpretation, not description |
| Stats in gray/colored background boxes | Stats float directly on slide background |
| Repeating the same layout on consecutive slides | Vary between stat row, plot, card, text patterns |
| Centered body text | Left-align paragraphs; center only divider/cover titles |
| More than 4 accent colors in one content slide | Use the 4-color accent sequence strictly |
| Bottom chrome bar on content slides | Footer text only (8pt, `#AFAFAF`) |
| Fonts outside Arial / Malgun Gothic | Stick to the two-font system |
| Colors outside the CQI palette | Ask the user if a new color is needed |

---

### 12. Tool Selection for DS Decks

| Situation | Tool |
|---|---|
| New deck from scratch | `pptxgenjs` (see pptxgenjs.md) |
| Editing an existing `.pptx` | python-pptx (see editing.md) |
| 50+ slides with many analysis plots | python-pptx — faster iteration, easier image insertion |
| Template with slide masters | pptxgenjs `defineSlideMaster` |

**For DS analysis decks with many plots from runs: use python-pptx.**
Build helper functions for each slide type (`chrome_stripe`, `section_label`, `footer`, `stat_row`, `insight_box`, `add_plot`) and reuse them consistently across all slides.

Python-pptx color helper:
```python
from pptx.dml.color import RGBColor

BLUE    = RGBColor(0x00, 0x44, 0xFF)
DARK    = RGBColor(0x23, 0x23, 0x24)
TEXT    = RGBColor(0x34, 0x3A, 0x40)
BLUE2   = RGBColor(0x66, 0x8F, 0xFF)
GRAY    = RGBColor(0xAF, 0xAF, 0xAF)
TEAL    = RGBColor(0x36, 0xA7, 0x82)
GREEN   = RGBColor(0x6B, 0xC9, 0x5D)
ORANGE  = RGBColor(0xFF, 0xA6, 0x20)
RED     = RGBColor(0xFF, 0x56, 0x3F)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
LBG     = RGBColor(0xFF, 0xFF, 0xFF)   # content slide background
```

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

## Creating from Scratch

**Read [pptxgenjs.md](pptxgenjs.md) for full details.**

Use when no template or reference presentation is available.

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

```bash
python -m markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert|this.*(page|slide).*layout"
```

### Visual QA

**⚠️ USE SUBAGENTS** — even for 2–3 slides. You've been staring at the code. Subagents have fresh eyes.

Convert slides to images, then use this prompt:

```
Visually inspect these slides. Assume there are issues — find them.

CQI design system rules to check:
- Content slides must have white background. Flag any dark-bg content slides.
- Cover and section dividers must have dark (#232324) background. Flag any light-bg dividers.
- Every content slide must have a thin blue (#0044FF) stripe at the top. Missing = bug.
- Every slide must have a footer in bottom-left. Missing = bug.
- Cards must have white fill + colored border. Gray fill cards = bug.
- Big stat numbers must float directly on background — no boxes behind them.
- Every plot image must have a caption, stat callout, or insight box. Orphan image = bug.
- Accent lines under content slide titles = bug. Accent lines under divider titles = correct.
- Yellow (#FFD21D) text on white background = invisible. Flag it.

General layout issues:
- Overlapping elements (text through shapes, stacked elements)
- Text overflow or cut off at edges
- Images stretched from original aspect ratio
- Annotation text that just re-describes the plot axes (not an interpretation)
- More than 4 accent colors on a single content slide
- Columns or similar elements not aligned consistently
- Empty bottom half of slides (unused space = missed opportunity)

For each slide, list issues or areas of concern, even if minor.
Report ALL issues found.
```

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Converting to Images

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

Pass the absolute paths printed above directly to the view tool.
`pdftoppm` zero-pads based on page count: `slide-1.jpg` (<10 pages), `slide-01.jpg` (10–99), `slide-001.jpg` (100+).

After fixes, rerun all four commands — the PDF must be regenerated from the edited `.pptx` before changes are visible.

---

## Dependencies

- `pip install "markitdown[pptx]"` — text extraction
- `pip install Pillow` — thumbnail grids, image dimension check
- `npm install -g pptxgenjs` — creating from scratch
- LibreOffice (`soffice`) — PDF conversion (auto-configured via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) — PDF to images
