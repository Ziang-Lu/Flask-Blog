# -*- coding: utf-8 -*-

"""
Flask application configurations module.
"""


class Config:
    """
    Flask application configuration class.
    """

    # Generate the secret key using secret.token_hex(16)
    SECRET_KEY = '8c2c224e4d10a93e56aa869c10d5e314'
    # Configure the SQLAlchemy database connection URI
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'password'
    POSTGRES_HOSTNAME = 'db'  # Note that this needs to be the same as the hostname of "db" service container
    POSTGRES_DB = 'flask_blog'
    SQLALCHEMY_DATABASE_URI = f'postgres+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}/{POSTGRES_DB}'
