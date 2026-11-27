# HTML

HTML rules: security, performance, semantics and accessibility. Load together with `core/`.

- Rule prefix: `HTML`
- Accessibility rules use the maintainability lens and follow WCAG 2.2.

## Security

### HTML-SEC-001: Allow scripts through a Content Security Policy, not inline code

**Level:** SHOULD · **Lens:** security

Inline `<script>` blocks and `onclick` attributes can only run if the policy allows inline code, which also lets injected markup run. Move code to files and send a CSP that lists the allowed sources.

```html
<!-- Bad -->
<button onclick="deleteItem(42)">Delete</button>

<!-- Good: Content-Security-Policy: script-src 'self' -->
<button type="button" data-item-id="42" class="js-delete">Delete</button>
<script src="/js/items.js" defer></script>
```

**Exceptions:** inline scripts allowed by a per-response nonce or hash.
**Source:** [MDN, Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

### HTML-SEC-002: Add `rel="noopener noreferrer"` to links that open untrusted sites in a new tab

**Level:** SHOULD · **Lens:** security

A page opened with `target="_blank"` could control the opener through `window.opener` in older browsers, and receives the full referrer URL. `noopener` and `noreferrer` cut both.

```html
<!-- Bad -->
<a href="https://other.example" target="_blank">Partner</a>

<!-- Good -->
<a href="https://other.example" target="_blank" rel="noopener noreferrer">Partner</a>
```

**Exceptions:** links to your own origin that need the referrer.
**Source:** [MDN, rel=noopener](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel/noopener)

### HTML-SEC-003: Use Subresource Integrity for scripts and styles from a CDN

**Level:** SHOULD · **Lens:** security

If a CDN is compromised, every site loading from it runs the attacker's code. The `integrity` hash makes the browser refuse a file that changed.

```html
<!-- Bad -->
<script src="https://cdn.example.com/lib@1.2.3/lib.min.js"></script>

<!-- Good -->
<script
  src="https://cdn.example.com/lib@1.2.3/lib.min.js"
  integrity="sha384-REPLACE_WITH_THE_FILE_HASH"
  crossorigin="anonymous"
></script>
```

**Exceptions:** files served from your own origin.
**Source:** [MDN, Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)

## Performance

### HTML-PERF-001: Load scripts with `defer` or `type="module"`

**Level:** SHOULD · **Lens:** performance

A plain `<script src>` in `<head>` stops HTML parsing until the file downloads and runs. `defer` and modules download in parallel and run after parsing, in order.

```html
<!-- Bad -->
<head>
  <script src="/js/app.js"></script>
</head>

<!-- Good -->
<head>
  <script src="/js/app.js" defer></script>
</head>
```

**Exceptions:** small scripts that must run before first paint (for example, setting the color theme).
**Source:** [MDN, script element, defer attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#defer)

### HTML-PERF-002: Give images and videos `width` and `height`

**Level:** SHOULD · **Lens:** performance

Without dimensions the browser does not know how much space to reserve, so content jumps when the media loads (Cumulative Layout Shift). The attributes set the aspect ratio; CSS can still make the image responsive.

```html
<!-- Bad -->
<img src="/img/team.jpg" alt="The team at the 2026 meetup">

<!-- Good -->
<img src="/img/team.jpg" alt="The team at the 2026 meetup" width="1200" height="800">
```

**Source:** [web.dev, optimize Cumulative Layout Shift](https://web.dev/articles/optimize-cls)

### HTML-PERF-003: Lazy-load offscreen images, but never the main image

**Level:** SHOULD · **Lens:** performance

`loading="lazy"` delays images below the fold until the user scrolls near them. On the largest image in the first view it delays the Largest Contentful Paint instead.

```html
<!-- Bad -->
<img src="/img/hero.jpg" alt="Product overview" width="1600" height="900" loading="lazy">

<!-- Good -->
<img src="/img/hero.jpg" alt="Product overview" width="1600" height="900" fetchpriority="high">
<img src="/img/footer-map.png" alt="Office location" width="600" height="400" loading="lazy">
```

**Source:** [web.dev, browser-level image lazy loading](https://web.dev/articles/browser-level-image-lazy-loading)

## Maintainability

### HTML-MAINT-001: Declare the page language on `<html>`

**Level:** MUST · **Lens:** maintainability

Screen readers choose pronunciation from `lang`, and browsers use it for translation, hyphenation and spell check.

```html
<!-- Bad -->
<html>

<!-- Good -->
<html lang="pt-BR">
```

**Source:** [WCAG 2.2, 3.1.1 Language of Page](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html)

### HTML-MAINT-002: Give every meaningful image a text alternative

**Level:** MUST · **Lens:** maintainability

Screen readers read `alt` in place of the image, and it is shown when the image fails to load. Describe what the image conveys; use `alt=""` for decoration so it is skipped.

```html
<!-- Bad -->
<img src="/img/chart-q3.png">

<!-- Good -->
<img src="/img/chart-q3.png" alt="Sales grew 18% in Q3, led by the south region">
<img src="/img/divider.svg" alt="">
```

**Source:** [WCAG 2.2, 1.1.1 Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

### HTML-MAINT-003: Use `<button>` for actions and `<a>` for navigation

**Level:** MUST · **Lens:** maintainability

A `<div>` with a click handler cannot be focused or activated with the keyboard and is not announced as a control. Native elements do this for free.

```html
<!-- Bad -->
<div class="btn" onclick="save()">Save</div>

<!-- Good -->
<button type="button" class="btn" id="save">Save</button>
```

**Source:** [MDN, button element accessibility](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#accessibility)

### HTML-MAINT-004: Label every form field

**Level:** MUST · **Lens:** maintainability

A placeholder disappears while typing and is not a reliable name for assistive technology. A `<label>` tied to the field names it and enlarges the click target.

```html
<!-- Bad -->
<input type="email" placeholder="Email">

<!-- Good -->
<label for="email">Email</label>
<input id="email" name="email" type="email" autocomplete="email">
```

**Source:** [WAI tutorials, labeling controls](https://www.w3.org/WAI/tutorials/forms/labels/)

### HTML-MAINT-005: Structure pages with landmarks and ordered headings

**Level:** SHOULD · **Lens:** maintainability

`<header>`, `<nav>`, `<main>` and `<footer>`, plus headings that do not skip levels, let screen reader users jump through the page and make the markup readable.

```html
<!-- Bad -->
<div class="header">...</div>
<div class="content">
  <div class="title">Orders</div>
  <h4>Pending</h4>
</div>

<!-- Good -->
<header>...</header>
<main>
  <h1>Orders</h1>
  <h2>Pending</h2>
</main>
```

**Source:** [WAI tutorials, page structure](https://www.w3.org/WAI/tutorials/page-structure/)
