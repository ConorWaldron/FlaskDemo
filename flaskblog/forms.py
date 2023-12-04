from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog import app
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #make custom validations
    def validate_username(self, proposed_username):
        with app.app_context():
            pre_existing_user = User.query.filter_by(username=proposed_username.data).first()
        if pre_existing_user:
            raise ValidationError('That username is already taken, please choose a different one')

    def validate_email(self, proposed_email):
        with app.app_context():
            pre_existing_user = User.query.filter_by(email=proposed_email.data).first()
        if pre_existing_user:
            raise ValidationError('That email is already taken, please choose a different one')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update your account details')

    # We need to update custom validations to allow the user to keep their existing username/email
    # we can use flask_login.current_user to check what the current user and email is
    def validate_username(self, proposed_username):
        if proposed_username.data != current_user.username:
            with app.app_context():
                pre_existing_user = User.query.filter_by(username=proposed_username.data).first()
            if pre_existing_user:
                raise ValidationError('That username is already taken, please choose a different one')

    def validate_email(self, proposed_email):
        if proposed_email.data != current_user.email:
            with app.app_context():
                pre_existing_user = User.query.filter_by(email=proposed_email.data).first()
            if pre_existing_user:
                raise ValidationError('That email is already taken, please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')