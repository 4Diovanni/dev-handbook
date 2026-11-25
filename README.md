# dev-handbook

[![CI](https://github.com/4Diovanni/dev-handbook/actions/workflows/ci.yml/badge.svg)](https://github.com/4Diovanni/dev-handbook/actions/workflows/ci.yml)
[![Docs](https://github.com/4Diovanni/dev-handbook/actions/workflows/pages.yml/badge.svg)](https://4diovanni.github.io/dev-handbook/)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

**English** · [Português](README.pt-BR.md)

A bilingual handbook of software engineering best practices, written to be read by people and loaded by AI coding assistants as a rulebook.

The English handbook is the source of truth: it is short and token-efficient, so assistants can load it on every review. The Brazilian Portuguese handbook mirrors it for human reading, and CI keeps both in sync.

## Principles

1. **The analysis belongs to the developer.** The handbook guides and AI assistants report findings. Nothing is refactored or rewritten automatically.
2. **Performance without behavior changes.** Every performance suggestion keeps the observable result of the code intact. Anything that changes behavior is flagged as such.
3. **Three lenses on every rule:** security, performance and impact (adoption cost, risk, measurable gain).
4. **Small and verifiable.** Each rule has a stable ID, a reason and a minimal bad / good example.

## Scope

| Area | Covered |
| --- | --- |
| Languages | Java, Python, JavaScript, TypeScript, HTML, CSS |
| Frameworks | Spring Boot, Flask |
| Practices | REST APIs, Git, Markdown |
| Cross-cutting | Security, performance, impact |
| AI | Claude Code skills that apply the handbook |
| Later | Per-language libraries, design foundations |

Out of scope on purpose: formatting rules that formatters already enforce, language tutorials, and "framework X vs Y" opinions. The full reasoning is in [ADR 0001](docs/adr/0001-record-phase-0-decisions.md).

## Repository layout

```text
handbook/
  en/          source of truth, loaded by AI assistants
  pt-BR/       mirror for human reading (same files, same rule IDs)
ai/
  skills/      Claude Code skills that apply the handbook
  guides/      how to use AI assistants with the handbook
examples/      runnable bad / good code, tested in CI
design/        reserved for design foundations
docs/adr/      architecture decision records for this repository
scripts/       parity, rule ID and attribution checks
```

## How a rule looks

```markdown
### PY-PERF-001: Prefer a set for repeated membership tests

**Level:** SHOULD · **Lens:** performance
```

IDs follow `SCOPE-LENS-NNN` and never change meaning. See the [handbook index](handbook/en/index.md) and the [rule template](handbook/en/_template.md).

## Roadmap

| Phase | Content | Status |
| --- | --- | --- |
| 0 | Rules and scope brainstorm | Done |
| 1 | Skeleton, governance, CI, docs site | In progress |
| 2 | Core lenses and the six languages, with runnable examples | Planned |
| 3 | Spring Boot, Flask, REST, Git, Markdown | Planned |
| 4 | AI skills, usage guides, installable plugin | Planned |
| 5 | Library rules | Planned |
| 6 | Design foundations | Planned |

## Run the checks locally

```bash
python -m pip install -r requirements-dev.txt
git config core.hooksPath .githooks   # once per clone
make check
```

## Licensing

- Code (scripts, examples, skills): [MIT](LICENSE).
- Handbook text and documentation: [CC BY 4.0](LICENSE-CC-BY-4.0). You can copy, translate and adapt it, including commercially, as long as you credit the source.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
