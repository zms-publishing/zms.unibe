#!/bin/bash

cd $(dirname $0)
BASEDIR=$(pwd)

DOCKER_IMAGE_NAME1="ep-devops.id.unibe.ch:5000/id/unibe-cmsapi"

cd ${BASEDIR}

if [ $# -eq 0 ] ; then
    echo 'Starting local build'
    docker build -t ${DOCKER_IMAGE_NAME1}:local .
    exit 1
fi

BRANCH=$1

# TODO: muss aus git flow kommen
VERSION=1
VERSION_TAG=""
if [[ ${BRANCH} = "master" ]] ; then
    VERSION_TAG=${VERSION}
elif [[ ${BRANCH} =~ ^release\/.* ]] ; then
    VERSION_TAG=rc-${VERSION}
else
    VERSION_TAG="latest"
fi

docker build -t ${DOCKER_IMAGE_NAME1}:${VERSION_TAG} .
docker tag ${DOCKER_IMAGE_NAME1}:${VERSION_TAG} ${DOCKER_IMAGE_NAME1}:latest
docker push ${DOCKER_IMAGE_NAME1}:${VERSION_TAG}
docker push ${DOCKER_IMAGE_NAME1}:latest
