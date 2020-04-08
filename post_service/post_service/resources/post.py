# -*- coding: utf-8 -*-

"""
Post-related RESTful API module.
"""

import requests
from flask import request
from flask_restful import Resource

from .. import db
from ..models import Comment, Post, User, following, post_schema, posts_schema, user_schema
from ..utils import USER_SERVICE, paginate


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

        username = request.args.get('user')
        if username:  # Fetch all the posts by all the users that this user follows as well as this user himself
            # r = requests.get(f'{USER_SERVICE}/users?username={username}')
            # user_data = r.json()['data']
            # followed_posts = Post.query\
            #     .join(following, (Post.user_id == following.c.followed_id))\
            #     .filter(following.c.follower_id == user_data['id'])
            # own_posts = Post.query.filter_by(user_id=user_data['id'])
            user = User.query.filter_by(username=username).first()
            followed_posts = Post.query\
                .join(following, (Post.user_id == following.c.followed_id))\
                .filter(following.c.follower_id == user.id)
            own_posts = user.posts
            return followed_posts.union(own_posts), user_schema.dump(user)

        author_name = request.args.get('author')
        if author_name:  # Fetch all the posts by this author
            author = User.query.filter_by(username=author_name).first()
            return author.posts, user_schema.dump(author)

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
        json_data = request.json
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
        db.session.delete(post)
        db.session.commit()
        return '', 204


class PostLike(Resource):
    """
    Resource for a post like.
    """

    def post(self, post_id: int):
        """
        Likes the given post.
        :param post_id: int
        :return:
        """
        post = Post.query.get(post_id)
        if not post:
            return {
                'message': 'Post not found'
            }, 404

        post.likes += 1
        db.session.commit()
        return {
            'status': 'success',
            'data': post_schema.dump(post)
        }, 201


class PostComments(Resource):
    """
    Resource for a collection of post comments.
    """

    def post(self, post_id: int):
        """
        Comments on the given post.
        :param post_id: int
        :return:
        """
        post = Post.query.get(post_id)
        if not post:
            return {
                'message': 'Post not found'
            }, 404

        comment_data = request.json
        new_comment = Comment(
            user_id=comment_data['user_id'],
            post_id=post_id,
            text=comment_data['text']
        )
        db.session.add(new_comment)
        db.session.commit()
        return {
            'status': 'success',
            'data': post_schema.dump(post)
        }, 201
