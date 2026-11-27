PYTHON ?= python3

.PHONY: check test lint parity ids claude attribution examples docs

check: lint test parity ids claude attribution examples

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

parity:
	$(PYTHON) scripts/check_parity.py

ids:
	$(PYTHON) scripts/check_rule_ids.py

claude:
	$(PYTHON) scripts/check_claude_config.py

attribution:
	$(PYTHON) scripts/check_ai_attribution.py --files

examples:
	$(PYTHON) scripts/check_examples.py

docs:
	mkdocs serve
