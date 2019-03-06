PY_SRC = $(shell git ls-files | grep '.py')

test:
	tox

lint: $(PY_SRC)
	isort $(PY_SRC)
	yapf -i $(PY_SRC)
