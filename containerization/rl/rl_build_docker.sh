#!/bin/bash
PROJECT_GIT="https://github.com/5growth/5gr-rl"
PROJECT_DIR="rl_git"
GIT_BRANCH="master"
FILE_RELEASE=".env"

SCRIPT="$(readlink --canonicalize-existing "$0")"
SCRIPTPATH="$(dirname "$SCRIPT")"
cd $SCRIPTPATH

netw="5gt_nw"

if [ -z $(sudo docker network ls --filter name=${netw}$ --format="{{ .Name }}") ] ; then
    sudo docker network create -d bridge ${netw} ;
fi

if [ -d "$PROJECT_DIR" ];
    then rm -Rf $PROJECT_DIR;
fi
git clone -b $GIT_BRANCH --recurse-submodules ${PROJECT_GIT} ${PROJECT_DIR}

cd $PROJECT_DIR
LAST_COMMIT=$(git rev-parse --short=8 HEAD)
COMMIT_DATE=$(git show -s --format=%aI $LAST_COMMIT --date=local)
cd ../

TAG=$LAST_COMMIT'_'$COMMIT_DATE
TAG=${TAG//[+:]/_}

echo TAG=$TAG > $FILE_RELEASE

sudo docker-compose up -d
