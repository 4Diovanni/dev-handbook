"""CORE-PERF-003, good: computing the invariant value once, before the loop."""

import json
import re

CONFIG = '{"pattern": "ERROR \\\\[(\\\\w+)\\\\]"}'
lines = [f"{'ERROR' if i % 7 == 0 else 'INFO'} [svc{i % 5}] event {i}" for i in range(50000)]

pattern = re.compile(json.loads(CONFIG)["pattern"])
matches = []
for line in lines:
    if pattern.search(line):
        matches.append(line)
print(len(matches), matches[0], matches[-1])
