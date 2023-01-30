#!/bin/bash
docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)

for file in ./*.yml
do
  echo "start $file ing..."
  docker-compose -f $file up -d

done
