from pathlib import Path

from check_parity import check_parity


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_matching_trees_pass(tmp_path):
    write(tmp_path / "en/languages/python.md", "### PY-PERF-001: Use sets\n")
    write(tmp_path / "pt-BR/languages/python.md", "### PY-PERF-001: Use conjuntos\n")
    assert check_parity(tmp_path, "en", ("pt-BR",)) == []


def test_missing_translation_is_reported(tmp_path):
    write(tmp_path / "en/languages/java.md", "# Java\n")
    (tmp_path / "pt-BR").mkdir()
    errors = check_parity(tmp_path, "en", ("pt-BR",))
    assert errors == ["pt-BR: missing translation of en/languages/java.md"]


def test_orphan_translation_is_reported(tmp_path):
    (tmp_path / "en").mkdir()
    write(tmp_path / "pt-BR/extra.md", "# Extra\n")
    assert check_parity(tmp_path, "en", ("pt-BR",)) == ["pt-BR: extra.md has no en source file"]


def test_rule_id_mismatch_is_reported(tmp_path):
    write(tmp_path / "en/a.md", "### PY-PERF-001: A\n### PY-SEC-001: B\n")
    write(tmp_path / "pt-BR/a.md", "### PY-PERF-001: A\n")
    [error] = check_parity(tmp_path, "en", ("pt-BR",))
    assert "missing PY-SEC-001" in error


def test_rule_order_matters(tmp_path):
    write(tmp_path / "en/a.md", "### PY-PERF-001: A\n### PY-SEC-001: B\n")
    write(tmp_path / "pt-BR/a.md", "### PY-SEC-001: B\n### PY-PERF-001: A\n")
    [error] = check_parity(tmp_path, "en", ("pt-BR",))
    assert "different order" in error


def test_ids_inside_code_fences_are_ignored(tmp_path):
    write(tmp_path / "en/a.md", "```md\n### PY-PERF-009: example\n```\n")
    write(tmp_path / "pt-BR/a.md", "Sem regras.\n")
    assert check_parity(tmp_path, "en", ("pt-BR",)) == []


def test_nested_fences_are_ignored(tmp_path):
    text = (
        "````markdown\n### PY-PERF-009: example\n```python\nx = 1\n```\n"
        "### PY-PERF-010: still example\n````\n"
    )
    write(tmp_path / "en/a.md", text)
    write(tmp_path / "pt-BR/a.md", "Sem regras.\n")
    assert check_parity(tmp_path, "en", ("pt-BR",)) == []
