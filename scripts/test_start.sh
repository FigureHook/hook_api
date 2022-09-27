#!/bin/bash

# set -e
# set -x

ENV='test'
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

echo "Build test database with image..."
docker run \
    -p 5432:5432 \
    -e POSTGRES_USER=kappa \
    -e POSTGRES_PASSWORD=test \
    -e POSTGRES_DB=hook_api_test \
    --name $CONTAINER_NAME \
    -d \
    $POSTGRES_IMAGE

echo "Run the test."
coverage run -m pytest
coverage report -m --skip-covered

clean_container $CONTAINER_NAME
