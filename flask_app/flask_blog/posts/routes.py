# -*- coding: utf-8 -*-

"""
Flask post-related routes module.
"""

from datetime import datetime

import flask_login
import requests
from flask import (
    Blueprint, abort, current_app, flash, redirect, render_template, request,
    url_for
)
from flask_login import current_user

from . import forms
from .. import RATELIMIT_DEFAULT, limiter
from ..utils import send_email

# Create a posts-related blueprint
posts_bp = Blueprint(name='posts', import_name=__name__)
# Rate-limit all the routes registered on this blueprint.
limiter.limit(RATELIMIT_DEFAULT)(posts_bp)


@posts_bp.route('/posts/<int:id>')
def post_detail(id: int):
    """
    Post detail page.
    :param id: int
    :return:
    """
    r = requests.get(f'http://post_service:8000/posts/{id}')
    if r.status_code == 404:
        flash(r.json()['message'], category='danger')
        return redirect(url_for('main.home'))
    post_data = r.json()['data']
    # Convert the datetime strings back to objects
    post_data['date_posted'] = datetime.fromisoformat(post_data['date_posted'])
    for comment in post_data['comments']:
        comment['date_posted'] = datetime.fromisoformat(comment['date_posted'])

    context = {
        'title': post_data['title'],
        'post': post_data
    }
    return render_template('post_detail.html', **context)


@posts_bp.route('/like-post/<int:post_id>', methods=['POST'])
@flask_login.login_required
def like_post(post_id: int):
    """
    Likes a post.
    :param post_id: int
    :return:
    """
    r = requests.post(f'http://post_service:8000/posts/{post_id}/likes')
    if r.status_code == 404:
        flash(r.json()['message'], category='danger')
        return redirect(url_for('main.home'))
    post_data = r.json()['data']
    send_email(
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipient=post_data['author']['email'],
        subject='Someone Liked Your Post!',
        body=f'{current_user.username} liked your post! Check it out!'
    )  # Internally a Celery asynchronous task
    return redirect(url_for('posts.post_detail', id=post_id))


@posts_bp.route('/comment-post/<int:post_id>', methods=['POST'])
@flask_login.login_required
def comment_post(post_id: int):
    """
    Comments a post.
    :param post_id: int
    :return:
    """
    comment = request.form['comment']
    r = requests.post(
        f'http://post_service:8000/posts/{post_id}/comments',
        json={
            'user_id': current_user.id,
            'post_id': post_id,
            'text': comment
        }
    )
    if r.status_code == 404:
        flash(r.json()['message'], category='danger')
        return redirect(url_for('main.home'))
    post_data = r.json()['data']
    send_email(
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipient=post_data['author']['email'],
        subject='Someone Commented on Your Post!',
        body=f'{current_user.username} commented on your post! Check it out!'
    )  # Internally a Celery asynchronous task
    return redirect(url_for('posts.post_detail', id=post_id))


@posts_bp.route('/posts/new', methods=['GET', 'POST'])
@flask_login.login_required
def new_post():
    """
    Post creation page.
    :return:
    """
    form = forms.PostForm()
    if form.validate_on_submit():  # "POST" request successful
        r = requests.post(
            'http://post_service:8000/posts',
            json={
                'user_id': current_user.id,
                'title': form.title.data,
                'content': form.content.data
            }
        )
        if r.status_code == 201:
            flash('Your post has been created!', category='success')
            return redirect(url_for('main.home'))

    context = {
        'title': 'New Post',
        'form': form,
        'legend': 'New Post'
    }
    return render_template('post_form.html', **context)


@posts_bp.route('/posts/<int:id>/update', methods=['GET', 'POST'])
@flask_login.login_required
def update_post(id: int):
    """
    Post detail page.
    :param id: int
    :return:
    """
    r = requests.get(f'http://post_service:8000/posts/{id}')
    if r.status_code == 404:
        flash(r.json()['message'], category='danger')
        return redirect(url_for('main.home'))
    post_data = r.json()['data']

    form = forms.PostForm()
    if form.validate_on_submit():  # "POST" request successful
        r = requests.put(
            f'http://post_service:8000/posts/{id}',
            json={
                'operator_id': current_user.id,
                'title': form.title.data,
                'content': form.content.data
            }
        )
        if r.status_code == 200:
            flash('Your post has been updated!', category='success')
            return redirect(url_for('posts.post_detail', id=post_data['id']))
        else:
            abort(r.status_code)
    elif request.method == 'GET':  # "GET" request
        # Populate the form with the current post's data
        form.title.data = post_data['title']
        form.content.data = post_data['content']

    context = {
        'title': 'Update Post',
        'form': form,
        'legend': 'Update Post'
    }
    return render_template('post_form.html', **context)


@posts_bp.route('/posts/<int:id>/delete', methods=['POST'])
@flask_login.login_required
def delete_post(id: int):
    """
    Delete post page.
    :param id: int
    :return:
    """
    r = requests.delete(
        f'http://post_service:8000/{id}',
        json={
            'operator_id': current_user.id
        }
    )
    if r.status_code == 204:
        flash('Your post has been deleted.', category='success')
    else:
        abort(r.status_code)
    return redirect(url_for('main.home'))
