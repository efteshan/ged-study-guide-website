# Design System PRD — Reverse-Engineered from index.html

> **Purpose**: This document captures EVERY visual design decision, UI pattern, color, font, spacing, animation, layout, component, and responsive behavior from the source website. Hand this PRD to any AI coding agent to reproduce the **exact same design** with completely different content.

---

## 1. Technology Stack

| Layer | Technology | Details |
|-------|-----------|---------|
| Structure | HTML5 | Single-file SPA, `<!DOCTYPE html>`, `lang="en"` |
| Styling | Vanilla CSS | All CSS is embedded in a single `<style>` block inside `<head>` |
| Typography | Google Fonts | `Inter` (weights: 400, 500, 600, 700, 800) and `JetBrains Mono` (weights: 400, 500) |
| Code Highlighting | highlight.js 11.9.0 | CDN-loaded, themes: `atom-one-dark` (dark) / `atom-one-light` (light) |
| JavaScript | Vanilla JS | No frameworks. All interactivity is plain DOM manipulation |
| External Dependencies | None | Everything is self-contained in one HTML file |

---

## 2. Architecture — Two-Tier Tab System

The site uses a **two-level navigation hierarchy**. This is the core UX pattern.

### Level 1: Top-Level Nav (Main Switcher)

- **Position**: Sticky at `top: 0`, `z-index: 200`
- **Layout**: Flexbox, horizontally centered, `gap: 15px`, `padding: 15px 20px`
- **Border**: `2px solid var(--border)` on the bottom
- **Buttons** (class `.main-switcher-btn`):
  - Transparent background by default
  - `2px solid transparent` border
  - `font-size: 1.05rem`, `font-weight: 700`
  - `padding: 10px 24px`, `border-radius: 8px`
  - **Hover**: text color brightens to primary, background becomes card color
  - **Active**: border becomes accent color, background becomes card color, gains `box-shadow`
- **Behavior**: Clicking a top-level button shows/hides entire content sections (`.main-tab`). Only one is visible at a time. Page scrolls to top smoothly on switch.
- **Theme toggle** button lives INSIDE this top nav bar (rightmost position)

### Level 2: Sub-Tab Navigation (Horizontal Scrolling Tabs)

- **Position**: Inside each main tab's `.container`
- **Structure**: `.tabs-wrapper` contains:
  1. Left scroll arrow button (`.scroll-btn`)
  2. `<nav class="tabs-nav">` — horizontally scrollable tab strip
  3. Right scroll arrow button (`.scroll-btn`)
- **Tab Strip** (`.tabs-nav`):
  - `display: flex`, `overflow-x: auto`, `white-space: nowrap`
  - Scrollbar completely hidden (both `-webkit-scrollbar: none` and `scrollbar-width: none`)
  - `-webkit-overflow-scrolling: touch` for iOS momentum scrolling
- **Tab Buttons** (`.tab-btn`):
  - `padding: 12px 20px`, `font-size: 0.9rem`, `font-weight: 600`
  - `border-bottom: 2px solid transparent`
  - **Hover**: text brightens, background becomes code background color
  - **Active**: text becomes primary color, `border-bottom: 2px solid var(--accent)`
- **Scroll Arrows** (`.scroll-btn`):
  - `width: 36px`, fixed on left/right edges
  - Unicode chevrons: `❮` (left) and `❯` (right)
  - Scrolls the tab strip by `200px` with `behavior: 'smooth'`
  - **Hidden on mobile** (`display: none` at `≤640px`)
- **Behavior**: Each tab button has a `data-target` attribute pointing to a `.tab-pane` ID. Clicking activates that pane, deactivates all others. Uses `fadeIn` animation. Scrolls page to top.

### Tab Content Panes

- Class `.tab-pane` — `display: none` by default
- Class `.tab-pane.active` — `display: block`
- Fade-in animation on activation (see Animations section)

---

## 3. Theme System (Dark Mode / Light Mode)

### Toggle Switch

