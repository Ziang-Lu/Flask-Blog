# -*- coding: utf-8 -*-

"""
Flask application configurations module.
"""


class Config:
    """
    Flask application configuration class.
    """

    # Generate the secret key using secrets.token_hex(16)
    SECRET_KEY = '8c2c224e4d10a93e56aa869c10d5e314'

    # Configure the SQLAlchemy database connection URI
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'password'
    POSTGRES_HOSTNAME = 'db'  # Note that this needs to be the same as the hostname of "db" service container
    POSTGRES_DB = 'flask_blog'
    SQLALCHEMY_DATABASE_URI = f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configure the Flask-Email related options
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'luziang_apply2019@163.com'
    MAIL_PASSWORD = 'kevinlue1005'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
