---
name: sbp-brandbook
description: Apply the Schuberg Philis visual brand identity when building any UI, HTML component, slide, document, or design asset for SBP. Use whenever output will represent SBP visually — colors, typography, logo, stylization, grids, photography, iconography. Ensures brand-consistent output without manual reminders.
metadata:
  domain: brand
  lifecycle: build
  source: https://brandbook.schubergphilis.com/8d157b10c/p/142798-our-brand-book
  license: proprietary
---

> **License notice:** This skill and all assets under `assets/` are the
> proprietary intellectual property of Schuberg Philis and are **not**
> covered by the Apache 2.0 license that applies to the rest of this
> repository. See `skills/sbp-brandbook/LICENSE` for terms. Do not
> redistribute or use outside of work for Schuberg Philis.

# SBP Brand — Full Spec

Apply these guidelines when building any UI, HTML component, slide, document, or design asset for Schuberg Philis.

For the full human-readable brand reference, see [brandbook.schubergphilis.com](https://brandbook.schubergphilis.com/8d157b10c/p/142798-our-brand-book).

---

## Colors

**Primary palette:**

| Color | Hex | CSS variable |
|---|---|---|
| SBP Blue (primary) | `#1E80ED` | `--sbp-blue` |
| Soft Blue | `#E8F2FD` | `--soft-blue` |
| Tropical Turquoise | `#1EE8ED` | `--tropical-turquoise` |
| Midnight Dark | `#020C17` | `--midnight-dark` |
| Space Gray | `#082646` | `--space-gray` |
| Joyful Yellow | `#FFDB4E` | `--joyful-yellow` |
| White | `#FFFFFF` | `--white` |

**Secondary palette:** Orange `#FF7000`, Green `#2AC0A1`, Violet `#6D5FF7`, Magenta `#FF0089`

**Signal colors only (not for general design):** True Green (positive), False Red (negative) — hex values from SBP marketing team.

**CSS custom properties:**
```css
:root {
  --sbp-blue: #1E80ED;
  --soft-blue: #E8F2FD;
  --tropical-turquoise: #1EE8ED;
  --midnight-dark: #020C17;
  --space-gray: #082646;
  --joyful-yellow: #FFDB4E;
  --white: #FFFFFF;
  --orange: #FF7000;
  --green: #2AC0A1;
  --violet: #6D5FF7;
  --magenta: #FF0089;
}
```

**Usage:** Lead with SBP Blue. Secondary colors support; never dominate. Tertiary signal colors for data/infographics only.

---

## Typography

**Font:** TT Interphases (commercial). TT Interphases Mono for labels/captions only.

**CRITICAL — fallback stack:**
```css
font-family: 'TT Interphases', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
/* Mono: */
font-family: 'TT Interphases Mono', 'Courier New', Courier, monospace;
```

**Do NOT** use Inter, Roboto, or any visually similar free font as a substitute.

**Size scale:**

| Element | Weight | Size | Letter spacing | Line height |
|---|---|---|---|---|
| H1 | Extra Bold 800 | `3rem` | `-0.04em` | `1.09` |
| H2 | Extra Bold 800 | `2.25rem` | `-0.04em` | `1.09` |
| H3 | Bold 700 | `1.75rem` | `-0.04em` | `1.09` |
| H4 | Bold 700 | `1.375rem` | `-0.04em` | `1.09` |
| Body | Regular 400 | `1rem` | `0` | `1.5` |
| Quote | Regular 400 | `1.125rem` | `0` | `1.25` |
| Caption | Mono Regular | `0.75rem` | `0` | `1.375` |
| Label/chapeau | Mono Regular | `0.6875rem` | `0` | `1.375` |

**Rules:** Always sentence case (never ALL CAPS). Mono is a "pinch of tech" — use sparingly. Never Regular/Light for headings.

---

## Stylization

**Concept:** Square (tech) + circle (human) = rounded corners on every shape.

**Corner radius:**
- Landscape canvas: 10% of canvas width
- Portrait canvas: 20% of canvas width
- Element within layout: 10% of element's own width

**Labels:** Pill with 1 straight corner. One line of text. This is the signature SBP shape.
**Buttons/tags:** Fully rounded pill. One line of text.

**SVG graphic assets** (bundled in `assets/` — copy to project asset dir):

| Category | Filenames | Usage |
|---|---|---|
| Slashes | `Slash_ble.svg` *(as-is on disk)*, `Slash_dark.svg`, `Slash_light.svg` | Brand dividers, decorative elements on matching backgrounds |
| Slashes (double) | `Slash_double-blue.svg`, `Slash_double-dark.svg` | Stronger emphasis dividers |
| Slashes (outline) | `Slash_outline_blue.svg`, `Slash_outline_dark.svg`, `Slash_outline_light.svg` | Lightweight decorative use |
| Squares | `Square_blue.svg`, `Square_dark.svg`, `Square_light.svg`, `Square_pink.svg`, `Square_yellow.svg` | Containers, backgrounds, section highlights |
| Corners | `Corner_Blue.svg`, `Corner_dark.svg` | Decorative corner accents |
| Buttons | `Button_Blue.svg`, `Button_dark.svg`, `Button_light.svg`, `Button_pink.svg`, `Button_yellow.svg` | Pre-styled button shapes |

Match asset variant (blue/dark/light) to the background it sits on.

---

## Logo

**Two SVG files** (bundled in `assets/`):
- `SBP_logo_black.svg` — use on SBP Blue backgrounds (default) and light backgrounds
- `SBP_logo_white.svg` — use on dark backgrounds and dark images

**Margins:** 50% of logo height (nav/banners), 100% (objects), 200% (center of canvas).

**Size:** 25% of canvas height (landscape), 25% of canvas width (portrait/square), 20% (A4).

**Rules:** Default to SBP Blue. Never swap slash and text colors. Always ensure sufficient contrast.

---

## Grids & Layouts

- **16-column grid** inside 10% margin (portrait: 10% width, landscape: 10% height)
- **Spacing:** multiples of logo height — `0.5x`, `1x`, `2x`, `3x`
- **Gutter:** 1 grid column between columns
- **Maximum 5 elements per layout** (logo, image, title, text, labels)
- One container width across all pages of a document

---

## Photography

Five principles: **Real** (actual SBP colleagues), **Warm** (light, bright, welcoming), **Depth of field** (human perspective, sharp subject), **A touch of blue** (SBP Blue present in every photo), **In action** (people doing real things).

Don'ts: no staged stock, no low quality, no Photoshop effects, no lens flares.

Photo assets: contact SBP marketing team.

---

## Iconography

Two types: **Flat rounded line icons** (PNG/SVG, thousands available) and **Custom-made icons** (focus area illustrations + sbp.cloud icons). All follow 10% corner roundness.

Icon assets: contact SBP marketing team.
