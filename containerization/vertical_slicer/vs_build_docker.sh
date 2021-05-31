#!/bin/bash
PROJECT_GIT="https://github.com/5growth/5gr-vs"
GIT_BRANCH="master"
PROJECT_DIR="vs_git"
FILE_RELEASE=".env"


SCRIPT="$(readlink --canonicalize-existing "$0")"
SCRIPTPATH="$(dirname "$SCRIPT")"
cd $SCRIPTPATH

netw="5gt_nw"

if [ -d "$PROJECT_DIR" ];
    then sudo rm -Rf $PROJECT_DIR;
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


#cat > ${PROJECT_DIR}/SEBASTIAN_WEB_GUI/index.html <<EOM
#<head>
#<meta http-equiv="refresh" content="1;URL=sebastian_web_gui" />
#</head>
#EOM
sudo docker-compose build --no-cache
sudo docker-compose up -d
