#!/bin/bash

# Build, tag and push the base image
docker build -f Dockerfile_base . -t flask-blog_base
docker tag flask-blog_base ziangl/flask-blog_base
docker push ziangl/flask-blog_base
