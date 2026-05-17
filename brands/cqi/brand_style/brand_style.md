# Brand Markdown Guide

## Purpose

Use this brand system as a strict visual reference for any UI, landing page, dashboard, document, or component generated for this brand. Preserve the color hierarchy, typography, and contrast rules consistently.

Do not improvise alternative palettes unless explicitly requested. When in doubt, prioritize the core brand blue, dark neutral, and clean white system.

---

## Brand Identity Summary

This brand uses a modern, high-contrast, technology-oriented visual system built around:

* **Primary blue** for emphasis and action
* **Dark charcoal** for structure and premium contrast
* **White and near-white** for clarity and clean space
* **A small set of status/accent colors** for alerts, warnings, highlights, and positive states

The overall visual language should feel:

* clean
* professional
* modern
* analytical
* high trust
* product-oriented

Avoid playful or overly decorative styling.

---

## Typography

### Primary Heading Font

* **Arial**
* Use for headings, titles, section labels, CTA emphasis, and strong UI labels.

### Secondary / Body Font

* **Malgun Gothic**
* Use for paragraphs, supporting text, descriptions, captions, UI body text, and long-form readability.

### Typography Rules

* Headings must use **Arial**.
* Body text should default to **Malgun Gothic**.
* If a system does not support these fonts, use the nearest clean sans-serif fallback while preserving the distinction between heading and body styles.

Recommended fallback stack:

```css
font-family: Arial, Helvetica, sans-serif;
font-family: "Malgun Gothic", "Segoe UI", sans-serif;
```

---

## Core Color Palette

### Primary Text Colors

Use these in order of priority.

| Role                    | Color     | Usage                                                                 |
| ----------------------- | --------- | --------------------------------------------------------------------- |
| Main dark text          | `#343a40` | Primary readable text, labels, paragraphs, borders in neutral layouts |
| Pure white text         | `#ffffff` | Text on dark or blue backgrounds                                      |
| Deep dark surface/text  | `#232324` | Dark sections, footer backgrounds, strong contrast blocks             |
| Near white text/surface | `#fefefe` | Alternative white for subtle contrast in clean layouts                |
| Primary brand blue      | `#0044ff` | CTA, links, active states, key highlights                             |
| Secondary brand blue    | `#668fff` | Hover states, secondary accents, lighter informational emphasis       |
| Muted gray              | `#afafaf` | Disabled text, low-priority labels, subtle metadata                   |

---

## Background Colors

| Role                  | Color       | Usage                                                             |
| --------------------- | ----------- | ----------------------------------------------------------------- |
| Transparent           | `#ffffff00` | Transparent overlays, no-fill backgrounds                         |
| Dark background       | `#232324`   | Dark sections, hero/footer, contrast panels                       |
| White background      | `#ffffff`   | Main page backgrounds, cards, content sections                    |
| Brand blue background | `#0044ff`   | Primary CTA buttons, active containers, emphasis blocks           |
| Alert / danger        | `#ff563f`   | Error, destructive actions, critical warning highlights           |
| Warning orange        | `#ffa620`   | Warnings, caution states, intermediate alerts                     |
| Highlight yellow      | `#ffd21d`   | Attention markers, badges, featured emphasis                      |
| Positive green        | `#6bc95d`   | Success states, approved actions, positive KPIs                   |
| Teal accent           | `#36a782`   | Informational-positive accents, alternative success/support state |

---

## Semantic Usage Rules

### 1. Neutral System

Use these for most layouts:

* `#ffffff` → primary background
* `#232324` → dark sections and structural contrast
* `#343a40` → default text and neutral borders
* `#afafaf` → secondary text only

### 2. Primary Brand Action

Use these for interaction and emphasis:

* `#0044ff` → primary button, primary link, active tab, selected state, key chart accent
* `#668fff` → secondary button state, hover state, lighter emphasis, helper highlight

### 3. Status Colors

Use sparingly and only when semantically justified:

