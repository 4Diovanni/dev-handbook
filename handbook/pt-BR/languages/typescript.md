# TypeScript

Regras de TypeScript além das de JavaScript (modo strict). Carregue junto com `core/` e `javascript.md`.

- Prefixo das regras: `TS`
- Formatação fica com o Prettier e não é regra aqui.

## Segurança

### TS-SEC-001: Valide dados externos em tempo de execução; os tipos somem

**Nível:** MUST · **Lente:** segurança

Os tipos desaparecem na compilação, então `as User` sobre uma resposta ou um corpo de requisição não confere nada. Valide dados não confiáveis com um schema ou um type guard antes de tratá-los como valor tipado.

```typescript
// Ruim
const user = (await response.json()) as User;

// Bom
const UserSchema = z.object({ id: z.number(), email: z.string().email() });
const user = UserSchema.parse(await response.json()); // throws on bad data
```

**Fonte:** [Handbook do TypeScript, type assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)

## Desempenho

### TS-PERF-001: Use `import type` para imports usados só como tipo

**Nível:** SHOULD · **Lente:** desempenho

Um import comum de um módulo usado só por tipos pode ficar na saída em algumas configurações do compilador, carregando o módulo e rodando seus efeitos colaterais em tempo de execução. `import type` é sempre apagado.

```typescript
// Ruim
import { User } from "./models";

// Bom
import type { User } from "./models";
```

**Fonte:** [Documentação do TypeScript, verbatimModuleSyntax](https://www.typescriptlang.org/tsconfig/#verbatimModuleSyntax)

## Manutenibilidade

### TS-MAINT-001: Ative `strict` no `tsconfig.json`

**Nível:** MUST · **Lente:** manutenibilidade

Sem `strict`, `null` e `undefined` cabem em qualquer tipo e `any` implícito é permitido, então o compilador deixa passar exatamente os bugs que o TypeScript existe para pegar.

```jsonc
// Ruim
{ "compilerOptions": { "target": "ES2022" } }

// Bom
{ "compilerOptions": { "target": "ES2022", "strict": true } }
```

**Exceções:** migrações de bases grandes de JavaScript, ativando as flags do strict uma de cada vez.
**Fonte:** [Documentação do TypeScript, strict](https://www.typescriptlang.org/tsconfig/#strict)

### TS-MAINT-002: Use `unknown` em vez de `any`

**Nível:** MUST · **Lente:** manutenibilidade

`any` desliga a checagem de tipos para o valor e para tudo o que ele toca. `unknown` aceita qualquer valor, mas obriga uma checagem antes do uso.

```typescript
// Ruim
function parse(raw: string): any {
  return JSON.parse(raw);
}

// Bom
function parse(raw: string): unknown {
  return JSON.parse(raw);
}
```

**Exceções:** tipagem de código de terceiros sem declarações, isolada num único lugar.
**Fonte:** [Handbook do TypeScript, unknown](https://www.typescriptlang.org/docs/handbook/2/functions.html#unknown)

### TS-MAINT-003: Evite a asserção de não nulo `!`

**Nível:** SHOULD · **Lente:** manutenibilidade

`value!` diz ao compilador que o valor nunca é `null` sem conferir, então uma suposição errada vira um `TypeError` em tempo de execução. Faça o narrowing com uma checagem.

```typescript
// Ruim
const button = document.querySelector("#save")!;

// Bom
const button = document.querySelector("#save");
if (!button) throw new Error("#save not found");
```

**Exceções:** valores que o compilador não consegue acompanhar mas que são garantidos, com um comentário explicando por quê.
**Fonte:** [Handbook do TypeScript, operador de asserção de não nulo](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#non-null-assertion-operator-postfix-)

### TS-MAINT-004: Modele variantes como uniões discriminadas com checagem exaustiva

**Nível:** SHOULD · **Lente:** manutenibilidade

Campos opcionais para cada variante permitem combinações impossíveis. Uma união com uma tag `kind` deixa o compilador estreitar cada caso, e uma checagem com `never` quebra o build quando uma variante nova não é tratada.

```typescript
// Ruim
type Shape = { kind: string; radius?: number; side?: number };

// Bom
type Shape = { kind: "circle"; radius: number } | { kind: "square"; side: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    default: {
      const unreachable: never = shape;
      throw new Error(`unknown shape ${unreachable}`);
    }
  }
}
```

**Fonte:** [Handbook do TypeScript, discriminated unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)

### TS-MAINT-005: Marque como `readonly` os dados que não devem mudar

**Nível:** SHOULD · **Lente:** manutenibilidade

Propriedades `readonly` e `ReadonlyArray` transformam mutação acidental em erro de compilação e documentam que a função não altera a entrada.

```typescript
// Ruim
function total(items: Item[]): number {
  items.sort((a, b) => a.price - b.price); // mutates the caller's array
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Bom
function total(items: readonly Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Fonte:** [Handbook do TypeScript, propriedades readonly](https://www.typescriptlang.org/docs/handbook/2/objects.html#readonly-properties)
