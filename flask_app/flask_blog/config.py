# -*- coding: utf-8 -*-

"""
Flask application configurations module.
"""

import os


class Config:
    """
    Flask application configuration class.
    """

    # Generate the secret key using secrets.token_hex(16)
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']

    # Configure the SQLAlchemy database connection URI
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    POSTGRES_HOSTNAME = 'db'  # Note that this needs to be the same as the hostname of "db" service container
    POSTGRES_DB = 'flask_blog'
    SQLALCHEMY_DATABASE_URI = f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class CeleryFlaskConfig:
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']

    # Configure the Flask-Mail related options
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
