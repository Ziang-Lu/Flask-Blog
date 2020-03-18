from celery import Celery, Task
from flask import Flask
from flask_login import LoginManager

from .config import Config

login_manager = LoginManager()


def create_app(config_class=Config) -> Flask:
    """
    Application factory.
    :param config_class:
    :return: Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from .main.routes import main_bp
    app.register_blueprint(main_bp)
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    from .posts.routes import posts_bp
    app.register_blueprint(posts_bp)

    return app
