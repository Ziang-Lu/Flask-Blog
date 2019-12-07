# -*- coding: utf-8 -*-

"""
Flask authentication-related utility functions module.
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
    picture_data.save(saved_path)
    return saved_filename
