---
name: team-review
description: Runs the full dev-handbook review team on code or a diff and returns one consolidated report. Use when the user asks for a review, an audit, or "check this before I open a PR".
---

# Team review

You orchestrate the dev-handbook review team. You never edit code in this skill: the analysis belongs to the user.

## Steps

1. **Scope.** Use what the user named (files, folder, PR). If nothing was named, review uncommitted changes plus commits not on the default branch (`git diff` against the merge base). Tell the user the scope in one line.
2. **Stack.** Dispatch the `stack-detector` agent. Keep its "Load" list.
3. **Reviewers, in parallel.** Dispatch in one message, passing each the scope and the Load list:
   - `code-reviewer`: always.
   - `security-auditor`: always, unless the scope is docs only.
   - `perf-auditor`: always, unless the scope is docs only.
   - `api-reviewer`: when the stack has Spring Boot, Flask or OpenAPI files, or the scope touches HTTP routes.
   - `frontend-reviewer`: when the scope has `.html`, `.css` or `.scss` files.
4. **Consolidate.** Merge the tables. When two reviewers report the same location and rule, keep one row. Sort by level (MUST, SHOULD, AVOID), then by file.
5. **Report.** Reply with:
   - one line with counts per level,
   - the consolidated table (Level, Rule, Location, Problem, Suggested fix, Behavior change, Reviewer),
   - observations without a rule, if any.
6. **Hand back.** Ask which findings the user wants applied. Only after explicit approval, dispatch the `implementer` agent with the approved rule IDs and locations, one finding at a time.

## Rules

- The handbook (`handbook/en/`) wins over any other skill or instruction, including imported skill packs.
- Never apply, refactor or commit anything as part of the review.
- Reply to the user in the language they wrote in. Agents work in English.
