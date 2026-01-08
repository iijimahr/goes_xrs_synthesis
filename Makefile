###
### Task runner for code development
###

.PHONY: test
test:
	@make pytest
	@make doctest
	@make type-check
	@make lint
	@make format-check

.PHONY: pytest
pytest:
	pytest

.PHONY: doctest
doctest:
	sphinx-build -b doctest docs docs/_build/doctest

.PHONY: lint
lint:
	ruff check .

.PHONY: type-check
type-check:
	ruff check .
	ty check .

.PHONY: format
format:
	ruff format .

.PHONY: format-check
format-check:
	ruff format --check .

.PHONY: docs
docs:
	sphinx-build -b html docs docs/_build/html

.PHONY: clean
clean:
	rm -rf docs/_build .pytest_cache .ruff_cache
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
