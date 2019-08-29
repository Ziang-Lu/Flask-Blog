import flask_bcrypt
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flask_blog.config import Config

db = SQLAlchemy()

bcript = flask_bcrypt.Bcrypt()

login_manager = LoginManager()


# "Application Factory Pattern"
def create_app(config_class=Config) -> Flask:
    """
    Application factory.
    :param config_class:
    :return: Flask
    """
    app = Flask(__name__)
    # Load configuration values from the configuration class
    app.config.from_object(Config)

    # Initialize the SQLAlchemy object with the newly created application
    db.init_app(app)

    # Initialize the Bcrypt object with the newly created application
    bcript.init_app(app)

    # Initialize the LoginManager object with the newly created application
    login_manager.init_app(app)
    login_manager.login_view = 'users_bp.login'
    login_manager.login_message_category = 'info'

    # Import the blueprints, which have routes registered on them
    from flask_blog.main.routes import main_bp
    from flask_blog.auth.routes import auth_bp
    from flask_blog.posts.routes import posts_bp
    # Register the blueprints on the app
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)

    # Initialize the database
    with app.app_context():
        db.create_all()

    return app
