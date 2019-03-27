.PHONY: clean clean-test clean-pyc clean-build dev venv help requirements-dev.txt
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
dev: venv requirements-dev.txt tests/data/source.sqlite ## setup dev environment
	venv/bin/pip-sync requirements-dev.txt

venv: ## create virtual environment
	python3 -m venv venv
	venv/bin/pip3 install pip-tools

requirements-dev.txt: requirements-dev.in ## create dev requirements
	venv/bin/pip-compile -o requirements-dev.txt \
	--no-header \
	--no-annotate \
	--no-index \
	--no-emit-trusted-host \
	requirements-dev.in

tests/data/source.sqlite: ## download test spatialite database
	wget -O $@ --show-progress https://storage.googleapis.com/tm-geomancer/test/source.sqlite

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
