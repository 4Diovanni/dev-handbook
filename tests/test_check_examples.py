from pathlib import Path

from check_examples import check_examples

RULES = {"PY-PERF-001"}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def pair(root: Path, rule: str, bad: str, good: str) -> None:
    write(root / "python" / rule / "bad.py", bad)
    write(root / "python" / rule / "good.py", good)


def test_same_output_passes(tmp_path):
    pair(tmp_path, "PY-PERF-001", "print(sum([1, 2]))\n", "print(sum((1, 2)))\n")
    assert check_examples(tmp_path, RULES) == ([], 1)


def test_different_output_fails(tmp_path):
    pair(tmp_path, "PY-PERF-001", "print(1)\n", "print(2)\n")
    errors, _ = check_examples(tmp_path, RULES)
    assert errors == ["python/PY-PERF-001: good.py prints a different result than bad.py"]


def test_empty_output_fails(tmp_path):
    pair(tmp_path, "PY-PERF-001", "x = 1\n", "x = 1\n")
    [error], _ = check_examples(tmp_path, RULES)
    assert "print nothing" in error


def test_crash_is_reported(tmp_path):
    pair(tmp_path, "PY-PERF-001", "print(1)\n", "raise SystemExit(3)\n")
    [error], _ = check_examples(tmp_path, RULES)
    assert error.startswith("python/PY-PERF-001/good.py:")
    assert "exited with 3" in error


def test_unknown_rule_id_fails(tmp_path):
    pair(tmp_path, "PY-PERF-999", "print(1)\n", "print(1)\n")
    errors, checked = check_examples(tmp_path, RULES)
    assert errors == ["python/PY-PERF-999: PY-PERF-999 is not declared in the handbook"]
    assert checked == 0


def test_missing_file_fails(tmp_path):
    write(tmp_path / "python/PY-PERF-001/bad.py", "print(1)\n")
    errors, _ = check_examples(tmp_path, RULES)
    assert errors == ["python/PY-PERF-001: missing good.py"]


def test_unknown_language_fails(tmp_path):
    (tmp_path / "cobol").mkdir()
    [error], _ = check_examples(tmp_path, RULES)
    assert error.startswith("cobol: unknown language folder")


def test_language_filter_skips_others(tmp_path):
    pair(tmp_path, "PY-PERF-001", "print(1)\n", "print(2)\n")
    assert check_examples(tmp_path, RULES, only={"java"}) == ([], 0)
