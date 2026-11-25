"""Validate the agents, skills and commands in .claude/.

* Agents: frontmatter with name (matching the file name), description, tools and model.
* Only agents listed in WRITE_ALLOWED may have tools that change files or run commands.
* Skills: one folder per skill with a SKILL.md whose name matches the folder.
* Every handbook path mentioned in these files must exist.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
READ_ONLY_TOOLS = frozenset({"Read", "Grep", "Glob"})
WRITE_ALLOWED = frozenset({"implementer"})
MODELS = frozenset({"haiku", "sonnet", "opus", "inherit"})
NAME_FORMAT = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HANDBOOK_PATH = re.compile(r"handbook/(?:en|pt-BR)/[\w./-]*?\.(?:md|txt)|handbook/retired-ids\.txt")
MAX_DESCRIPTION = 1024


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse simple `key: value` frontmatter. Returns None when there is none."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return None


def check_agent(path: Path) -> list[str]:
    where = path.as_posix()
    meta = parse_frontmatter(path.read_text(encoding="utf-8"))
    if meta is None:
        return [f"{where}: missing frontmatter"]
    errors = []
    for key in ("name", "description", "tools", "model"):
        if not meta.get(key):
            errors.append(f"{where}: missing '{key}'")
    name = meta.get("name", "")
    if name and name != path.stem:
        errors.append(f"{where}: name '{name}' does not match file name '{path.stem}'")
    if meta.get("model") and meta["model"] not in MODELS:
        errors.append(f"{where}: unknown model '{meta['model']}'")
    tools = {t.strip() for t in meta.get("tools", "").split(",") if t.strip()}
    extra = sorted(tools - READ_ONLY_TOOLS)
    if extra and path.stem not in WRITE_ALLOWED:
        errors.append(f"{where}: reviewers must be read-only, found {', '.join(extra)}")
    return errors


def check_skill(skill_dir: Path) -> list[str]:
    skill_file = skill_dir / "SKILL.md"
    where = skill_file.as_posix()
    if not skill_file.is_file():
        return [f"{skill_dir.as_posix()}: missing SKILL.md"]
    meta = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
    if meta is None:
        return [f"{where}: missing frontmatter"]
    errors = []
    name, description = meta.get("name", ""), meta.get("description", "")
    if not name:
        errors.append(f"{where}: missing 'name'")
    elif name != skill_dir.name:
        errors.append(f"{where}: name '{name}' does not match folder '{skill_dir.name}'")
    elif not NAME_FORMAT.match(name):
        errors.append(f"{where}: name must be lowercase words joined by hyphens")
    if not description:
        errors.append(f"{where}: missing 'description'")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"{where}: description longer than {MAX_DESCRIPTION} characters")
    return errors


def check_handbook_links(path: Path, repo_root: Path) -> list[str]:
    errors = []
    for ref in sorted(set(HANDBOOK_PATH.findall(path.read_text(encoding="utf-8")))):
        if not (repo_root / ref).exists():
            errors.append(f"{path.as_posix()}: references missing file {ref}")
    return errors


def check_config(repo_root: Path) -> list[str]:
    claude_dir = repo_root / ".claude"
    if not claude_dir.is_dir():
        return [f"missing {claude_dir}"]
    errors: list[str] = []
    agents = sorted((claude_dir / "agents").glob("*.md"))
    if not agents:
        errors.append(".claude/agents: no agents found")
    for agent in agents:
        errors += check_agent(agent)
    skills_dir = claude_dir / "skills"
    if skills_dir.is_dir():
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            errors += check_skill(skill_dir)
    for md in sorted(claude_dir.rglob("*.md")):
        errors += check_handbook_links(md, repo_root)
    return [e.replace(f"{repo_root.as_posix()}/", "") for e in errors]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)
    errors = check_config(args.root.resolve())
    for error in errors:
        print(f"error: {error}")
    if errors:
        print(f"\n.claude check failed with {len(errors)} error(s)")
        return 1
    print(".claude check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