- **Element**: `<button>` with class `.theme-toggle`
- **Dimensions**: `width: 52px`, `height: 28px`
- **Shape**: `border-radius: 14px` (pill shape)
- **Knob**: CSS `::after` pseudo-element, `22px × 22px` circle, `3px` offset from edges
- **Icons**: Moon 🌙 emoji (left) and Sun ☀️ emoji (right) inside `.toggle-icons` span
- **Animation**: Knob slides `translateX(24px)` when switching to light mode
- **Persistence**: Theme saved to `localStorage` under key `'theme'`
- **Default**: Dark mode (`data-theme="dark"` on `<html>`)

### Theme Implementation

Themes are controlled via `data-theme` attribute on `<html>` element. All colors use CSS custom properties.

### Dark Theme Variables (`[data-theme="dark"]`)

```css
--bg-primary: #000000           /* Pure black background */
--bg-secondary: #0a0a0a         /* Near-black for secondary areas */
--bg-card: #111111              /* Slightly lighter for card surfaces */
--bg-code: #1a1a1a              /* Code block backgrounds */
--bg-table-header: #1a1a1a      /* Table header row */
--bg-table-row: #111111         /* Table body rows */
--bg-table-row-alt: #0d0d0d     /* Alternating table rows */
--bg-tip: rgba(255,255,255,0.04)       /* Callout backgrounds (subtle white overlay) */
--bg-important: rgba(255,255,255,0.04)
--bg-note: rgba(255,255,255,0.04)
--text-primary: #ffffff         /* Main text — pure white */
--text-secondary: #a0a0a0       /* Body paragraphs — medium gray */
--text-muted: #666666           /* Least important text — dark gray */
--accent: #ffffff               /* Accent color — white (used for active borders) */
--border: #222222               /* Primary borders */
--border-light: #1a1a1a         /* Subtle borders (table row separators) */
--tip-border: #3b82f6           /* Blue — tip callouts */
--important-border: #f59e0b     /* Amber — important callouts */
--note-border: #8b5cf6          /* Purple — note callouts & practice boxes */
--caution-border: #ef4444       /* Red — caution callouts */
--scrollbar-thumb: #333333
--scrollbar-track: #111111
--toggle-bg: #222222
--toggle-knob: #ffffff
--shadow: 0 1px 3px rgba(0,0,0,0.5)
```

### Light Theme Variables (`[data-theme="light"]`)

```css
--bg-primary: #ffffff
--bg-secondary: #f8f8f8
--bg-card: #ffffff
--bg-code: #f5f5f5
--bg-table-header: #f0f0f0
--bg-table-row: #ffffff
--bg-table-row-alt: #fafafa
--bg-tip: rgba(0,0,0,0.03)
--bg-important: rgba(0,0,0,0.03)
--bg-note: rgba(0,0,0,0.03)
--text-primary: #000000
--text-secondary: #555555
--text-muted: #999999
--accent: #000000
--border: #e0e0e0
--border-light: #eeeeee
--tip-border: #2563eb
--important-border: #d97706
--note-border: #7c3aed
--caution-border: #dc2626
--scrollbar-thumb: #cccccc
--scrollbar-track: #f0f0f0
--toggle-bg: #e0e0e0
--toggle-knob: #000000
--shadow: 0 1px 3px rgba(0,0,0,0.1)
```

### Design Philosophy

- **Dark mode**: Pure black (`#000`) background with white text. Monochromatic with colored accents only on callout borders. Very OLED-friendly.
- **Light mode**: Pure white (`#fff`) background with black text. Same monochromatic philosophy inverted.
- **Both modes**: The accent colors (blue, amber, purple, red) remain consistent semantic markers.

---

## 4. Typography

### Font Stack

| Usage | Font Family | Fallbacks |
|-------|-----------|-----------|
| Body / UI | `'Inter'` | `-apple-system, BlinkMacSystemFont, sans-serif` |
| Code / Monospace | `'JetBrains Mono'` | `'Fira Code', 'Consolas', monospace` |

### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### Type Scale

