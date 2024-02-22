#!/bin/bash -xe

echo "Run linters and tests from script"
export VIRTUALENV_PIP=21.3.1
export PYTHONPATH=${PYTHONPATH}:${PWD}/${PACKAGE_DIR}:${PWD}/tests
export TEMPLATE_FOLDER="./templates"
pipenv sync --dev
pipenv run spectral lint --fail-on-unmatched-globs --fail-severity warn openapi.yaml
pipenv run prettier . -c
pipenv run cfn-lint ${TEMPLATE_FOLDER}/* -f parseable
pipenv run bandit -r ${PACKAGE_DIR}
pipenv run black --check .
pipenv run pylint ${PACKAGE_DIR}
pipenv run isort . --check --diff
pipenv run pytest ${UNIT_TEST_RESULTS}
