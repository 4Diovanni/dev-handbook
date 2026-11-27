# JavaScript

Regras de JavaScript para navegador e Node.js (ES2022+). Carregue junto com `core/`; projetos TypeScript também carregam `typescript.md`.

- Prefixo das regras: `JS`
- Formatação fica com o Prettier e não é regra aqui.

## Segurança

### JS-SEC-001: Nunca coloque dados não confiáveis em `innerHTML`

**Nível:** MUST · **Lente:** segurança

`innerHTML`, `outerHTML`, `insertAdjacentHTML` e `document.write` interpretam a entrada como HTML, então um valor com `<img onerror=...>` executa script (XSS). Use `textContent` ou monte os nós com a API do DOM.

```javascript
// Ruim
comment.innerHTML = `<p>${userText}</p>`;

// Bom
const p = document.createElement("p");
p.textContent = userText;
comment.replaceChildren(p);
```

**Exceções:** HTML que precisa ser renderizado passa antes por um sanitizador como o DOMPurify.
**Fonte:** [OWASP DOM-based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)

### JS-SEC-002: Nunca execute strings como código

**Nível:** MUST · **Lente:** segurança

`eval`, `new Function` e strings passadas para `setTimeout` / `setInterval` executam qualquer texto que recebem. Leia dados com `JSON.parse` e passe funções, não strings.

```javascript
// Ruim
const settings = eval(`(${response})`);
setTimeout("refresh()", 1000);

// Bom
const settings = JSON.parse(response);
setTimeout(refresh, 1000);
```

