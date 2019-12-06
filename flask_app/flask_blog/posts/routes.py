# -*- coding: utf-8 -*-

"""
Flask post-related routes module.
"""

from datetime import datetime

import flask_login
import requests
from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for
)

from . import forms
from .utils import send_email
from .. import RATELIMIT_DEFAULT, limiter, mail

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
        flash(r.json()['message'], category='dangerous')
        return redirect(url_for('main.home'))
    post_data = r.json()['data']
    post_data['date_posted'] = datetime.fromisoformat(post_data['date_posted'])
    context = {
        'title': post_data['title'],
        'post': post_data
    }
    return render_template('post_detail.html', **context)


@posts_bp.route('/posts/<int:id>', methods=['POST'])
@flask_login.login_required
def like_post(id: int):
    """
    Likes a post.
    :param id: int
    :return:
    """
    r = requests.put(
        f'http://post_service:8000/posts/{id}', json={'like': True}
    )
    if r.status_code == 404:
        flash(r.json()['message'], category='dangerous')
        return redirect(url_for('main.home'))
    post_data = r.json()['data']
    author_email = post_data['author']['email']
    send_email(
        recipient=author_email,
        subject='Someone Liked Your Post!',
        body=f'{flask_login.current_user.username} liked your post! Check it '
             f'out!'
    )  # Internally a Celery asynchronous task
    return redirect(url_for('posts.post_detail', id=id))


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
                'user_id': flask_login.current_user.id,
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
        flash(r.json()['message'], category='dangerous')
        return redirect(url_for('main.home'))
    post_data = r.json()['data']

    form = forms.PostForm()
    if form.validate_on_submit():  # "POST" request successful
        r = requests.put(
            f'http://post_service:8000/posts/{id}',
            json={
                'operator_id': flask_login.current_user.id,
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
            'operator_id': flask_login.current_user.id
        }
    )
    if r.status_code == 204:
        flash('Your post has been deleted.', category='success')
    else:
        abort(r.status_code)
    return redirect(url_for('main.home'))
