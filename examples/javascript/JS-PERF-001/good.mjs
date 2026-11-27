// JS-PERF-001, good: independent async calls run concurrently with Promise.all.
const fetchUser = (id) => new Promise((resolve) => setTimeout(() => resolve({ id, name: `user-${id}` }), 20));

const ids = Array.from({ length: 20 }, (_, i) => i + 1);
const users = await Promise.all(ids.map((id) => fetchUser(id)));
console.log(users.length, users.map((u) => u.name).join(","));
