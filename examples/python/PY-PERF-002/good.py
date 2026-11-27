"""PY-PERF-002, good: building a string with str.join."""

rows = [(str(i), f"name-{i}", str(i * 7 % 100)) for i in range(20000)]

csv = "".join(",".join(row) + "\n" for row in rows)
print(len(csv), csv.splitlines()[12345])
