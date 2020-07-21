#!/bin/bash

projectRoot="$1"

if [ -z "$projectRoot" ]
then
  echo "No path to pepper_comet specified!"
  echo "In voke as"
  echo "> source $(basename $0) path/to/pepper_comet"
else
  echo "Installing $projectRoot/client"

  cd "$projectRoot/client"
  pip install -r requirements.txt
  python setup.py install
  cd -
fi
