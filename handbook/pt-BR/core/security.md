# Segurança

Regras de segurança transversais: validação de entrada, segredos, injeção, controle de acesso, criptografia e dependências. Valem para qualquer linguagem; os arquivos de cada linguagem trazem as APIs concretas.

- Prefixo das regras: `CORE`
- Os exemplos usam Python por ser curto, a não ser quando a regra pede outra linguagem.

## Regras

### CORE-SEC-001: Valide entradas não confiáveis na fronteira de confiança

**Nível:** MUST · **Lente:** segurança

Dados vindos de usuários, arquivos, filas e outros serviços podem ser qualquer coisa. Confira tipo, tamanho, faixa e formato com uma lista de permitidos (allowlist) no ponto em que o dado entra no sistema, e rejeite o que não bater.

```python
# Ruim
def set_page_size(raw: str) -> int:
    return int(raw)  # "-1", "999999999" and "abc" all get through or crash


# Bom
def set_page_size(raw: str) -> int:
    if not raw.isdigit() or not 1 <= int(raw) <= 100:
        raise ValueError("page size must be between 1 and 100")
    return int(raw)
```

**Exceções:** valores já validados por um schema tipado na mesma fronteira (por exemplo, um modelo de requisição).
**Fonte:** [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

### CORE-SEC-002: Mantenha segredos fora do código-fonte

**Nível:** MUST · **Lente:** segurança

Tudo o que é commitado vai para cada clone, fork e backup, e continua no histórico mesmo depois de apagado. Leia segredos de variáveis de ambiente ou de um cofre de segredos, e falhe logo na inicialização se faltarem.

```python
# Ruim
API_KEY = "sk_live_4f9a..."

# Bom
API_KEY = os.environ["PAYMENTS_API_KEY"]  # KeyError at startup if missing
```

**Exceções:** valores claramente falsos em testes e exemplos (`"test-key"`).
**Fonte:** [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

### CORE-SEC-003: Nunca monte queries ou comandos concatenando entradas

**Nível:** MUST · **Lente:** segurança

A concatenação deixa a entrada mudar a estrutura do SQL, do comando de shell, do LDAP ou do template. Passe a entrada como parâmetro, para que o interpretador a trate como dado.

```python
# Ruim
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# Bom
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

**Exceções:** identificadores (nomes de tabela ou coluna) não podem ser parametrizados; escolha-os de uma lista fixa de permitidos.
**Fonte:** [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)

### CORE-SEC-004: Verifique a autorização em toda requisição, no servidor

**Nível:** MUST · **Lente:** segurança

Esconder um botão ou confiar num ID enviado pelo cliente não é controle de acesso. Negue por padrão e confira se o usuário atual pode agir sobre aquele recurso específico.

```python
# Ruim
def get_invoice(invoice_id: int) -> Invoice:
    return repo.find(invoice_id)  # any logged-in user can read any invoice


# Bom
def get_invoice(invoice_id: int, user: User) -> Invoice:
    invoice = repo.find(invoice_id)
    if invoice is None or invoice.owner_id != user.id:
        raise NotFound()  # same answer for "missing" and "not yours"
    return invoice
```

**Fonte:** [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

### CORE-SEC-005: Mantenha segredos e dados pessoais fora de logs e respostas de erro

**Nível:** MUST · **Lente:** segurança

Logs e stack traces são lidos por mais gente e guardados por mais tempo que os dados que descrevem. Registre identificadores, nunca credenciais ou dados pessoais, e devolva ao cliente erros genéricos.

```python
# Ruim
log.info("login %s with password %s", email, password)
return {"error": traceback.format_exc()}, 500

# Bom
log.info("login attempt for user_id=%s", user_id)
return {"error": "internal error", "request_id": request_id}, 500
```

**Fonte:** [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

### CORE-SEC-006: Use bibliotecas consagradas para senhas e criptografia

**Nível:** MUST · **Lente:** segurança

Hashes rápidos (MD5, SHA-1, SHA-256) foram feitos para ser baratos, então hashes de senha vazados são quebrados depressa. Guarde senhas com Argon2id, scrypt ou bcrypt, e nunca escreva sua própria criptografia.

```python
# Ruim
stored = hashlib.sha256(password.encode()).hexdigest()

# Bom
from argon2 import PasswordHasher

stored = PasswordHasher().hash(password)  # salted, slow on purpose
```

**Exceções:** checksums que não são segredo (chaves de cache, integridade de arquivo) podem usar hashes rápidos.
**Fonte:** [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

### CORE-SEC-007: Fixe as versões das dependências e verifique vulnerabilidades conhecidas

**Nível:** SHOULD · **Lente:** segurança

Faixas de versão abertas puxam código novo para cada build sem revisão. Commite um lock file ou versões exatas e rode um scanner de vulnerabilidades (Dependabot, `pip-audit`, OWASP Dependency-Check) no CI.

```text
# Ruim (requirements.txt)
requests

# Bom (requirements.txt)
requests==2.32.3
```

**Exceções:** bibliotecas publicadas para terceiros declaram faixas compatíveis; quem fixa é a aplicação que as usa.
**Fonte:** [OWASP Vulnerable Dependency Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html)
