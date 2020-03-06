from celery import Celery, Task
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from .celeryconfig import CeleryConfig
from .config import Config

login_manager = LoginManager()
mail = Mail()

celery = Celery(__name__)
celery.config_from_object(CeleryConfig, silent=True)


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

    mail.init_app(app)

    # ----- Celery Setup -----
    # Additionally configure the celery app
    class ContextTask(Task):
        """
        Adds support for Flask's application contexts.
        """
        abstract = True

        def __call__(self, *args, **kwargs):
            # Wrap the task execution in an application context
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.conf.update(app.config)
    celery.Task = ContextTask
    # ------------------------

    from .main.routes import main_bp
    app.register_blueprint(main_bp)
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    from .posts.routes import posts_bp
    app.register_blueprint(posts_bp)

    return app
