# -*- coding: utf-8 -*-

"""
Flask application configurations module.
"""


class Config:
    """
    Flask application configuration class.
    """

    # Generate the secret key using secrets.token_hex(16)
    SECRET_KEY = '1bafd5e75e63859c3e417239328fac7b'

    # Configure the SQLAlchemy-related options
    postgres_user = 'postgres'
    postgres_password = 'password'
    postgres_hostname = 'db'
    postgres_db = 'flask_blog'
    SQLALCHEMY_DATABASE_URI = f'postgres://{postgres_user}:{postgres_password}@{postgres_hostname}/{postgres_db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
