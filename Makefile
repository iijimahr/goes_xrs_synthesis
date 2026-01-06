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
