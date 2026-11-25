from pathlib import Path

from check_claude_config import check_config

READER = "---\nname: {name}\ndescription: Reviews code.\ntools: {tools}\nmodel: {model}\n---\n\nBody.\n"
SKILL = "---\nname: {name}\ndescription: {description}\n---\n\n# Skill\n"


def build(tmp_path: Path, agents: dict[str, str], skills: dict[str, str] | None = None) -> Path:
    (tmp_path / ".claude/agents").mkdir(parents=True)
    for name, text in agents.items():
        (tmp_path / f".claude/agents/{name}.md").write_text(text, encoding="utf-8")
    for folder, text in (skills or {}).items():
        (tmp_path / f".claude/skills/{folder}").mkdir(parents=True)
        (tmp_path / f".claude/skills/{folder}/SKILL.md").write_text(text, encoding="utf-8")
    return tmp_path


def test_valid_config_passes(tmp_path):
    root = build(
        tmp_path,
        {"code-reviewer": READER.format(name="code-reviewer", tools="Read, Grep, Glob", model="sonnet")},
        {"team-review": SKILL.format(name="team-review", description="Runs the team.")},
    )
    assert check_config(root) == []


def test_reviewer_with_write_tool_is_rejected(tmp_path):
    root = build(
        tmp_path, {"code-reviewer": READER.format(name="code-reviewer", tools="Read, Edit", model="sonnet")}
    )
    [error] = check_config(root)
    assert "read-only" in error and "Edit" in error


def test_implementer_may_write(tmp_path):
    text = READER.format(name="implementer", tools="Read, Edit, Write, Bash", model="sonnet")
    assert check_config(build(tmp_path, {"implementer": text})) == []


def test_name_must_match_file(tmp_path):
    root = build(tmp_path, {"perf-auditor": READER.format(name="perf", tools="Read", model="sonnet")})
    assert any("does not match file name" in e for e in check_config(root))


def test_unknown_model(tmp_path):
    root = build(tmp_path, {"a": READER.format(name="a", tools="Read", model="gpt")})
    assert any("unknown model" in e for e in check_config(root))


def test_skill_name_must_match_folder(tmp_path):
    root = build(
        tmp_path,
        {"a": READER.format(name="a", tools="Read", model="haiku")},
        {"perf-audit": SKILL.format(name="perf", description="x")},
    )
    assert any("does not match folder" in e for e in check_config(root))


def test_missing_handbook_reference(tmp_path):
    text = READER.format(name="a", tools="Read", model="haiku") + "Load handbook/en/languages/cobol.md\n"
    root = build(tmp_path, {"a": text})
    [error] = check_config(root)
    assert "handbook/en/languages/cobol.md" in error
