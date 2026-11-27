# CSS

CSS rules: performance, maintainability and accessibility. Load together with `core/`; they apply to `.scss` too.

- Rule prefix: `CSS`
- Formatting and property order are left to Prettier or Stylelint and are not rules here.

## Performance

### CSS-PERF-001: Animate `transform` and `opacity`, not layout properties

**Level:** SHOULD · **Lens:** performance

Animating `top`, `left`, `width` or `height` recalculates layout and repaints on every frame. `transform` and `opacity` can run on the compositor without layout.

```css
/* Bad */
.drawer {
  left: -300px;
  transition: left 0.3s;
}
.drawer.open {
  left: 0;
}

/* Good */
.drawer {
  transform: translateX(-300px);
  transition: transform 0.3s;
}
.drawer.open {
  transform: translateX(0);
}
```

**Source:** [web.dev, high-performance CSS animations](https://web.dev/articles/animations-guide)

### CSS-PERF-002: Set `font-display` for web fonts

**Level:** SHOULD · **Lens:** performance

By default text can stay invisible for up to three seconds while a web font downloads. `font-display: swap` shows a fallback font at once and swaps when the font arrives.

```css
/* Bad */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter.woff2") format("woff2");
}

/* Good */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter.woff2") format("woff2");
  font-display: swap;
}
```

**Exceptions:** icon fonts, where a fallback glyph is meaningless (`block` fits better).
**Source:** [MDN, font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display)

### CSS-PERF-003: Avoid `@import` in CSS files

**Level:** AVOID · **Lens:** performance

The browser discovers an `@import` only after downloading the file that contains it, so imported sheets load one after another. Use `<link>` tags or let the bundler concatenate the files.

```css
/* Bad: main.css */
@import url("reset.css");
@import url("layout.css");

/* Good: bundled at build time, or one <link> per file in the HTML */
```

**Exceptions:** Sass `@use` and `@import`, which are resolved at build time.
**Source:** [MDN, @import](https://developer.mozilla.org/en-US/docs/Web/CSS/@import)

## Maintainability

### CSS-MAINT-001: Never remove the focus outline without a visible replacement

**Level:** MUST · **Lens:** maintainability

Keyboard users rely on the focus indicator to know where they are. `outline: none` with nothing in its place makes the page unusable for them.

```css
/* Bad */
button:focus {
  outline: none;
}

/* Good */
button:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 2px;
}
```

**Source:** [WCAG 2.2, 2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)

### CSS-MAINT-002: Avoid `!important`

**Level:** AVOID · **Lens:** maintainability

`!important` wins over normal specificity, so the next override needs another `!important`, and the cascade stops being predictable. Fix the selector or use cascade layers.

```css
/* Bad */
.button {
  color: white !important;
}

/* Good */
@layer base, components;
@layer components {
  .button {
    color: white;
  }
}
```

**Exceptions:** utility classes meant to always win, and overriding third-party inline styles you cannot change.
**Source:** [MDN, @layer](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)

### CSS-MAINT-003: Keep selectors short and specificity low

**Level:** SHOULD · **Lens:** maintainability

ID selectors and deep descendant chains are hard to override and break when the markup moves. One class per component part keeps specificity flat.

```css
/* Bad */
#sidebar ul li a.active {
  font-weight: bold;
}

/* Good */
.nav-link--active {
  font-weight: bold;
}
```

**Source:** [MDN, specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity)

### CSS-MAINT-004: Store repeated values in custom properties

**Level:** SHOULD · **Lens:** maintainability

The same color or spacing typed in many places drifts over time and makes themes (such as dark mode) expensive. Custom properties give each value one name and one place to change.

```css
/* Bad */
.card {
  border: 1px solid #d0d7de;
}
.input {
  border: 1px solid #d0d7de;
}

/* Good */
:root {
  --color-border: #d0d7de;
}
.card,
.input {
  border: 1px solid var(--color-border);
}
```

**Source:** [MDN, using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

### CSS-MAINT-005: Size text in `rem`, not `px`

**Level:** SHOULD · **Lens:** maintainability

Text in `px` ignores the font size the user set in the browser. `rem` scales with it.

```css
/* Bad */
body {
  font-size: 14px;
}

/* Good */
body {
  font-size: 0.875rem;
}
```

**Exceptions:** borders and hairlines, which should stay thin.
**Source:** [WCAG 2.2, 1.4.4 Resize Text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)

### CSS-MAINT-006: Respect `prefers-reduced-motion`

**Level:** SHOULD · **Lens:** maintainability

Large or parallax animations can cause dizziness and nausea for people with vestibular disorders. Reduce or remove non-essential motion when the user asks for it.

```css
/* Bad */
.hero {
  animation: float 3s infinite;
}

/* Good */
.hero {
  animation: float 3s infinite;
}
@media (prefers-reduced-motion: reduce) {
  .hero {
    animation: none;
  }
}
```

**Source:** [MDN, prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
