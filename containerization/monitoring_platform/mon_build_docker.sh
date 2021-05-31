#!/bin/bash
PROJECT_GIT="https://github.com/5growth/5gr-mon"
GIT_BRANCH="master"
PROJECT_DIR="mon_git"
FILE_RELEASE=".env"
ELK_VERSION=7.3.1

SCRIPT="$(readlink --canonicalize-existing "$0")"
SCRIPTPATH="$(dirname "$SCRIPT")"
cd $SCRIPTPATH

netw="5gt_nw"

if [ -d "$PROJECT_DIR" ];
    then rm -Rf $PROJECT_DIR;
fi

if [ -z $(sudo docker network ls --filter name=${netw}$ --format="{{ .Name }}") ] ; then
    sudo docker network create -d bridge ${netw} ;
fi

git clone -b $GIT_BRANCH --recurse-submodules ${PROJECT_GIT} ${PROJECT_DIR}

cd $PROJECT_DIR
LAST_COMMIT=$(git rev-parse --short=8 HEAD)
COMMIT_DATE=$(git show -s --format=%aI $LAST_COMMIT --date=local)
cd ../

TAG=$LAST_COMMIT'_'$COMMIT_DATE
TAG=${TAG//[+:]/_}


echo TAG=$TAG > $FILE_RELEASE
echo ELK_VERSION=$ELK_VERSION >> $FILE_RELEASE

sudo docker-compose up -d --build
