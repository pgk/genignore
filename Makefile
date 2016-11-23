PYTHON?=python2.7
ENV?=env
VIRTUALENV?=virtualenv

deps: clean
	virtualenv --python=$(PYTHON) --no-site-packages $(ENV)
	$(ENV)/bin/python setup.py develop

deps3: clean
		pyvenv $(ENV)
		$(ENV)/bin/python setup.py develop

clean:
	rm -rf $(ENV)
	mkdir -p $(ENV)

rmpyc:
	find . -name "*.pyc" -exec rm -rf {} \;

.PHONY: deps
