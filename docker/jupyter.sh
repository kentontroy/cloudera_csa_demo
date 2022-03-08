#!/usr/bin/bash

docker run -it -p 8888:8888 -v ${CML_DEMO_DIR}:/home/jovyan/work --rm --name jupyter jupyter/datascience-notebook
