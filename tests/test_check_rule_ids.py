from pathlib import Path

from check_rule_ids import check_rule_ids


def make(tmp_path: Path, files: dict[str, str]) -> Path:
    root = tmp_path / "en"
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


def test_valid_ids_pass(tmp_path):
    root = make(tmp_path, {"python.md": "### PY-PERF-001: A\n### PY-SEC-001: B\n"})
    assert check_rule_ids(root, set()) == []


def test_duplicate_across_files(tmp_path):
    root = make(tmp_path, {"a.md": "### JAVA-SEC-001: A\n", "b.md": "### JAVA-SEC-001: B\n"})
    [error] = check_rule_ids(root, set())
    assert "duplicate JAVA-SEC-001" in error


def test_unknown_scope_and_lens(tmp_path):
    root = make(tmp_path, {"a.md": "### RUBY-FAST-001: A\n"})
    errors = check_rule_ids(root, set())
    assert any("unknown scope RUBY" in e for e in errors)
    assert any("unknown lens FAST" in e for e in errors)


def test_number_zero_rejected(tmp_path):
    root = make(tmp_path, {"a.md": "### CSS-MAINT-000: A\n"})
    [error] = check_rule_ids(root, set())
    assert "start at 001" in error


def test_retired_id_cannot_return(tmp_path):
    root = make(tmp_path, {"a.md": "### REST-SEC-002: A\n"})
    [error] = check_rule_ids(root, {"REST-SEC-002"})
    assert "retired" in error
