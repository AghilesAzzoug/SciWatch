SHELL=/bin/bash

export PYTHONPATH:=${PYTHONPATH}:${PWD}/src

LINTER_THRESHOLD ?= 3
COVERAGE_THRESHOLD ?= 90
VULTURE_THRESHOLD = 80

REPORT_OUTPUT_DIRECTORY = "reports"
COVERAGE_HTML_DIR = ./${REPORT_OUTPUT_DIRECTORY}/html_coverage
TESTS_HTML_DIR = ./${REPORT_OUTPUT_DIRECTORY}/html_unit_tests

.PHONY: install
install:
	@poetry install --no-dev

.PHONY: install-dev
install-dev:
	@poetry install

.PHONY: format
format:
	@poetry run python -m black -t py38 src/*

.PHONY: linter
linter:
	@poetry run python -m pylint --fail-under ${LINTER_THRESHOLD} --rcfile=.pylintrc src/*

.PHONY: pre-commit
pre-commit:
	@poetry run pre-commit run --all-files

.PHONY: sort-imports
sort-imports:
	@poetry run python -m isort src/* tests/*

.PHONY: find-dead-code
find-dead-code:
	@poetry run python -m vulture --min-confidence ${VULTURE_THRESHOLD} src/* tests/*

.PHONY: coverage
coverage:
	@poetry run python -m coverage run -m pytest tests/* --html=${TESTS_HTML_DIR}/html_report.html --self-contained-html

.PHONY: coverage-report-html
coverage-report-html:
	@poetry run python -m coverage html -d ${COVERAGE_HTML_DIR}

.PHONY: reports
reports: coverage coverage-report-html
	@poetry run python -m coverage report --fail-under=${COVERAGE_THRESHOLD}

.PHONY: build
build:
	@poetry build -n

.PHONY: docs
docs: clean-docs
	@poetry run sphinx-apidoc -T -M -e -o docs src/sci_watch/
	@poetry run sphinx-build -M html docs docs/_build

.PHONY: clean-docs
clean-docs:
	@rm -rf ${DOCUMENT_BUILD_PATTERN}