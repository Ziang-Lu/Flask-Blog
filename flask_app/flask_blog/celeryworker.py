# -*- coding: utf-8 -*-

"""
Celery process instantiation module.

The Celery application runs in another process, which cannot share the Flask
with the main process. However, in the Celery application (within the tasks), we
may need configuration values in the Flask application.
Therefore, we need to create a separate Flask application with the same
configuration.
"""

from . import celery, create_app

app = create_app()
