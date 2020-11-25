#!/usr/bin/env bash
docker rm -f report_generator_doc
docker rmi report_generator_image
docker build -t report_generator_image . --no-cache
docker run -p 8077:80 -d --restart=always --name report_generator_doc -t report_generator_image 
