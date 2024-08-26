#!/bin/bash -i

DIR="$( cd "$( dirname "$0" )" && pwd )"
echo "Script location: ${DIR}"

$DIR/.venv/bin/python $DIR/main.py