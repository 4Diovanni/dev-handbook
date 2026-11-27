# Contributing

[Português](#contribuindo-pt-br) below.

## Workflow

1. Open an issue using one of the templates (new rule, correction, new language).
2. Create a short-lived branch from `main`: `type/short-description`, for example `feat/python-perf-rules`.
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/) in English: `feat:`, `fix:`, `docs:`, `ci:`, `chore:`, `test:`.
4. Open a pull request with the template filled in. CI must be green; `main` only takes squash merges.
5. Releases, tags and `CHANGELOG.md` are generated from the commit history.

## Commit hook

Enable the repository hooks once per clone:

```bash
git config core.hooksPath .githooks
```

The `commit-msg` hook rejects AI-assistant attribution (co-author trailers, session links, "generated with" banners). The same check runs in CI on commits, pull request descriptions and tracked files.

## Adding or changing a rule

- Write the rule in `handbook/en/` first, using [the template](handbook/en/_template.md).
- Add the same rule, with the same ID and in the same position, to `handbook/pt-BR/`.
- Rule IDs are permanent. To remove a rule, delete it from both locales and add its ID to `handbook/retired-ids.txt`. Removing a rule or changing its meaning is a breaking change (`feat!:`).
- Never put secrets, tokens or personal data in examples.
- For a performance rule, consider adding a runnable bad / good pair under `examples/` (see [examples/README.md](examples/README.md)).

## Checks

```bash
python -m pip install -r requirements-dev.txt
make check
```

---

## Contribuindo (pt-BR)

1. Abra uma issue com um dos templates (nova regra, correção, nova linguagem).
2. Crie uma branch curta a partir da `main`: `tipo/descricao-curta`, por exemplo `feat/python-perf-rules`.
3. Faça commits em [Conventional Commits](https://www.conventionalcommits.org/pt-br/), em inglês.
4. Abra um PR preenchendo o template. O CI precisa estar verde e a `main` só aceita squash merge.
5. Releases, tags e `CHANGELOG.md` são gerados a partir do histórico de commits.

Ative os hooks uma vez por clone com `git config core.hooksPath .githooks`. O hook `commit-msg` bloqueia atribuição de assistentes de IA, e o CI repete a checagem.

Toda regra nasce em `handbook/en/` e é espelhada em `handbook/pt-BR/` com o mesmo ID e na mesma posição. IDs são permanentes: regra removida vai para `handbook/retired-ids.txt`. Regras de desempenho podem ganhar um par ruim / bom executável em `examples/`.
