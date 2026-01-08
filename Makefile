###
### Task runner for code development
###

.PHONY: test
test:
	@make pytest
	@make doctest
	@make lint
	@make format

.PHONY: pytest
pytest:
	pytest

.PHONY: doctest
doctest:
	sphinx-build -b doctest docs docs/_build/doctest

.PHONY: lint
lint:
	ruff check .
	ty check .

.PHONY: format
format:
	ruff format .

.PHONY: docs
docs:
	sphinx-build -b html docs docs/_build/html

.PHONY: clean
clean:
	rm -rf docs/_build .pytest_cache .ruff_cache
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
