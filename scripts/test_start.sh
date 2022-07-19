#!/bin/bash

set -e
set -x

ENV='test'

python -m app.clean_test_database

pytest /workspace/app "$@"
