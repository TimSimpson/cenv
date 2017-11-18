#!/bin/bash

# Runs the same stuff Tox does, but quicker.
set -e
echo '* * Flake 8 * *'
.tox/pep8/bin/flake8 --import-order-style=google
echo '* * MyPy 2.7 Mode * *'
.tox/mypy/bin/mypy --ignore-missing-imports --py2 --strict-optional --check-untyped-defs cenv
echo '* * MyPy 3.6 Mode * *'
.tox/mypy/bin/mypy --ignore-missing-imports --strict-optional --check-untyped-defs cenv
echo '* * Tests 2.7 * *'
.tox/py27/bin/pytest cenv/tests -v -s -x
echo '* * Tests 3.6 * *'
.tox/py36/bin/pytest cenv/tests -v -s -x
echo '* * OK! :) * *'
