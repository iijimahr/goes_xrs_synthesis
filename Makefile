###
### Task runner for code development
###

.PHONY: test
test:
	@make pytest
	@make doctest

.PHONY: pytest
pytest:
	pytest

.PHONY: doctest
doctest:
	sphinx-build -b doctest docs docs/_build/doctest


.PHONY: doc
doc:
	sphinx-build -b html docs docs/_build/html

.PHONY: clean
clean:
	rm -rf docs/_build .pytest_cache
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
