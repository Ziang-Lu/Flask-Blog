# -*- coding: utf-8 -*-

"""
Flask routes module.
"""

import os
import secrets

import flask_bcrypt
import flask_login
from flask import abort, flash, redirect, render_template, request, url_for
# from PIL import Image

from . import app, db, forms
from .models import Post, User


bcript = flask_bcrypt.Bcrypt(app)


@app.route('/')
@app.route('/home')
def home():
    """
    Home page.
    When a "GET" request is forwarded to "/", this function gets called.
    :return:
    """
    # Pagination (3 posts per page)
    page = request.args.get('page', type=int, default=1)
    posts = Post.query.order_by(Post.date_posted.desc())\
        .paginate(per_page=3, page=page)

    context = {
        'posts': posts
    }
    return render_template('home.html', **context)


@app.route('/user/<string:username>/posts')
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


@app.route('/about')
def about():
    """
    About page.
    When a "GET" request is forwarded to "/about", this function gets called.
    :return:
    """
    context = {
        'title': 'About'
    }
    return render_template('about.html', **context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register page.
    :return:
    """
    # If a logged-in user goes to "/register", that user won't need to register
    # again, and automatically go back to the home page.
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('home'))

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
        return redirect(url_for('login'))
    context = {
        'title': 'Registration',
        'form': form
    }
    return render_template('register.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page.
    :return:
    """
    # If a logged-in user goes to "/login", that user won't need to log in
    # again, and automatically go back to the home page.
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('home'))

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
            return redirect(url_for('home'))
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


@app.route('/logout')
@flask_login.login_required
def logout():
    """
    Log-out page.
    (Log-in required)
    When a "GET" request is forwarded to "/logout", this function gets called.
    :return:
    """
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
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


def save_picture(username: str, picture_data) -> str:
    """
    Saves the given picture file for the given user.
    :param username: str
    :param picture_data:
    :return: str
    """
    user_random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(picture_data.filename)
    saved_filename = f'{username}_{user_random_hex}{ext}'
    saved_path = os.path.join(
        app.root_path, 'static/profile_pics', saved_filename
    )

    # # Resize the picture if it is too large
    # img = Image.open(picture_data)
    # if img.width > 300 or img.height > 300:
    #     img.thumbnail((300, 300))
    #     img.save(saved_path)

    picture_data.save(saved_path)
    return saved_filename


@app.route('/post/<int:post_id>')
def post_detail(post_id: int):
    """
    Post detail page.
    :param post_id: int
    :return:
    """
    post = Post.query.get_or_404(post_id)

    context = {
        'title': post.title,
        'post': post
    }
    return render_template('post_detail.html', **context)


@app.route('/post/new', methods=['GET', 'POST'])
@flask_login.login_required
def new_post():
    """
    Post creation page.
    (Log-in required)
    :return:
    """
    form = forms.PostForm()
    if form.validate_on_submit():
        post = Post(
            user_id=flask_login.current_user.id,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('home'))

    context = {
        'title': 'New Post',
        'form': form,
        'legend': 'New Post'
    }
    return render_template('post_form.html', **context)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@flask_login.login_required
def update_post(post_id: int):
    """
    Post detail page.
    (Log-in required)
    :param post_id: int
    :return:
    """
    post = Post.query.get_or_404(post_id)
    if post.author != flask_login.current_user:
        abort(403)

    form = forms.PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('post_detail', post_id=post.id))
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


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@flask_login.login_required
def delete_post(post_id: int):
    """
    Delete post page.
    (Log-in required)
    When a "POST" request is forwarded to "/post/<post_id>/delete", this
    function gets called.
    :param post_id: int
    :return:
    """
    post = Post.query.get_or_404(post_id)
    if post.author != flask_login.current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', category='success')
    return redirect(url_for('home'))
