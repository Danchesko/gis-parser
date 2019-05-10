#!/bin/bash

project_name=parser
selenium=selenium/standalone-chrome

echo deleting container if exists
docker container rm -f $project_name

echo deleting image if exists 
docker image rm $(docker image ls -q $project_name | uniq)

echo building new image 
docker build -t $project_name .

echo delete selenium if exists
docker container rm -f `docker ps -a -q  --filter ancestor=$selenium`

echo running selenium standalone chrome
docker run -p 4444:4444 -d $selenium

echo wait for selenium to run
sleep 10

echo running project 
while ! docker run --name=$project_name --net=host -it --rm $project_name
do
    echo apparently selenium crashed, booting it up again
    docker container rm -f `docker ps -a -q  --filter ancestor=$selenium`
    docker run -p 4444:4444 -d $selenium
    sleep 10
done