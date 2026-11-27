# Performance

Cross-cutting performance rules. Every suggestion must keep observable behavior unchanged; if it does not, label it "behavior change" (see `CORE-IMPACT-001`).

- Rule prefix: `CORE`
- Examples use Python for brevity; language files add the concrete APIs.

## Rules

### CORE-PERF-001: Batch I/O instead of calling it once per item

**Level:** SHOULD · **Lens:** performance

Each database query, HTTP call or file open pays a fixed latency. One call per item in a loop (the N+1 pattern) multiplies that cost by N.

```python
# Bad
orders = db.fetch_all("SELECT * FROM orders WHERE day = %s", (day,))
for order in orders:
    order.customer = db.fetch_one("SELECT * FROM customers WHERE id = %s", (order.customer_id,))

# Good
orders = db.fetch_all("SELECT * FROM orders WHERE day = %s", (day,))
ids = list({o.customer_id for o in orders})
customers = {c.id: c for c in db.fetch_all("SELECT * FROM customers WHERE id = ANY(%s)", (ids,))}
for order in orders:
    order.customer = customers[order.customer_id]
```

**Exceptions:** very small N where the batch query is harder to read than it is worth.
**Source:** [Django docs, database access optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)

### CORE-PERF-002: Index data by key instead of scanning it in a loop

**Level:** SHOULD · **Lens:** performance

Searching a list inside another loop is O(n·m). Building a hash map once makes each lookup O(1) on average.

```python
# Bad
for payment in payments:
    user = next(u for u in users if u.id == payment.user_id)

# Good
users_by_id = {u.id: u for u in users}
for payment in payments:
    user = users_by_id[payment.user_id]
```

**Exceptions:** collections with a handful of items. A missing key raised `StopIteration` before and raises `KeyError` after; keep the original error if callers depend on it. With duplicate IDs, `next` returns the first match while the dict keeps the last.
**Source:** [Python wiki, time complexity](https://wiki.python.org/moin/TimeComplexity)

### CORE-PERF-003: Move loop-invariant work out of the loop

**Level:** SHOULD · **Lens:** performance

Work whose result does not change between iterations (compiling a pattern, parsing config, opening a connection) is repeated for nothing on every pass.

```python
# Bad
for line in lines:
    if re.compile(config.load()["pattern"]).search(line):
        matches.append(line)

# Good
pattern = re.compile(config.load()["pattern"])
for line in lines:
    if pattern.search(line):
        matches.append(line)
```

**Exceptions:** when the "invariant" can actually change during the loop (config reload, time-based values).
**Source:** [Python docs, re.compile](https://docs.python.org/3/library/re.html#re.compile)

### CORE-PERF-004: Stream large data instead of loading it all into memory

**Level:** SHOULD · **Lens:** performance

Reading a whole file, result set or response before processing makes memory grow with input size and delays the first result. Process records as they arrive.

```python
# Bad
with open(path) as f:
    lines = f.readlines()
errors = sum(1 for line in lines if "ERROR" in line)

# Good
with open(path) as f:
    errors = sum(1 for line in f if "ERROR" in line)
```

**Exceptions:** data that must be sorted or traversed more than once and fits comfortably in memory.
**Source:** [Python docs, reading files](https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects)

### CORE-PERF-005: Set a timeout on every network call

**Level:** MUST · **Lens:** performance

A call with no timeout can wait forever on a slow peer, holding a thread, a connection and memory until the pool is exhausted. Choose an explicit connect and read timeout.

```python
# Bad
response = requests.get(url)

# Good
response = requests.get(url, timeout=(3.05, 10))  # connect, read in seconds
```

**Exceptions:** none for request/response calls; long-lived streams use heartbeats instead.
**Source:** [Requests docs, timeouts](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)
