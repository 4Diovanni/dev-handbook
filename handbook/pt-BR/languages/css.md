# CSS

Regras de CSS: desempenho, manutenibilidade e acessibilidade. Carregue junto com `core/`; valem também para `.scss`.

- Prefixo das regras: `CSS`
- Formatação e ordem de propriedades ficam com o Prettier ou o Stylelint e não são regras aqui.

## Desempenho

### CSS-PERF-001: Anime `transform` e `opacity`, não propriedades de layout

**Nível:** SHOULD · **Lente:** desempenho

Animar `top`, `left`, `width` ou `height` recalcula o layout e repinta a cada quadro. `transform` e `opacity` podem rodar no compositor, sem layout.

```css
/* Ruim */
.drawer {
  left: -300px;
  transition: left 0.3s;
}
.drawer.open {
  left: 0;
}

/* Bom */
.drawer {
  transform: translateX(-300px);
  transition: transform 0.3s;
}
.drawer.open {
  transform: translateX(0);
}
```

**Fonte:** [web.dev, high-performance CSS animations](https://web.dev/articles/animations-guide)

### CSS-PERF-002: Defina `font-display` nas web fonts

**Nível:** SHOULD · **Lente:** desempenho

Por padrão, o texto pode ficar invisível por até três segundos enquanto a fonte baixa. `font-display: swap` mostra uma fonte reserva na hora e troca quando a fonte chega.

```css
/* Ruim */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter.woff2") format("woff2");
}

/* Bom */
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter.woff2") format("woff2");
  font-display: swap;
}
```

**Exceções:** fontes de ícones, em que um caractere reserva não faz sentido (`block` serve melhor).
**Fonte:** [MDN, font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display)

### CSS-PERF-003: Evite `@import` em arquivos CSS

**Nível:** AVOID · **Lente:** desempenho

O navegador só descobre um `@import` depois de baixar o arquivo que o contém, então as folhas importadas carregam uma depois da outra. Use tags `<link>` ou deixe o bundler juntar os arquivos.

```css
/* Ruim: main.css */
@import url("reset.css");
@import url("layout.css");

/* Bom: bundled at build time, or one <link> per file in the HTML */
```

**Exceções:** `@use` e `@import` do Sass, que são resolvidos no build.
**Fonte:** [MDN, @import](https://developer.mozilla.org/en-US/docs/Web/CSS/@import)

## Manutenibilidade

### CSS-MAINT-001: Nunca remova o contorno de foco sem um substituto visível

**Nível:** MUST · **Lente:** manutenibilidade

Quem navega pelo teclado depende do indicador de foco para saber onde está. `outline: none` sem nada no lugar deixa a página inutilizável para essas pessoas.

```css
/* Ruim */
button:focus {
  outline: none;
}

/* Bom */
button:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 2px;
}
```

**Fonte:** [WCAG 2.2, 2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)

### CSS-MAINT-002: Evite `!important`

**Nível:** AVOID · **Lente:** manutenibilidade

`!important` passa por cima da especificidade normal, então a próxima sobrescrita precisa de outro `!important`, e a cascata deixa de ser previsível. Corrija o seletor ou use cascade layers.

```css
/* Ruim */
.button {
  color: white !important;
}

/* Bom */
@layer base, components;
@layer components {
  .button {
    color: white;
  }
}
```

**Exceções:** classes utilitárias feitas para sempre vencer, e sobrescrever estilos inline de terceiros que você não controla.
**Fonte:** [MDN, @layer](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)

### CSS-MAINT-003: Mantenha seletores curtos e especificidade baixa

**Nível:** SHOULD · **Lente:** manutenibilidade

Seletores de ID e cadeias longas de descendentes são difíceis de sobrescrever e quebram quando a marcação muda. Uma classe por parte do componente mantém a especificidade plana.

```css
/* Ruim */
#sidebar ul li a.active {
  font-weight: bold;
}

/* Bom */
.nav-link--active {
  font-weight: bold;
}
```

**Fonte:** [MDN, especificidade](https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity)

### CSS-MAINT-004: Guarde valores repetidos em custom properties

**Nível:** SHOULD · **Lente:** manutenibilidade

A mesma cor ou espaçamento digitado em vários lugares diverge com o tempo e encarece temas (como o modo escuro). Custom properties dão a cada valor um nome e um lugar único para mudar.

```css
/* Ruim */
.card {
  border: 1px solid #d0d7de;
}
.input {
  border: 1px solid #d0d7de;
}

/* Bom */
:root {
  --color-border: #d0d7de;
}
.card,
.input {
  border: 1px solid var(--color-border);
}
```

**Fonte:** [MDN, usando custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

### CSS-MAINT-005: Dimensione textos em `rem`, não em `px`

**Nível:** SHOULD · **Lente:** manutenibilidade

Texto em `px` ignora o tamanho de fonte que o usuário configurou no navegador. `rem` acompanha essa configuração.

```css
/* Ruim */
body {
  font-size: 14px;
}

/* Bom */
body {
  font-size: 0.875rem;
}
```

**Exceções:** bordas e linhas finas, que devem continuar finas.
**Fonte:** [WCAG 2.2, 1.4.4 Resize Text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)

### CSS-MAINT-006: Respeite `prefers-reduced-motion`

**Nível:** SHOULD · **Lente:** manutenibilidade

Animações grandes ou de parallax podem causar tontura e náusea em pessoas com distúrbios vestibulares. Reduza ou remova movimentos não essenciais quando o usuário pedir.

```css
/* Ruim */
.hero {
  animation: float 3s infinite;
}

/* Bom */
.hero {
  animation: float 3s infinite;
}
@media (prefers-reduced-motion: reduce) {
  .hero {
    animation: none;
  }
}
```

**Fonte:** [MDN, prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
