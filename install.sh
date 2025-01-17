#!/bin/bash

echo "This script with install dependency both in local and in docker."


if [ -z "$1" ]; then
    echo "Error: Dependency not provided as CL arg."
    exit 1
else
    echo Installing "$1" in local machine.
    pip3 install "$1"

    echo Installing "$1" inside Docker.
    docker exec -it server bash -c "pip3 install $1"
fi


echo "Installation complete."