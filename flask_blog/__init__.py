from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_blog import forms


app = Flask(__name__)
app.config.from_object(__name__)
# Generate the secret key using secret.token_hex(16)
app.config['SECRET_KEY'] = '8c2c224e4d10a93e56aa869c10d5e314'
# Configure the SQLAlchemy database connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from . import routes
