---
name: handbook-review
description: Quick single-pass review of a snippet or a single file against the dev-handbook rules, without dispatching agents. Use for small pastes or one file; use team-review for a diff or a PR.
---

# Handbook review

1. Identify the language of the snippet or file.
2. Read `handbook/en/index.md`, then load `handbook/en/core/` and only the files the index lists for that language.
3. Report findings in a table: Level, Rule, Location, Problem, Suggested fix, Behavior change. Sort by level (MUST, SHOULD, AVOID).
4. Every finding cites a rule ID. Problems without a rule go under "Observations".
5. Do not rewrite the code. Offer to apply specific findings; apply only the ones the user approves.
