"""PY-PERF-003, good: generator expressions consumed once."""

amounts = [(i * 37) % 1000 for i in range(200000)]
roles = ["user"] * 199999 + ["admin"]

total = sum(amount for amount in amounts)
has_admin = any(role == "admin" for role in roles)
print(total, has_admin)