**Fonte:** [MDN, nunca use eval()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval#never_use_direct_eval!)

### JS-SEC-003: Não mescle objetos não confiáveis em objetos comuns sem filtrar as chaves

**Nível:** MUST · **Lente:** segurança

Uma chave como `__proto__` ou `constructor` num JSON recebido pode alterar o `Object.prototype` durante um merge profundo, afetando todos os objetos do processo (prototype pollution). Copie só as chaves conhecidas, ou use `Map` para chaves arbitrárias.

```javascript
// Ruim
function merge(target, source) {
  for (const key in source) {
    if (typeof source[key] === "object") merge((target[key] ??= {}), source[key]);
    else target[key] = source[key];
  }
}
merge(config, JSON.parse(body));

// Bom
const { theme, language } = JSON.parse(body);
Object.assign(config, { theme, language });
```

**Fonte:** [OWASP Prototype Pollution Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html)

### JS-SEC-004: Use a Web Crypto API, não `Math.random`, para tokens

**Nível:** MUST · **Lente:** segurança

`Math.random` não é criptograficamente seguro e sua saída pode ser prevista. `crypto.randomUUID` e `crypto.getRandomValues` existem no navegador e no Node.js.

```javascript
// Ruim
const token = Math.random().toString(36).slice(2);

// Bom
const token = crypto.randomUUID();
```

**Exceções:** usos sem relação com segurança, como animações ou embaralhar dados de demonstração.
**Fonte:** [MDN, Crypto.getRandomValues()](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/getRandomValues)

### JS-SEC-005: No Node.js, rode processos com `execFile` ou `spawn`, não com `exec`

**Nível:** MUST · **Lente:** segurança

`child_process.exec` passa a string por um shell, então `;` ou `$()` na entrada executam comandos extras. `execFile` e `spawn` recebem um array de argumentos e, por padrão, não usam shell.

```javascript
// Ruim
exec(`convert ${fileName} out.png`);

// Bom
execFile("convert", [fileName, "out.png"]);
```

**Exceções:** comandos fixos, sem nenhuma entrada externa.
**Fonte:** [Documentação do Node.js, child_process](https://nodejs.org/api/child_process.html#child_processexecfilefile-args-options-callback)

### JS-SEC-006: Confira a origem de todo evento `message`

**Nível:** MUST · **Lente:** segurança

Qualquer janela pode fazer `postMessage` para a sua. Sem checar a origem, uma página maliciosa pode mandar comandos em que o seu handler confia.

```javascript
// Ruim
window.addEventListener("message", (event) => {
  applySettings(event.data);
});

// Bom
window.addEventListener("message", (event) => {
  if (event.origin !== "https://app.example.com") return;
  applySettings(event.data);
});
```

**Fonte:** [MDN, Window.postMessage(), questões de segurança](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage#security_concerns)

## Desempenho

### JS-PERF-001: Rode chamadas assíncronas independentes em paralelo

**Nível:** SHOULD · **Lente:** desempenho

`await` dentro de um laço espera cada chamada terminar antes de começar a próxima, então o tempo total é a soma de todas. `Promise.all` começa todas juntas, e o tempo total fica perto do da mais lenta.

```javascript
// Ruim
const users = [];
for (const id of ids) {
  users.push(await fetchUser(id));
}

// Bom
const users = await Promise.all(ids.map((id) => fetchUser(id)));
```

**Exceções:** chamadas que dependem umas das outras, precisam de ordem ou sobrecarregariam o servidor; limite a concorrência em listas grandes. Rodar em paralelo muda a ordem dos efeitos colaterais, o que é mudança de comportamento quando a ordem importa.
**Fonte:** [MDN, Promise.all()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)

### JS-PERF-002: Agrupe as leituras do DOM antes das escritas

**Nível:** SHOULD · **Lente:** desempenho

Ler o layout (`offsetHeight`, `getBoundingClientRect`) logo depois de mudar um estilo obriga o navegador a recalcular o layout na hora. Alternar leituras e escritas num laço faz isso a cada volta (layout thrashing).

```javascript
// Ruim
for (const box of boxes) {
  box.style.width = `${box.parentElement.offsetWidth / 2}px`;
}

// Bom
const widths = boxes.map((box) => box.parentElement.offsetWidth);
boxes.forEach((box, i) => {
  box.style.width = `${widths[i] / 2}px`;
});
```

**Fonte:** [web.dev, avoid large, complex layouts and layout thrashing](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing)

### JS-PERF-003: Use `Set` e `Map` para buscas repetidas

**Nível:** SHOULD · **Lente:** desempenho

`array.includes` e `array.find` percorrem o array, O(n) cada. Dentro de um laço isso vira O(n·m); `Set.has` e `Map.get` são O(1) em média.

```javascript
// Ruim
const active = orders.filter((o) => activeIds.includes(o.customerId));

// Bom
const activeSet = new Set(activeIds);
const active = orders.filter((o) => activeSet.has(o.customerId));
```

**Exceções:** arrays com poucos itens.
**Fonte:** [MDN, Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)

### JS-PERF-004: Use throttle ou debounce em eventos de alta frequência

**Nível:** SHOULD · **Lente:** desempenho

`scroll`, `resize`, `pointermove` e `input` podem disparar dezenas de vezes por segundo. Trabalho pesado em cada evento trava a thread principal; marque listeners de scroll e toque como `passive` e use debounce no trabalho caro.

```javascript
// Ruim
input.addEventListener("input", () => search(input.value));

// Bom
let timer;
input.addEventListener("input", () => {
  clearTimeout(timer);
  timer = setTimeout(() => search(input.value), 300);
});
```

**Exceções:** handlers baratos. O debounce atrasa o trabalho, o que é uma mudança de comportamento visível; combine o atraso.
**Fonte:** [MDN, EventTarget.addEventListener(), listeners passivos](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener#using_passive_listeners)

### JS-PERF-005: Remova listeners e timers quando o dono deixa de existir

**Nível:** SHOULD · **Lente:** desempenho

Listeners em `window` ou `document` e intervals ativos mantêm vivas as suas closures, e tudo o que elas referenciam, depois que o componente é removido. Limpe-os, por exemplo com um único `AbortController`.

```javascript
// Ruim
function mount(widget) {
  window.addEventListener("resize", () => widget.layout());
}

// Bom
function mount(widget) {
  const controller = new AbortController();
  window.addEventListener("resize", () => widget.layout(), { signal: controller.signal });
  return () => controller.abort(); // call on unmount
}
```

**Fonte:** [MDN, opção signal do addEventListener()](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener#signal)

## Manutenibilidade

### JS-MAINT-001: Use `const` e `let`, nunca `var`

**Nível:** MUST · **Lente:** manutenibilidade

`var` tem escopo de função e sofre hoisting, então vaza para fora de blocos e pode ser usado antes da própria linha. `const` indica um vínculo que nunca muda; use `let` só quando ele muda.

```javascript
// Ruim
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i)); // 3, 3, 3
}

// Bom
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i)); // 0, 1, 2
}
```

**Fonte:** [MDN, let](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let)

### JS-MAINT-002: Use `===` e `!==`

**Nível:** MUST · **Lente:** manutenibilidade

`==` converte tipos com regras surpreendentes (`"" == 0`, `"0" == false`, `null == undefined`). A igualdade estrita compara sem conversão.

```javascript
// Ruim
if (quantity == "0") reject();

// Bom
if (quantity === 0) reject();
```

**Exceções:** `value == null` como checagem proposital de `null` e `undefined` juntos, se o projeto permitir.
**Fonte:** [MDN, comparações de igualdade](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness)

### JS-MAINT-003: Trate toda rejeição de promise

**Nível:** MUST · **Lente:** manutenibilidade

Uma promise sem `await` e sem `.catch` falha em silêncio no navegador e derruba o processo no Node.js 15+. Use `await` dentro de `try`, ou anexe um handler.

```javascript
// Ruim
saveDraft(draft);

// Bom
saveDraft(draft).catch((error) => showError("Draft not saved", error));
```

**Fonte:** [MDN, usando promises, tratamento de erros](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises#error_handling)

### JS-MAINT-004: Use `??` para valores padrão quando `0`, `""` ou `false` são válidos

**Nível:** SHOULD · **Lente:** manutenibilidade

`||` substitui qualquer valor falsy, então um `0` ou uma string vazia de verdade vira o padrão. `??` substitui só `null` e `undefined`.

```javascript
// Ruim
const retries = options.retries || 3; // retries: 0 becomes 3

// Bom
const retries = options.retries ?? 3;
```

**Exceções:** quando substituir todo valor falsy é a intenção. Trocar `||` por `??` em código existente é mudança de comportamento.
**Fonte:** [MDN, operador de coalescência nula](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing)

### JS-MAINT-005: Use ES modules, não variáveis globais

**Nível:** SHOULD · **Lente:** manutenibilidade

Globais colidem entre scripts e escondem dependências. Módulos declaram o que importam e exportam, são strict por padrão e permitem tree shaking.

```javascript
// Ruim
window.formatPrice = (value) => `$${value.toFixed(2)}`;

// Bom
export function formatPrice(value) {
  return `$${value.toFixed(2)}`;
}
```

**Exceções:** código legado carregado por tags `<script>` simples, até ser migrado.
**Fonte:** [MDN, módulos JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
