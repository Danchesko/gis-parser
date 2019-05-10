#!/bin/bash

project_name=parser
selenium=selenium/standalone-chrome

echo deleting container if exists
docker container rm -f $project_name

echo deleting image if exists 
docker image rm $(docker image ls -q $project_name | uniq)

echo building new image 
docker build -t $project_name .

echo stop running selenium 
docker container rm -f `docker ps -a -q  --filter ancestor=$selenium`

echo running selenium standalone chrom
docker run -p 4444:4444 -d $selenium

echo running project 
docker run --name=$project_name -d $project_name 