# -*- coding: utf-8 -*-

"""
Flask forms module.
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    """
    Registration form to be submitted.
    """

    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), Length(min=8), EqualTo('password')]
    )

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    Login form to be submitted.
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8)]
    )
    remember = BooleanField('Remember Me')

    submit = SubmitField('Log In')