* `#ff563f` → destructive, error, urgent alert
* `#ffa620` → warning
* `#ffd21d` → attention / highlight
* `#6bc95d` → success / positive completion
* `#36a782` → supportive positive or informational success

Do not use status colors decoratively.

---

## Contrast and Accessibility Rules

* White text (`#ffffff` or `#fefefe`) should be used on `#232324` or `#0044ff` backgrounds.
* Dark text (`#343a40` or `#232324`) should be used on white or very light backgrounds.
* Avoid placing `#668fff` text on white for small typography unless size and weight are increased.
* Avoid low-contrast gray-on-white combinations for core content.
* Use muted gray (`#afafaf`) only for secondary metadata, never for essential content.

---

## Buttons

### Primary Button

* Background: `#0044ff`
* Text: `#ffffff`
* Font: Arial for prominent CTA label or Malgun Gothic if integrated into UI system
* Border: none or subtle `#304cff`
* Hover: `#668fff` or slightly darker blue if available within system constraints

### Secondary Button

* Background: `#ffffff`
* Text: `#343a40`
* Border: use a blue or neutral outline depending on context
* Hover: subtle gray or light blue emphasis

### Destructive Button

* Background: `#ff563f`
* Text: `#ffffff`

---

## Cards and Panels

### Standard Card

* Background: `#ffffff`
* Text: `#343a40`
* Border: subtle neutral or blue-tinted outline
* Shadow: `rgba(0, 0, 0, 0.1) 0px 10px 15px 0px`

### Dark Card

* Background: `#232324`
* Text: `#ffffff`
* Use for contrast sections, premium blocks, or hero highlights

### Highlight Card

Use only when needed:

* Blue emphasis: `#0044ff`
* Warning emphasis: `#ffa620`
* Success emphasis: `#6bc95d`
* Highlight emphasis: `#ffd21d`

---

## Box Shadow

Use this as the standard elevated surface shadow:

```css
box-shadow: rgba(0, 0, 0, 0.1) 0px 10px 15px 0px;
```

Guidance:

* Use on cards, floating panels, modals, dropdowns, or featured containers.
* Do not stack multiple shadows unless explicitly requested.
* Maintain a clean, product-style depth system.

---

## Outline / Border System

The system uses a fairly rich outline palette. Apply these with discipline.

### Neutral / Structural Outlines

| Color     | Usage                                              |
| --------- | -------------------------------------------------- |
| `#343a40` | Main neutral outline, dark border, strong division |
| `#000000` | Strong hard edge when needed, use sparingly        |
| `#999999` | Soft neutral border for inputs or dividers         |

### Blue Outline System

| Color     | Usage                                                 |
| --------- | ----------------------------------------------------- |
| `#2b7fcc` | Secondary blue outline                                |
| `#a5d8ff` | Soft blue border, light containers, subtle emphasis   |
| `#339af0` | Informational border, active but lighter than primary |
| `#304cff` | Strong brand-aligned border or active control         |
| `#1e6fb8` | Mid-blue emphasis border                              |
| `#0d4f8f` | Dark blue structural border                           |
| `#155fa3` | Deep interface accent border                          |

### Warm Status Outlines

| Color     | Usage                             |
| --------- | --------------------------------- |
| `#cb9800` | Highlight/warning border          |
| `#ef8400` | Warning or orange emphasis border |
| `#ff3f25` | Error/critical border             |

### Border Usage Rules

* Prefer neutral borders for layout structure.
* Prefer blue borders for active, interactive, or selected elements.
* Prefer warm borders only for warnings, alerts, and exceptional states.
* Do not mix too many outline colors in the same component group.

---

## Background Image / Graphic Assets

These assets appear in the current visual system and may be reused when appropriate:

### White Chevron Asset

```text
url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8' fill='none'%3E%3Cpath d='M1 1L6 6L11 1' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")
```

Use for:

* select dropdown indicators
* white icon overlays on dark or blue surfaces

### Main Banner Image

