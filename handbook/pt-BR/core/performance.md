# Desempenho

Regras de desempenho transversais. Toda sugestão precisa manter o comportamento observável igual; se não mantiver, marque como "behavior change" (veja `CORE-IMPACT-001`).

- Prefixo das regras: `CORE`
- Os exemplos usam Python por ser curto; os arquivos de cada linguagem trazem as APIs concretas.

## Regras

### CORE-PERF-001: Agrupe operações de I/O em vez de fazer uma por item

**Nível:** SHOULD · **Lente:** desempenho

Cada query, chamada HTTP ou abertura de arquivo paga uma latência fixa. Uma chamada por item dentro de um laço (o padrão N+1) multiplica esse custo por N.

```python
# Ruim
orders = db.fetch_all("SELECT * FROM orders WHERE day = %s", (day,))
for order in orders:
    order.customer = db.fetch_one("SELECT * FROM customers WHERE id = %s", (order.customer_id,))

# Bom
orders = db.fetch_all("SELECT * FROM orders WHERE day = %s", (day,))
ids = list({o.customer_id for o in orders})
customers = {c.id: c for c in db.fetch_all("SELECT * FROM customers WHERE id = ANY(%s)", (ids,))}
for order in orders:
    order.customer = customers[order.customer_id]
```

**Exceções:** N muito pequeno, em que a query em lote fica mais difícil de ler do que vale a pena.
**Fonte:** [Documentação do Django, otimização de acesso ao banco](https://docs.djangoproject.com/en/stable/topics/db/optimization/)

### CORE-PERF-002: Indexe os dados por chave em vez de varrê-los dentro de um laço

**Nível:** SHOULD · **Lente:** desempenho

Procurar numa lista dentro de outro laço custa O(n·m). Montar um mapa (hash) uma vez deixa cada busca O(1) em média.

```python
# Ruim
for payment in payments:
    user = next(u for u in users if u.id == payment.user_id)

# Bom
users_by_id = {u.id: u for u in users}
for payment in payments:
    user = users_by_id[payment.user_id]
```

**Exceções:** coleções com poucos itens. Uma chave ausente levantava `StopIteration` e passa a levantar `KeyError`; mantenha o erro original se quem chama depende dele. Com IDs repetidos, `next` devolve o primeiro e o dict guarda o último.
**Fonte:** [Wiki do Python, complexidade de tempo](https://wiki.python.org/moin/TimeComplexity)

### CORE-PERF-003: Tire do laço o trabalho que não muda entre as iterações

**Nível:** SHOULD · **Lente:** desempenho

Trabalho cujo resultado não muda de uma volta para outra (compilar um padrão, ler configuração, abrir conexão) é repetido à toa a cada passada.

```python
# Ruim
for line in lines:
    if re.compile(config.load()["pattern"]).search(line):
        matches.append(line)

# Bom
pattern = re.compile(config.load()["pattern"])
for line in lines:
    if pattern.search(line):
        matches.append(line)
```

**Exceções:** quando o valor "fixo" pode mudar durante o laço (recarga de configuração, valores que dependem do tempo).
**Fonte:** [Documentação do Python, re.compile](https://docs.python.org/3/library/re.html#re.compile)

### CORE-PERF-004: Processe dados grandes em fluxo em vez de carregar tudo na memória

**Nível:** SHOULD · **Lente:** desempenho

Ler um arquivo, um resultado de query ou uma resposta inteira antes de processar faz a memória crescer com o tamanho da entrada e atrasa o primeiro resultado. Processe os registros conforme chegam.

```python
# Ruim
with open(path) as f:
    lines = f.readlines()
errors = sum(1 for line in lines if "ERROR" in line)

# Bom
with open(path) as f:
    errors = sum(1 for line in f if "ERROR" in line)
```

**Exceções:** dados que precisam ser ordenados ou percorridos mais de uma vez e cabem com folga na memória.
**Fonte:** [Documentação do Python, lendo arquivos](https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects)

### CORE-PERF-005: Defina timeout em toda chamada de rede

**Nível:** MUST · **Lente:** desempenho

Uma chamada sem timeout pode esperar para sempre por um serviço lento, prendendo thread, conexão e memória até o pool esgotar. Defina timeouts explícitos de conexão e de leitura.

```python
# Ruim
response = requests.get(url)

# Bom
response = requests.get(url, timeout=(3.05, 10))  # connect, read in seconds
```

**Exceções:** nenhuma para chamadas de requisição e resposta; conexões de longa duração usam heartbeats.
**Fonte:** [Documentação do Requests, timeouts](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)
