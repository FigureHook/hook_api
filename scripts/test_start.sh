#!/bin/bash

set -e
set -x

ENV='test'

python -m app.clean_test_database

coverage run -m pytest /workspace/app "$@"
coverage report -m --skip-covered
