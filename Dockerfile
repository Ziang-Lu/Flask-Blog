FROM alpine:latest
LABEL maintainer="luziang1005@gmail.com"
# Install Bash
RUN apk add --update bash && rm -rf /var/cache/apk/*
# Later on to install the Python package "cffi", install some necessary stuff
RUN apk add --update build-base libffi-dev openssl-dev
# Install Python 3 and pip, and upgrade pip
RUN apk add --no-cache python3-dev && pip3 install -U pip
# Setting for Python 3 encoding
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

# Copy the current directory to "./flask_blog_app" directory in the container
COPY . /flask_blog_app
# Specify the working directory as "./flask_blog_app"
WORKDIR /flask_blog_app
# Install all the dependency packages
RUN pip3 install -r requirements.txt
# Expose port 5000
EXPOSE 5000
# When the container is run, initialize the database as necessary, and run the
# applcation
ENTRYPOINT ["./docker_run.sh"]
