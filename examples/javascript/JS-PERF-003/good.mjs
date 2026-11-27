// JS-PERF-003, good: a Set built once, O(n+m).
const activeIds = Array.from({ length: 5000 }, (_, i) => i * 3);
const orders = Array.from({ length: 20000 }, (_, i) => ({ id: i, customerId: (i * 7) % 15000 }));

const activeSet = new Set(activeIds);
const active = orders.filter((o) => activeSet.has(o.customerId));
console.log(active.length, active[0].id, active.at(-1).id);