| Element | Size | Weight | Letter-Spacing | Other |
|---------|------|--------|----------------|-------|
| Hero `h1` | `clamp(1.8rem, 5vw, 2.6rem)` | 800 | `-0.03em` | `line-height: 1.2` |
| Site header `h1` | `1.1rem` | 700 | `-0.02em` | `text-overflow: ellipsis` |
| Section `h2` | `1.4rem` | 700 | `-0.02em` | — |
| `h3` | `1.1rem` | 600 | `-0.01em` | `margin: 28px 0 12px` |
| `h4` | `1rem` | 600 | — | `margin: 20px 0 10px` |
| Body `p` | inherit (~`1rem`) | 400 | — | `line-height: 1.7`, `color: --text-secondary` |
| `strong` | — | 600 | — | `color: --text-primary` (stands out from gray body text) |
| `code` (inline) | `0.85em` | — | — | Monospace, with border and background |
| `pre code` | `0.88rem` | — | — | `line-height: 1.6` |
| Table `th` | `0.8rem` | 600 | `0.04em` | `text-transform: uppercase` |
| Table `td` | `0.9rem` (table font-size) | — | — | — |
| Section number badge | `0.75rem` | 700 | `0.05em` | `text-transform: uppercase` |
| Callout title | `0.8rem` | 700 | `0.05em` | `text-transform: uppercase` |
| Tab button | `0.9rem` | 600 | — | — |
| Main switcher button | `1.05rem` | 700 | — | — |

### Key Typography Rules

- **`-webkit-font-smoothing: antialiased`** on body for crisp text rendering
- **Negative letter-spacing** on headings (`-0.01em` to `-0.03em`) for tighter, modern heading feel
- **Positive letter-spacing** on labels/badges (`0.04em` to `0.05em`) with `text-transform: uppercase` for small caps look
- **Body text is SECONDARY color** (gray), NOT primary — this is critical. `<strong>` tags pop to primary (white/black) for emphasis

---

## 5. Layout System

### Container

- `max-width: 780px` — narrow, readable column
- `margin: 0 auto` — centered
- `padding: 40px 24px 80px` (generous bottom padding)

### Site Header

- Full-width bar at very top (NOT sticky — the top-level nav below it IS sticky)
- `padding: 16px 24px`
- Flexbox: `align-items: center`, `justify-content: center`
- `border-bottom: 1px solid var(--border)`
- Contains: `<h1>` title + theme toggle button

> **Note**: In the actual file, the theme toggle is inside `.top-level-nav`, not a separate header. The `.site-header` class exists in CSS but the HTML uses `.top-level-nav` as the primary header bar.

### Hero Section

- `text-align: center`, `padding: 48px 0 40px`
- `border-bottom: 1px solid var(--border)`, `margin-bottom: 48px`
- Contains centered `h1` (fluid size) and subtitle `p` (`max-width: 520px`, `margin: 0 auto`)

### Section Pattern

Each content section follows this structure:
```
.section
  .section-header (flex row with bottom border)
    .section-number (badge/pill)
    h2 (section title)
  p (intro paragraph)
  [content blocks: code, tables, callouts, practice boxes]
```

- Section spacing: `margin-bottom: 56px`
- Section header: `gap: 12px`, `padding-bottom: 12px`, `border-bottom: 1px solid var(--border)`

---

## 6. Component Library

### 6.1 Section Number Badge (`.section-number`)

- `font-size: 0.75rem`, `font-weight: 700`
- `color: var(--text-muted)`
- `background: var(--bg-code)`, `border: 1px solid var(--border)`
- `padding: 4px 10px`, `border-radius: 4px`
- `text-transform: uppercase`, `letter-spacing: 0.05em`

### 6.2 Code Blocks (`pre` / `code`)

**Block code (`<pre>`):**
- `background: var(--bg-code)`, `border: 1px solid var(--border)`
- `border-radius: 8px`, `padding: 20px`
- `margin: 16px 0`, `overflow-x: auto`
- `font-size: 0.88rem`, `line-height: 1.6`

**Inline code (`<code>`):**
- `background: var(--bg-code)`, `border: 1px solid var(--border)`
- `padding: 2px 6px`, `border-radius: 4px`
- `font-size: 0.85em`, `color: var(--text-primary)`

### 6.3 Tables

**Wrapper** (`.table-wrapper`):
- `overflow-x: auto`, `margin: 16px 0`
- `border: 1px solid var(--border)`, `border-radius: 8px`

