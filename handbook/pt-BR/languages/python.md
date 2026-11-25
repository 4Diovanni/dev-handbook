# Python

Regras da linguagem Python (base: Python 3.11+). Carregue junto com `core/`.

- Prefixo das regras: `PY`
- Formatação e ordem de imports ficam com o Ruff e não são regras aqui.

## Segurança

### PY-SEC-001: Use queries parametrizadas, nunca f-strings ou `%` no SQL

**Nível:** MUST · **Lente:** segurança

Formatar a string coloca a entrada dentro do texto SQL, e um valor malicioso pode mudar a query. Drivers DB-API recebem os parâmetros separados e cuidam do escape.

```python
# Ruim
cur.execute(f"SELECT id FROM users WHERE name = '{name}'")

# Bom
cur.execute("SELECT id FROM users WHERE name = %s", (name,))  # placeholder style depends on the driver
```

**Exceções:** nomes de tabela ou coluna, que precisam vir de uma lista fixa de permitidos.
**Fonte:** [PEP 249, paramstyle](https://peps.python.org/pep-0249/#paramstyle)

### PY-SEC-002: Rode subprocessos com lista de argumentos e sem shell

**Nível:** MUST · **Lente:** segurança

Com `shell=True` a string é interpretada pelo shell, então `;`, `|` ou `$()` na entrada executam comandos extras. Uma lista de argumentos chega ao programa exatamente como está.

```python
# Ruim
subprocess.run(f"convert {filename} out.png", shell=True)

# Bom
subprocess.run(["convert", filename, "out.png"], check=True)
```

**Exceções:** strings de comando fixas, sem nenhuma entrada externa.
**Fonte:** [Documentação do Python, considerações de segurança do subprocess](https://docs.python.org/3/library/subprocess.html#security-considerations)

### PY-SEC-003: Nunca use pickle ou `yaml.load` com dados não confiáveis

**Nível:** MUST · **Lente:** segurança

`pickle`, `marshal`, `shelve` e `yaml.load` com o loader completo podem construir objetos arbitrários e executar código durante a leitura. Para dados de fora, use JSON ou `yaml.safe_load`.

```python
# Ruim
settings = pickle.loads(request.body)
config = yaml.load(text, Loader=yaml.Loader)

# Bom
settings = json.loads(request.body)
config = yaml.safe_load(text)
```

**Exceções:** arquivos que o seu próprio processo gravou e que ninguém mais consegue alterar.
**Fonte:** [Documentação do Python, pickle](https://docs.python.org/3/library/pickle.html)

### PY-SEC-004: Use `secrets`, não `random`, para tokens e senhas

**Nível:** MUST · **Lente:** segurança

`random` é um gerador previsível feito para simulações; a saída dele pode ser reproduzida. `secrets` usa a fonte criptográfica do sistema operacional.

```python
# Ruim
token = "".join(random.choices(string.ascii_letters, k=32))

# Bom
token = secrets.token_urlsafe(32)
```

**Exceções:** usos sem relação com segurança, como embaralhar dados de teste ou tirar amostras.
**Fonte:** [Documentação do Python, secrets](https://docs.python.org/3/library/secrets.html)

### PY-SEC-005: Nunca passe entrada não confiável para `eval` ou `exec`

**Nível:** MUST · **Lente:** segurança

`eval` e `exec` executam qualquer código Python que recebem, com as permissões do seu processo. Leia literais com `ast.literal_eval` ou `json`, e mapeie nomes para funções de forma explícita.

```python
# Ruim
value = eval(request.args["filter"])

# Bom
value = ast.literal_eval(request.args["filter"])  # literals only: numbers, strings, lists, dicts
```

**Fonte:** [Documentação do Python, ast.literal_eval](https://docs.python.org/3/library/ast.html#ast.literal_eval)

### PY-SEC-006: Resolva caminhos de arquivo e mantenha-os dentro do diretório permitido

**Nível:** MUST · **Lente:** segurança

Um nome como `../../etc/passwd` ou um caminho absoluto escapa da pasta que você queria servir. Resolva o caminho final e confira se ele continua dentro do diretório base.

```python
# Ruim
path = UPLOAD_DIR / filename
return path.read_bytes()

# Bom
path = (UPLOAD_DIR / filename).resolve()
if not path.is_relative_to(UPLOAD_DIR.resolve()):
    raise PermissionError(filename)
return path.read_bytes()
```

**Fonte:** [OWASP, path traversal](https://owasp.org/www-community/attacks/Path_Traversal)

## Desempenho

### PY-PERF-001: Prefira set para testes de pertencimento repetidos

**Nível:** SHOULD · **Lente:** desempenho

`x in list` é O(n) por busca; `x in set` é O(1) em média. Dentro de laços, isso transforma O(n·m) em O(n+m).

```python
# Ruim
allowed = ["a", "b", "c"]
valid = [item for item in items if item in allowed]

# Bom
allowed = {"a", "b", "c"}
valid = [item for item in items if item in allowed]
```

**Exceções:** coleções com poucos itens consultadas uma única vez, ou itens que não são hashable.
**Fonte:** [Documentação do Python, tipos set](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)

### PY-PERF-002: Monte strings com `str.join`, não com `+=` num laço

**Nível:** SHOULD · **Lente:** desempenho

Strings são imutáveis, então cada `+=` pode copiar tudo o que já foi montado, chegando a O(n²) no pior caso. `join` calcula o tamanho uma vez e copia cada pedaço uma vez só.

```python
# Ruim
csv = ""
for row in rows:
    csv += ",".join(row) + "\n"

# Bom
csv = "".join(",".join(row) + "\n" for row in rows)
```

**Exceções:** poucas concatenações fora de laços.
**Fonte:** [Documentação do Python, operações comuns de sequência, nota 6](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)

### PY-PERF-003: Use generator expressions quando o resultado é consumido uma vez

**Nível:** SHOULD · **Lente:** desempenho

Uma list comprehension monta a lista inteira na memória antes de `sum`, `any` ou `max` lerem. Um gerador entrega um item por vez, e `any` / `all` podem parar antes do fim.

```python
# Ruim
total = sum([order.amount for order in orders])
has_admin = any([user.is_admin for user in users])

# Bom
total = sum(order.amount for order in orders)
has_admin = any(user.is_admin for user in users)
```

**Exceções:** quando o resultado é reutilizado ou o tamanho dele é necessário. A parada antecipada de `any` / `all` pula efeitos colaterais dos itens seguintes; mantenha a lista se eles importarem.
**Fonte:** [PEP 289, generator expressions](https://peps.python.org/pep-0289/)

### PY-PERF-004: Use `collections.deque` para filas

**Nível:** SHOULD · **Lente:** desempenho

`list.pop(0)` e `list.insert(0, x)` deslocam todos os elementos, O(n) cada. `deque` insere e remove nas duas pontas em O(1).

```python
# Ruim
queue = [start]
while queue:
    node = queue.pop(0)
    queue.extend(node.children)

# Bom
queue = deque([start])
while queue:
    node = queue.popleft()
    queue.extend(node.children)
```

**Exceções:** código que precisa de acesso rápido por índice no meio da coleção.
**Fonte:** [Documentação do Python, collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)

### PY-PERF-005: Faça cache de funções puras e caras com `functools.cache`

**Nível:** SHOULD · **Lente:** desempenho

Uma função chamada várias vezes com os mesmos argumentos recalcula a mesma resposta toda vez. Se o resultado depende só dos argumentos, guarde-o em cache.

```python
# Ruim
def tax_rate(region: str) -> Decimal:
    return parse_rate_table()[region]  # parses the whole table on every call


# Bom
@functools.cache
def tax_rate(region: str) -> Decimal:
    return parse_rate_table()[region]
```

**Exceções:** funções com efeitos colaterais, resultados que precisam se atualizar com o tempo, argumentos que não são hashable, ou conjuntos de argumentos sem limite (use `lru_cache(maxsize=...)`). Fazer cache de uma função impura é uma mudança de comportamento.
**Fonte:** [Documentação do Python, functools.cache](https://docs.python.org/3/library/functools.html#functools.cache)

## Manutenibilidade

### PY-MAINT-001: Nunca use um valor mutável como argumento padrão

**Nível:** MUST · **Lente:** manutenibilidade

O valor padrão é avaliado uma única vez, quando a função é definida, então a mesma lista ou dict é compartilhada por todas as chamadas e vai crescendo.

```python
# Ruim
def add_tag(tag: str, tags: list[str] = []) -> list[str]:
    tags.append(tag)
    return tags


# Bom
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    tags = [] if tags is None else tags
    tags.append(tag)
    return tags
```

**Fonte:** [Documentação do Python, valores padrão de argumentos](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values)

### PY-MAINT-002: Capture exceções específicas, nunca um `except` vazio

**Nível:** MUST · **Lente:** manutenibilidade

Um `except:` sem tipo ou um `except Exception:` silencioso esconde bugs e captura até `KeyboardInterrupt`. Capture o que você sabe tratar e relance com `from` para preservar a causa.

```python
# Ruim
try:
    config = load_config(path)
except:
    config = {}

# Bom
try:
    config = load_config(path)
except FileNotFoundError:
    config = {}
except json.JSONDecodeError as exc:
    raise ConfigError(f"invalid config in {path}") from exc
```

**Exceções:** um handler no nível mais alto que registra o traceback completo e encerra ou devolve uma resposta de erro.
**Fonte:** [PEP 8, recomendações de programação](https://peps.python.org/pep-0008/#programming-recommendations)

### PY-MAINT-003: Gerencie recursos com `with`

**Nível:** MUST · **Lente:** manutenibilidade

Arquivos, sockets, locks e conexões abertos sem gerenciador de contexto vazam quando uma exceção pula a chamada de `close()`.

```python
# Ruim
f = open(path)
data = json.load(f)
f.close()

# Bom
with open(path) as f:
    data = json.load(f)
```

**Fonte:** [Documentação do Python, o comando with](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)

### PY-MAINT-004: Adicione type hints às funções públicas

**Nível:** SHOULD · **Lente:** manutenibilidade

As anotações documentam o contrato e deixam um verificador de tipos (mypy, Pyright) pegar chamadas erradas antes da execução.

```python
# Ruim
def find_user(id, include_deleted=False): ...


# Bom
def find_user(user_id: int, include_deleted: bool = False) -> User | None: ...
```

**Exceções:** scripts curtos e funções auxiliares privadas com tipos óbvios.
**Fonte:** [Documentação do Python, typing](https://docs.python.org/3/library/typing.html)

### PY-MAINT-005: Use `logging`, não `print`, fora de scripts

**Nível:** SHOULD · **Lente:** manutenibilidade

`print` não pode ser filtrado por nível, redirecionado ou desligado pela aplicação que usa o seu código. Um logger por módulo pode.

```python
# Ruim
print(f"retrying {url}")

# Bom
logger = logging.getLogger(__name__)
logger.warning("retrying %s", url)
```

**Exceções:** ferramentas de linha de comando cuja saída é o próprio produto.
**Fonte:** [Documentação do Python, logging HOWTO](https://docs.python.org/3/howto/logging.html)
