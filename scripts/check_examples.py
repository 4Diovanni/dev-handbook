"""Run the bad / good example pairs and check that both print the same output.

Layout: examples/<language>/<RULE-ID>/ with one bad and one good file. Each
file is a complete program that prints its result to stdout. A pair passes when:

* the folder name is a rule ID declared in the English handbook;
* both programs compile and exit with status 0;
* both print the same, non-empty output.

Java files are compiled with ``-Xlint:all -Werror``. Python files are linted by
Ruff in the lint step, like the rest of the repository.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from handbook_lib import HANDBOOK_DIR, REPO_ROOT, RULE_ID_FORMAT, SOURCE_LOCALE, extract_rules

EXAMPLES_DIR = REPO_ROOT / "examples"
TIMEOUT_SECONDS = 120


@dataclass(frozen=True)
class Language:
    bad: str
    good: str
    tool: str
    run: Callable[[Path, Path], list[list[str]]]  # (source file, build dir) -> commands; last one prints


def _python(source: Path, build: Path) -> list[list[str]]:
    return [[sys.executable, "-I", str(source)]]


def _java(source: Path, build: Path) -> list[list[str]]:
    return [
        ["javac", "-Xlint:all", "-Werror", "-d", str(build), str(source)],
        ["java", "-cp", str(build), source.stem],
    ]


def _javascript(source: Path, build: Path) -> list[list[str]]:
    return [["node", str(source)]]


LANGUAGES: dict[str, Language] = {
    "python": Language("bad.py", "good.py", sys.executable, _python),
    "java": Language("Bad.java", "Good.java", "javac", _java),
    "javascript": Language("bad.mjs", "good.mjs", "node", _javascript),
}


def known_rule_ids(handbook_root: Path = HANDBOOK_DIR) -> set[str]:
    source = handbook_root / SOURCE_LOCALE
    return {rule.rule_id for path in source.rglob("*.md") for rule in extract_rules(path)}


def run_program(language: Language, source: Path) -> tuple[str | None, str]:
    """Return (stdout, error). stdout is None when the program failed."""
    with tempfile.TemporaryDirectory() as build:
        output = ""
        for command in language.run(source, Path(build)):
            try:
                result = subprocess.run(
                    command,
                    cwd=source.parent,
                    capture_output=True,
                    text=True,
                    timeout=TIMEOUT_SECONDS,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                return None, f"timed out after {TIMEOUT_SECONDS}s"
            if result.returncode != 0:
                detail = (result.stderr or result.stdout).strip().splitlines()[-5:]
                program = Path(command[0]).name
                return None, f"`{program}` exited with {result.returncode}: " + " | ".join(detail)
            output = result.stdout
        return output, ""


def check_examples(
    examples_dir: Path,
    rule_ids: set[str],
    only: set[str] | None = None,
) -> tuple[list[str], int]:
    """Return (errors, number of pairs checked)."""
    errors: list[str] = []
    checked = 0
    if not examples_dir.is_dir():
        return [f"missing examples directory: {examples_dir}"], 0

    for lang_dir in sorted(p for p in examples_dir.iterdir() if p.is_dir()):
        language = LANGUAGES.get(lang_dir.name)
        if language is None:
            expected = ", ".join(LANGUAGES)
            errors.append(f"{lang_dir.name}: unknown language folder (expected one of {expected})")
            continue
        if only is not None and lang_dir.name not in only:
            continue
        if shutil.which(language.tool) is None:
            errors.append(f"{lang_dir.name}: `{language.tool}` is not installed")
            continue

        for rule_dir in sorted(p for p in lang_dir.iterdir() if p.is_dir()):
            where = f"{lang_dir.name}/{rule_dir.name}"
            if not RULE_ID_FORMAT.match(rule_dir.name):
                errors.append(f"{where}: folder name is not a rule ID")
                continue
            if rule_dir.name not in rule_ids:
                errors.append(f"{where}: {rule_dir.name} is not declared in the handbook")
                continue
            files = [rule_dir / language.bad, rule_dir / language.good]
            missing = [f.name for f in files if not f.is_file()]
            if missing:
                errors.append(f"{where}: missing {', '.join(missing)}")
                continue

            outputs = []
            for source in files:
                stdout, error = run_program(language, source)
                if stdout is None:
                    errors.append(f"{where}/{source.name}: {error}")
                outputs.append(stdout)
            checked += 1
            bad, good = outputs
            if bad is None or good is None:
                continue
            if not good.strip():
                errors.append(f"{where}: the programs print nothing, so there is nothing to compare")
            elif bad != good:
                errors.append(f"{where}: {language.good} prints a different result than {language.bad}")
    return errors, checked


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=EXAMPLES_DIR)
    parser.add_argument("--handbook", type=Path, default=HANDBOOK_DIR)
    parser.add_argument("--lang", action="append", choices=sorted(LANGUAGES), help="check only this language")
    args = parser.parse_args(argv)

    only = set(args.lang) if args.lang else None
    errors, checked = check_examples(args.root, known_rule_ids(args.handbook), only)
    for error in errors:
        print(f"error: {error}")
    if errors:
        print(f"\nexamples check failed with {len(errors)} error(s)")
        return 1
    print(f"examples check passed ({checked} pair(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
