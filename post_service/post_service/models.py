# -*- coding: utf-8 -*-

"""
Authentication-related models module.
"""

from datetime import datetime

from marshmallow import EXCLUDE, fields

from . import db, ma

##### MODELS #####


class User(db.Model):
    """
    User model.
    """
    __tablename__ = 'users'

    IMAGE_FILE_MAX_LEN = 20

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    # Since we'll frequently query usernames and emails, we create indices on
    # them,
    password = db.Column(db.String(255), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    # Since the relationship is lazy-loaded, "user.posts" is loaded from the
    # database only when actually accessing it.

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


##### SCHEMAS #####
# Note!!!!!
# The data validation is done in the upstream "flask_blog_app" on form level, so
# no validation is needed on schema level, i.e., these UserSchema and PostScehma
# is only used for data serialization.


class UserSchema(ma.Schema):
    """
    User schema.
    """

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    image_file = fields.Str()


    class Meta:
        unknown = EXCLUDE


user_schema = UserSchema()


class PostSchema(ma.Schema):
    """
    Post schema.
    """

    id = fields.Int(dump_only=True)
    author = fields.Nested(
        UserSchema, required=True, only=('username', 'image_file')
    )
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    date_posted = fields.DateTime(dump_only=True)

    class Meta:
        unknown = EXCLUDE


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
