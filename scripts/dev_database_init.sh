#!/bin/bash

set -e
set -x

ENV='development'

alembic upgrade head
