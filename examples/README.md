# Examples

Runnable bad / good pairs for handbook rules. Each pair shows that the good version keeps the result of the bad one, which is the first principle of every performance suggestion (`CORE-IMPACT-001`).

[Português](#exemplos-pt-br) below.

## Layout

```text
examples/
  python/<RULE-ID>/bad.py, good.py
  java/<RULE-ID>/Bad.java, Good.java
  javascript/<RULE-ID>/bad.mjs, good.mjs
```

Each file is a complete program with deterministic input that prints its result.

## What CI checks

`scripts/check_examples.py` runs in the "Examples" job and in `make check`. A pair passes when:

1. the folder name is a rule ID declared in `handbook/en/`;
2. both programs run and exit with status 0 (Java compiles with `-Xlint:all -Werror`; Python is linted by Ruff);
3. both print the same, non-empty output.

The check proves equivalence, not speed. To compare speed, time both files on your machine, for example `python -m timeit` or `hyperfine "python bad.py" "python good.py"`.

## Available pairs

| Language | Rules |
| --- | --- |
| Python | `CORE-PERF-002`, `CORE-PERF-003`, `PY-PERF-001` to `PY-PERF-005` |
| Java | `JAVA-PERF-001` to `JAVA-PERF-005` |
| JavaScript | `JS-PERF-001`, `JS-PERF-003` |

## Adding a pair

1. Create `examples/<language>/<RULE-ID>/` with the two files.
2. Start each file with a one-line comment naming the rule and whether it is the bad or the good version.
3. Keep the input deterministic and small enough to run in a few seconds.
4. Run `python3 scripts/check_examples.py` (needs Python 3.11+, Java 21 and Node.js 22).

Rules whose good version changes behavior on purpose (security fixes, bug fixes) do not get a pair here.

---

## Exemplos (pt-BR)

Pares ruim / bom executáveis das regras do handbook. Cada par mostra que a versão boa mantém o resultado da ruim, que é o primeiro princípio de toda sugestão de desempenho (`CORE-IMPACT-001`).

- Estrutura: uma pasta por ID de regra dentro da pasta da linguagem, com `bad` e `good` (em Java, `Bad.java` e `Good.java`).
- O CI roda `scripts/check_examples.py` no job "Examples" e no `make check`. O par passa quando o ID existe no handbook, os dois programas rodam sem erro (Java compila com `-Xlint:all -Werror`) e imprimem a mesma saída, que não pode ser vazia.
- A checagem prova equivalência, não velocidade. Para comparar velocidade, meça os dois arquivos na sua máquina.
- Regras cuja versão boa muda o comportamento de propósito (correções de segurança ou de bug) não ganham par aqui.
