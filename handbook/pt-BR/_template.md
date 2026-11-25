# Modelo de regra

Copie o bloco abaixo para o arquivo certo. Esta é a versão de leitura: pode explicar mais que a versão em inglês, mas o ID, o nível e os exemplos são os mesmos.

````markdown
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

**Exceções:** coleções com poucos itens consultadas uma única vez.
**Fonte:** [Documentação do Python, tipos set](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
````

## Campos obrigatórios

- ID e título no cabeçalho.
- Nível e lente.
- Porquê, em no máximo duas frases.
- Um par mínimo ruim / bom.

Exceções e fonte são recomendadas. O arquivo em inglês é a fonte da verdade: este arquivo precisa ter os mesmos IDs, na mesma ordem.
