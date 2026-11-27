"""PY-PERF-004, good: breadth-first traversal with deque.popleft, O(1) per pop."""

from collections import deque

children = {n: [c for c in (2 * n + 1, 2 * n + 2) if c < 30000] for n in range(30000)}

order = []
queue = deque([0])
while queue:
    node = queue.popleft()
    order.append(node)
    queue.extend(children[node])
print(len(order), order[:5], order[-1])
