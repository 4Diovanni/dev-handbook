# ADR 0001: Scope, structure and governance of the handbook

- Status: accepted
- Date: 2026-11-25

## Context

The repository is a best-practices handbook with two readers: the owner, who reads Portuguese, and AI coding assistants, which load the rules to decide what to flag. It is also a portfolio piece, so the workflow and pipeline are part of the product.

## Decision

### Principles

- The analysis belongs to the developer. Assistants report findings with rule IDs and never refactor on their own.
- Performance suggestions must keep observable behavior unchanged.
- Every rule is judged through security, performance and impact.

### Scope

| Topic | Decision | Reason |
| --- | --- | --- |
| Java, Python, JavaScript, TypeScript, HTML, CSS | In (core) | Daily stack; base for everything else |
| Spring Boot, Flask | In | Real frameworks in use; many security rules live there |
| REST APIs, Git, Markdown | In | Cross-cutting; this repository follows them too |
| Security and performance | In, as lenses per language plus `core/` files | No language is left without the basics |
| Libraries | Later, folder reserved | Filled on demand |
| AI and Claude Code skills | In | Skills are how the handbook is applied |
| Formatting rules | Out; formatter config only | Prettier, Black, Ruff, google-java-format already enforce them |
| Tutorials and basic syntax | Out | The handbook says what and why, not how to learn the language |
| Automatic refactoring by AI | Out | Conflicts with the first principle |
| "X vs Y" comparisons | Out | Opinions age fast; decisions go into ADRs |
| Design foundations | Later (phase 6) | Collected in `design/` first |

### Structure and languages

- English (`handbook/en/`) is the source of truth; `handbook/pt-BR/` mirrors it with the same files and rule IDs.
- Code examples use English identifiers and comments in both locales.
- Rule IDs follow `SCOPE-LENS-NNN`, are permanent, and retired IDs are never reused.

### Governance

- Public repository on GitHub, GitHub Flow, Conventional Commits, squash merges, branch protection on `main`.
- No AI-assistant attribution in commits, pull requests or files, enforced by a hook and by CI.
- Semantic versioning; removing a rule or changing its meaning is a major change.
- Licensing: MIT for code, CC BY 4.0 for handbook text.
- Documentation site on GitHub Pages with MkDocs Material and a language switch.
- Skills are distributed as an installable plugin in phase 4.

## Alternatives considered

| Option | Why not |
| --- | --- |
| Portuguese as the source of truth | Assistants read English with fewer tokens, so English must always be correct |
| One big rules file | Assistants would load every language for every project |
| MIT for everything | MIT is written for software; CC BY 4.0 fits prose and keeps the credit requirement |
| Local-only repository | The repository is meant for the portfolio |

## Consequences

- Every rule change touches two files; CI fails if they drift.
- Assistants load `index.md` plus only the files for the detected stack.
- Phase 2 can start writing rules on top of a validated structure.
