# Impact

How to weigh a change before suggesting it: risk of breaking behavior, adoption cost and measurable gain. These rules apply to every finding, from every reviewer.

- Rule prefix: `CORE`
- Examples use Python for brevity.

## Rules

### CORE-IMPACT-001: Keep observable behavior unchanged, or label the change

**Level:** MUST · **Lens:** impact

An optimization or cleanup that silently changes output, ordering, errors or side effects is a bug. If a fix changes behavior, say so and label it "behavior change".

```python
# Bad: suggested as a "faster dedupe", but it loses the original order
unique = list(set(items))

# Good: same speed class, keeps first-seen order
unique = list(dict.fromkeys(items))
```

**Source:** [Martin Fowler, refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html)

### CORE-IMPACT-002: Back performance claims with a measurement

**Level:** SHOULD · **Lens:** impact

Intuition about speed is often wrong, and an unmeasured change adds risk with no proven gain. Show a profile or benchmark from realistic input before and after.

```python
# Bad
# "This should be faster."

# Good
# python -m timeit -s "from app import old, new, data" "old(data)"  -> 41.2 ms per loop
# python -m timeit -s "from app import old, new, data" "new(data)"  ->  3.8 ms per loop
```

**Exceptions:** fixes for a known complexity class (for example O(n²) to O(n)) on inputs that are clearly large.
**Source:** [Python docs, timeit](https://docs.python.org/3/library/timeit.html)

### CORE-IMPACT-003: Suggest the smallest change that fixes the finding

**Level:** SHOULD · **Lens:** impact

Large rewrites are hard to review, mix unrelated changes and hide regressions. Fix the reported problem only; propose wider refactors as separate findings.

```python
# Bad: the finding was a missing timeout; the fix rewrites the client
class HttpClient: ...  # 80 new lines, new retry policy, new logging


# Good
response = requests.get(url, timeout=10)
```

**Source:** [Google engineering practices, small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)

### CORE-IMPACT-004: Deprecate public APIs before removing or changing them

**Level:** SHOULD · **Lens:** impact

Callers you cannot see break when a public function, endpoint or field disappears. Keep the old entry point working, mark it deprecated with the replacement, and remove it in a later major version.

```python
# Bad: renamed in place, every caller breaks
def fetch_user(user_id: int) -> User: ...


# Good
def get_user(user_id: int) -> User:
    warnings.warn("get_user is deprecated, use fetch_user", DeprecationWarning, stacklevel=2)
    return fetch_user(user_id)


def fetch_user(user_id: int) -> User: ...
```

**Exceptions:** internal code with no callers outside the repository.
**Source:** [Semantic Versioning 2.0.0](https://semver.org/)

### CORE-IMPACT-005: Avoid adding a dependency for trivial functionality

**Level:** AVOID · **Lens:** impact

Every dependency adds supply-chain risk, upgrade work and install size. Use the standard library when it already does the job in a few lines.

```python
# Bad
from slugify_tiny import slugify  # new dependency for one call


# Good
def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
```

**Exceptions:** problems that look small but are not (dates and time zones, cryptography, parsing standards).
**Source:** [OWASP Vulnerable Dependency Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html)
