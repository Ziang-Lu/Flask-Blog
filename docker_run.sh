#!/bin/bash

# This shell script is only for using a Docker container to run the application.

source ./env.sh

# When running the application in its own container, we use Gunicorn, rather
# than the default Flask development server.
# Since we want everyone to be able to access the application, we set the host
# to be "0.0.0.0"
gunicorn -w 4 -b "0.0.0.0" "flask_blog:create_app()"
