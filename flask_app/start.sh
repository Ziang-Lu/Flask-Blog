#!/bin/bash

celery worker -A "flask_blog.celeryworker.celery" -D --loglevel=INFO
gunicorn -w 4 -b 0.0.0.0 "flask_blog:create_app()"
