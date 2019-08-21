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

    db.init_app(app)

    bcript.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'users_bp.login'
    login_manager.login_message_category = 'info'

    # Import the blueprints, which have routes registered on them
    from flask_blog.main.routes import main_bp
    from flask_blog.users.routes import users_bp
    from flask_blog.posts.routes import posts_bp

    # Register the blueprints on the app

    # main_bp.register(app)
    # users_bp.register(app)
    # posts_bp.register(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)

    return app
