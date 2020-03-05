#!/bin/bash

# Build and tag the service images
docker-compose build
docker tag flask-blog_nginx ziangl/flask-blog_nginx
docker tag flask-blog_user_service ziangl/flask-blog_user_service
docker tag flask-blog_post_service ziangl/flask-blog_post_service
docker tag flask-blog_flask ziangl/flask-blog_flask

# Remove dangling images
docker rmi $(docker images -f "dangling=true" -q)
