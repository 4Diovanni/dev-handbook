# Impacto

Como pesar uma mudança antes de sugeri-la: risco de quebrar comportamento, custo de adoção e ganho mensurável. Estas regras valem para toda sugestão, de qualquer revisor.

- Prefixo das regras: `CORE`
- Os exemplos usam Python por ser curto.

## Regras

### CORE-IMPACT-001: Mantenha o comportamento observável, ou sinalize a mudança

**Nível:** MUST · **Lente:** impacto

Uma otimização ou limpeza que muda em silêncio a saída, a ordem, os erros ou os efeitos colaterais é um bug. Se a correção muda comportamento, diga isso e marque como "behavior change".

```python
# Ruim: suggested as a "faster dedupe", but it loses the original order
unique = list(set(items))

# Bom: same speed class, keeps first-seen order
unique = list(dict.fromkeys(items))
```

**Fonte:** [Martin Fowler, refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html)

### CORE-IMPACT-002: Comprove ganhos de desempenho com medição

**Nível:** SHOULD · **Lente:** impacto

A intuição sobre velocidade costuma errar, e uma mudança sem medição adiciona risco sem ganho comprovado. Mostre um profile ou benchmark com entrada realista, antes e depois.

```python
# Ruim
# "This should be faster."

# Bom
# python -m timeit -s "from app import old, new, data" "old(data)"  -> 41.2 ms per loop
# python -m timeit -s "from app import old, new, data" "new(data)"  ->  3.8 ms per loop
```

**Exceções:** correções de uma classe de complexidade conhecida (por exemplo, de O(n²) para O(n)) em entradas claramente grandes.
**Fonte:** [Documentação do Python, timeit](https://docs.python.org/3/library/timeit.html)

### CORE-IMPACT-003: Sugira a menor mudança que resolve o problema

**Nível:** SHOULD · **Lente:** impacto

Reescritas grandes são difíceis de revisar, misturam mudanças sem relação e escondem regressões. Corrija só o problema apontado; refatorações maiores viram sugestões separadas.

```python
# Ruim: the finding was a missing timeout; the fix rewrites the client
class HttpClient: ...  # 80 new lines, new retry policy, new logging


# Bom
response = requests.get(url, timeout=10)
```

**Fonte:** [Google engineering practices, small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)

### CORE-IMPACT-004: Deprecie APIs públicas antes de removê-las ou alterá-las

**Nível:** SHOULD · **Lente:** impacto

Quem chama o seu código e você não vê quebra quando uma função, endpoint ou campo público some. Mantenha a entrada antiga funcionando, marque-a como deprecated apontando a substituta, e remova numa versão major futura.

```python
# Ruim: renamed in place, every caller breaks
def fetch_user(user_id: int) -> User: ...


# Bom
def get_user(user_id: int) -> User:
    warnings.warn("get_user is deprecated, use fetch_user", DeprecationWarning, stacklevel=2)
    return fetch_user(user_id)


def fetch_user(user_id: int) -> User: ...
```

**Exceções:** código interno sem chamadas de fora do repositório.
**Fonte:** [Semantic Versioning 2.0.0](https://semver.org/lang/pt-BR/)

### CORE-IMPACT-005: Evite adicionar uma dependência para algo trivial

**Nível:** AVOID · **Lente:** impacto

Toda dependência traz risco de cadeia de suprimentos, trabalho de atualização e tamanho de instalação. Use a biblioteca padrão quando ela já resolve em poucas linhas.

```python
# Ruim
from slugify_tiny import slugify  # new dependency for one call


# Bom
def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
```

**Exceções:** problemas que parecem pequenos mas não são (datas e fusos horários, criptografia, parsing de padrões).
**Fonte:** [OWASP Vulnerable Dependency Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html)
