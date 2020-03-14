FROM ziangl/flask-blog_base

# Copy the current directory to "/flask_blog_app/" directory in the container
COPY . /flask_blog_app
# Specify the working directory as "/flask_blog_app/"
WORKDIR /flask_blog_app

# Set environment variables
ENV FLASK_SECRET_KEY 8c2c224e4d10a93e56aa869c10d5e314
# PostgresSQL
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
# Google Sign-In
ENV GOOGLE_APP_CLIENT_ID 513794990149-5n8q524podj4l6r7dr1a7ri0klcrir21.apps.googleusercontent.com
# GitHub Sign-In
ENV GITHUB_APP_CLIENT_ID Iv1.390bd8ecd5f318a0
ENV GITHUB_APP_CLIENT_SECRET 22af471157619fefaf12597174f8c8510345e87e
# Flask-Mail
ENV MAIL_USERNAME luziang_apply2019@163.com
ENV MAIL_PASSWORD kevinlue1005

# When running the application in its own container, we use Gunicorn, rather
# than the default Flask development server.
# Since we want everyone outside the Docker container to be able to access the
# application, we set the host to be "0.0.0.0"
ENTRYPOINT ["./start.sh"]
