FROM ziangl/flask-blog_base

# Copy the current directory to "/flask_blog_app/" directory in the container
COPY . /flask_blog_app
# Specify the working directory as "/flask_blog_app/"
WORKDIR /flask_blog_app
# When running the application in its own container, we use Gunicorn, rather
# than the default Flask development server.
# Since we want everyone outside the Docker container to be able to access the
# application, we set the host to be "0.0.0.0"
ENTRYPOINT ["./start.sh"]
