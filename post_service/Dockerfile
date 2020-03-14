FROM ziangl/flask-blog_base

# Copy the current directory to "/post_service/" directory in the container
COPY . /post_service
# Specify the working directory as "/post_service/"
WORKDIR /post_service

# Set environment variables
ENV FLASK_SECRET_KEY a2c6ba730959debd7e7d8d92b9b75b97
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password

ENTRYPOINT ["gunicorn", "-w", "9", "--worker-class", "gevent", "--worker-connections", "1000",  "-b", "0.0.0.0", "post_service:create_app()"]
