# -*- coding: utf-8 -*-

"""
Flask authentication-related routes module.
"""

import os
from datetime import datetime

import flask_login
import requests
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for
)
from flask_login import current_user
from google.auth.transport import requests as g_requests
from google.oauth2 import id_token

from . import forms
from .utils import save_picture
from ..models import User
from ..utils import POST_SERVICE, USER_SERVICE, get_iter_pages, send_email

# Create a user-related blueprint
auth_bp = Blueprint(name='auth', import_name=__name__)


@auth_bp.route('/users/<string:author>/posts')
def user_posts(author: str):
    """
    User posts page.
    :param author: str
    :return:
    """
    page = request.args.get('page', type=int, default=1)
    r = requests.get(
        f'{POST_SERVICE}/posts?author={author}&page={page}&per_page=5'
    )
    if r.status_code == 404:
        flash(r.json()['message'], category='danger')
        return redirect(url_for('main.home'))
    paginated_data = r.json()
    posts_data = paginated_data['data']['posts']
    for post in posts_data:
        post['date_posted'] = datetime.fromisoformat(post['date_posted'])
    pages = paginated_data['pagination_meta']['pages']

    context = {
        'author': paginated_data['data']['user_data'],
        'p': {
            'items': posts_data,
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
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = forms.RegistrationForm()
    if form.validate_on_submit():  # Successfully passed form validation
        r = requests.post(
            f'{USER_SERVICE}/users',
            json={
                'username': form.username.data,
                'email': form.email.data,
                'password': form.password.data
            }
        )
        if r.status_code == 201:  # "POST" request successful
            flash(
                'Your account has been created! You are now able to log in.',
                category='success'
            )
            return redirect(url_for('auth.login'))
        else:
            flash(r.json()['message'], category='danger')
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
    # If a logged-in user goes to "/login", that user won't need to log-in
    # again, and automatically go back to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = forms.LoginForm()
    if form.validate_on_submit():  # Successfully passed form validation
        r = requests.get(
            f'{USER_SERVICE}/user-auth?email={form.email.data}',
            json={
                'password': form.password.data
            }
        )
        if r.status_code == 200:  # "POST" request successful
            # Log-in on the main application side
            _app_login(user_data=r.json()['data'], remember=form.remember.data)
            # If the user comes from a page which requires "logged-in", then the
            # URL will contain a "next" argument. In this case, when logged in,
            # the user should be redirected back to that original page.
            from_page = request.args.get('next')
            if from_page:
                return redirect(from_page)
            return redirect(url_for('main.home'))
        else:
            flash(r.json()['message'], category='danger')
    context = {
        'title': 'Log In',
        'form': form
    }
    return render_template('login.html', **context)


def _app_login(user_data: dict, remember: bool) -> None:
    """
    Private helper function to log-in the application user.
    :param user_data: dict
    :param remember: bool
    :return: None
    """
    user = User().from_json(user_data)
    flask_login.login_user(user, remember=remember)


@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    """
    Log-in page for Google users.
    Backend implementation according to:
    https://developers.google.com/identity/sign-in/web/backend-auth
    :return:
    """
    # If a logged-in user goes to "/google-login", that user won't need to
    # log-in again, and automatically go back to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Google Sign-In constants
    GOOGLE_APP_CLIENT_ID = os.environ['GOOGLE_APP_CLIENT_ID']
    GOOGLE_AUTHORIZATION_SERVERS = [
        'accounts.google.com',
        'https://accounts.google.com'
    ]

    # 1. Verifies and decrypts id_token with Google, to get the Google user
    #    information
    id_info = id_token.verify_oauth2_token(
        id_token=request.args['id_token'],
        request=g_requests.Request(),
        audience=GOOGLE_APP_CLIENT_ID
    )
    # Check issuer (authorization server)
    if id_info['iss'] not in GOOGLE_AUTHORIZATION_SERVERS:
        raise ValueError('Wrong issuer (authorization server)')

    # 2. Successfully got the Google user information from Google
    #    -> Associate a local account with that Google user
    #       (Similar workflow as user registeration or log-in)
    google_user_id = id_info['sub']
    return _oauth_local_login(
        oauth_username=f'Google-User-{google_user_id}',
        email=id_info['email'],
        image_url=id_info['picture']
    )


def _oauth_local_login(oauth_username: str, email: str, image_url: str):
    """
    Private helper function to associate a local account with the given OAuth
    user.
    :param oauth_username: str
    :param email: str
    :param image_url: str
    :return:
    """
    pseudo_password = f'{oauth_username},{email}'
    # Check whether this OAuth user exists
    r = requests.get(f'{USER_SERVICE}/users/?email={email}')
    if r.status_code == 404:  # Not existing
        # Register the OAuth user
        requests.post(
            f'{USER_SERVICE}/users',
            json={
                'username': oauth_username,
                'email': email,
                'password': pseudo_password,
                'from_oauth': True,
                'image_url': image_url
            }
        )
    # Log-in this OAuth user
    r = requests.get(
        f'{USER_SERVICE}/user-auth?email={email}',
        json={
            'password': pseudo_password
        }
    )
    # Log-in on the main application side
    _app_login(user_data=r.json()['data'], remember=True)
    from_page = request.args.get('next')
    if from_page:
        return redirect(from_page)
    return redirect(url_for('main.home'))


@auth_bp.route('/github-login')
def github_login():
    """
    Log-in page for GitHub users.
    Backend implementation according to:
    https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/#web-application-flow
    :return:
    """
    # If a logged-in user goes to "/login", that user won't need to log in
    # again, and automatically go back to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # GitHub Sign-In constants
    GITHUB_APP_CLIENT_ID = os.environ['GITHUB_APP_CLIENT_ID']
    GITHUB_APP_CLIENT_SECRET = os.environ['GITHUB_APP_CLIENT_SECRET']
    GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    GITHUB_USERINFO_URL = 'https://api.github.com/user'

    # After authorization and redirection back from GitHub, the authorization
    # code should be in the query parameters.
    code = request.args.get('code')
    if not code:
        raise ValueError('Need authorization code to process')

    # 1. Exchange the authorization code for access token
    r = requests.post(
        GITHUB_ACCESS_TOKEN_URL,
        headers={
            'Accept': 'application/json'
        },
        params={
            'client_id': GITHUB_APP_CLIENT_ID,
            'client_secret': GITHUB_APP_CLIENT_SECRET,
            'code': code
        }
    )
    json_data = r.json()
    if 'error' in json_data:
        raise ValueError(json_data['error_description'])
    access_token = json_data['access_token']

    # 2. Exchange the access token for GitHub user information
    r = requests.get(
        GITHUB_USERINFO_URL,
        headers={
            'Authorization': f'token {access_token}'
        }
    )
    json_data = r.json()
    if 'error' in json_data:
        raise ValueError(json_data['error_description'])

    # 3. Successfully got the GitHub user information from GitHub
    #    -> Associate a local account with that GitHub user
    #       (Similar workflow as user registeration or log-in)
    return _oauth_local_login(
        oauth_username=f"GitHub-User-{json_data['id']}",
        email=json_data['email'],
        image_url=json_data['avatar_url']
    )


@auth_bp.route('/account', methods=['GET', 'POST'])
@flask_login.login_required
def account():
    """
    Account page.
    :return:
    """
    if current_user.from_oauth:  # OAuth users are not allowed to modify their account.
        flash(
            'OAuth users are not allowed to modify their account.',
            category='danger'
        )
        return redirect(url_for('main.home'))

    # Normal user

    form = forms.AccountUpdateForm()
    if form.validate_on_submit():  # Successfully passed form validation
        update = {}
        if form.username.data != current_user.username:
            update['username'] = form.username.data
        if form.email.data != current_user.email:
            update['email'] = form.email.data
        if form.picture.data:
            saved_filename = save_picture(form.username.data, form.picture.data)
            update['image_filename'] = saved_filename
        if update:
            r = requests.put(
                f'{USER_SERVICE}/users/{current_user.id}', json=update
            )
            if r.status_code == 200:
                current_user.username = form.username.data
                current_user.email = form.email.data
                if form.picture.data:
                    current_user.image_filename = saved_filename
                flash('Your account has been updated!', category='success')
            return redirect(url_for('auth.account'))
    elif request.method == 'GET':  # "GET" request
        # Populate the form with the current user's information
        form.username.data = current_user.username
        form.email.data = current_user.email

    context = {
        'title': 'Account',
        'form': form,
        'image_file': url_for(
            'static',
            filename=os.path.join('profile_pics', current_user.image_filename)
        )
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


@auth_bp.route('/follow/<string:username>')
@flask_login.login_required
def follow_user(username: str):
    """
    Follow user page.
    :param username: str
    :return:
    """
    r = requests.post(
        f'{USER_SERVICE}/user-follow/{current_user.id}/{username}'
    )
    if r.status_code == 201:
        followed_data = r.json()['data']
        send_email(
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipient=followed_data['email'],
            subject='Someone Followed You!',
            body=f'{current_user.username} followed you! Check it out!'
        )  # Internally a Celery asynchronous task
        flash(f'You followed {username}!', category='success')
    else:
        flash(r.json()['message'], category='danger')
    return redirect(url_for('main.home'))


@auth_bp.route('/unfollow/<string:username>')
@flask_login.login_required
def unfollow_user(username: str):
    """
    Unfollow user page.
    :param username: str
    :return:
    """
    r = requests.delete(
        f'{USER_SERVICE}/user-follow/{current_user.id}/{username}'
    )
    if r.status_code == 204:
        flash(f'You unfollowed {username}!', category='success')
    else:
        flash(r.json()['message'], category='danger')
    return redirect(url_for('main.home'))
