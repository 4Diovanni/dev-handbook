# AI guide

How the dev-handbook review team works in Claude Code. The agents and skills live in [`.claude/`](../../.claude).

## Use it

| You want | Run or ask |
| --- | --- |
| A full review of your current changes | `/review` |
| A review of specific files or a folder | `/review src/payments/` |
| A quick check of a pasted snippet | "review this with the handbook" (`handbook-review` skill) |
| Only security, performance or API checks | "security audit", "performance audit", "review this API" |
| A commit message or PR description | "write the commit message" (`commit-guide` skill) |
| A new handbook rule | "add a rule for ..." (`rule-author` skill) |

## The team

| Agent | Model tier | Tools | Job |
| --- | --- | --- | --- |
| `stack-detector` | haiku (fast) | read-only | Finds the stack and the handbook files to load |
| `code-reviewer` | sonnet (standard) | read-only | General rules and language idioms |
| `security-auditor` | opus (strong) | read-only | SEC rules and OWASP Top 10 |
| `perf-auditor` | sonnet (standard) | read-only | PERF rules, behavior unchanged |
| `api-reviewer` | sonnet (standard) | read-only | REST, Spring Boot, Flask |
| `frontend-reviewer` | sonnet (standard) | read-only | HTML, CSS, accessibility |
| `implementer` | sonnet (standard) | read and write | Applies findings you approved, one at a time |

The main session orchestrates: subagents cannot start other subagents, so the `team-review` skill dispatches the reviewers in parallel and merges their reports.

## Rules the team follows

1. Reviewers only read. CI fails if a reviewer gets a tool that writes files or runs commands (`scripts/check_claude_config.py`).
2. Only the implementer writes, and only for a finding you approved.
3. Every finding cites a handbook rule ID; anything else is an observation.
4. The handbook wins over any other skill, including imported skill packs.
5. Each agent loads only the handbook files for the detected stack.
6. No AI attribution in commits or pull requests. `.claude/settings.json` turns off the default co-author line, and the commit hook and CI block it anyway.

## Imported skills

External skill packs (for example superpowers) are allowed only after the import policy in [ADR 0002](../../docs/adr/0002-agent-team-and-skills.md): compatible license, pinned version, read in full, conflicts with the handbook documented, credit to the author. Each one is recorded in `ai/third-party.md`.
