# JavaScript

JavaScript rules for browser and Node.js (ES2022+). Load together with `core/`; TypeScript projects also load `typescript.md`.

- Rule prefix: `JS`
- Formatting is left to Prettier and is not a rule here.

## Security

### JS-SEC-001: Never put untrusted data into `innerHTML`

**Level:** MUST · **Lens:** security

`innerHTML`, `outerHTML`, `insertAdjacentHTML` and `document.write` parse their input as HTML, so a value containing `<img onerror=...>` runs script (XSS). Use `textContent` or build nodes with the DOM API.

```javascript
// Bad
comment.innerHTML = `<p>${userText}</p>`;

// Good
const p = document.createElement("p");
p.textContent = userText;
comment.replaceChildren(p);
```

**Exceptions:** HTML that must be rendered goes through a sanitizer such as DOMPurify first.
**Source:** [OWASP DOM-based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)

### JS-SEC-002: Never run strings as code

**Level:** MUST · **Lens:** security

`eval`, `new Function` and string arguments to `setTimeout` / `setInterval` execute whatever text they receive. Parse data with `JSON.parse` and pass functions, not strings.

```javascript
// Bad
const settings = eval(`(${response})`);
setTimeout("refresh()", 1000);

// Good
const settings = JSON.parse(response);
setTimeout(refresh, 1000);
```

