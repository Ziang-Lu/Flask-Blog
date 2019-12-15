# -*- coding: utf-8 -*-

"""
API definition module.
"""

from flask import Blueprint
from flask_restful import Api

from .resources.post import PostComments, PostItem, PostLike, PostList

# Create an API-related blueprint
api_bp = Blueprint(name='api', import_name=__name__)

api = Api(api_bp)
api.add_resource(PostList, '/posts')
api.add_resource(PostItem, '/posts/<int:id>')
api.add_resource(PostLike, '/posts/<int:post_id>/likes')
api.add_resource(PostComments, '/posts/<int:post_id>/comments')
