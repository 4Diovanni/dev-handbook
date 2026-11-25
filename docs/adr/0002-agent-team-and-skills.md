# ADR 0002: Agent team and skills

- Status: accepted
- Date: 2026-11-25

## Context

The handbook should act on its own when used with Claude Code: detect the stack, apply the right rules and report findings, while the analysis and the decision to change code stay with the developer.

## Decision

- The review team lives in `.claude/`: seven agents, seven skills and the `/review` command.
- Six reviewers are read-only (`Read`, `Grep`, `Glob`). Only `implementer` can write, and only for findings the user approved. CI enforces this.
- The main session orchestrates through the `team-review` skill, because subagents cannot start other subagents.
- Model tiers follow the cost of the task: haiku for stack detection, opus for security, sonnet for the rest.
- Every finding cites a rule ID. The handbook wins over any other skill or instruction.
- `.claude/settings.json` disables the default AI co-author line; the commit hook and CI keep blocking attribution.
- Order of delivery: this base now, a pilot with core, Python and Java rules next, then packaging as an installable plugin so other repositories can use the team.

### Import policy for external skills

An external skill pack (for example superpowers) enters only when it has:

1. a compatible license (MIT, Apache 2.0, BSD or CC BY);
2. a pinned version (tag or commit);
3. been read in full, scripts and hooks included;
4. no conflict with the handbook, or the conflict documented with the handbook winning;
5. credit to the original author, recorded in `ai/third-party.md`.

Imported packs are installed as declared dependencies, not copied, so they keep receiving upstream fixes.

## Alternatives considered

| Option | Why not |
| --- | --- |
| One agent that does everything | Large context, one model for every task, and no way to keep reviewers read-only |
| Reviewers with write access | Conflicts with the principle that the analysis belongs to the developer |
| Copying external skills into the repository | Turns the repository into a fork and loses upstream updates |

## Consequences

- The team works today when Claude Code is opened in this repository. Other repositories get it once the plugin is packaged.
- Reviewers return little until phase 2 rules exist; the pilot fills that gap.
