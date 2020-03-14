FROM ziangl/flask-blog_base

# Copy the current directory to "/user_service/" directory in the container
COPY . /user_service
# Specify the working directory as "/user_service/"
WORKDIR /user_service

# Set environment variables
ENV FLASK_SECRET_KEY 1bafd5e75e63859c3e417239328fac7b
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password

ENTRYPOINT ["gunicorn", "-w", "9", "--worker-class", "gevent", "--worker-connections", "1000",  "-b", "0.0.0.0", "user_service:create_app()"]
