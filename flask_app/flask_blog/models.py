# -*- coding: utf-8 -*-

"""
Flask models module.
"""

from datetime import datetime
from typing import Union

from flask_login import UserMixin

from flask_blog import db, login_manager


class User(db.Model, UserMixin):
    """
    User table.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)  # Since the relationship is lazy-loaded, "user.posts" is loaded from the database only when actually accessing it.

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """
    Post table.
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )  # When the user is deleted, all of his/her posts are deleted as well.
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


@login_manager.user_loader
def user_loader(user_id: int) -> Union[User, None]:
    """
    Flask-login user loader for reloading the logged-in user from the session.
    :param user_id: str
    :return: User or None
    """
    return User.query.get(user_id)
