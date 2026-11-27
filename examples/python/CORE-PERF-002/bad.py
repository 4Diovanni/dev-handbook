"""CORE-PERF-002, bad: scanning a list for every lookup, O(n*m)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    name: str


users = [User(i, f"user-{i}") for i in range(3000)]
payments = [(i * 13) % 3000 for i in range(6000)]

names = []
for user_id in payments:
    user = next(u for u in users if u.id == user_id)
    names.append(user.name)
print(len(names), names[:3], names[-1])
