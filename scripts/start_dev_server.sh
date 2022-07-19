#!/bin/bash

set -e
set -x

ENV='development'

uvicorn app.main:app --reload
