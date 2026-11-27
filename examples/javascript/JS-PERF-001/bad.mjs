// JS-PERF-001, bad: independent async calls awaited one after another.
const fetchUser = (id) => new Promise((resolve) => setTimeout(() => resolve({ id, name: `user-${id}` }), 20));

const ids = Array.from({ length: 20 }, (_, i) => i + 1);
const users = [];
for (const id of ids) {
  users.push(await fetchUser(id));
}
console.log(users.length, users.map((u) => u.name).join(","));
