# -*- coding: utf-8 -*-

"""
Flask models module.
"""

from typing import Optional

import requests
from flask_login import UserMixin

from . import login_manager


class User(UserMixin):
    """
    Self-defined User class, which represents a user of the application.
    """

    def from_json(self, user_data: dict):
        """
        Populates this User object from the given user data.
        :param user_data: dict
        :return: User
        """
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.image_file = user_data['image_file']
        return self


@login_manager.user_loader
def user_loader(user_id: int) -> Optional[User]:
    """
    Flask-login user loader for reloading the logged-in user from the session.
    :param user_id: int
    :return: User or None
    """
    user_data = _get_user(user_id)
    if user_data:
        return User().from_json(user_data)


def _get_user(id: int) -> Optional[dict]:
    """
    Private helper function to return the user with the given email.
    :param id: int
    :return: dict or None
    """
    r = requests.get(f'http://user_post_service:8000/users/{id}')
    if r.status_code == 200:
        return r.json()['data']
