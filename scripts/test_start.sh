#!/bin/bash

# set -e
# set -x

ENV="test"
ENVFILE="test.env"
POSTGRES_IMAGE=postgres:14.5
CONTAINER_NAME=hook-api-test-db

docker image inspect $POSTGRES_IMAGE &>/dev/null

if [ $? -eq 1 ]; then
    echo "database image was not found."
    echo "Start pulling the image..."
    docker pull $POSTGRES_IMAGE
fi

clean_container() {
    docker stop $1 &>/dev/null
    docker rm $1 &>/dev/null
}

docker container inspect $CONTAINER_NAME &>/dev/null

if [ $? -eq 0 ]; then
    clean_container $CONTAINER_NAME
fi

if [ -f $ENVFILE ]; then
    echo "Loading environment variables in $ENVFILE"
    export $(cat $ENVFILE | xargs);
else
    echo "The '$ENVFILE' file doesn't exist.";
    exit 1
fi

echo "Build test database with image..."
docker run \
    -d \
    -p $POSTGRES_PORT:5432 \
    -e POSTGRES_USER=$POSTGRES_USER \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e POSTGRES_DB=$POSTGRES_DATABASE \
    --name $CONTAINER_NAME \
    $POSTGRES_IMAGE

echo "Run the test."
coverage run -m pytest
coverage report -m --skip-covered

clean_container $CONTAINER_NAME
