PYTHON?=python2.7
PYTHON_THREE?=`which python3`
ENV?=env
VIRTUALENV?=virtualenv

deps: clean venv develop

deps3: clean venv3 develop

venv:
	virtualenv --python=$(PYTHON) --no-site-packages $(ENV)

venv3:
	$(PYTHON_THREE) -m venv $(ENV)

develop:
	$(ENV)/bin/python setup.py develop

clean: rmpyc
	rm -rf $(ENV)
	mkdir -p $(ENV)

rmpyc:
	find . -name "*.pyc" -exec rm -rf {} \;

release:
	# sdist
	rm -rf dist
	$(ENV)/bin/python setup.py sdist
	twine upload dist/*

.PHONY: deps deps3 release
