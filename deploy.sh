#!/bin/bash

project_name=parser
selenium=selenium/standalone-chrome

echo DELETING CONTAINER IF EXISTS
docker container rm -f $project_name

echo DELETING IMAGE IF EXISTS 
docker image rm $(docker image ls -q $project_name | uniq)

echo BUILDING NEW IMAGE 
docker build -t $project_name .

echo DELETE SELENIUM IF EXISTS
docker container rm -f `docker ps -a -q  --filter ancestor=$selenium`

echo RUNNING SELENIUM STANDALONE CHROME
docker run -p 4444:4444 -d $selenium

echo WAIT FOR SELENIUM TO RUN
sleep 10

docker create --name=$project_name --net=host -it $project_name

echo RUNNING PROJECT 
while ! docker start $project_name
do
    echo APPARENTLY SELENIUM CRASHED, BOOTING IT UP AGAIN
    docker container rm -f `docker ps -a -q  --filter ancestor=$selenium`
    docker run -p 4444:4444 -d $selenium
    echo RESTARTING A PROJECT
    sleep 10
done

echo PARSING IS COMPLETE