**Table**:
- `width: 100%`, `border-collapse: collapse`, `font-size: 0.9rem`

**Header** (`th`):
- `background: var(--bg-table-header)`
- `padding: 12px 16px`, `font-weight: 600`
- `font-size: 0.8rem`, `text-transform: uppercase`, `letter-spacing: 0.04em`
- `color: var(--text-secondary)`, `border-bottom: 1px solid var(--border)`

**Cells** (`td`):
- `padding: 12px 16px`, `border-bottom: 1px solid var(--border-light)`
- `color: var(--text-secondary)`, `vertical-align: top`

**Alternating rows**: `tr:nth-child(even)` → `background: var(--bg-table-row-alt)`

**Last row**: No bottom border on `td`

### 6.4 Callout Boxes (`.callout`)

**Base styles**:
- `border-left: 3px solid` (color varies by type)
- `border-radius: 0 8px 8px 0` (rounded on right only)
- `padding: 16px 20px`, `margin: 20px 0`, `font-size: 0.9rem`

**Title** (`.callout-title`):
- `font-weight: 700`, `font-size: 0.8rem`
- `text-transform: uppercase`, `letter-spacing: 0.05em`
- Flex row with `gap: 6px` for emoji + text

**Three variants**:

| Variant | Class | Border Color | Title Color | Emoji |
|---------|-------|-------------|-------------|-------|
| Tip | `.callout.tip` | `--tip-border` (#3b82f6 blue) | Blue | 💡 |
| Important | `.callout.important` | `--important-border` (#f59e0b amber) | Amber | ⚠️ |
| Note | `.callout.note` | `--note-border` (#8b5cf6 purple) | Purple | (none or custom) |

**Background**: All use semi-transparent overlay (`rgba(255,255,255,0.04)` dark / `rgba(0,0,0,0.03)` light)

### 6.5 Practice Box (`.practice-box`)

- `margin-top: 40px`
- `border: 1px solid var(--note-border)` (purple border)
- `border-radius: 8px`, `overflow: hidden`
- `background: var(--bg-card)`

**Header** (`.practice-header`):
- `background: var(--bg-secondary)`, `padding: 12px 16px`
- `font-weight: 700`, `font-size: 1rem`
- `border-bottom: 1px solid var(--border)`
- `color: var(--note-border)` (purple text)

**Body** (`.practice-body`):
- `padding: 20px`

**Question** (`.practice-question`):
- `font-size: 0.95rem`, `margin-bottom: 15px`, `line-height: 1.5`

**Show Answer Button** (`.show-answer-btn`):
- `background: var(--note-border)` (purple), `color: #fff`
- `padding: 10px 18px`, `border-radius: 6px`
- `font-weight: 600`
- Hover: `opacity: 0.85`
- **Behavior**: On click, reveals the `.practice-answer` div and hides itself (`this.style.display='none'`)

**Answer** (`.practice-answer`):
- `display: none` by default, shown by adding `.show` class
- `margin-top: 20px`, `padding-top: 15px`
- `border-top: 1px dashed var(--border)`

### 6.6 Browser Preview (`.browser-preview`)

- `background: var(--bg-code)`, `border: 1px solid var(--border)`
- `border-radius: 8px`, `padding: 16px 20px`, `margin: 12px 0`
- Label: `.browser-preview-label` — `font-size: 0.75rem`, `font-weight: 600`, uppercase, muted color

### 6.7 Diagram Box (`.diagram-box`)

- `background: var(--bg-code)`, `border: 1px solid var(--border)`
- `border-radius: 8px`, `padding: 20px`
- `text-align: center`, `font-family: 'JetBrains Mono'`
- `font-size: 0.85rem`, `line-height: 2`
- `white-space: pre` (preserves ASCII art formatting)
- `overflow-x: auto`

### 6.8 Content Lists (`.content-list`)

- `padding-left: 24px`, `margin: 8px 0 14px`
- `color: var(--text-secondary)`
- List items: `margin-bottom: 4px`

### 6.9 Divider (`<hr class="divider">`)

- `border: none`, `border-top: 1px solid var(--border)`
- `margin: 48px 0`

---

## 7. Custom Scrollbar

```css
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--scrollbar-track); }
::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 3px; }
```

- Thin 6px scrollbar
- Theme-aware colors

---

## 8. Animations

### Fade In (`@keyframes fadeIn`)

```css
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to   { opacity: 1; transform: translateY(0); }
}
```

- Duration: `0.3s`, easing: `ease-in-out`
- Applied to: `.tab-pane` and `.main-tab` on activation
- Creates subtle slide-up + fade effect

### Transition Speed

- Global: `--transition-speed: 0.3s`
- Applied to: theme changes (background, color, border), button hovers, toggle knob

---

## 9. Responsive Design

### Breakpoint: `≤640px` (Mobile)

| Element | Change |
|---------|--------|
| `.site-header` | `padding: 12px 16px` |
| `.site-header h1` | `font-size: 0.95rem` |
| `.container` | `padding: 24px 16px 60px` |
| `.hero` | `padding: 32px 0 28px`, `margin-bottom: 32px` |
| `.section` | `margin-bottom: 40px` |
| `.section-header` | `flex-direction: column`, `align-items: flex-start`, `gap: 6px` |
| `.section-header h2` | `font-size: 1.2rem` |
| `pre` | `padding: 14px`, `font-size: 0.82rem`, `border-radius: 6px` |
| `th, td` | `padding: 10px 12px`, `font-size: 0.85rem` |
| `.callout` | `padding: 14px 16px` |
| `.scroll-btn` | `display: none` (tab scroll arrows hidden) |

### Breakpoint: `≤380px` (Small Mobile)

| Element | Change |
|---------|--------|
| `.site-header h1` | `font-size: 0.85rem` |
| `.hero h1` | `font-size: 1.5rem` |
| `pre` | `font-size: 0.78rem`, `padding: 12px` |
| `th, td` | `padding: 8px 10px`, `font-size: 0.8rem` |

### Mobile Tab Behavior

- Tab strip becomes touch-scrollable (momentum scrolling via `-webkit-overflow-scrolling: touch`)
- Scroll arrows hidden since user can swipe
- Section headers stack vertically (badge above title)

---

## 10. JavaScript Behavior Specification

### Theme Toggle

```
1. On page load: read localStorage('theme'), default to 'dark'
2. Set html[data-theme] attribute
3. Set highlight.js stylesheet URL accordingly
4. On toggle click: flip theme, update attribute, update hljs URL, save to localStorage
```

### Main Tab Switching

```
1. Click a .main-switcher-btn
2. Remove .active from ALL .main-switcher-btn elements
3. Remove .active from ALL .main-tab elements
4. Add .active to clicked button
5. Determine target: button id 'nav-X' maps to 'tab-X'
6. Add .active to target .main-tab
7. Smooth scroll to top
8. Re-highlight any un-highlighted code blocks in the newly visible tab
```

### Sub-Tab Switching (Scoped per tab group)

```
1. Initialize with initTabs(wrapperSelector) for each .tabs-wrapper
2. On .tab-btn click:
   a. Remove .active from all sibling .tab-btn
   b. Add .active to clicked button
   c. Get data-target attribute → find target pane by ID
   d. Remove .active from all sibling .tab-pane
   e. Add .active to target pane
   f. Highlight code blocks in pane
   g. Smooth scroll to top
3. Scroll arrows: scrollBy({left: ±200, behavior: 'smooth'})
```

---

## 11. Page Structure Template

```
<html data-theme="dark">
<head>
  [Google Fonts: Inter + JetBrains Mono]
  [highlight.js CSS theme]
  [highlight.js JS]
  <style> [All CSS from Section 3-9 above] </style>
</head>
<body>
  <!-- LEVEL 1: Top Nav (sticky) -->
  <div class="top-level-nav">
    <button class="main-switcher-btn active">Tab A</button>
    <button class="main-switcher-btn">Tab B</button>
    <button class="theme-toggle">🌙 ☀️</button>
  </div>

  <!-- MAIN TAB A -->
  <div id="tab-a" class="main-tab active">
    <div class="container">
      <!-- LEVEL 2: Sub-tab nav -->
      <div class="tabs-wrapper">
        <button class="scroll-btn">❮</button>
        <nav class="tabs-nav">
          <button class="tab-btn active" data-target="pane-1">Sub 1</button>
          <button class="tab-btn" data-target="pane-2">Sub 2</button>
          <!-- ... more tabs ... -->
        </nav>
        <button class="scroll-btn">❯</button>
      </div>

      <!-- Sub-tab content panes -->
      <div class="section tab-pane active" id="pane-1">
        <div class="section-header">
          <span class="section-number">LABEL</span>
          <h2>Title</h2>
        </div>
        <!-- Content: paragraphs, code blocks, tables, callouts, practice boxes -->
      </div>
      <div class="section tab-pane" id="pane-2">...</div>
    </div>
  </div>

  <!-- MAIN TAB B (same internal structure) -->
  <div id="tab-b" class="main-tab">
    <div class="container">
      <div class="tabs-wrapper">...</div>
      <!-- Sub-tab panes -->
    </div>
  </div>

  <script> [All JS from Section 10 above] </script>
</body>
</html>
```

---

## 12. Design Philosophy Summary

| Principle | Implementation |
|-----------|---------------|
| **Monochromatic base** | Black/white only for backgrounds and text. No decorative colors in the base UI. |
| **Semantic color accents** | Color ONLY appears on functional elements: blue=tip, amber=important, purple=note/practice, red=caution |
| **Content-first layout** | Narrow 780px column, generous whitespace, high line-height (1.7) |
| **Progressive disclosure** | Two-tier tabs hide complexity. Practice answers hidden behind buttons. |
| **Zero-decoration** | No gradients, no shadows (except subtle on active buttons), no images, no icons (except emojis) |
| **Typography hierarchy** | 5+ distinct weights (400-800), negative letter-spacing on headings, uppercase small-caps on labels |
| **Consistent component patterns** | Every content type (code, table, callout, practice) has consistent spacing, borders, and radii |
| **Smooth transitions** | All interactive state changes use 0.3s transitions. Tab panes fade in with subtle translateY. |
| **Mobile-first considerations** | Touch scrolling on tabs, stacked layouts, reduced spacing/font-sizes |
| **Persistence** | Theme preference survives page reloads via localStorage |

---

## 13. Critical Implementation Notes for AI Agents

> [!IMPORTANT]
> **These rules MUST be followed exactly to reproduce the design:**

1. **Body text color is SECONDARY (gray), not primary.** Primary color (white/black) is reserved for headings, `<strong>` tags, and active UI elements. This creates the distinctive muted-body-with-bold-highlights feel.

2. **The accent color is monochromatic** — white in dark mode, black in light mode. NOT a brand color.

3. **All borders are `1px solid var(--border)`** — thin, subtle. The only `2px` borders are on the top nav bottom edge and active tab underlines.

4. **Callout boxes use `border-left: 3px solid`** with rounded corners only on the RIGHT side (`border-radius: 0 8px 8px 0`).

5. **Tables are wrapped in `.table-wrapper`** with `overflow-x: auto` and the wrapper gets the border-radius, not the table itself.

6. **Code blocks inside `<pre>` must override highlight.js styles**: `background: none !important`, `padding: 0 !important`, `border: none !important`.

7. **The tab system is SCOPED.** Each `.tabs-wrapper` operates independently. The `initTabs()` function takes a CSS selector and only operates within that DOM subtree. This allows multiple independent tab groups.

8. **Font smoothing**: Apply `-webkit-font-smoothing: antialiased` to `body`.

9. **CSS Reset**: Use `*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }`.

10. **`border-radius: 8px`** is the standard radius for cards, code blocks, tables, callouts. Smaller elements (badges, inline code) use `4px`. Buttons use `6px-8px`.

11. **The hero section is OPTIONAL per main tab.** The source only uses it in one tab. Each main tab can have its own hero or skip it.

12. **Practice boxes use the NOTE/PURPLE color** for their border and header text — tying them visually to the "note" semantic.

13. **All transitions use `var(--transition-speed)` (0.3s)** — never hardcode transition durations.
