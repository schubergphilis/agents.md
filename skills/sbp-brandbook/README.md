# Schuberg Philis Design System

Human-readable companion to `SKILL.md`. This design system contains the brand
elements, visual foundations, typography, colors, slide templates, and preview
cards for Schuberg Philis — a premium IT consultancy focused on
mission-critical infrastructure.

> **License:** This directory is proprietary SBP intellectual property — see
> `LICENSE`. Not covered by the repository's open-source license.

## Company context

**Schuberg Philis** is a high-end technology consultancy specializing in
mission-critical infrastructure and cloud transformation. The brand
communicates **confidence, precision, and technical mastery** through:

- Clean, structured layouts that prioritize clarity over decoration
- A restrained palette anchored by SBP Blue and naval tones
- Professional typography with TT Interphases (a geometric sans-serif)
- Insight-driven content that leads with value, not labels

## What's inside

```
sbp-brandbook/
├── SKILL.md             ← Agent skill definition + full visual spec
├── README.md            ← You are here (human reference)
├── colors_and_type.css  ← Color tokens + typography variables (import-ready)
├── fonts/               ← TT Interphases web fonts (WOFF2 subset) + README
├── assets/              ← Logos (new system) + stylization shapes (slash/square/corner/button)
├── slides/              ← Six ready-to-use HTML slide templates
└── preview/             ← Design-system reference cards (colors, type, spacing, components)
```

## Content fundamentals

**Tone & voice** — Confident authority and technical precision. Professional
but not stuffy: direct, expert-led, results-oriented. Copy is
**insight-driven**: every slide title asserts a finding, never merely labels.

**Writing conventions**
- **Sentence case everywhere** — Titles, eyebrows, body, subheads. Never title
  case. Never all caps except rare axis labels.
- **Insight-first titles** — Titles carry the message, not the category. Write
  "Three options, one recommendation — with consequences named", not
  "Decision options".
- **Hyphen separators in metadata** — Eyebrows use middle-hyphen with spaces:
  `M01.58 - Matrix - Maturity Heat`. Never pipes or middle dots here.
- **Pipe separators in footers** — `Schuberg Philis  |  M01 FOUNDATIONS`.
- **Em dashes in titles only** — For two-clause framing; avoided in body copy.
- **No emoji** — Technical precision over playfulness.
- **Third person, implied "you"** — No "I" or "we"; insights are presented as
  authoritative findings.

**Content structure** — Every content slide has a three-part header: **Eyebrow**
(context/reference) → **Title** (the insight) → **Subhead** (how to read it).
The marker bar sits between title and subhead. Titles are one line preferred,
two acceptable, never three.

## Visual foundations

**Color philosophy** — Intentionally restrained. SBP Blue (`#1E80ED`) is the
primary brand color. Soft Blue (`#E8F2FD`) provides calm backgrounds for tables
and dense content. **Yellow (`#FFDB4E`) is reserved exclusively for
decisions** — recommendation bars, highlighted matrix cells, the chosen option.
It never appears as passive decoration.

**Typography** — A single family: **TT Interphases**. Two weights dominate:
**Regular** (400) for body and **Black** (900) for titles and emphasis.
**TT Interphases Mono** is used exclusively for eyebrows.

**Backgrounds** — Light slides (≈78% of content) use White or Soft Blue. Dark
slides (covers, chapters, statements) use Space Gray (`#082646`) full-bleed. No
gradients, no textures, no photos as backgrounds. The **sandwich structure**:
decks open dark → transition to light → return to dark.

**The marker bar** — The **1.5 cm × 0.1 cm** horizontal bar is the signature
SBP element, on every slide: SBP Blue on light, Joyful Yellow on dark.
Positioned between title and subhead. Always 1.5 cm wide (never full-width).
This is not decorative — it is the brand's visual signature.

**Cards & panels** — Three constructions dominate:
1. **Indexed cards** — Blue header strip with white number (01, 02…) + white body
2. **Pale panel cards** — Soft blue fill, no header strip (matrices, frameworks)
3. **Decision cards** — Space Gray body with yellow accents + full-width yellow
   recommendation bar

**Shadows, borders, corners** — No drop shadows. No borders (cards differentiate
by fill color only). Subtle corner radii. Flat, layered composition.

## Key design principles

1. **Insight-first titles** — Every slide title asserts value, never just labels
2. **The marker bar** — The 1.5 × 0.1 cm bar is the signature SBP element
3. **Yellow signals decisions** — Only for recommendations/chosen outcomes
4. **Sandwich structure** — Dark (covers) → light (content) → dark (dividers)
5. **Numbered cards for enumeration** — Listing 2–5 items: indexed cards
6. **Sentence case throughout**

---

_For precise measurements, the size scale, stylization rules, grids, logo
margins, and asset usage, see `SKILL.md`. Based on the SBP Master Library._
