"""Shared helpers for the handbook checks.

Rules are Markdown level-3 headings that start with a rule ID, for example:

    ### PY-PERF-001: Prefer sets for repeated membership tests
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HANDBOOK_DIR = REPO_ROOT / "handbook"
SOURCE_LOCALE = "en"
MIRROR_LOCALES = ("pt-BR",)
RETIRED_IDS_FILE = HANDBOOK_DIR / "retired-ids.txt"

SCOPES = frozenset(
    {
        "CORE",
        "JAVA",
        "PY",
        "JS",
        "TS",
        "HTML",
        "CSS",
        "SPRING",
        "FLASK",
        "REST",
        "GIT",
        "MD",
        "LIB",
    }
)
LENSES = frozenset({"SEC", "PERF", "MAINT", "IMPACT"})

RULE_HEADING = re.compile(r"^###\s+([A-Z]+-[A-Z]+-\d{3})\b")
RULE_ID_FORMAT = re.compile(r"^(?P<scope>[A-Z]+)-(?P<lens>[A-Z]+)-(?P<num>\d{3})$")
FENCE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})")


@dataclass(frozen=True)
class RuleRef:
    rule_id: str
    path: Path
    line: int


def locale_dir(locale: str, root: Path = HANDBOOK_DIR) -> Path:
    return root / locale


def markdown_files(directory: Path) -> list[Path]:
    """All Markdown files under ``directory``, as paths relative to it."""
    return sorted(p.relative_to(directory) for p in directory.rglob("*.md"))


def extract_rules(path: Path) -> list[RuleRef]:
    """Rule IDs declared in a Markdown file, in order, ignoring fenced code."""
    rules: list[RuleRef] = []
    open_fence: str | None = None  # the fence that opened the current code block
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fence = FENCE.match(line)
        if fence:
            marker = fence["fence"]
            if open_fence is None:
                open_fence = marker
                continue
            # CommonMark: a closing fence uses the same character, is at least as long, has no info string.
            if (
                marker[0] == open_fence[0]
                and len(marker) >= len(open_fence)
                and not line.strip()[len(marker) :]
            ):
                open_fence = None
                continue
        if open_fence is not None:
            continue
        match = RULE_HEADING.match(line)
        if match:
            rules.append(RuleRef(match.group(1), path, number))
    return rules


def read_retired_ids(path: Path = RETIRED_IDS_FILE) -> set[str]:
    if not path.exists():
        return set()
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            ids.add(line)
    return ids
