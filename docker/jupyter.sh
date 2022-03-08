#!/usr/bin/bash

WORKDIR=/home/ec2-user/demo/dev/docker

docker run -it -p 8888:8888 -v ${WORKDIR}:/home/jovyan/work --rm --name jupyter jupyter/datascience-notebook
