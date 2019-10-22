# -*- coding: utf-8 -*-

"""
Flask post-related routes module.
"""

import flask_login
from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for
)

from . import forms
from .. import db, limiter
from ..models import Post

# Create a posts-related blueprint
posts_bp = Blueprint(name='posts', import_name=__name__)
# Rate-limit all the routes registered on this blueprint.
limiter.limit()(posts_bp)


@posts_bp.route('/post/<int:post_id>')
def post_detail(post_id: int):
    """
    Post detail page.
    :param post_id: int
    :return:
    """
    post = Post.query.get_or_404(post_id, description='Post not found')

    context = {
        'title': post.title,
        'post': post
    }
    return render_template('post_detail.html', **context)


@posts_bp.route('/post/new', methods=['GET', 'POST'])
@flask_login.login_required
def new_post():
    """
    Post creation page.
    :return:
    """
    form = forms.PostForm()
    if form.validate_on_submit():  # "POST" request successful
        post = Post(
            user_id=flask_login.current_user.id,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('main.home'))

    context = {
        'title': 'New Post',
        'form': form,
        'legend': 'New Post'
    }
    return render_template('post_form.html', **context)


@posts_bp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@flask_login.login_required
def update_post(post_id: int):
    """
    Post detail page.
    :param post_id: int
    :return:
    """
    post = Post.query.get_or_404(post_id, description='Post not found')
    if post.author != flask_login.current_user:
        abort(403)

    form = forms.PostForm()
    if form.validate_on_submit():  # "POST" request successful
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('posts.post_detail', post_id=post.id))
    elif request.method == 'GET':  # "GET" request
        # Populate the form with the current post's data
        form.title.data = post.title
        form.content.data = post.content

    context = {
        'title': 'Update Post',
        'form': form,
        'legend': 'Update Post'
    }
    return render_template('post_form.html', **context)


@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@flask_login.login_required
def delete_post(post_id: int):
    """
    Delete post page.
    :param post_id: int
    :return:
    """
    post = Post.query.get_or_404(post_id, description='Post not found')
    if post.author != flask_login.current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', category='success')
    return redirect(url_for('main.home'))
