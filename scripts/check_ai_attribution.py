"""Block AI-assistant attribution in commit messages, PR bodies and files.

This repository is authored by its owner. Tool-generated trailers such as
co-author lines for AI assistants, session links or "generated with" banners
are rejected. Writing *about* AI tools (as handbook content) is allowed: only
attribution patterns are matched.

Usage:
    check_ai_attribution.py --message-file .git/COMMIT_EDITMSG   # commit-msg hook
    check_ai_attribution.py --git-range origin/main..HEAD        # CI, commits
    check_ai_attribution.py --text "$PR_BODY"                    # CI, PR body
    check_ai_attribution.py --files                              # CI, tracked files
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

AI_TOOLS = r"(claude|anthropic|copilot|chatgpt|openai|gemini|cursor|codeium|tabnine|devin|aider)"

PATTERNS: dict[str, re.Pattern[str]] = {
    "AI co-author trailer": re.compile(rf"^[ \t]*co-authored-by:.*{AI_TOOLS}", re.I | re.M),
    "AI session trailer": re.compile(rf"^[ \t]*{AI_TOOLS}[\w-]*-session:", re.I | re.M),
    "AI session link": re.compile(rf"https?://\S*{AI_TOOLS}\S*/(code/)?session", re.I),
    "generated-with banner": re.compile(rf"generated\s+(with|by)\s+\[?{AI_TOOLS}", re.I),
}

# This checker and its tests have to spell the patterns out.
SELF_EXEMPT = {"scripts/check_ai_attribution.py", "tests/test_check_ai_attribution.py"}
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".java",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".xml",
    ".cfg",
    ".ini",
    ".sh",
    ".properties",
    ".gradle",
    "",
}


def find_violations(text: str) -> list[str]:
    hits = []
    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            hits.append(f"line {line}: {label}: {match.group(0).strip()}")
    return hits


def commit_messages(git_range: str) -> list[tuple[str, str]]:
    out = subprocess.run(
        ["git", "log", "--format=%H%x00%B%x1e", git_range],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    commits = []
    for record in out.split("\x1e"):
        record = record.strip("\n")
        if record:
            sha, _, body = record.partition("\x00")
            commits.append((sha[:12], body))
    return commits


def tracked_files() -> list[Path]:
    out = subprocess.run(["git", "ls-files"], check=True, capture_output=True, text=True).stdout
    return [Path(p) for p in out.splitlines() if p]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--message-file", type=Path)
    group.add_argument("--git-range")
    group.add_argument("--text")
    group.add_argument("--files", action="store_true")
    args = parser.parse_args(argv)

    problems: list[str] = []
    if args.message_file:
        text = args.message_file.read_text(encoding="utf-8")
        # Ignore comment lines git adds to the editor buffer.
        text = "\n".join(ln for ln in text.splitlines() if not ln.startswith("#"))
        problems += [f"commit message {v}" for v in find_violations(text)]
    elif args.git_range:
        for sha, body in commit_messages(args.git_range):
            problems += [f"commit {sha} {v}" for v in find_violations(body)]
    elif args.text is not None:
        problems += [f"text {v}" for v in find_violations(args.text)]
    else:
        for path in tracked_files():
            if path.as_posix() in SELF_EXEMPT or path.suffix not in TEXT_SUFFIXES or not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            problems += [f"{path} {v}" for v in find_violations(content)]

    for problem in problems:
        print(f"error: {problem}")
    if problems:
        print("\nAI attribution found. Remove these lines: this repository is authored by its owner.")
        return 1
    print("no AI attribution found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
