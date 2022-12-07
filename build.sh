#!/bin/bash

cd $(dirname $0)
BASEDIR=$(pwd)

IMAGE_API="ep-devops.id.unibe.ch:5000/id/unibe-cmsapi-v3"

cd ${BASEDIR}

if [ $# -eq 0 ] ; then
    echo BUILDING API
    docker build -t ${IMAGE_API}:local .
    echo '======================================================'

    echo BUILDING DOCS
    docker build -t squidfunk/mkdocs-material:local docs
    echo '======================================================'

    exit 1
fi

BRANCH=$1

# TODO: muss aus git flow kommen
VERSION="3.0.0"
VERSION_TAG=""
if [[ ${BRANCH} = "master" || ${BRANCH} = "main" ]] ; then
    VERSION_TAG=${VERSION}
elif [[ ${BRANCH} =~ ^release\/.* ]] ; then
    VERSION_TAG=rc-${VERSION}
else
    VERSION_TAG="latest"
fi

echo BUILDING API
docker build -t ${IMAGE_API}:${VERSION_TAG} .
docker tag ${IMAGE_API}:${VERSION_TAG} ${IMAGE_API}:latest
docker push ${IMAGE_API}:${VERSION_TAG}
docker push ${IMAGE_API}:latest
echo '======================================================'
