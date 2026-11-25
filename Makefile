PYTHON ?= python3

.PHONY: check test lint parity ids attribution docs

check: lint test parity ids attribution

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

parity:
	$(PYTHON) scripts/check_parity.py

ids:
	$(PYTHON) scripts/check_rule_ids.py

attribution:
	$(PYTHON) scripts/check_ai_attribution.py --files

docs:
	mkdocs serve
