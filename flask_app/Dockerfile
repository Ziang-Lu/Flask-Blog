FROM python:3.7-stretch
LABEL maintainer="luziang1005@gmail.com"
# Setting for Python 3 encoding
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

# Copy the current directory to "./flask_blog_app" directory in the container
COPY . /flask_blog_app
# Specify the working directory as "./flask_blog_app"
WORKDIR /flask_blog_app
# Install all the dependency packages
RUN pip3 install -r requirements.txt
# When running the application in its own container, we use Gunicorn, rather
# than the default Flask development server.
ENTRYPOINT ["gunicorn", "-w", "4", "flask_blog:create_app()"]
