# Bash Script to clean everything including running containers
# their associated volumes and their images.
# Warning take backup before you tear down everything in production.

echo "Initiating Kill Script"
echo "
/**
* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* ~__        ___    ____  _   _ ___ _   _  ____ ~
* ~\ \      / / \  |  _ \| \ | |_ _| \ | |/ ___|~
* ~ \ \ /\ / / _ \ | |_) |  \| || ||  \| | |  _ ~
* ~  \ V  V / ___ \|  _ <| |\  || || |\  | |_| |~
* ~   \_/\_/_/   \_\_| \_\_| \_|___|_| \_|\____|~
* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
"
echo "!!!This will kill everything including docker containers , images and volumes.!!!"
echo "!!!The script will start after a delay of 10 seconds. Consider exiting the script before that happens.!!!"
echo ">> Press Cmd / Ctrl C  to stop execution and exit."
#sleep 10
#!/bin/bash

echo "Starting Kill Script"
# Stop all running containers
docker stop $(docker ps -q)

# Delete all stopped containers
docker rm $(docker ps -a -q)

# Delete all associated volumes
docker volume rm $(docker volume ls -q)

# Delete all associated images
docker rmi $(docker images -q)

echo "Clean Script Completed"