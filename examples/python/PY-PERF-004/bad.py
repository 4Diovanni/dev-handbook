"""PY-PERF-004, bad: breadth-first traversal with list.pop(0), O(n) per pop."""

children = {n: [c for c in (2 * n + 1, 2 * n + 2) if c < 30000] for n in range(30000)}

order = []
queue = [0]
while queue:
    node = queue.pop(0)
    order.append(node)
    queue.extend(children[node])
print(len(order), order[:5], order[-1])
