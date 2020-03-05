#!/bin/bash

# Push the service images
docker push ziangl/flask-blog_nginx
docker push ziangl/flask-blog_user_service
docker push ziangl/flask-blog_post_service
docker push ziangl/flask-blog_flask
