# -*- coding: utf-8 -*-

"""
Celery application tasks module.
"""

from typing import List

from flask_mail import Message

from . import celery, mail


@celery.task(ignore_result=True)
def send_email_async(sender: str, recipients: List[str], subject: str,
                     body: str) -> None:
    """
    Celery asynchronous task to send an email to the given recipient, with the
    given subject and body.
    IMPORTANT NOTE!!!!!
    The parameters must be serializable!!!!! In this case, we are passing a list
    of strings, as well as pure strings, which is totally fine.
    :param sender: str
    :param recipients: list[str]
    :param subject: str
    :param body: str
    :return: None
    """
    msg = Message(subject, sender=sender, recipients=recipients, body=body)
    mail.send(msg)
