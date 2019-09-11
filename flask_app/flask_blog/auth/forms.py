# -*- coding: utf-8 -*-

"""
Flask authentication-related forms module.
"""

import flask_login
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField, Field, PasswordField, StringField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError
)

from ..models import User


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

    # We want the usernames and the emails to be unique. However, we only add
    # these constraints on the database-side.
    # => When a user registers with a duplicate username/email, that user will
    #    successfully pass the form validation, and only raises an error until
    #    that user's data is committed to the database.
    #    => Not user-friendly
    # => We want these constraints to be on the form-side, so that when a user
    #    registers with a duplicate username/email, that user will get a nicely
    #    formatted error message on the form.
    # => Define customized validators as follows

    def validate_username(self, username: Field) -> None:
        """
        Validates username field to make sure it is unique.
        :param username: Field
        :return: None
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username has been taken.')

    def validate_email(self, email: Field) -> None:
        """
        Validates email field to make sure it is unique.
        :param email: Field
        :return: None
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email has been taken.')


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


class AccountUpdateForm(FlaskForm):
    """
    Account update form to be submitted.
    """

    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'])]
    )

    submit = SubmitField('Update')

    # Custom validators
    def validate_username(self, username: Field) -> None:
        """
        Validates the updated username field to make sure it is unique.
        :param username: Field
        :return: None
        """
        # Check whether the username is updated
        # -> If not, no need to validate
        if username.data != flask_login.current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username has been taken.')

    def validate_email(self, email: Field) -> None:
        """
        Validates the updated email field to make sure it is unique.
        :param email: Field
        :return: None
        """
        # Check whether the email is updated
        # -> If not, no need to validate
        if email.data != flask_login.current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email has been taken.')
