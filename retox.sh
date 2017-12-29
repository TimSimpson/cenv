#!/bin/bash

# Runs the same stuff Tox does, but quicker.
set -e
echo '* * Flake 8 * *'
.tox/pep8/bin/flake8 --import-order-style=google cenv
echo '* * MyPy 2.7 Mode * *'
.tox/mypy/bin/mypy \
    --py2 \
    --strict-optional \
    --ignore-missing-imports \
    --disallow-untyped-calls \
    --disallow-untyped-defs \
    cenv
echo '* * MyPy 3.6 Mode * *'
.tox/mypy/bin/mypy \
    --ignore-missing-imports \
    --strict-optional \
    --disallow-untyped-calls \
    --disallow-untyped-defs \
    cenv
echo '* * Tests 2.7 * *'
PATH=$PATH:.tox/py27/bin .tox/py27/bin/pytest cenv/tests -vv -s -x
echo '* * Tests 3.6 * *'
PATH=$PATH:.tox/py36/bin .tox/py36/bin/pytest cenv/tests -vv -s -x
echo '* * OK! :) * *'
