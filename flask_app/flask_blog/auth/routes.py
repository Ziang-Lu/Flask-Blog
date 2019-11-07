# -*- coding: utf-8 -*-

"""
Flask authentication-related routes module.
"""

import os

import flask_login
import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import forms
from .utils import save_picture
from .. import RATELIMIT_DEFAULT, limiter
from ..models import User
from ..utils import get_iter_pages

# Create a user-related blueprint
auth_bp = Blueprint(name='auth', import_name=__name__)
# Rate-limit all the routes registered on this blueprint.
limiter.limit(RATELIMIT_DEFAULT)(auth_bp)


@auth_bp.route('/users/<string:username>/posts')
def user_posts(username: str):
    """
    User posts page.
    :param username: str
    :return:
    """
    page = request.args.get('page', type=int, default=1)
    r = requests.get(
        f'http://user_post_service:8000/posts?username={username}&page={page}'
    )
    if r.status_code == 404:
        flash(r.json()['message'], category='dangerous')
        return redirect(url_for('main.home'))
    paginated_data = r.json()
    pages = paginated_data['pagination_meta']['pages']

    context = {
        'username': username,
        'p': {
            'items': paginated_data['data'],
            'page': page,
            'pages': pages,
            'total': paginated_data['pagination_meta']['total'],
            'iter_pages': get_iter_pages(pages, page)
        }
    }
    return render_template('user_posts.html', **context)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register page.
    :return:
    """
    # If a logged-in user goes to "/register", that user won't need to register
    # again, and automatically go back to the home page.
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = forms.RegistrationForm()
    if form.validate_on_submit():  # Successful passed form validation
        r = requests.post(
            'http://user_post_service:8000/users', json={
                'username': form.username.data,
                'email': form.email.data,
                'password': form.password.data,
            }
        )
        if r.status_code == 201:  # "POST" request successful
            flash(
                'Your account has been created! You are now able to log in.',
                category='success'
            )
            return redirect(url_for('auth.login'))
        else:
            flash(r.json()['message'], category='dangerous')
    context = {
        'title': 'Registration',
        'form': form
    }
    return render_template('register.html', **context)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page.
    :return:
    """
    # If a logged-in user goes to "/login", that user won't need to log in
    # again, and automatically go back to the home page.
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = forms.LoginForm()
    if form.validate_on_submit():  # Successful passed form validation
        r = requests.get(
            f'http://user_post_service:8000/user-auth?email={form.email.data}',
            json={
                'password': form.password.data
            }
        )
        if r.status_code == 200:  # "POST" request successful
            user_data = r.json()['data']
            user = User().from_json(user_data)
            flask_login.login_user(user, remember=form.remember.data)
            # If the user comes from a page which requires "logged-in", then the
            # URL will contain a "next" argument.
            # => In this case, when logged in, the user should be redirected
            #    back to that original page.
            from_page = request.args.get('next')
            if from_page:
                return redirect(from_page)
            return redirect(url_for('main.home'))
        else:
            flash(r.json()['message'], category='dangerous')
    context = {
        'title': 'Log In',
        'form': form
    }
    return render_template('login.html', **context)


@auth_bp.route('/account', methods=['GET', 'POST'])
@flask_login.login_required
def account():
    """
    Account page.
    :return:
    """
    form = forms.AccountUpdateForm()
    if form.validate_on_submit():  # Successful passed form validation
        update = {}
        if form.username.data != flask_login.current_user.username:
            update['username'] = form.username.data
        if form.email.data != flask_login.current_user.email:
            update['email'] = form.email.data
        if form.picture.data:
            saved_filename = save_picture(
                form.username.data, form.picture.data)
            update['image_file'] = saved_filename

        if update:
            user_id = flask_login.current_user.user_id
            r = requests.put(
                f'http://user_post_service/users/{user_id}',
                json=update
            )
            if r.status_code == 200:
                flask_login.current_user.username = form.username.data
                flask_login.current_user.email = form.email.data
                flask_login.current_user.image_file = saved_filename
                flash('Your account has been updated!', category='success')
            return redirect(url_for('auth.account'))
    elif request.method == 'GET':  # "GET" request
        # Populate the form with the current user's information
        form.username.data = flask_login.current_user.username
        form.email.data = flask_login.current_user.email

    image_file = url_for(
        'static',
        filename=os.path.join(
            'profile_pics', flask_login.current_user.image_file
        )
    )

    context = {
        'title': 'Account',
        'form': form,
        'image_file': image_file
    }
    return render_template('account.html', **context)


@auth_bp.route('/logout')
@flask_login.login_required
def logout():
    """
    Log-out page.
    :return:
    """
    flask_login.logout_user()
    return redirect(url_for('auth.login'))
