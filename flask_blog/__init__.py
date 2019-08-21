from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(__name__)
# Generate the secret key using secret.token_hex(16)
app.config['SECRET_KEY'] = '8c2c224e4d10a93e56aa869c10d5e314'
# Configure the SQLAlchemy database connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from . import routes
