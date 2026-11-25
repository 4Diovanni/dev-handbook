# Python

Python language rules (Python 3.11+ baseline). Load together with `core/`.

- Rule prefix: `PY`
- Formatting and import order are left to Ruff and are not rules here.

## Security

### PY-SEC-001: Use parameterized queries, never f-strings or `%` in SQL

**Level:** MUST · **Lens:** security

String formatting puts input inside the SQL text, so a crafted value can change the query. DB-API drivers take parameters separately and escape them.

```python
# Bad
cur.execute(f"SELECT id FROM users WHERE name = '{name}'")

# Good
cur.execute("SELECT id FROM users WHERE name = %s", (name,))  # placeholder style depends on the driver
```

**Exceptions:** table or column names, which must come from a fixed allowlist.
**Source:** [PEP 249, paramstyle](https://peps.python.org/pep-0249/#paramstyle)

### PY-SEC-002: Run subprocesses with an argument list and no shell

**Level:** MUST · **Lens:** security

With `shell=True` the string is parsed by the shell, so `;`, `|` or `$()` in input runs extra commands. A list of arguments is passed to the program as is.

```python
# Bad
subprocess.run(f"convert {filename} out.png", shell=True)

# Good
subprocess.run(["convert", filename, "out.png"], check=True)
```

**Exceptions:** fixed command strings with no external input.
**Source:** [Python docs, subprocess security considerations](https://docs.python.org/3/library/subprocess.html#security-considerations)

### PY-SEC-003: Never unpickle or `yaml.load` untrusted data

**Level:** MUST · **Lens:** security

`pickle`, `marshal`, `shelve` and `yaml.load` with the full loader can build arbitrary objects and run code while loading. Use JSON or `yaml.safe_load` for data from outside.

```python
# Bad
settings = pickle.loads(request.body)
config = yaml.load(text, Loader=yaml.Loader)

# Good
settings = json.loads(request.body)
config = yaml.safe_load(text)
```

**Exceptions:** files your own process wrote and that no one else can modify.
**Source:** [Python docs, pickle](https://docs.python.org/3/library/pickle.html)

### PY-SEC-004: Use `secrets`, not `random`, for tokens and passwords

**Level:** MUST · **Lens:** security

`random` is a predictable generator made for simulations; its output can be reproduced. `secrets` uses the operating system's cryptographic source.

```python
# Bad
token = "".join(random.choices(string.ascii_letters, k=32))

# Good
token = secrets.token_urlsafe(32)
```

**Exceptions:** non-security uses such as shuffling test data or sampling.
**Source:** [Python docs, secrets](https://docs.python.org/3/library/secrets.html)

### PY-SEC-005: Never pass untrusted input to `eval` or `exec`

**Level:** MUST · **Lens:** security

`eval` and `exec` run any Python code they receive, with the permissions of your process. Parse literals with `ast.literal_eval` or `json`, and map names to functions explicitly.

```python
# Bad
value = eval(request.args["filter"])

# Good
value = ast.literal_eval(request.args["filter"])  # literals only: numbers, strings, lists, dicts
```

**Source:** [Python docs, ast.literal_eval](https://docs.python.org/3/library/ast.html#ast.literal_eval)

### PY-SEC-006: Resolve file paths and keep them inside the allowed directory

**Level:** MUST · **Lens:** security

A name like `../../etc/passwd` or an absolute path escapes the folder you meant to serve. Resolve the final path and check that it is still under the base directory.

```python
# Bad
path = UPLOAD_DIR / filename
return path.read_bytes()

# Good
path = (UPLOAD_DIR / filename).resolve()
if not path.is_relative_to(UPLOAD_DIR.resolve()):
    raise PermissionError(filename)
return path.read_bytes()
```

**Source:** [OWASP, path traversal](https://owasp.org/www-community/attacks/Path_Traversal)

## Performance

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

**Exceptions:** collections with a handful of items checked once, or items that are not hashable.
**Source:** [Python docs, set types](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)

### PY-PERF-002: Build strings with `str.join`, not `+=` in a loop

**Level:** SHOULD · **Lens:** performance

Strings are immutable, so each `+=` may copy everything built so far, which is O(n²) in the worst case. `join` computes the size once and copies each piece once.

```python
# Bad
csv = ""
for row in rows:
    csv += ",".join(row) + "\n"

# Good
csv = "".join(",".join(row) + "\n" for row in rows)
```

**Exceptions:** a few concatenations outside loops.
**Source:** [Python docs, common sequence operations, note 6](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)

### PY-PERF-003: Use generator expressions when the result is consumed once

**Level:** SHOULD · **Lens:** performance

A list comprehension builds the whole list in memory before `sum`, `any` or `max` read it. A generator yields one item at a time, and `any` / `all` can stop early.

```python
# Bad
total = sum([order.amount for order in orders])
has_admin = any([user.is_admin for user in users])

# Good
total = sum(order.amount for order in orders)
has_admin = any(user.is_admin for user in users)
```

**Exceptions:** when the result is reused or its length is needed. Early exit in `any` / `all` skips side effects of later items; keep the list if those matter.
**Source:** [PEP 289, generator expressions](https://peps.python.org/pep-0289/)

### PY-PERF-004: Use `collections.deque` for queues

**Level:** SHOULD · **Lens:** performance

`list.pop(0)` and `list.insert(0, x)` shift every element, O(n) each. `deque` adds and removes at both ends in O(1).

```python
# Bad
queue = [start]
while queue:
    node = queue.pop(0)
    queue.extend(node.children)

# Good
queue = deque([start])
while queue:
    node = queue.popleft()
    queue.extend(node.children)
```

**Exceptions:** code that needs fast random access by index in the middle.
**Source:** [Python docs, collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)

### PY-PERF-005: Cache pure, expensive functions with `functools.cache`

**Level:** SHOULD · **Lens:** performance

A function called repeatedly with the same arguments recomputes the same answer each time. If its result depends only on its arguments, cache it.

```python
# Bad
def tax_rate(region: str) -> Decimal:
    return parse_rate_table()[region]  # parses the whole table on every call


# Good
@functools.cache
def tax_rate(region: str) -> Decimal:
    return parse_rate_table()[region]
```

**Exceptions:** functions with side effects, results that must refresh over time, unhashable arguments, or unbounded argument sets (use `lru_cache(maxsize=...)`). Caching an impure function is a behavior change.
**Source:** [Python docs, functools.cache](https://docs.python.org/3/library/functools.html#functools.cache)

## Maintainability

### PY-MAINT-001: Never use a mutable value as a default argument

**Level:** MUST · **Lens:** maintainability

Defaults are evaluated once, when the function is defined, so the same list or dict is shared by every call and keeps growing.

```python
# Bad
def add_tag(tag: str, tags: list[str] = []) -> list[str]:
    tags.append(tag)
    return tags


# Good
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    tags = [] if tags is None else tags
    tags.append(tag)
    return tags
```

**Source:** [Python docs, default argument values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values)

### PY-MAINT-002: Catch specific exceptions, never a bare `except`

**Level:** MUST · **Lens:** maintainability

A bare `except:` or a silent `except Exception:` hides bugs and even catches `KeyboardInterrupt`. Catch what you can handle, and re-raise with `from` to keep the cause.

```python
# Bad
try:
    config = load_config(path)
except:
    config = {}

# Good
try:
    config = load_config(path)
except FileNotFoundError:
    config = {}
except json.JSONDecodeError as exc:
    raise ConfigError(f"invalid config in {path}") from exc
```

**Exceptions:** a top-level handler that logs the full traceback and exits or returns an error response.
**Source:** [PEP 8, programming recommendations](https://peps.python.org/pep-0008/#programming-recommendations)

### PY-MAINT-003: Manage resources with `with`

**Level:** MUST · **Lens:** maintainability

Files, sockets, locks and connections opened without a context manager leak when an exception skips the `close()` call.

```python
# Bad
f = open(path)
data = json.load(f)
f.close()

# Good
with open(path) as f:
    data = json.load(f)
```

**Source:** [Python docs, the with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)

### PY-MAINT-004: Add type hints to public functions

**Level:** SHOULD · **Lens:** maintainability

Hints document the contract and let a type checker (mypy, Pyright) catch wrong calls before runtime.

```python
# Bad
def find_user(id, include_deleted=False): ...


# Good
def find_user(user_id: int, include_deleted: bool = False) -> User | None: ...
```

**Exceptions:** short scripts and private helpers whose types are obvious.
**Source:** [Python docs, typing](https://docs.python.org/3/library/typing.html)

### PY-MAINT-005: Use `logging`, not `print`, outside scripts

**Level:** SHOULD · **Lens:** maintainability

`print` cannot be filtered by level, routed or turned off by the application that uses your code. A module-level logger can.

```python
# Bad
print(f"retrying {url}")

# Good
logger = logging.getLogger(__name__)
logger.warning("retrying %s", url)
```

**Exceptions:** command-line tools whose output is the product.
**Source:** [Python docs, logging HOWTO](https://docs.python.org/3/howto/logging.html)
