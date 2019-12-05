# -*- coding: utf-8 -*-

"""
Flask posts-related utility functions module.
"""

from ..celerytasks import *


def send_email(recipient: str, subject: str, body: str) -> None:
    """
    Sends an email to the given recipient, with the given subject and body.
    :param recipient: str
    :param subject: str
    :param body: str
    :return: None
    """
    # Call the Celery asynchronous task
    send_email_async.delay([recipient], subject, body)
    # IMPORTANT NOTE!!!!!
    # The arguments passed to a Celery task must be serializable!!!!! In this
    # case, we are passing a list of strings, as well as pure strings, which is
    # totally fine.
