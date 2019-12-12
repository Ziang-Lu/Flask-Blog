#!/bin/bash

celery worker -A "flask_blog.celeryworker.celery" -D --loglevel=INFO
# For IO-bound application and a 4-core machine, we use (2 x # of CPUs + 1) as
# the number of workers (processes), and for each worker, we use asynchronous
# worker type based on "gevent", and allows 1000 client connections per worker.
gunicorn -w 9 --worker-class=gevent --worker-connections=1000 -b 0.0.0.0 "flask_blog:create_app()"
