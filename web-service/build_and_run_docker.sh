#!/usr/bin/env bash
docker rm -f report_generator
docker build -t report_generator_image .
docker run -p 8000:80 -d --restart=always --name report_generator -t report_generator_image bash