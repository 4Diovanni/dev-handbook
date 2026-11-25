---
name: rule-author
description: Adds or changes a rule in the dev-handbook, in English and Brazilian Portuguese, with a valid rule ID. Use when the user wants to add, edit or retire a handbook rule.
---

# Rule author

1. Read `handbook/en/_template.md` and the target file in `handbook/en/`.
2. Pick the ID: `SCOPE-LENS-NNN`, the next free number for that scope and lens. Never reuse an ID listed in `handbook/retired-ids.txt`.
3. Write the English rule first: heading with ID and title, level, lens, why in at most two sentences, a minimal bad / good pair, exceptions, source. Keep it short: assistants load this file.
4. Write the same rule in `handbook/pt-BR/` at the same position, with the same ID, level and code. The prose may explain more.
5. To retire a rule: remove it from both locales and add its ID to `handbook/retired-ids.txt` with a reason. This is a breaking change (`feat!:`).
6. Run `make check` (or `python3 scripts/check_parity.py && python3 scripts/check_rule_ids.py`) and fix what fails.
7. Show the user both versions before committing. Commit with the `commit-guide` skill.
