FROM ziangl/flask-blog_base

# Copy the current directory to "/post_service/" directory in the container
COPY . /post_service
# Specify the working directory as "/post_service/"
WORKDIR /post_service
# When running the application in its own container, we use Gunicorn, rather
# than the default Flask development server.
# Since we want everyone outside the Docker container to be able to access the
# application, we set the host to be "0.0.0.0"
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0", "post_service:create_app()"]
