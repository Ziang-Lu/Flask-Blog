#!/bin/bash

# This shell script is only for using a Docker container to run the application.

source ./env.sh

# Since we want everyone to be able to access the application, we set the host
# to be "0.0.0.0"
flask run --host="0.0.0.0"
