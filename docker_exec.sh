#!/bin/bash

docker build -f Dockerfile_base . -t flask-blog_base
docker tag flask-blog_base ziangl/flask-blog_base
docker-compose build
docker tag flask-blog_nginx ziangl/flask-blog_nginx
docker tag flask-blog_user_service ziangl/flask-blog_user_service
docker tag flask-blog_post_service ziangl/flask-blog_post_service
docker tag flask-blog_flask ziangl/flask-blog_flask
docker rmi $(docker images -f "dangling=true" -q)
