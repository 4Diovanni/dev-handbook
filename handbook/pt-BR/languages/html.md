# HTML

Regras de HTML: segurança, desempenho, semântica e acessibilidade. Carregue junto com `core/`.

- Prefixo das regras: `HTML`
- As regras de acessibilidade usam a lente de manutenibilidade e seguem a WCAG 2.2.

## Segurança

### HTML-SEC-001: Libere scripts por uma Content Security Policy, não com código inline

**Nível:** SHOULD · **Lente:** segurança

Blocos `<script>` inline e atributos `onclick` só rodam se a política liberar código inline, e isso também deixa rodar marcação injetada. Mova o código para arquivos e envie uma CSP com as origens permitidas.

```html
<!-- Ruim -->
<button onclick="deleteItem(42)">Delete</button>

<!-- Bom: Content-Security-Policy: script-src 'self' -->
<button type="button" data-item-id="42" class="js-delete">Delete</button>
<script src="/js/items.js" defer></script>
```

**Exceções:** scripts inline liberados por um nonce ou hash por resposta.
**Fonte:** [MDN, Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

### HTML-SEC-002: Use `rel="noopener noreferrer"` em links que abrem sites não confiáveis numa nova aba

**Nível:** SHOULD · **Lente:** segurança

Uma página aberta com `target="_blank"` podia controlar a página de origem por `window.opener` em navegadores antigos, e recebe a URL completa de referência. `noopener` e `noreferrer` cortam as duas coisas.

```html
<!-- Ruim -->
<a href="https://other.example" target="_blank">Partner</a>

<!-- Bom -->
<a href="https://other.example" target="_blank" rel="noopener noreferrer">Partner</a>
```

**Exceções:** links para a sua própria origem que precisam do referrer.
**Fonte:** [MDN, rel=noopener](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel/noopener)

### HTML-SEC-003: Use Subresource Integrity em scripts e estilos vindos de CDN

**Nível:** SHOULD · **Lente:** segurança

Se uma CDN for comprometida, todo site que carrega dela roda o código do atacante. O hash em `integrity` faz o navegador recusar um arquivo que mudou.

```html
<!-- Ruim -->
<script src="https://cdn.example.com/lib@1.2.3/lib.min.js"></script>

<!-- Bom -->
<script
  src="https://cdn.example.com/lib@1.2.3/lib.min.js"
  integrity="sha384-REPLACE_WITH_THE_FILE_HASH"
  crossorigin="anonymous"
></script>
```

**Exceções:** arquivos servidos pela sua própria origem.
**Fonte:** [MDN, Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)

## Desempenho

### HTML-PERF-001: Carregue scripts com `defer` ou `type="module"`

**Nível:** SHOULD · **Lente:** desempenho

Um `<script src>` simples no `<head>` para a leitura do HTML até o arquivo baixar e rodar. `defer` e módulos baixam em paralelo e rodam depois da leitura, na ordem.

```html
<!-- Ruim -->
<head>
  <script src="/js/app.js"></script>
</head>

<!-- Bom -->
<head>
  <script src="/js/app.js" defer></script>
</head>
```

**Exceções:** scripts pequenos que precisam rodar antes da primeira pintura (por exemplo, definir o tema de cores).
**Fonte:** [MDN, elemento script, atributo defer](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#defer)

### HTML-PERF-002: Defina `width` e `height` em imagens e vídeos

**Nível:** SHOULD · **Lente:** desempenho

Sem dimensões, o navegador não sabe quanto espaço reservar, e o conteúdo pula quando a mídia carrega (Cumulative Layout Shift). Os atributos definem a proporção; o CSS ainda pode deixar a imagem responsiva.

```html
<!-- Ruim -->
<img src="/img/team.jpg" alt="The team at the 2026 meetup">

<!-- Bom -->
<img src="/img/team.jpg" alt="The team at the 2026 meetup" width="1200" height="800">
```

**Fonte:** [web.dev, optimize Cumulative Layout Shift](https://web.dev/articles/optimize-cls)

### HTML-PERF-003: Use lazy loading em imagens fora da tela, mas nunca na imagem principal

**Nível:** SHOULD · **Lente:** desempenho

`loading="lazy"` adia as imagens abaixo da dobra até o usuário rolar perto delas. Na maior imagem da primeira tela, ele atrasa o Largest Contentful Paint.

```html
<!-- Ruim -->
<img src="/img/hero.jpg" alt="Product overview" width="1600" height="900" loading="lazy">

<!-- Bom -->
<img src="/img/hero.jpg" alt="Product overview" width="1600" height="900" fetchpriority="high">
<img src="/img/footer-map.png" alt="Office location" width="600" height="400" loading="lazy">
```

**Fonte:** [web.dev, browser-level image lazy loading](https://web.dev/articles/browser-level-image-lazy-loading)

## Manutenibilidade

### HTML-MAINT-001: Declare o idioma da página em `<html>`

**Nível:** MUST · **Lente:** manutenibilidade

Leitores de tela escolhem a pronúncia pelo `lang`, e os navegadores o usam para tradução, hifenização e corretor ortográfico.

```html
<!-- Ruim -->
<html>

<!-- Bom -->
<html lang="pt-BR">
```

**Fonte:** [WCAG 2.2, 3.1.1 Language of Page](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html)

### HTML-MAINT-002: Dê um texto alternativo a toda imagem com significado

**Nível:** MUST · **Lente:** manutenibilidade

Leitores de tela leem o `alt` no lugar da imagem, e ele aparece quando a imagem não carrega. Descreva o que a imagem transmite; use `alt=""` em imagens decorativas para que sejam puladas.

```html
<!-- Ruim -->
<img src="/img/chart-q3.png">

<!-- Bom -->
<img src="/img/chart-q3.png" alt="Sales grew 18% in Q3, led by the south region">
<img src="/img/divider.svg" alt="">
```

**Fonte:** [WCAG 2.2, 1.1.1 Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

### HTML-MAINT-003: Use `<button>` para ações e `<a>` para navegação

**Nível:** MUST · **Lente:** manutenibilidade

Uma `<div>` com handler de clique não recebe foco, não é ativada pelo teclado e não é anunciada como controle. Os elementos nativos fazem isso de graça.

```html
<!-- Ruim -->
<div class="btn" onclick="save()">Save</div>

<!-- Bom -->
<button type="button" class="btn" id="save">Save</button>
```

**Fonte:** [MDN, acessibilidade do elemento button](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#accessibility)

### HTML-MAINT-004: Dê um rótulo a todo campo de formulário

**Nível:** MUST · **Lente:** manutenibilidade

O placeholder some enquanto a pessoa digita e não é um nome confiável para tecnologias assistivas. Um `<label>` ligado ao campo dá o nome e aumenta a área de clique.

```html
<!-- Ruim -->
<input type="email" placeholder="Email">

<!-- Bom -->
<label for="email">Email</label>
<input id="email" name="email" type="email" autocomplete="email">
```

**Fonte:** [Tutoriais WAI, rotulando controles](https://www.w3.org/WAI/tutorials/forms/labels/)

### HTML-MAINT-005: Estruture as páginas com landmarks e títulos em ordem

**Nível:** SHOULD · **Lente:** manutenibilidade

`<header>`, `<nav>`, `<main>` e `<footer>`, mais títulos que não pulam níveis, deixam quem usa leitor de tela navegar pela página e tornam a marcação legível.

```html
<!-- Ruim -->
<div class="header">...</div>
<div class="content">
  <div class="title">Orders</div>
  <h4>Pending</h4>
</div>

<!-- Bom -->
<header>...</header>
<main>
  <h1>Orders</h1>
  <h2>Pending</h2>
</main>
```

**Fonte:** [Tutoriais WAI, estrutura de página](https://www.w3.org/WAI/tutorials/page-structure/)
