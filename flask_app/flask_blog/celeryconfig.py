# -*- coding: utf-8 -*-

"""
Celery application configurations module.
"""

from datetime import timedelta

imports = ('flask_blog.celerytasks')

broker_url = 'redis://redis:6379/1'
task_serializer = 'json'
accept_content = ['json', 'pickle']

task_track_started = True

task_ignore_result = False
result_backend = 'redis://redis:6379/1'
result_serializer = 'json'
result_accept_content = ['json']

broker_transport_options = {
    'fanout_prefix': True,  # Broadcast messages only to active virtual hosts
    'fanout_patterns': True  # Workers may only subscribe to worker-related events.
}
