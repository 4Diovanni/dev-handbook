# Índice do handbook

Carregue só os arquivos que o projeto precisa. Sempre carregue `core/` e depois os arquivos de cada stack detectada.

| Detectado no projeto | Carregar |
| --- | --- |
| Qualquer código | `core/security.md`, `core/performance.md`, `core/impact.md` |
| `pom.xml`, `build.gradle`, `*.java` | `languages/java.md` |
| Dependência `spring-boot-starter-*` | `languages/java.md`, `frameworks/spring-boot.md`, `practices/rest-api.md` |
| `*.py`, `pyproject.toml`, `requirements*.txt` | `languages/python.md` |
| Dependência `flask` | `languages/python.md`, `frameworks/flask.md`, `practices/rest-api.md` |
| `*.js`, `package.json` | `languages/javascript.md` |
| `*.ts`, `tsconfig.json` | `languages/javascript.md`, `languages/typescript.md` |
| `*.html` | `languages/html.md` |
| `*.css`, `*.scss` | `languages/css.md` |
| Commits, branches, PRs | `practices/git.md` |
| `*.md` | `practices/markdown.md` |

## Formato das regras

Veja `_template.md`. Todo título de regra começa com um ID estável: `ESCOPO-LENTE-NNN`.

| Parte | Valores |
| --- | --- |
| Escopo | `CORE`, `JAVA`, `PY`, `JS`, `TS`, `HTML`, `CSS`, `SPRING`, `FLASK`, `REST`, `GIT`, `MD`, `LIB` |
| Lente | `SEC` segurança, `PERF` desempenho, `MAINT` manutenção, `IMPACT` custo de adoção e risco |
| Nível | `MUST` sempre apontar, `SHOULD` apontar com contexto, `AVOID` apontar o antipadrão |

## Como aplicar as regras

- Reporte os achados. Nunca edite, refatore ou reescreva código, a menos que o usuário peça explicitamente.
- Cite o ID da regra em cada achado.
- Sugestões de desempenho precisam manter o comportamento observável. Se a correção muda comportamento, marque como "mudança de comportamento".
- Ordene os achados por nível: `MUST`, depois `SHOULD`, depois `AVOID`.
