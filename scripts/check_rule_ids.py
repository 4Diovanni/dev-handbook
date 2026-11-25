"""Validate rule IDs in the source handbook.

* Format is SCOPE-LENS-NNN with a known scope and lens.
* Each ID is declared once.
* Retired IDs (handbook/retired-ids.txt) are never reused.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from handbook_lib import (
    HANDBOOK_DIR,
    LENSES,
    RULE_ID_FORMAT,
    SCOPES,
    SOURCE_LOCALE,
    extract_rules,
    read_retired_ids,
)


def check_rule_ids(locale_root: Path, retired: set[str]) -> list[str]:
    errors: list[str] = []
    seen: dict[str, str] = {}
    for path in sorted(locale_root.rglob("*.md")):
        for rule in extract_rules(path):
            where = f"{path.relative_to(locale_root.parent)}:{rule.line}"
            match = RULE_ID_FORMAT.match(rule.rule_id)
            if not match:
                errors.append(f"{where}: malformed rule ID {rule.rule_id}")
                continue
            if match["scope"] not in SCOPES:
                errors.append(f"{where}: unknown scope {match['scope']} in {rule.rule_id}")
            if match["lens"] not in LENSES:
                errors.append(f"{where}: unknown lens {match['lens']} in {rule.rule_id}")
            if match["num"] == "000":
                errors.append(f"{where}: rule numbers start at 001 ({rule.rule_id})")
            if rule.rule_id in retired:
                errors.append(f"{where}: {rule.rule_id} is retired and cannot be reused")
            if rule.rule_id in seen:
                errors.append(f"{where}: duplicate {rule.rule_id} (first declared at {seen[rule.rule_id]})")
            else:
                seen[rule.rule_id] = where
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=HANDBOOK_DIR)
    args = parser.parse_args(argv)

    retired = read_retired_ids(args.root / "retired-ids.txt")
    errors = check_rule_ids(args.root / SOURCE_LOCALE, retired)
    for error in errors:
        print(f"error: {error}")
    if errors:
        print(f"\nrule ID check failed with {len(errors)} error(s)")
        return 1
    print("rule ID check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
