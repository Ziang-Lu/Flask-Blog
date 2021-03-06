# -*- coding: utf-8 -*-

"""
Authentication-related models module.
"""

from datetime import datetime

from marshmallow import EXCLUDE, fields

from . import db, ma

##### MODELS #####


# For the following system, check out
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers
following = db.Table(
    'following',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


class User(db.Model):
    """
    User model.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(120), unique=True, nullable=False, index=True
    )
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    # Since we'll frequently query usernames and emails, we create indices on
    # them.
    password = db.Column(db.String(255), nullable=False)

    from_oauth = db.Column(db.Boolean, nullable=False, default=False)
    image_filename = db.Column(db.String(255), default='default.jpg')

    posts = db.relationship(
        'Post', lazy='dynamic', cascade='all, delete-orphan', backref='author'
    )  # User.posts returns a query.
    comments = db.relationship(
        'Comment', lazy=True, cascade='all, delete-orphan', backref='user'
    )  # User.comments is lazy-loading.

    # Assume follower_id -> followed_id
    following = db.relationship(
        'User',
        secondary=following,  # Association table defined above
        primaryjoin=(following.c.follower_id == id),  # Join condition for the left-side of the relationship
        secondaryjoin=(following.c.followed_id == id),  # Join condition for the right-side of the relationship
        lazy='dynamic',
        backref=db.backref('followers', lazy='dynamic'),
    )  # Both User.following and User.followers return a query.

    def follow(self, user) -> None:
        """
        Follows the given user.
        :param user: User
        :return: None
        """
        if not self._is_following(user):
            # User.following is a query.
            self.following.append(user)

    def _is_following(self, user) -> bool:
        """
        Private helper method to check whether this user is following the given
        user.
        :param: User
        :return: bool
        """
        # User.following is a query.
        return self.following.filter(following.c.followed_id == user.id).count() > 0

    def unfollow(self, user) -> None:
        """
        Unfollows the given user.
        :param user: User
        :return: None
        """
        if self._is_following(user):
            # User.following is a query.
            self.following.remove(user)


class Post(db.Model):
    """
    Post table.
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )  # When the user is updated or deleted, all of his/her posts are deleted as well.
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    likes = db.Column(db.Integer, nullable=False, default=0)
    comments = db.relationship(
        'Comment', lazy=False, cascade='all, delete-orphan', backref='post'
    )  # Post.comments is eager-loading.


class Comment(db.Model):
    """
    Comment table.
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )  # When the user is updated or deleted, all of his/her comments are deleted as well.
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )  # When the post is updated or deleted, all of its comments are deleted as well.
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )


##### SCHEMAS #####
# Note!!!!!
# The data validation is done in the upstream "flask_blog_app" on form level, so
# no validation is needed on schema level, i.e., these UserSchema and PostSchema
# is only used for data serialization.


class UserSchema(ma.Schema):
    """
    User schema.
    """

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    from_oauth = fields.Boolean()
    image_filename = fields.Str()
    following_count = fields.Method(
        serialize='_get_following_count', dump_only=True
    )
    follower_count = fields.Method(
        serialize='_get_follower_count', dump_only=True
    )

    def _get_following_count(self, obj: User) -> int:
        """
        Returns the number of following users of the given user.
        :param obj: User
        :return: int
        """
        if not obj:
            return 0
        return obj.following.count()  # User.following is a query.

    def _get_follower_count(self, obj: User) -> int:
        """
        Returns the number of followers of the given user.
        :param obj: User
        :return: int
        """
        if not obj:
            return 0
        return obj.followers.count()  # User.following is a query.

    class Meta:
        unknown = EXCLUDE


user_schema = UserSchema()


class PostSchema(ma.Schema):
    """
    Post schema.
    """

    id = fields.Int(dump_only=True)
    author = fields.Nested(
        'UserSchema', required=True, only=('username', 'email', 'image_file')
    )
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    date_posted = fields.DateTime(dump_only=True)
    likes = fields.Int()

    class Meta:
        unknown = EXCLUDE


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
