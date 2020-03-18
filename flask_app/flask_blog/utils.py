# -*- coding: utf-8 -*-

"""
Utility functions.
"""

from .celerytasks import send_email_async

USER_SERVICE = 'http://user_service:8000'
POST_SERVICE = 'http://post_service:8000'


def get_iter_pages(pages: int, page: int, edge: int=2, around: int=2) -> list:
    """
    Gets the iteration pages to display on the page bottom.
    :param pages: int
    :param page: int
    :param edge: int
    :param around: int
    :return: list
    """
    iter_pages = []
    for i in range(1, pages + 1):
        if i == page or i <= edge or i > pages - edge or i >= page - around or \
                i <= page + around:
            iter_pages.append(i)
    return iter_pages


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
