# dev-handbook

[![CI](https://github.com/4Diovanni/dev-handbook/actions/workflows/ci.yml/badge.svg)](https://github.com/4Diovanni/dev-handbook/actions/workflows/ci.yml)
[![Docs](https://github.com/4Diovanni/dev-handbook/actions/workflows/pages.yml/badge.svg)](https://4diovanni.github.io/dev-handbook/pt-BR/)
[![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-blue.svg)](LICENSE)
[![Conteúdo: CC BY 4.0](https://img.shields.io/badge/conte%C3%BAdo-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

[English](README.md) · **Português**

Um handbook bilíngue de boas práticas de engenharia de software, escrito para ser lido por pessoas e carregado por assistentes de código com IA como um livro de regras.

O handbook em inglês é a fonte da verdade: é curto e econômico em tokens, para que os assistentes possam carregá-lo em todo review. O handbook em português espelha o inglês para leitura humana, e o CI mantém os dois sincronizados.

## Princípios

1. **A análise é de quem desenvolve.** O handbook orienta e os assistentes de IA reportam achados. Nada é refatorado ou reescrito automaticamente.
2. **Desempenho sem mudar comportamento.** Toda sugestão de desempenho mantém o resultado observável do código. O que muda comportamento é marcado como tal.
3. **Três lentes em toda regra:** segurança, desempenho e impacto (custo de adoção, risco, ganho mensurável).
4. **Pequeno e verificável.** Cada regra tem um ID estável, um porquê e um exemplo mínimo ruim / bom.

## Escopo

| Área | Coberto |
| --- | --- |
| Linguagens | Java, Python, JavaScript, TypeScript, HTML, CSS |
| Frameworks | Spring Boot, Flask |
| Práticas | APIs REST, Git, Markdown |
| Transversal | Segurança, desempenho, impacto |
| IA | Agentes e skills do Claude Code que aplicam o handbook |
| Depois | Bibliotecas de cada linguagem, design base |

Fora do escopo de propósito: regras de formatação que os formatters já aplicam, tutoriais de linguagem e opiniões "framework X vs Y". O raciocínio completo está no [ADR 0001](docs/adr/0001-record-phase-0-decisions.md).

## Estrutura do repositório

```text
handbook/
  en/          fonte da verdade, carregada pelos assistentes de IA
  pt-BR/       espelho para leitura humana (mesmos arquivos, mesmos IDs)
.claude/
  agents/      o time de revisão: seis revisores só leitura e um implementador
  skills/      skills que aplicam o handbook (team-review, perf-audit, ...)
  commands/    /review, o ponto de entrada do time
ai/guides/     como usar assistentes de IA com o handbook
examples/      pares ruim / bom executáveis que precisam imprimir o mesmo resultado
design/        reservado para o design base
docs/adr/      registros de decisões de arquitetura deste repositório
scripts/       checagens de paridade, IDs de regra e atribuição
```

## Como é uma regra

```markdown
### PY-PERF-001: Prefira set para testes de pertencimento repetidos

**Nível:** SHOULD · **Lente:** desempenho
```

Os IDs seguem `ESCOPO-LENTE-NNN` e nunca mudam de significado. Veja o [índice do handbook](handbook/pt-BR/index.md) e o [modelo de regra](handbook/pt-BR/_template.md).

## Time de revisão com IA

Abra este repositório no Claude Code e rode `/review`. Um detector de stack escolhe os arquivos do handbook que se aplicam, e revisores de código, segurança, desempenho, APIs REST e frontend rodam em paralelo e devolvem um relatório único, em que cada achado cita o ID de uma regra. Os revisores só leem; o implementador só aplica achados que você aprovar. Veja [o guia de IA](ai/guides/README.md).

## Roadmap

| Fase | Conteúdo | Status |
| --- | --- | --- |
| 0 | Regras e brainstorm de escopo | Concluída |
| 1 | Esqueleto, governança, CI, site de documentação | Concluída |
| 2 | Lentes do núcleo e as seis linguagens, com exemplos executáveis | Concluída |
| 3 | Spring Boot, Flask, REST, Git, Markdown | Planejada |
| 4 | Time de revisão com IA: agentes e skills (base pronta), plugin instalável | Em andamento |
| 5 | Regras de bibliotecas | Planejada |
| 6 | Design base | Planejada |

## Rodar as checagens localmente

```bash
python -m pip install -r requirements-dev.txt
git config core.hooksPath .githooks   # uma vez por clone
make check
```

## Licenças

- Código (scripts, exemplos, agentes, skills): [MIT](LICENSE).
- Texto do handbook e documentação: [CC BY 4.0](LICENSE-CC-BY-4.0). Qualquer pessoa pode copiar, traduzir e adaptar, inclusive comercialmente, desde que dê o crédito à fonte.

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md).
