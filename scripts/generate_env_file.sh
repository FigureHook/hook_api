#!/bin/bash

set -e

POSTGRES_URL="127.0.0.1"
POSTGRES_USER="figurehook"
POSTGRES_DATABASE="hook_api"
POSTGRES_PASSWORD="hookpw"

file="dev.env"
if [ ! -f $file ]; then
cat << EOF >  $file
ENV="development"
POSTGRES_URL=$POSTGRES_URL
POSTGRES_USER=$POSTGRES_USER
POSTGRES_DATABASE="hook_api_dev"
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_PORT=5432
FIGURE_HOOK_SECRET="$(openssl rand -base64 32)"
API_TOKEN="$(openssl rand -base64 32)"
EOF
fi

file="test.env"
if [ ! -f  $file ]; then
cat << EOF >  $file
ENV="test"
POSTGRES_URL=$POSTGRES_URL
POSTGRES_USER=$POSTGRES_USER
POSTGRES_DATABASE="hook_api_dev_test"
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_PORT=7788
EOF
fi