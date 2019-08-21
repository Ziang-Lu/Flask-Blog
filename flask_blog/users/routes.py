# -*- coding: utf-8 -*-

"""
Flask user-related routes module.
"""

import os

import flask_login
from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import forms
from .utils import save_picture
from .. import db
from ..models import Post, User

# Create a user-related blueprint
users_bp = Blueprint(name='users_bp', import_name=__name__)

# Register all the routes on the blueprint


@users_bp.route('/user/<string:username>/posts')
def user_posts(username: str):
    """
    User posts page.
    When a "GET" request is forwarded to "/user/<username>/posts", this function
    gets called.
    :param username: str
    :return:
    """
    user = User.query.filter_by(username=username).first_or_404()
    # Pagination (3 posts per page)
    page = request.args.get('page', type=int, default=1)
    posts = Post.query.filter_by(user_id=user.id)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=3, page=page)

    context = {
        'user': user,
        'posts': posts
    }
    return render_template('user_posts.html', **context)


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register page.
    :return:
    """
    # If a logged-in user goes to "/register", that user won't need to register
    # again, and automatically go back to the home page.
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcript.generate_password_hash(form.password.data) \
            .decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )
        # TODO: Figure out Flask-SQLAlchemy
        db.session.add(user)
        db.session.commit()
        flash(
            'Your account has been created! You are now able to log in.',
            category='success'
        )
        return redirect(url_for('users_bp.login'))
    context = {
        'title': 'Registration',
        'form': form
    }
    return render_template('register.html', **context)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page.
    :return:
    """
    # If a logged-in user goes to "/login", that user won't need to log in
    # again, and automatically go back to the home page.
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and \
            bcript.check_password_hash(user.password, form.password.data):
            flask_login.login_user(user, remember=form.remember.data)
            # If the user comes from a page which requires "logged-in", then the
            # URL will contain the "next" argument.
            # => In this case, when logged in, the user should be redirected
            #    back to that original page.
            from_page = request.args.get('next')
            if from_page:
                return redirect(from_page)
            return redirect(url_for('main_bp.home'))
        else:
            flash(
                'Login unsuccessful. Please check your email and password.',
                category='dangerous'
            )
    context = {
        'title': 'Log In',
        'form': form
    }
    return render_template('login.html', **context)


@users_bp.route('/logout')
@flask_login.login_required
def logout():
    """
    Log-out page.
    (Log-in required)
    When a "GET" request is forwarded to "/logout", this function gets called.
    :return:
    """
    flask_login.logout_user()
    return redirect(url_for('users_bp.login'))


@users_bp.route('/account', methods=['GET', 'POST'])
@flask_login.login_required
def account():
    """
    Account page.
    (Log-in required)
    :return:
    """
    form = forms.AccountUpdateForm()
    if form.validate_on_submit():  # "POST" request
        flask_login.current_user.username = form.username.data
        flask_login.current_user.email = form.email.data
        if form.picture.data:
            saved_filename = save_picture(form.username.data, form.picture.data)
            flask_login.current_user.image_file = saved_filename
        db.session.commit()
        flash('Your account has been updated.', category='success')
        return redirect(url_for('users_bp.account'))
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
