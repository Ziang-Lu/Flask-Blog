# -*- coding: utf-8 -*-

"""
Celery process instantiation module.

The Celery application runs in another process, which cannot share the Flask
application with the main process.
Therefore, we need to create a separate Flask application with configurations
related to Flask-Mail.
"""

from celery import Celery, Task
from flask import Flask
from flask_mail import Mail

from .celeryconfig import CeleryConfig
from .config import CeleryFlaskConfig

# Prepare a Flask app for the Celery app
app = Flask(__name__)
app.config.from_object(CeleryFlaskConfig)  # For Flask-Mail configurations

mail = Mail(app)

# Celery app
celery = Celery(__name__)
celery.config_from_object(CeleryConfig, silent=True)
# Load the Flask app configurations to the Celery app
celery.conf.update(app.config)


# Additionally configure the Celery app
class ContextTask(Task):
    """
    Adds support for Flask's application contexts.
    """
    abstract = True

    def __call__(self, *args, **kwargs):
        # Wrap the task execution in an application context
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask
