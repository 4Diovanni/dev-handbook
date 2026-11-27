"""PY-PERF-002, bad: building a string with += in a loop."""

rows = [(str(i), f"name-{i}", str(i * 7 % 100)) for i in range(20000)]

csv = ""
for row in rows:
    csv += ",".join(row) + "\n"
print(len(csv), csv.splitlines()[12345])
