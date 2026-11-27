# Security

Cross-cutting security rules: input validation, secrets, injection, access control, cryptography and dependencies. They apply to every language; language files add the concrete APIs.

- Rule prefix: `CORE`
- Examples use Python for brevity unless a rule needs another language.

## Rules

### CORE-SEC-001: Validate untrusted input at the trust boundary

**Level:** MUST · **Lens:** security

Data from users, files, queues and other services can be anything. Check type, length, range and format with an allowlist where it enters the system, and reject what does not match.

```python
# Bad
def set_page_size(raw: str) -> int:
    return int(raw)  # "-1", "999999999" and "abc" all get through or crash


# Good
def set_page_size(raw: str) -> int:
    if not raw.isdigit() or not 1 <= int(raw) <= 100:
        raise ValueError("page size must be between 1 and 100")
    return int(raw)
```

**Exceptions:** values already validated by a typed schema at the same boundary (for example a request model).
**Source:** [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

### CORE-SEC-002: Keep secrets out of source code

**Level:** MUST · **Lens:** security

Anything committed is copied to every clone, fork and backup, and stays in history after deletion. Read secrets from the environment or a secret manager and fail fast when they are missing.

```python
# Bad
API_KEY = "sk_live_4f9a..."

# Good
API_KEY = os.environ["PAYMENTS_API_KEY"]  # KeyError at startup if missing
```

**Exceptions:** clearly fake values in tests and examples (`"test-key"`).
**Source:** [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

### CORE-SEC-003: Never build queries or commands by concatenating input

**Level:** MUST · **Lens:** security

Concatenation lets input change the structure of SQL, shell, LDAP or template code. Pass input as parameters so the interpreter treats it as data.

```python
# Bad
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# Good
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

**Exceptions:** identifiers (table or column names) cannot be parameterized; pick them from a fixed allowlist instead.
**Source:** [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)

### CORE-SEC-004: Check authorization on every request, server side

**Level:** MUST · **Lens:** security

Hiding a button or trusting an ID from the client is not access control. Deny by default and check that the current user may act on the specific resource.

```python
# Bad
def get_invoice(invoice_id: int) -> Invoice:
    return repo.find(invoice_id)  # any logged-in user can read any invoice


# Good
def get_invoice(invoice_id: int, user: User) -> Invoice:
    invoice = repo.find(invoice_id)
    if invoice is None or invoice.owner_id != user.id:
        raise NotFound()  # same answer for "missing" and "not yours"
    return invoice
```

**Source:** [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

### CORE-SEC-005: Keep secrets and personal data out of logs and error responses

**Level:** MUST · **Lens:** security

Logs and stack traces are read by more people and kept longer than the data they describe. Log identifiers, not credentials or personal data, and return generic errors to clients.

```python
# Bad
log.info("login %s with password %s", email, password)
return {"error": traceback.format_exc()}, 500

# Good
log.info("login attempt for user_id=%s", user_id)
return {"error": "internal error", "request_id": request_id}, 500
```

**Source:** [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

### CORE-SEC-006: Use vetted libraries for passwords and cryptography

**Level:** MUST · **Lens:** security

Fast hashes (MD5, SHA-1, SHA-256) are built to be cheap, so stolen password hashes are cracked quickly. Hash passwords with Argon2id, scrypt or bcrypt, and never write your own crypto.

```python
# Bad
stored = hashlib.sha256(password.encode()).hexdigest()

# Good
from argon2 import PasswordHasher

stored = PasswordHasher().hash(password)  # salted, slow on purpose
```

**Exceptions:** non-secret checksums (cache keys, file integrity) can use fast hashes.
**Source:** [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

### CORE-SEC-007: Pin dependencies and scan them for known vulnerabilities

**Level:** SHOULD · **Lens:** security

Unpinned ranges pull new code into every build without review. Commit a lock file or exact versions and run a vulnerability scanner (Dependabot, `pip-audit`, OWASP Dependency-Check) in CI.

```text
# Bad (requirements.txt)
requests

# Good (requirements.txt)
requests==2.32.3
```

**Exceptions:** libraries published for others declare compatible ranges; the applications that use them pin.
**Source:** [OWASP Vulnerable Dependency Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html)
