#!/bin/bash

LACK_FLAG=0
ENVFILE="dev.env"
CONTAINER_NAME="hook-api-dev-db"
POSTGRES_IMAGE="postgres:14.5"

check_command() {
    if ! command -v $1 &>/dev/null; then
        echo -e "[\033[31;1mx\033[0m] \033[36;1m$1\033[0m is not installed."
        IS_LACK=1
    fi
    echo -e "[\033[32;1mv\033[0m] \033[36;1m$1\033[0m is installed."
}

commands=('poetry' 'docker')
echo "Checking necessary commands..."
for command in ${commands[@]}; do
    check_command $command
done

if [ $LACK_FLAG != 0 ]; then
    exit 1
fi

if [ $VIRTUAL_ENV == "" ]; then
    poetry shell
fi

echo "Installing dependencies..."
poetry install

if docker container inspect $CONTAINER_NAME &>/dev/null ; then
    echo "Container name: $CONTAINER_NAME was used."
    exit 1
fi

if [ -f $ENVFILE ]; then
    echo "Loading environment variables in $ENVFILE"
    export $(cat $ENVFILE | xargs);
else
    echo "The '$ENVFILE' file doesn't exist.";
    exit 1
fi

echo "Start database containers."; echo
docker compose up -d

ENV="development"
echo; echo "Migrating database..."
alembic upgrade head

echo
docker compose ps
echo
