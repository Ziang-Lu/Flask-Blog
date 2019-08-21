# -*- coding: utf-8 -*-

"""
Flask user-related utility functions module.
"""

import os
import secrets

from flask import current_app


def save_picture(username: str, picture_data) -> str:
    """
    Saves the given picture file for the given user.
    :param username: str
    :param picture_data:
    :return: str
    """
    user_random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(picture_data.filename)
    saved_filename = f'{username}_{user_random_hex}{ext}'
    saved_path = os.path.join(
        current_app.root_path, 'static/profile_pics', saved_filename
    )
    # Note that since we used "Application Factory Pattern", we don't have
    # access to an "app" object, so we need to use "current_app" proxy to access
    # the current application

    # # Resize the picture if it is too large
    # img = Image.open(picture_data)
    # if img.width > 300 or img.height > 300:
    #     img.thumbnail((300, 300))
    #     img.save(saved_path)

    picture_data.save(saved_path)
    return saved_filename
