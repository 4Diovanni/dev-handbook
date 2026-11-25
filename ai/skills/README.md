# Skills

Claude Code skills that apply the handbook. Each skill has a short `SKILL.md` that says when to act and which handbook files to load for the detected stack. Every skill reports findings with rule IDs and never edits code.

| Skill | Triggers on | Output |
| --- | --- | --- |
| `handbook-review` | "review this code", before a pull request | Findings by rule ID, level and line, sorted by severity |
| `perf-audit` | "this is slow", "optimize" | Bottlenecks with estimated gain, behavior unchanged |
| `security-audit` | External input, auth, SQL | Risks mapped to OWASP Top 10 and `*-SEC-*` rules |
| `api-review` | Spring controllers, Flask routes, OpenAPI | Deviations from the REST rules |
| `commit-guide` | Writing commits or pull requests | Conventional Commits message with no attribution lines |

Status: planned for phase 4. Until the plugin exists, copy this folder into a project's `.claude/skills/`.
