# -*- coding: utf-8 -*-

"""
Flask models module.
"""

from datetime import datetime

from . import db


class User(db.Model):
    """
    User table.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # TODO: Add the default.jpg

    posts = db.relationship('Post', backref='author', lazy=True)
    # TODO: backref: Similar to adding a column "author" to the "Post" model
    # i.e., "post.author" will give us the actual "User" object, who authored
    #       that post.

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """
    Post table.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
