"""PY-PERF-001, bad: membership test against a list inside a loop, O(n*m)."""

allowed = [f"user-{i}" for i in range(0, 4000, 3)]
items = [f"user-{i}" for i in range(4000)]

valid = [item for item in items if item in allowed]
print(len(valid), valid[:3], valid[-1])
