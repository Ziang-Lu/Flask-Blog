# -*- coding: utf-8 -*-

"""
Flask routes module.
"""

import flask_bcrypt
from flask import flash, redirect, render_template, url_for

from . import app, db, forms
from .models import User

bcript = flask_bcrypt.Bcrypt(app)


@app.route('/')
def home():
    """
    Home page.
    When a "GET" request is forwarded to "/", this function gets called.
    :return:
    """
    context = {
        'posts': []
    }
    return render_template('home.html', **context)


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
    When a "GET" request is forwarded to "/register", this function gets called.
    :return:
    """
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcript.generate_password_hash(form.password.data)\
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


@app.route('/login')
def login():
    """
    Login page.
    When a "GET" request is forwarded to "/login", this function gets called.
    :return:
    """
    form = forms.LoginForm()
    context = {
        'title': 'Log In',
        'form': form
    }
    return render_template('login.html', **context)
