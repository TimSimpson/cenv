#!/bin/bash

# Runs the same stuff Tox does, but quicker.
set -e
python ci.py flake8
python ci.py mypy
echo '* * Tests 2.7 * *'
PATH=$PATH:.tox/py27/bin .tox/py27/bin/pytest cenv/tests -vv -s -x
echo '* * Tests 3.6 * *'
PATH=$PATH:.tox/py36/bin .tox/py36/bin/pytest cenv/tests -vv -s -x
echo '* * OK! :) * *'
