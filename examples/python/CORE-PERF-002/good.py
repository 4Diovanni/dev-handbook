"""CORE-PERF-002, good: indexing the list by key once, O(n+m)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    name: str


users = [User(i, f"user-{i}") for i in range(3000)]
payments = [(i * 13) % 3000 for i in range(6000)]

users_by_id = {u.id: u for u in users}
names = []
for user_id in payments:
    user = users_by_id[user_id]
    names.append(user.name)
print(len(names), names[:3], names[-1])
