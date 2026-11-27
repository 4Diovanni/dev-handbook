# TypeScript

TypeScript rules on top of the JavaScript ones (strict mode). Load together with `core/` and `javascript.md`.

- Rule prefix: `TS`
- Formatting is left to Prettier and is not a rule here.

## Security

### TS-SEC-001: Validate external data at runtime; types are erased

**Level:** MUST · **Lens:** security

Types disappear at compile time, so `as User` on a response or request body checks nothing. Parse untrusted data with a schema or a type guard before treating it as a typed value.

```typescript
// Bad
const user = (await response.json()) as User;

// Good
const UserSchema = z.object({ id: z.number(), email: z.string().email() });
const user = UserSchema.parse(await response.json()); // throws on bad data
```

**Source:** [TypeScript handbook, type assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)

## Performance

### TS-PERF-001: Use `import type` for imports used only as types

**Level:** SHOULD · **Lens:** performance

A plain import of a module used only for types can be kept in the output under some compiler settings, loading the module and running its side effects at runtime. `import type` is always erased.

```typescript
// Bad
import { User } from "./models";

// Good
import type { User } from "./models";
```

**Source:** [TypeScript docs, verbatimModuleSyntax](https://www.typescriptlang.org/tsconfig/#verbatimModuleSyntax)

## Maintainability

### TS-MAINT-001: Enable `strict` in `tsconfig.json`

**Level:** MUST · **Lens:** maintainability

Without `strict`, `null` and `undefined` fit every type and implicit `any` is allowed, so the compiler misses the bugs TypeScript exists to catch.

```jsonc
// Bad
{ "compilerOptions": { "target": "ES2022" } }

// Good
{ "compilerOptions": { "target": "ES2022", "strict": true } }
```

**Exceptions:** migrations of large JavaScript code bases, enabling the strict flags one at a time.
**Source:** [TypeScript docs, strict](https://www.typescriptlang.org/tsconfig/#strict)

### TS-MAINT-002: Use `unknown` instead of `any`

**Level:** MUST · **Lens:** maintainability

`any` turns off type checking for the value and everything it touches. `unknown` accepts any value but forces a check before use.

```typescript
// Bad
function parse(raw: string): any {
  return JSON.parse(raw);
}

// Good
function parse(raw: string): unknown {
  return JSON.parse(raw);
}
```

**Exceptions:** typing third-party code with no declarations, isolated in one place.
**Source:** [TypeScript handbook, unknown](https://www.typescriptlang.org/docs/handbook/2/functions.html#unknown)

### TS-MAINT-003: Avoid the non-null assertion `!`

**Level:** SHOULD · **Lens:** maintainability

`value!` tells the compiler a value is never `null` without checking it, so a wrong assumption becomes a runtime `TypeError`. Narrow with a check instead.

```typescript
// Bad
const button = document.querySelector("#save")!;

// Good
const button = document.querySelector("#save");
if (!button) throw new Error("#save not found");
```

**Exceptions:** values the compiler cannot follow but that are guaranteed, with a comment saying why.
**Source:** [TypeScript handbook, non-null assertion operator](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#non-null-assertion-operator-postfix-)

### TS-MAINT-004: Model variants as discriminated unions with an exhaustive check

**Level:** SHOULD · **Lens:** maintainability

Optional fields for every variant allow impossible combinations. A union with a `kind` tag lets the compiler narrow each case, and a `never` check fails the build when a new variant is not handled.

```typescript
// Bad
type Shape = { kind: string; radius?: number; side?: number };

// Good
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

**Source:** [TypeScript handbook, discriminated unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)

### TS-MAINT-005: Mark data that should not change as `readonly`

**Level:** SHOULD · **Lens:** maintainability

`readonly` properties and `ReadonlyArray` make accidental mutation a compile error and document that a function does not modify its input.

```typescript
// Bad
function total(items: Item[]): number {
  items.sort((a, b) => a.price - b.price); // mutates the caller's array
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Good
function total(items: readonly Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Source:** [TypeScript handbook, readonly properties](https://www.typescriptlang.org/docs/handbook/2/objects.html#readonly-properties)
