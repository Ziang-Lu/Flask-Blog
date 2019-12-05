# -*- coding: utf-8 -*-

"""
Post-related RESTful API module.
"""

import requests
from flask import request
from flask_restful import Resource

from .. import db
from ..models import Post, User, post_schema, posts_schema
from ..utils import paginate


class PostList(Resource):
    """
    Resource for a collection of posts.
    """

    @paginate(posts_schema)
    def get(self):
        """
        Returns all the posts.
        :return:
        """
        # For pagination, we need to return a query that hasn't run yet.
        username = request.args.get('username')
        if username:
            user = User.query.filter_by(username=username).first()
            r = requests.get(
                f'http://user_service:8000/users?username={username}'
            )
            if r.status_code == 404:
                return r.json(), r.status_code
            user_data = r.json()['data']
            return Post.query.filter_by(user_id=user_data['id'])

        return Post.query

    def post(self):
        """
        Adds a new post.
        :return:
        """
        post_data = request.json
        new_post = Post(
            user_id=post_data['user_id'],
            title=post_data['title'],
            content=post_data['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return {
            'status': 'success',
            'data': post_schema.dump(new_post)
        }, 201


class PostItem(Resource):
    """
    Resource for a single post.
    """

    def get(self, id: int):
        """
        Returns the post with the given ID.
        :param id: int
        :return:
        """
        post = Post.query.get(id)
        if not post:
            return {
                'message': 'Post not found'
            }, 404
        return {
            'status': 'success',
            'data': post_schema.dump(post)
        }

    def put(self, id: int):
        """
        Updates the post with the given ID.
        :param id: int
        :return:
        """
        post = Post.query.get(id)
        if not post:
            return {
                'message': 'Post not found'
            }, 404

        json_data = request.json

        if 'like' in json_data:  # Simply like the post
            post.likes += 1
            db.session.commit()
            return {
                'status': 'success',
                'data': post_schema.dump(post)
            }

        operator_id = json_data['operator_id']
        if operator_id != post.user_id:
            return {
                'message': 'Only the author of the post can operate on it.'
            }, 403

        post.title = json_data['title']
        post.content = json_data['content']
        db.session.commit()
        return {
            'status': 'success',
            'data': post_schema.dump(post)
        }

    def delete(self, id: int):
        """
        Deletes the post with the given ID.
        :param id: int
        :return:
        """
        post = Post.query.get(id)
        if not post:
            return {
                'message': 'Post not found'
            }, 404

        operator_id = request.json['operator_id']
        if operator_id != post.user_id:
            return {
                'message': 'Only the author of the post can operate on it.'
            }, 403

        db.session.delete(post)
        db.session.commit()
        return '', 204
