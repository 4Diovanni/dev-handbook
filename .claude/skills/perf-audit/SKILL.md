---
name: perf-audit
description: Performance audit with dev-handbook PERF rules, keeping behavior unchanged. Use when the user says code is slow, asks to optimize, or worries about memory or cost.
---

# Performance audit

1. Define the scope: what the user named, or the current diff if nothing was named.
2. Dispatch the `stack-detector` agent to get the Load list, unless the stack is obvious from a single file.
3. Dispatch the `perf-auditor` agent with the scope and the Load list.
4. Return its table as is, with one line of counts per level on top.
5. Do not apply any fix. Ask which findings the user wants applied; for approved ones, dispatch the `implementer` agent.

If agents are not available in this environment, do the same review yourself following `.claude/agents/perf-auditor.md`.
