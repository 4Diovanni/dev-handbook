"""Check that every mirror locale matches the English source handbook.

Both trees must contain the same Markdown files, and each file pair must
declare the same rule IDs in the same order.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from handbook_lib import HANDBOOK_DIR, MIRROR_LOCALES, SOURCE_LOCALE, extract_rules, markdown_files


def check_parity(root: Path, source: str, mirrors: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    source_dir = root / source
    if not source_dir.is_dir():
        return [f"missing source locale directory: {source_dir}"]
    source_files = set(markdown_files(source_dir))

    for mirror in mirrors:
        mirror_dir = root / mirror
        if not mirror_dir.is_dir():
            errors.append(f"missing locale directory: {mirror_dir}")
            continue
        mirror_files = set(markdown_files(mirror_dir))

        for rel in sorted(source_files - mirror_files):
            errors.append(f"{mirror}: missing translation of {source}/{rel}")
        for rel in sorted(mirror_files - source_files):
            errors.append(f"{mirror}: {rel} has no {source} source file")

        for rel in sorted(source_files & mirror_files):
            src_ids = [r.rule_id for r in extract_rules(source_dir / rel)]
            dst_ids = [r.rule_id for r in extract_rules(mirror_dir / rel)]
            if src_ids != dst_ids:
                missing = [i for i in src_ids if i not in dst_ids]
                extra = [i for i in dst_ids if i not in src_ids]
                detail = []
                if missing:
                    detail.append(f"missing {', '.join(missing)}")
                if extra:
                    detail.append(f"extra {', '.join(extra)}")
                if not detail:
                    detail.append("same IDs in a different order")
                errors.append(f"{mirror}/{rel}: rule IDs differ from {source} ({'; '.join(detail)})")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=HANDBOOK_DIR)
    args = parser.parse_args(argv)

    errors = check_parity(args.root, SOURCE_LOCALE, MIRROR_LOCALES)
    for error in errors:
        print(f"error: {error}")
    if errors:
        print(f"\nparity check failed with {len(errors)} error(s)")
        return 1
    print("parity check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
