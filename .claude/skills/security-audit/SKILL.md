---
name: security-audit
description: Security audit with dev-handbook SEC rules mapped to OWASP Top 10. Use when the user asks if code is safe, or the code handles input, auth, secrets, SQL or files.
---

# Security audit

1. Define the scope: what the user named, or the current diff if nothing was named.
2. Dispatch the `stack-detector` agent to get the Load list, unless the stack is obvious from a single file.
3. Dispatch the `security-auditor` agent with the scope and the Load list.
4. Return its table as is, with one line of counts per level on top.
5. Do not apply any fix. Ask which findings the user wants applied; for approved ones, dispatch the `implementer` agent.

If agents are not available in this environment, do the same review yourself following `.claude/agents/security-auditor.md`.
