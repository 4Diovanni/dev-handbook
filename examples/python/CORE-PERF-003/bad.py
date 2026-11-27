"""CORE-PERF-003, bad: rebuilding an invariant value on every iteration."""

import json
import re

CONFIG = '{"pattern": "ERROR \\\\[(\\\\w+)\\\\]"}'
lines = [f"{'ERROR' if i % 7 == 0 else 'INFO'} [svc{i % 5}] event {i}" for i in range(50000)]

matches = []
for line in lines:
    if re.compile(json.loads(CONFIG)["pattern"]).search(line):
        matches.append(line)
print(len(matches), matches[0], matches[-1])
