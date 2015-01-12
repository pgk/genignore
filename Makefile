PYTHON?=python2.7
ENV?=env
VIRTUALENV?=virtualenv

deps: rmpyc
	rm -rf $(ENV)
	mkdir -p $(ENV)
	virtualenv --python=$(PYTHON) --no-site-packages $(ENV)
	$(ENV)/bin/pip install nose
	$(ENV)/bin/pip install mock
	$(ENV)/bin/pip install pep8
	$(ENV)/bin/python setup.py develop

rmpyc:
	find . -name "*.pyc" -exec rm -rf {} \;

test: rmpyc
	$(ENV)/bin/nosetests genignore/tests

.PHONY: deps