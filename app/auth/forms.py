from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask import current_app
from app.models import User

class LoginForm(Form):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(Form):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=30)])
    email = StringField('email', validators=[DataRequired(), Email(), Length(max=128)])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password', message='Please enter matching passwords.')])

    def validate_username(self, username):
        username=username.data.lower()
        user = User.query.filter(User.lowercase_username==username).first()
        if user is not None:
            raise ValidationError('Username is already in use.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address is already in use.')