```text
url("https://cqisense.com/images/main-banner.png")
```

Use for:

* hero/banner contexts
* only when a branded marketing section is needed

### Solution Image

```text
url("https://cqisense.com/images/img-solution.png?v=1.1")
```

Use for:

* solution overview sections
* explanatory or product-related visual panels

Do not overuse background images in dense analytical layouts.

---

## Layout Guidance

### Preferred Visual Style

* clean spacing
* generous whitespace
* high readability
* strong CTA hierarchy
* restrained use of accents
* dark/light contrast blocks
* polished SaaS / enterprise product feel

### Avoid

* random gradients not defined in the system
* pastel overload
* neon colors outside the approved palette
* decorative color use without semantic meaning
* too many accent colors in the same viewport

---

## Recommended Color Hierarchy by Importance

1. `#0044ff` → brand action and emphasis
2. `#232324` → structural depth and dark contrast
3. `#ffffff` / `#fefefe` → clarity and space
4. `#343a40` → primary readable text
5. `#668fff` → secondary blue accent
6. status colors only when semantically required

---

## Ready-to-Use AI Styling Instructions

Use the following instructions when asking another AI to generate design, code, or formatted content.

### General Prompt Block

```markdown
Follow this brand system strictly:

- Use Arial for headings.
- Use Malgun Gothic for body text.
- Primary brand color: #0044ff.
- Main dark neutral: #232324.
- Default text color: #343a40.
- Primary background: #ffffff.
- White text on dark or blue surfaces: #ffffff or #fefefe.
- Secondary accent blue: #668fff.
- Muted gray only for secondary text: #afafaf.
- Success: #6bc95d.
- Info-success accent: #36a782.
- Warning: #ffa620.
- Highlight: #ffd21d.
- Error/destructive: #ff563f.
- Standard elevated shadow: rgba(0, 0, 0, 0.1) 0px 10px 15px 0px.

Design style must feel modern, clean, professional, high-trust, and product-oriented.
Avoid introducing colors outside this palette unless explicitly requested.
```

---

## CSS Token Version

```css
:root {
  --font-heading: Arial, Helvetica, sans-serif;
  --font-body: "Malgun Gothic", "Segoe UI", sans-serif;

  --color-text-primary: #343a40;
  --color-text-white: #ffffff;
  --color-text-dark: #232324;
  --color-text-soft-white: #fefefe;
  --color-primary: #0044ff;
  --color-primary-light: #668fff;
  --color-text-muted: #afafaf;

  --bg-transparent: #ffffff00;
  --bg-dark: #232324;
  --bg-white: #ffffff;
  --bg-primary: #0044ff;
  --bg-danger: #ff563f;
  --bg-warning: #ffa620;
  --bg-highlight: #ffd21d;
  --bg-success: #6bc95d;
  --bg-success-alt: #36a782;

  --outline-neutral: #343a40;
  --outline-blue-soft: #a5d8ff;
  --outline-blue: #2b7fcc;
  --outline-blue-mid: #339af0;
  --outline-brand: #304cff;
  --outline-dark: #000000;
  --outline-gray: #999999;
  --outline-warning: #cb9800;
  --outline-warning-strong: #ef8400;
  --outline-error: #ff3f25;
  --outline-blue-deep: #1e6fb8;
  --outline-blue-darker: #0d4f8f;
  --outline-blue-alt: #155fa3;

  --shadow-elevated: rgba(0, 0, 0, 0.1) 0px 10px 15px 0px;
}
```

---

## Final Enforcement Rule for AI Systems

When generating any output for this brand:

* do not replace the core blue with another blue
* do not replace Arial headings with decorative fonts
* do not replace Malgun Gothic body text with serif fonts
* do not use colors outside this palette unless explicitly instructed
* do not invent gradient systems beyond the provided assets
* preserve a clean enterprise-tech visual tone
* prefer clarity and consistency over novelty

If there is a conflict between creativity and brand consistency, choose brand consistency.
