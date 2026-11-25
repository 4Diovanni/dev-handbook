# Handbook index

Load only the files a project needs. Always load `core/`, then add the files for each detected stack.

| Detected in the project | Load |
| --- | --- |
| Any code | `core/security.md`, `core/performance.md`, `core/impact.md` |
| `pom.xml`, `build.gradle`, `*.java` | `languages/java.md` |
| `spring-boot-starter-*` dependency | `languages/java.md`, `frameworks/spring-boot.md`, `practices/rest-api.md` |
| `*.py`, `pyproject.toml`, `requirements*.txt` | `languages/python.md` |
| `flask` dependency | `languages/python.md`, `frameworks/flask.md`, `practices/rest-api.md` |
| `*.js`, `package.json` | `languages/javascript.md` |
| `*.ts`, `tsconfig.json` | `languages/javascript.md`, `languages/typescript.md` |
| `*.html` | `languages/html.md` |
| `*.css`, `*.scss` | `languages/css.md` |
| Commits, branches, PRs | `practices/git.md` |
| `*.md` | `practices/markdown.md` |

## Rule format

See `_template.md`. Every rule heading starts with a stable ID: `SCOPE-LENS-NNN`.

| Part | Values |
| --- | --- |
| Scope | `CORE`, `JAVA`, `PY`, `JS`, `TS`, `HTML`, `CSS`, `SPRING`, `FLASK`, `REST`, `GIT`, `MD`, `LIB` |
| Lens | `SEC` security, `PERF` performance, `MAINT` maintainability, `IMPACT` adoption cost and risk |
| Level | `MUST` always flag, `SHOULD` flag with context, `AVOID` flag the anti-pattern |

## How to apply rules

- Report findings. Never edit, refactor or rewrite code unless the user explicitly asks.
- Cite the rule ID for every finding.
- Performance suggestions must keep observable behavior unchanged. If a fix changes behavior, label it "behavior change".
- Sort findings by level: `MUST`, then `SHOULD`, then `AVOID`.
