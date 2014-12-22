PYTHON?=python2.7
ENV?=env
VIRTUALENV?=virtualenv

deps:
	rm -rf $(ENV)
	mkdir -p $(ENV)
	virtualenv --python=$(PYTHON) --no-site-packages $(ENV)
	$(ENV)/bin/python setup.py develop

rmpyc:
	find . -name "*.pyc" -exec rm -rf {} \;

.PHONY: deps