#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PYCODE_DIR=$(dirname "$SCRIPT_DIR")

echo "Looking for pytests in ${PYCODE_DIR} and its subdirectories"
cd ${PYCODE_DIR}

echo "Checking number of student pytests..."
numtests=$(python -m pytest --collect-only -q --ignore=autograder | grep 'Function test_' | wc -l)
# check that there are at least 5 tests
if [ $numtests -lt 5 ]; then
    echo "*** FAIL: Not enough tests: found $numtests tests (expected at least 5)"
    exit 1
else
    echo ">>> PASS: Found $numtests tests"
fi

echo "Running student pytests"
python -m pytest -vs --ignore=autograder
if [ $? -eq 0 ]; then
    echo ">>> PASS: All tests passed"
else
    echo "*** FAIL: Some tests failed"
    exit 1
fi