**Source:** [MDN, never use eval()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval#never_use_direct_eval!)

### JS-SEC-003: Do not merge untrusted objects into plain objects without filtering keys

**Level:** MUST · **Lens:** security

A key like `__proto__` or `constructor` in parsed JSON can change `Object.prototype` during a deep merge, affecting every object in the process (prototype pollution). Copy only known keys, or use `Map` for arbitrary keys.

```javascript
// Bad
function merge(target, source) {
  for (const key in source) {
    if (typeof source[key] === "object") merge((target[key] ??= {}), source[key]);
    else target[key] = source[key];
  }
}
merge(config, JSON.parse(body));

// Good
const { theme, language } = JSON.parse(body);
Object.assign(config, { theme, language });
```

**Source:** [OWASP Prototype Pollution Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html)

### JS-SEC-004: Use the Web Crypto API, not `Math.random`, for tokens

**Level:** MUST · **Lens:** security

`Math.random` is not cryptographically secure and its output can be predicted. `crypto.randomUUID` and `crypto.getRandomValues` are available in browsers and Node.js.

```javascript
// Bad
const token = Math.random().toString(36).slice(2);

// Good
const token = crypto.randomUUID();
```

**Exceptions:** non-security uses such as animations or shuffling demo data.
**Source:** [MDN, Crypto.getRandomValues()](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/getRandomValues)

### JS-SEC-005: In Node.js, run processes with `execFile` or `spawn`, not `exec`

**Level:** MUST · **Lens:** security

`child_process.exec` runs its string through a shell, so `;` or `$()` in input runs extra commands. `execFile` and `spawn` take an argument array and use no shell by default.

```javascript
// Bad
exec(`convert ${fileName} out.png`);

// Good
execFile("convert", [fileName, "out.png"]);
```

**Exceptions:** fixed commands with no external input.
**Source:** [Node.js docs, child_process](https://nodejs.org/api/child_process.html#child_processexecfilefile-args-options-callback)

### JS-SEC-006: Check the origin of every `message` event

**Level:** MUST · **Lens:** security

Any window can `postMessage` to yours. Without an origin check, a malicious page can send commands your handler trusts.

```javascript
// Bad
window.addEventListener("message", (event) => {
  applySettings(event.data);
});

// Good
window.addEventListener("message", (event) => {
  if (event.origin !== "https://app.example.com") return;
  applySettings(event.data);
});
```

**Source:** [MDN, Window.postMessage() security concerns](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage#security_concerns)

## Performance

### JS-PERF-001: Run independent async calls concurrently

**Level:** SHOULD · **Lens:** performance

`await` inside a loop waits for each call before starting the next, so total time is the sum of all calls. `Promise.all` starts them together, so total time is close to the slowest one.

```javascript
// Bad
const users = [];
for (const id of ids) {
  users.push(await fetchUser(id));
}

// Good
const users = await Promise.all(ids.map((id) => fetchUser(id)));
```

**Exceptions:** calls that depend on each other, must run in order, or would overload the server; limit concurrency for large lists. Running in parallel changes the order of side effects, which is a behavior change when order matters.
**Source:** [MDN, Promise.all()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)

### JS-PERF-002: Batch DOM reads before DOM writes

**Level:** SHOULD · **Lens:** performance

Reading layout (`offsetHeight`, `getBoundingClientRect`) right after a style change forces the browser to recalculate layout synchronously. Alternating reads and writes in a loop does this on every pass (layout thrashing).

```javascript
// Bad
for (const box of boxes) {
  box.style.width = `${box.parentElement.offsetWidth / 2}px`;
}

// Good
const widths = boxes.map((box) => box.parentElement.offsetWidth);
boxes.forEach((box, i) => {
  box.style.width = `${widths[i] / 2}px`;
});
```

**Source:** [web.dev, avoid large, complex layouts and layout thrashing](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing)

### JS-PERF-003: Use `Set` and `Map` for repeated lookups

**Level:** SHOULD · **Lens:** performance

`array.includes` and `array.find` scan the array, O(n) each. Inside a loop that becomes O(n·m); `Set.has` and `Map.get` are O(1) on average.

```javascript
// Bad
const active = orders.filter((o) => activeIds.includes(o.customerId));

// Good
const activeSet = new Set(activeIds);
const active = orders.filter((o) => activeSet.has(o.customerId));
```

**Exceptions:** arrays with a handful of items.
**Source:** [MDN, Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)

### JS-PERF-004: Throttle or debounce high-frequency event handlers

**Level:** SHOULD · **Lens:** performance

`scroll`, `resize`, `pointermove` and `input` can fire dozens of times per second. Heavy work in each event blocks the main thread; mark scroll and touch listeners `passive` and debounce expensive work.

```javascript
// Bad
input.addEventListener("input", () => search(input.value));

// Good
let timer;
input.addEventListener("input", () => {
  clearTimeout(timer);
  timer = setTimeout(() => search(input.value), 300);
});
```

**Exceptions:** cheap handlers. Debouncing delays the work, which is a visible behavior change; agree on the delay.
**Source:** [MDN, EventTarget.addEventListener() passive listeners](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener#using_passive_listeners)

### JS-PERF-005: Remove listeners and timers when their owner goes away

**Level:** SHOULD · **Lens:** performance

Listeners on `window` or `document` and running intervals keep their closures, and everything those reference, alive after a component is removed. Clean them up, for example with one `AbortController`.

```javascript
// Bad
function mount(widget) {
  window.addEventListener("resize", () => widget.layout());
}

// Good
function mount(widget) {
  const controller = new AbortController();
  window.addEventListener("resize", () => widget.layout(), { signal: controller.signal });
  return () => controller.abort(); // call on unmount
}
```

**Source:** [MDN, addEventListener() signal option](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener#signal)

## Maintainability

### JS-MAINT-001: Use `const` and `let`, never `var`

**Level:** MUST · **Lens:** maintainability

`var` is function-scoped and hoisted, so it leaks out of blocks and can be used before its line. `const` signals a binding that never changes; use `let` only when it does.

```javascript
// Bad
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i)); // 3, 3, 3
}

// Good
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i)); // 0, 1, 2
}
```

**Source:** [MDN, let](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let)

### JS-MAINT-002: Use `===` and `!==`

**Level:** MUST · **Lens:** maintainability

`==` converts types with surprising rules (`"" == 0`, `"0" == false`, `null == undefined`). Strict equality compares without conversion.

```javascript
// Bad
if (quantity == "0") reject();

// Good
if (quantity === 0) reject();
```

**Exceptions:** `value == null` as a deliberate check for both `null` and `undefined`, if the project allows it.
**Source:** [MDN, equality comparisons and sameness](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness)

### JS-MAINT-003: Handle every promise rejection

**Level:** MUST · **Lens:** maintainability

A promise that is neither awaited nor given a `.catch` fails silently in browsers and crashes the process in Node.js 15+. Await it inside `try`, or attach a handler.

```javascript
// Bad
saveDraft(draft);

// Good
saveDraft(draft).catch((error) => showError("Draft not saved", error));
```

**Source:** [MDN, using promises, error handling](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises#error_handling)

### JS-MAINT-004: Use `??` for defaults when `0`, `""` or `false` are valid

**Level:** SHOULD · **Lens:** maintainability

`||` replaces every falsy value, so a real `0` or empty string becomes the default. `??` replaces only `null` and `undefined`.

```javascript
// Bad
const retries = options.retries || 3; // retries: 0 becomes 3

// Good
const retries = options.retries ?? 3;
```

**Exceptions:** when replacing every falsy value is the intent. Switching between `||` and `??` in existing code is a behavior change.
**Source:** [MDN, nullish coalescing operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing)

### JS-MAINT-005: Use ES modules, not globals

**Level:** SHOULD · **Lens:** maintainability

Globals collide across scripts and hide dependencies. Modules declare what they import and export, are strict by default, and enable tree shaking.

```javascript
// Bad
window.formatPrice = (value) => `$${value.toFixed(2)}`;

// Good
export function formatPrice(value) {
  return `$${value.toFixed(2)}`;
}
```

**Exceptions:** legacy code loaded by plain `<script>` tags until it is migrated.
**Source:** [MDN, JavaScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
