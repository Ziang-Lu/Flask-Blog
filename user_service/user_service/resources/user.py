# -*- coding: utf-8 -*-

"""
User-related RESTful API module.
"""

from typing import Tuple, Union

from flask import request
from flask_restful import Resource

from .. import bcrypt, db
from ..models import User, user_schema


def _repeat_username(username: str) -> Union[Tuple, bool]:
    """
    Private helper function to check whether the given username is repeated.
    :param username: str
    :return:
    """
    user = User.query.filter_by(username=username).first()
    if user:
        return {
            'message': 'This username has been taken.'
        }, 400
    return False


def _repeat_email(email: str) -> Union[Tuple, bool]:
    """
    Private helper function to check whether the given email is repeated.
    :param email: str
    :return:
    """
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'message': 'This email has been taken.'
        }, 400
    return False


class UserList(Resource):
    """
    Resource for a collection of users.
    """

    def get(self):
        """
        Returns a user with a specified username or email.
        :return:
        """
        username = request.args.get('username')
        email = request.args.get('email')
        if not username and not email:
            return {
                'message': 'Username or email argument not provided'
            }, 400

        if username:
            user = User.query.filter_by(username=username).first()
            if not user:
                return {
                    'message': f'No user with username {username}'
                }, 404
        else:
            user = User.query.filter_by(email=email).first()
            if not user:
                return {
                    'message': f'No user with email {email}'
                }, 404
        return {
            'status': 'success',
            'data': user_schema.dump(user)
        }

    def post(self):
        """
        Adds a new user.
        :return:
        """
        user_data = request.json
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']

        repeat_username_check = _repeat_username(username)
        if repeat_username_check:
            return repeat_username_check
        repeat_email_check = _repeat_email(email)
        if repeat_email_check:
            return repeat_email_check

        new_user = User(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8')
        )
        if 'from_oauth' in user_data:
            new_user.from_oauth = True
            new_user.image_filename = user_data['image_url']
        db.session.add(new_user)
        db.session.commit()
        return {
            'status': 'success',
            'data': user_schema.dump(new_user)
        }, 201


class UserItem(Resource):
    """
    Resource for a single user.
    """

    def get(self, id: int):
        """
        Returns the user with the given ID.
        :param id: int
        :return:
        """
        user = User.query.get(id)
        return {
            'status': 'success',
            'data': user_schema.dump(user)
        }

    def put(self, id: int):
        """
        Updates the user with the given ID.
        :param id: int
        :return:
        """
        user = User.query.get(id)

        update = request.json
        if 'username' in update:
            repeat_username_check = _repeat_username(update['username'])
            if repeat_username_check:
                return repeat_username_check
            user.username = update['username']
        if 'email' in update:
            repeat_email_check = _repeat_email(update['email'])
            if repeat_email_check:
                return repeat_email_check
            user.email = update['email']
        if 'image_filename' in update:
            user.image_filename = update['image_filename']
        db.session.commit()
        return {
            'status': 'success',
            'data': user_schema.dump(user)
        }


class UserAuth(Resource):
    """
    Resource for user authentication.
    """

    def get(self):
        """
        Handles user authentication.
        :return:
        """
        email = request.args['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            return {
                'message': f'No user with email {email}'
            }, 404

        if not bcrypt.check_password_hash(
            user.password, request.json['password']
        ):
            return {
                'message': 'Login unsuccessful. Please check your email and '
                           'password.'
            }, 401
        return {
            'status': 'success',
            'data': user_schema.dump(user)
        }


class UserFollow(Resource):
    """
    Resource for user following relationship.
    """

    def post(self, follower_id: int, followed_username: str):
        """
        Lets the given follower follow the user with the given username.
        :param follower_id: int
        :param followed_username: str
        :return:
        """
        followed = User.query.filter_by(username=followed_username).first()
        if not followed:
            return {
                'message': f'No user with username {followed_username}'
            }, 404
        if follower_id == followed.id:
            return {
                'message': 'You cannot follow yourself.'
            }, 400

        follower = User.query.get(follower_id)
        follower.follow(followed)
        db.session.commit()
        return {
            'status': 'success',
            'data': user_schema.dump(followed)
        }, 201

    def delete(self, follower_id: int, followed_username: str):
        """
        Lets the given follower unfollows the user with the given username.
        :param follower_id: int
        :param followed_username: str
        :return:
        """
        followed = User.query.filter_by(username=followed_username).first()
        if not followed:
            return {
                'message': f'No user with username {followed_username}'
            }, 404
        if follower_id == followed.id:
            return {
                'message': 'You cannot unfollow yourself.'
            }, 400

        follower = User.query.get(follower_id)
        follower.unfollow(followed)
        db.session.commit()
        return {}, 204
