from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config

RATELIMIT_DEFAULT = '1 per second'

login_manager = LoginManager()
limiter = Limiter(
    default_limits=[RATELIMIT_DEFAULT], key_func=get_remote_address
)


# "Application Factory Pattern"
def create_app(config_class=Config) -> Flask:
    """
    Application factory.
    :param config_class:
    :return: Flask
    """
    app = Flask(__name__)
    # Load configuration values from the configuration class
    app.config.from_object(config_class)

    # Initialize the LoginManager object with the newly created application
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Since we'll place this web service behind a proxy server (Nginx), in order
    # for rate-limiting to get the correct remote address from
    # "X-Forwarded-For" header, we need to do some extra setup here.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    # Initialize the Limiter object with the newly created application
    limiter.init_app(app)

    # Import the blueprints, which have routes registered on them
    from .main.routes import main_bp
    # Register the blueprint on the app
    app.register_blueprint(main_bp)
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    from .posts.routes import posts_bp
    app.register_blueprint(posts_bp)

    return app
