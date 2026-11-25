# Rule template

Copy the block below into the right file. Keep the English version short: it is what AI assistants read.

````markdown
### PY-PERF-001: Prefer a set for repeated membership tests

**Level:** SHOULD · **Lens:** performance

`x in list` is O(n) per lookup; `x in set` is O(1) on average. Inside loops this turns O(n·m) into O(n+m).

```python
# Bad
allowed = ["a", "b", "c"]
valid = [item for item in items if item in allowed]

# Good
allowed = {"a", "b", "c"}
valid = [item for item in items if item in allowed]
```

**Exceptions:** collections with a handful of items checked once.
**Source:** [Python docs, set types](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
````

## Required fields

- ID and title in the heading.
- Level and lens.
- Why, in at most two sentences.
- A minimal bad / good pair.

Exceptions and source are recommended. The pt-BR file must declare the same IDs in the same order.
